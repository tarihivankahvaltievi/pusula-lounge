(() => {
  const track = document.querySelector('.reviews-track');
  const controls = document.querySelector('.reviews-controls');
  if (!track || !controls) return;
  const slides = [...track.querySelectorAll('.review-serving')];
  const previous = controls.querySelector('.reviews-prev');
  const next = controls.querySelector('.reviews-next');
  const position = controls.querySelector('.reviews-position');
  const mobile = matchMedia('(max-width: 999px)');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const section = document.querySelector('.guest-reviews');
  let current = 0;
  let scheduled = false;
  function update() {
    scheduled = false;
    current = Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / track.clientWidth)));
    position.textContent = `${current + 1} / ${slides.length}`;
    previous.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    slides.forEach((slide, index) => {
      slide.inert = mobile.matches && index !== current;
      slide.classList.toggle('is-current', index === current);
    });
  }
  function goTo(index) {
    track.scrollTo({ left: Math.max(0, Math.min(slides.length - 1, index)) * track.clientWidth, behavior: reducedMotion.matches ? 'instant' : 'smooth' });
  }
  function layout() {
    controls.hidden = !mobile.matches;
    track.tabIndex = mobile.matches ? 0 : -1;
    track.scrollTo({ left: 0, behavior: 'instant' });
    update();
  }
  previous.addEventListener('click', () => goTo(current - 1));
  next.addEventListener('click', () => goTo(current + 1));
  track.addEventListener('keydown', event => {
    if (!mobile.matches || event.target !== track) return;
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      goTo(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  track.addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
  }, { passive: true });
  mobile.addEventListener('change', layout);
  let previousWidth = track.clientWidth;
  addEventListener('resize', () => {
    if (track.clientWidth === previousWidth) return;
    previousWidth = track.clientWidth;
    if (mobile.matches) track.scrollTo({left: current * track.clientWidth, behavior: 'instant'});
    update();
  }, { passive: true });
  layout();
  section.classList.add('reviews-enhanced');
  // The artwork stays still on mobile; only the selected review changes.
  // All content is visible by default, including when scripting is unavailable.
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (!entries[0].isIntersecting) return;
      observer.disconnect();
      if (reducedMotion.matches) return;
      section.querySelector('.reviews-table').animate(
        [{ opacity: .8, transform: 'translateY(10px)' }, { opacity: 1, transform: 'translateY(0)' }],
        { duration: 480, easing: 'cubic-bezier(.16, 1, .3, 1)' }
      );
    }, { threshold: .15 });
    observer.observe(section);
  }
})();
