// 21st.dev / piyushxdev: 3D Parallax Unfurling Gallery, native scroll adaptation.
(() => {
  const section = document.querySelector('.venue-gallery');
  if (!section) return;
  const wall = section.querySelector('.wall-scroll');
  const matrix = section.querySelector('.wall-matrix');
  const intro = section.querySelector('.venue-gallery-intro');
  const banner = section.querySelector('.wall-banner');
  const hint = section.querySelector('.wall-hint');
  const open = section.querySelector('.stream-open');
  const dialog = section.querySelector('.stream-viewer');
  const photo = dialog.querySelector('img');
  const caption = dialog.querySelector('#stream-viewer-caption');
  const counter = dialog.querySelector('.stream-viewer-count');
  const sources = [...section.querySelectorAll('.stream-sources a')];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = matchMedia('(max-width: 760px)');
  let index = 0;
  let touchStart = null;
  let returnFocus = open;
  let columns = [];
  let columnCycles = [];
  let current = 0, velocity = 0, frame = 0, previous = 0;
  const clamp = value => Math.max(0, Math.min(1, value));

  function buildWall() {
    matrix.replaceChildren();
    columns = Array.from({length: mobile.matches ? 2 : 4}, (_, columnIndex) => {
      const column = document.createElement('div');
      column.className = 'wall-column';
      const group = sources.map((source, index) => ({source, index})).filter(item => item.index % (mobile.matches ? 2 : 4) === columnIndex);
      [...group, ...group, ...group].forEach(({source, index}, repeatIndex) => {
        const link = document.createElement('a');
        link.className = 'wall-photo';
        link.href = source.href;
        link.dataset.index = index;
        link.setAttribute('aria-label', source.dataset.caption);
        if (repeatIndex >= group.length) { link.tabIndex = -1; link.setAttribute('aria-hidden', 'true'); }
        const image = document.createElement('img');
        image.src = source.getAttribute('href').replace('-1200.webp', '-600.webp');
        image.alt = source.dataset.alt;
        image.loading = 'lazy';
        image.decoding = 'async';
        image.draggable = false;
        link.append(image);
        column.append(link);
      });
      matrix.append(column);
      return column;
    });
    measureColumns();
    requestUpdate();
  }
  function measureColumns() {
    columnCycles = columns.map(column => (column.firstElementChild.offsetHeight + parseFloat(getComputedStyle(column).gap)) * sources.length / columns.length);
  }
  function render(progress) {
    // The opening completes before either column starts travelling.
    const unfold = clamp(progress / .26);
    const parallax = reduced.matches ? 0 : clamp((progress - .26) / .74);
    const mix = (from, to) => from + (to - from) * unfold;
    const small = mobile.matches;
    matrix.style.transform = `translateZ(${mix(small ? -180 : -600, 0)}px) rotateY(${mix(small ? -30 : -45, small ? 0 : -5)}deg) rotateX(${mix(small ? 18 : 25, small ? 0 : 2)}deg) rotateZ(${mix(small ? 9 : 15, 0)}deg)`;
    banner.style.transform = `scale(${.94 + .06 * unfold}, ${.9 + .1 * unfold})`;
    columns.forEach((column, i) => {
      // Left/even columns descend; right/odd columns rise by a full photo sequence.
      const offset = (i % 2 ? -1 : 1) * parallax * columnCycles[i];
      column.style.transform = `translateY(${offset}px)`;
    });
    hint.style.opacity = 1 - clamp(progress / .3);
  }
  function tick(time) {
    const header = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--header-height')) || 60;
    const travel = wall.offsetHeight - wall.querySelector('.wall-sticky').offsetHeight;
    const wallTop = wall.getBoundingClientRect().top;
    const introTop = intro.getBoundingClientRect().top;
    const viewportHeight = window.visualViewport?.height || window.innerHeight;
    // Begin when the gallery heading reaches the lower screen, as it enters from the story.
    // Finish unfolding at the sticky position; then start opposing column travel.
    const startLine = viewportHeight * .86;
    const openingDistance = Math.max(1, startLine - header + (wallTop - introTop));
    const opening = clamp((startLine - introTop) / openingDistance);
    const columnTravel = clamp((header - wallTop) / Math.max(1, travel));
    const target = reduced.matches ? 1 : .26 * opening + .74 * columnTravel;
    const dt = Math.min((time - (previous || time - 16)) / 1000, .032);
    previous = time;
    if (reduced.matches) { current = target; velocity = 0; }
    else { velocity += ((target - current) * 200 - velocity * 40) * dt; current += velocity * dt; }
    render(clamp(current));
    if (Math.abs(target - current) > .0005 || Math.abs(velocity) > .0005) frame = requestAnimationFrame(tick);
    else { current = target; render(target); frame = 0; previous = 0; }
  }
  function requestUpdate() { if (!frame) frame = requestAnimationFrame(tick); }
  window.addEventListener('scroll', requestUpdate, {passive: true});
  window.addEventListener('resize', () => { measureColumns(); requestUpdate(); }, {passive: true});
  reduced.addEventListener('change', requestUpdate);
  mobile.addEventListener('change', buildWall);
  new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) matrix.querySelectorAll('img').forEach(image => { image.loading = 'eager'; });
  }, {rootMargin: '200px'}).observe(wall);
  buildWall();
  open.hidden = false;
  function openViewer(nextIndex, trigger) {
    returnFocus = trigger;
    show(nextIndex);
    dialog.showModal();
    document.body.classList.add('stream-viewer-open');
    dialog.querySelector('.stream-viewer-close').focus({preventScroll: true});
  }
  matrix.addEventListener('click', event => {
    const link = event.target.closest('.wall-photo');
    if (!link) return;
    event.preventDefault();
    openViewer(Number(link.dataset.index), link);
  });
  function show(nextIndex) {
    index = (nextIndex + sources.length) % sources.length;
    const source = sources[index];
    photo.src = source.href;
    photo.alt = source.dataset.alt;
    caption.textContent = source.dataset.caption;
    counter.textContent = `${index + 1} / ${sources.length}`;
  }
  open.addEventListener('click', () => openViewer(0, open));
  dialog.querySelector('.stream-viewer-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.stream-viewer-prev').addEventListener('click', () => show(index - 1));
  dialog.querySelector('.stream-viewer-next').addEventListener('click', () => show(index + 1));
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => { document.body.classList.remove('stream-viewer-open'); returnFocus.focus({preventScroll: true}); requestUpdate(); });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      show(index + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  photo.addEventListener('touchstart', event => { touchStart = event.touches[0].clientX; }, {passive: true});
  photo.addEventListener('touchend', event => {
    if (touchStart === null) return;
    const delta = event.changedTouches[0].clientX - touchStart;
    if (Math.abs(delta) > 45) show(index + (delta < 0 ? 1 : -1));
    touchStart = null;
  }, {passive: true});
})();
