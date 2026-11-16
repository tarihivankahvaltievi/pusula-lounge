(() => {
  'use strict';
  const form = document.getElementById('reservation-form');
  if (!form) return;
  const text = JSON.parse(document.getElementById('reservation-copy').textContent);
  const fields = ['date', 'time', 'guests', 'name', 'phone'].map(id => form.elements[id]);
  const visitType = form.elements.visitType;
  const requestedVisit = new URLSearchParams(location.search).get('visit');
  if (Array.from(visitType.options).some(option => option.value === requestedVisit && option.value)) {
    visitType.value = requestedVisit;
    for (const link of document.querySelectorAll('.language-switch a')) {
      const destination = new URL(link.href);
      destination.searchParams.set('visit', requestedVisit);
      link.href = destination.pathname + destination.search;
    }
  }
  const [date, time, guests] = fields;
  const summary = document.getElementById('request-summary');
  const requestText = document.getElementById('request-text');
  const status = document.getElementById('copy-status');
  const language = document.documentElement.lang;
  const number = '905078162994';
  const emit = name => window.dispatchEvent(new CustomEvent('pusula:interaction', {
    detail: { name, path: location.pathname, language }
  }));
  function trackWhatsApp(continueNavigation) {
    const event = new CustomEvent('pusula:interaction', {
      cancelable: Boolean(continueNavigation),
      detail: { name: 'reservation_whatsapp_open', path: location.pathname, language }
    });
    event.continueNavigation = continueNavigation;
    window.dispatchEvent(event);
    return event.defaultPrevented;
  }
  // Input and message text never enter telemetry or browser storage.
  const digits = value => value.replace(/[٠-٩۰-۹]/g, c => String(c.charCodeAt(0) - (c <= '٩' ? 0x660 : 0x6f0)));
  function venueNow() {
    const parts = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Istanbul',
      year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
    }).formatToParts(new Date());
    const value = key => parts.find(part => part.type === key).value;
    return { date: `${value('year')}-${value('month')}-${value('day')}`, time: `${value('hour')}:${value('minute')}` };
  }
  function refreshDate() { date.min = venueNow().date; }
  refreshDate();
  date.addEventListener('focus', refreshDate);
  window.addEventListener('pageshow', refreshDate);
  function errorFor(field) {
    const value = field.value.trim();
    if (!value) return field.required ? text.required : '';
    const now = venueNow();
    if (field === date && (!field.validity.valid || value < now.date)) return text.dateError;
    if (field === time && (!field.validity.valid || (date.value === now.date && value <= now.time))) return text.timeError;
    if (field === guests && (!Number.isSafeInteger(Number(value)) || Number(value) < 1 || Number(value) > 999)) return text.guestsError;
    if (field.id === 'name' && Array.from(value).length < 2) return text.nameError;
    if (field.id === 'phone') {
      const phone = digits(value);
      const count = phone.replace(/\D/g, '').length;
      if (!/^\+?[\d\s().-]+$/.test(phone) || count < 7 || count > 15) return text.phoneError;
    }
    return '';
  }
  function validate(field) {
    const message = errorFor(field);
    document.getElementById(`${field.id}-error`).textContent = message;
    if (message) field.setAttribute('aria-invalid', 'true');
    else field.removeAttribute('aria-invalid');
    return !message;
  }
  fields.forEach(field => {
    const check = () => {
      if (field.hasAttribute('aria-invalid')) validate(field);
      if (field === date && time.hasAttribute('aria-invalid')) validate(time);
    };
    field.addEventListener('input', check);
    field.addEventListener('change', check);
  });
  function stepGuests(delta) {
    const current = Number(guests.value);
    guests.value = String(Math.min(999, Math.max(1, (Number.isFinite(current) ? Math.floor(current) : 1) + delta)));
    validate(guests);
    syncStepper();
  }
  function syncStepper() {
    document.getElementById('guest-minus').disabled = Number(guests.value) <= 1;
    document.getElementById('guest-plus').disabled = Number(guests.value) >= 999;
  }
  document.getElementById('guest-minus').addEventListener('click', () => stepGuests(-1));
  document.getElementById('guest-plus').addEventListener('click', () => stepGuests(1));
  guests.addEventListener('input', syncStepper);
  syncStepper();
  form.addEventListener('submit', event => {
    event.preventDefault();
    refreshDate();
    if (!fields.map(validate).every(Boolean)) {
      const firstInvalid = fields.find(field => field.hasAttribute('aria-invalid'));
      const options = firstInvalid.closest('details');
      if (options) options.open = true;
      firstInvalid.focus();
      return;
    }
    // ISO date and explicit timezone stay unambiguous for the restaurant team.
    const pairs = [[text.date, date.value], [text.time, `${time.value} (Europe/Istanbul)`],
      [text.guests, guests.value], [text.name, form.elements.name.value.trim()]];
    const phone = form.elements.phone.value.trim();
    if (phone) pairs.push([text.phone, digits(phone)]);
    if (visitType.value) pairs.splice(2, 0, [text.visitTypeMessage, visitType.options[visitType.selectedIndex].text]);
    const note = form.elements.note.value.trim();
    if (note) pairs.push([text.note, note]);
    requestText.value = `${text.intro}\n\n${pairs.map(([label, value]) => `${label}: ${value}`).join('\n')}\n\n${text.outro}`;
    const encoded = encodeURIComponent(requestText.value);
    const url = `https://wa.me/${number}?text=${encoded}`;
    document.getElementById('whatsapp-request').href = url;
    // iOS uses &body, Android and desktop handlers use ?body.
    const ios = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    document.getElementById('sms-request').href = `sms:+${number}${ios ? '&' : '?'}body=${encoded}`;
    form.hidden = true;
    summary.hidden = false;
    document.getElementById('summary-title').focus();
    status.textContent = '';
    // The site can verify preparation, not delivery or confirmation in WhatsApp.
    emit('reservation_form_prepared');
    // Same-tab navigation works without pop-up permission on mobile and desktop.
    // The prepared message and edit/copy/call options remain available on Back.
    const openWhatsApp = () => window.location.assign(url);
    if (!trackWhatsApp(openWhatsApp)) openWhatsApp();
  });
  for (const id of ['whatsapp-request', 'direct-whatsapp']) {
    const link = document.getElementById(id);
    let resuming = false;
    link.addEventListener('click', event => {
      if (resuming || event.defaultPrevented) return;
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
        trackWhatsApp();
        return;
      }
      if (trackWhatsApp(() => {
        resuming = true;
        link.click();
        resuming = false;
      })) event.preventDefault();
    });
  }
  document.getElementById('edit-request').addEventListener('click', () => {
    summary.hidden = true;
    form.hidden = false;
    date.focus();
  });
  document.getElementById('copy-request').addEventListener('click', async () => {
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(requestText.value);
      status.textContent = text.copied;
      emit('reservation_text_copied');
    } catch {
      requestText.focus();
      requestText.select();
      requestText.setSelectionRange(0, requestText.value.length);
      status.textContent = text.copyFallback;
    }
  });
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    if (link.protocol === 'tel:') emit('phone_click');
    else if (link.hostname === 'share.google') emit('map_profile_click');
    else if (link.origin === location.origin && /^\/(?:en\/|ru\/|ar\/)?menu\/$/.test(link.pathname)) emit('menu_click');
  });
  form.querySelector('[type=submit]').disabled = false;
})();
