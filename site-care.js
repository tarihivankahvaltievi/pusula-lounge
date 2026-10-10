// Prioritize the first photo; prepare decorative slides only after it is ready.
(() => {
  const hero = document.querySelector('.hero');
  if (!hero) return;
  const primary = hero.querySelector('.hero-slide--venue');
  const deferred = [...hero.querySelectorAll('img[data-src]')];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let visible = false;
  let primaryReady = primary.complete && primary.naturalWidth > 0;
  let ready = deferred.length === 0;
  let loading = false;
  let timer = 0;
  function update() {
    const active = visible && !document.hidden && !reduced.matches;
    hero.classList.toggle('motion-paused', !active || !ready);
    hero.classList.toggle('motion-running', active && ready);
    if (!active && timer) { clearTimeout(timer); timer = 0; }
    if (active && primaryReady && !ready && !loading && !timer) {
      timer = setTimeout(async () => {
        timer = 0;
        loading = true;
        try {
          await Promise.all(deferred.map(image => {
            if (image.dataset.srcset) image.srcset = image.dataset.srcset;
            image.src = image.dataset.src;
            return image.decode();
          }));
          ready = true;
        } catch {
          // Keep the primary photo visible if a decorative slide cannot load.
          hero.classList.add('hero-images-failed');
        }
        update();
      }, 1500);
    }
  }
  primary.addEventListener('load', () => { primaryReady = true; update(); }, {once: true});
  update();
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; update(); }).observe(hero);
  document.addEventListener('visibilitychange', update);
  reduced.addEventListener('change', update);
})();
