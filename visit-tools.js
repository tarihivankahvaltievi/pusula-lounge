/* Progressive enhancement: directions and the address also work without JS. */
(() => {
  'use strict';
  document.querySelectorAll('.arrival-guide').forEach(guide => {
    const address = guide.querySelector('[data-visit-address]');
    const status = guide.querySelector('[role="status"]');
    const copy = guide.querySelector('[data-copy-address]');
    const print = guide.querySelector('[data-print-visit]');
    function emit(name) {
      window.dispatchEvent(new CustomEvent('pusula:interaction', {detail:{name,path:location.pathname,language:document.documentElement.lang}}));
    }
    copy.hidden = false;
    print.hidden = false;
    copy.addEventListener('click', async () => {
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Copy unavailable');
        await navigator.clipboard.writeText(address.textContent.trim());
        status.textContent = guide.dataset.copied;
        emit('address_copy');
      } catch {
        const range = document.createRange();
        range.selectNodeContents(address);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        status.textContent = guide.dataset.copyFallback;
      }
    });
    print.addEventListener('click', () => {
      emit('visit_card_print');
      window.print();
    });
  });
})();
