(() => {
  'use strict';
  const form = document.querySelector('#reservation-form');
  const summary = document.querySelector('#request-summary');
  const fields = ['date', 'time', 'guests', 'name', 'phone'].map(id => document.getElementById(id));
  const requestText = document.querySelector('#request-text');
  const status = document.querySelector('#copy-status');
  form.querySelector('[type=submit]').disabled = false;
  const dateInput = document.querySelector('#date');
  const timeInput = document.querySelector('#time');
  const guestsInput = document.querySelector('#guests');
  const guestChoices = [...document.querySelectorAll('[data-guests]')];
  const customGuests = document.querySelector('#custom-guests');
  const gallery = document.querySelector('.gallery-photos');
  if (gallery && 'IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        gallery.classList.add('is-visible');
        observer.disconnect();
      }
    }, { threshold: 0.15 });
    observer.observe(gallery);
  }

  function localDate() {
    // The venue's date is independent of the guest's device timezone.
    const parts = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Istanbul', year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(new Date());
    const part = type => parts.find(item => item.type === type).value;
    return `${part('year')}-${part('month')}-${part('day')}`;
  }
  function venueTime() {
    return new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Istanbul', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).format(new Date());
  }
  function refreshDate() { dateInput.min = localDate(); }
  refreshDate();
  dateInput.addEventListener('focus', refreshDate);
  function errorFor(field) {
    const value = field.value.trim();
    if (!value) return { date: 'Lütfen bir tarih seçin.', time: 'Lütfen bir saat seçin.', guests: 'Lütfen kişi sayısını seçin.', name: 'Lütfen adınızı ve soyadınızı yazın.', phone: 'Lütfen telefon numaranızı yazın.' }[field.id];
    if (field.id === 'date' && (!field.validity.valid || value < localDate())) return 'Bugünü veya ileri bir tarihi seçin.';
    if (field.id === 'time' && (!field.validity.valid || (dateInput.value === localDate() && value <= venueTime()))) return 'Lütfen ileri bir saat seçin (İstanbul saati).';
    if (field.id === 'guests' && (!Number.isSafeInteger(Number(value)) || Number(value) < 1 || (!field.hidden && Number(value) < 5))) return '5 veya daha fazla kişi için tam sayı yazın.';
    if (field.id === 'name' && value.length < 2) return 'Lütfen adınızı ve soyadınızı yazın.';
    if (field.id === 'phone') {
      const digits = value.replace(/\D/g, '');
      if (!/^[+\d\s().-]+$/.test(value) || digits.length < 10 || digits.length > 15) return 'Lütfen alan koduyla birlikte geçerli bir telefon numarası yazın.';
    }
    return '';
  }
  function validate(field) {
    const message = errorFor(field);
    document.querySelector(`#${field.id}-error`).textContent = message;
    if (message) field.setAttribute('aria-invalid', 'true');
    else field.removeAttribute('aria-invalid');
    return !message;
  }
  fields.forEach(field => {
    field.addEventListener('input', () => { if (field.hasAttribute('aria-invalid')) validate(field); });
    field.addEventListener('change', () => { if (field.hasAttribute('aria-invalid')) validate(field); });
  });
  function syncGuestChoices() {
    guestChoices.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.guests === guestsInput.value)));
    customGuests.setAttribute('aria-pressed', String(!guestsInput.hidden));
  }
  guestChoices.forEach(button => button.addEventListener('click', () => {
    guestsInput.value = button.dataset.guests;
    guestsInput.hidden = true;
    syncGuestChoices();
    if (guestsInput.hasAttribute('aria-invalid')) validate(guestsInput);
  }));
  customGuests.addEventListener('click', () => {
    if (guestsInput.hidden) guestsInput.value = '';
    guestsInput.hidden = false;
    syncGuestChoices();
    guestsInput.focus();
  });
  guestsInput.addEventListener('input', syncGuestChoices);
  form.addEventListener('submit', event => {
    event.preventDefault();
    refreshDate();
    const valid = fields.map(validate).every(Boolean);
    if (!valid) {
      const firstInvalid = fields.find(field => field.hasAttribute('aria-invalid'));
      (firstInvalid === guestsInput && guestsInput.hidden ? customGuests : firstInvalid).focus();
      return;
    }
    const data = new FormData(form);
    const formattedDate = new Intl.DateTimeFormat('tr-TR', { day: 'numeric', month: 'long', year: 'numeric', weekday: 'long' }).format(new Date(`${data.get('date')}T12:00:00`));
    const pairs = [['Tarih', formattedDate], ['Saat', `${data.get('time')} (İstanbul)`], ['Kişi sayısı', data.get('guests')], ['Ad soyad', data.get('name').trim()], ['Telefon', data.get('phone').trim()]];
    const note = data.get('note').trim();
    if (note) pairs.push(['Not', note]);
    const details = document.querySelector('#summary-details');
    details.replaceChildren();
    pairs.forEach(([label, value]) => {
      const row = document.createElement('div');
      row.className = 'summary-row';
      const term = document.createElement('dt');
      const description = document.createElement('dd');
      term.textContent = label;
      description.textContent = value;
      row.append(term, description);
      details.append(row);
    });
    requestText.value = `Merhaba, Pusula Lounge için rezervasyon talebim var.\n\n${pairs.map(([label, value]) => `${label}: ${value}`).join('\n')}\n\nMüsaitliği ve rezervasyonumu teyit edebilir misiniz?`;
    const whatsapp = document.querySelector('#whatsapp-request');
    if (whatsapp) whatsapp.href = `https://wa.me/${whatsapp.dataset.number}?text=${encodeURIComponent(requestText.value)}`;
    window.dispatchEvent(new CustomEvent('pusula:interaction', { detail: { name: 'reservation_text_prepared', path: location.pathname, language: 'tr' } }));
    status.textContent = '';
    form.hidden = true;
    summary.hidden = false;
    document.querySelector('#summary-title').focus();
  });
  document.querySelector('#edit-request').addEventListener('click', () => {
    summary.hidden = true;
    form.hidden = false;
    status.textContent = '';
    dateInput.focus();
  });
  document.querySelector('#copy-request').addEventListener('click', async () => {
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(requestText.value);
      window.dispatchEvent(new CustomEvent('pusula:interaction', { detail: { name: 'reservation_text_copied', path: location.pathname, language: 'tr' } }));
      status.textContent = 'Talep metni kopyalandı. İşletmeye henüz gönderilmedi.';
    } catch {
      requestText.focus();
      requestText.select();
      requestText.setSelectionRange(0, requestText.value.length);
      status.textContent = 'Metni seçtik. Cihazınızın Kopyala seçeneğini kullanın; işletmeye henüz gönderilmedi.';
    }
  });
})();
