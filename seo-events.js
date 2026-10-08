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
    if (url.hostname === 'wa.me') emit('reservation_whatsapp_open');
    else if (url.protocol === 'tel:') emit('phone_click');
    else if (url.hostname === 'share.google' || url.hostname.endsWith('google.com') && url.pathname.includes('/maps')) emit('map_profile_click');
    else if (url.pathname === '/menu/' || url.pathname === '/en/menu/') emit('menu_click');
    else if (url.pathname === '/rezervasyon/') emit('reservation_page_click');
  });
})();
