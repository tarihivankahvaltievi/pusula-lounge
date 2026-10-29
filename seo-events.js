/* No tracker is loaded here. Optional analytics listens to these anonymous events.
   Names, phone numbers, dates, notes and request messages must never enter telemetry. */
(() => {
  'use strict';
  function emit(name) {
    window.dispatchEvent(new CustomEvent('pusula:interaction', { detail: { name, path: location.pathname, language: document.documentElement.lang } }));
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    const url = new URL(link.href, location.href);
    const google = url.hostname === 'google.com' || url.hostname.endsWith('.google.com');
    if (url.hostname === 'wa.me') emit(link.dataset.interaction === 'menu-inquiry' ? 'menu_inquiry_whatsapp_open' : 'reservation_whatsapp_open');
    else if (url.protocol === 'tel:') emit('phone_click');
    else if ((google || url.hostname === 'share.google') && link.dataset.interaction === 'reviews') emit('reviews_click');
    else if (google && /^\/maps\/dir(?:\/|$)/.test(url.pathname)) emit('directions_click');
    else if (url.hostname === 'share.google' || google && /^\/maps(?:\/|$)/.test(url.pathname)) emit('map_profile_click');
    else if (url.origin === location.origin && /^\/(?:en\/|ru\/|ar\/)?menu\/$/.test(url.pathname)) emit('menu_click');
    else if (url.origin === location.origin && (url.pathname === '/rezervasyon/' || /^\/(?:en|ru|ar|ko|zh)\/reservation\/$/.test(url.pathname))) emit('reservation_page_click');
  });
})();
