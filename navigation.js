(() => {
        const header = document.querySelector('.site-header');
        const toggle = document.querySelector('.menu-toggle');
        const menu = document.querySelector('.site-menu');
        const backdrop = document.querySelector('.menu-backdrop');
        const mobile = matchMedia('(max-width: 760px)');
        const label = toggle.querySelector('.menu-toggle-label');
        const background = [document.querySelector('main'), document.querySelector('.site-footer'), document.querySelector('.brand')];
        let open = false;
        // Keep the anchor-based menu usable when JavaScript is unavailable.
        document.documentElement.classList.add('nav-enhanced');
        menu.inert = true;
        menu.setAttribute('role', 'dialog');
        menu.setAttribute('aria-modal', 'true');
        function setOpen(next, restoreFocus = true) {
          open = next && mobile.matches;
          menu.inert = !open;
          menu.classList.toggle('is-open', open);
          document.body.classList.toggle('menu-is-open', open);
          toggle.setAttribute('aria-expanded', String(open));
          toggle.setAttribute('aria-label', open ? 'Menüyü kapat' : 'Menüyü aç');
          label.textContent = open ? 'Kapat' : 'Menü';
          if (open) menu.scrollTop = 0;
          background.forEach(element => { element.inert = open; });
          if (open) menu.querySelector('nav a').focus({ preventScroll: true });
          else if (restoreFocus) toggle.focus({ preventScroll: true });
        }
        toggle.addEventListener('click', event => { event.preventDefault(); setOpen(!open); });
        backdrop.addEventListener('click', event => { event.preventDefault(); setOpen(false); });
        menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setOpen(false)));
        document.addEventListener('keydown', event => {
          if (!open) return;
          if (event.key === 'Escape') { event.preventDefault(); setOpen(false); }
          if (event.key === 'Tab') {
            const controls = [...menu.querySelectorAll('a')].filter(link => link.getClientRects().length).concat(toggle);
            const current = controls.indexOf(document.activeElement);
            event.preventDefault();
            const next = (current + (event.shiftKey ? -1 : 1) + controls.length) % controls.length;
            controls[next].focus();
          }
        });
        mobile.addEventListener('change', () => { if (open) setOpen(false, false); });
        function updateScroll() { header.classList.toggle('is-scrolled', window.scrollY > 12); }
        window.addEventListener('scroll', updateScroll, { passive: true });
        updateScroll();
        const sections = [document.querySelector('.hero'), document.querySelector('#sofra'), document.querySelector('#hikayemiz')];
        if ('IntersectionObserver' in window) {
          const activeSection = new IntersectionObserver(entries => {
            entries.forEach(entry => {
              if (!entry.isIntersecting) return;
              const href = entry.target.classList.contains('hero') ? '#top' : '#' + entry.target.id;
              document.querySelectorAll('.desktop-nav a, .mobile-nav a').forEach(link => {
                if (link.getAttribute('href') === href) link.setAttribute('aria-current', 'page');
                else link.removeAttribute('aria-current');
              });
            });
          }, { rootMargin: '-25% 0px -55% 0px' });
          sections.forEach(section => activeSection.observe(section));
        }
      })();
