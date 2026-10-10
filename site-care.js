// Pause decorative motion when it cannot be seen, including background tabs.
(() => {
  const hero = document.querySelector('.hero');
  if (!hero) return;
  let visible = false;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  function update() {
    const running = visible && !document.hidden && !reduced.matches;
    hero.classList.toggle('motion-paused', !running);
    hero.classList.toggle('motion-running', running);
  }
  update();
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; update(); }).observe(hero);
  document.addEventListener('visibilitychange', update);
  reduced.addEventListener('change', update);
})();
