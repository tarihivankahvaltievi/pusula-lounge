/* Progressive enhancement: the journal remains complete without JavaScript. */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const entries = [...document.querySelectorAll('.blog-entries .journal-entry')];
  const filters = [...document.querySelectorAll('[data-journal-filter]')];
  const count = document.querySelector('[data-filter-count]');
  filters.forEach(button => button.addEventListener('click', () => {
    const category = button.dataset.journalFilter;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    entries.forEach(entry => {
      entry.hidden = category !== 'all' && entry.dataset.category !== category;
      entry.classList.add('is-visible');
      entry.classList.toggle('journal-entry--lead', category === 'all' && entry === entries[0]);
    });
    if (count) count.textContent = `${entries.filter(entry => !entry.hidden).length} ${document.documentElement.lang === 'tr' ? 'yazı' : 'stories'}`;
  }));
  document.querySelector('.journal-filters')?.removeAttribute('hidden');
  if (!reduced.matches && 'IntersectionObserver' in window) {
    const reveals = new IntersectionObserver(items => items.forEach(item => {
      if (item.isIntersecting) { item.target.classList.add('is-visible'); reveals.unobserve(item.target); }
    }), { threshold: .06 });
    document.querySelectorAll('.journal-entry').forEach(entry => {
      if (entry.getBoundingClientRect().top > innerHeight) { entry.classList.add('reveal-ready'); reveals.observe(entry); }
    });
    reduced.addEventListener('change', () => {
      if (reduced.matches) { document.querySelectorAll('.reveal-ready').forEach(item => item.classList.add('is-visible')); reveals.disconnect(); }
    });
  }
  const contents = document.querySelector('.article-sidebar details');
  const small = matchMedia('(max-width: 700px)');
  const setContents = () => { if (contents) contents.open = !small.matches; };
  setContents(); small.addEventListener('change', setContents);
  const sections = [...document.querySelectorAll('.article-body section[id]')];
  if (sections.length && 'IntersectionObserver' in window) {
    const active = new IntersectionObserver(items => items.forEach(item => {
      if (!item.isIntersecting) return;
      document.querySelectorAll('.article-sidebar a').forEach(link => {
        if (link.hash === `#${item.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }), { rootMargin: '-10% 0px -65% 0px', threshold: 0 });
    sections.forEach(section => active.observe(section));
  }
  const progress = document.querySelector('.reading-progress');
  if (progress) {
    let pending = false;
    const update = () => {
      const body = document.querySelector('.article-body');
      const start = body.getBoundingClientRect().top + scrollY;
      const length = Math.max(1, body.offsetHeight - innerHeight * .5);
      progress.style.transform = `scaleX(${Math.min(1, Math.max(0, (scrollY - start + innerHeight * .3) / length))})`;
      pending = false;
    };
    addEventListener('scroll', () => { if (!pending) { pending = true; requestAnimationFrame(update); } }, { passive: true });
    addEventListener('resize', update); update();
  }
})();
