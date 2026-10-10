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
  let current = 0, frame = 0, previous = 0;
  let geometry = null;
  let nearScene = false;
  let lastProgress = -1;
  const preparedImages = new WeakSet();
  const clamp = value => Math.max(0, Math.min(1, value));

  function buildWall() {
    lastProgress = -1;
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
    measureScene();
    requestUpdate();
  }
  // Read layout only when its dimensions change, never during scroll frames.
  function measureScene() {
    lastProgress = -1;
    columnCycles = columns.map(column => {
      const gap = parseFloat(getComputedStyle(column).gap) || 0;
      return (column.firstElementChild.offsetHeight + gap) * column.children.length / 3;
    });
    const header = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--header-height')) || 60;
    const wallTop = wall.getBoundingClientRect().top + window.scrollY;
    const introTop = intro.getBoundingClientRect().top + window.scrollY;
    const startLine = window.innerHeight * .86;
    geometry = { header, wallTop, introTop, startLine,
      openingDistance: Math.max(1, startLine - header + wallTop - introTop),
      travel: Math.max(1, wall.offsetHeight - wall.querySelector('.wall-sticky').offsetHeight) };
  }
  function render(progress) {
    if (progress === lastProgress) return;
    lastProgress = progress;
    // The opening completes before either column starts travelling.
    const opening = clamp(progress / .26);
    const unfold = opening * opening * (3 - 2 * opening);
    const travelProgress = clamp((progress - .26) / .74);
    const parallax = reduced.matches ? 0 : travelProgress * travelProgress * (3 - 2 * travelProgress);
    const mix = (from, to) => from + (to - from) * unfold;
    const small = mobile.matches;
    matrix.style.transform = `translateZ(${mix(small ? -180 : -600, 0)}px) rotateY(${mix(small ? -30 : -45, small ? 0 : -5)}deg) rotateX(${mix(small ? 18 : 25, small ? 0 : 2)}deg) rotateZ(${mix(small ? 9 : 15, 0)}deg)`;
    banner.style.transform = `scale(${.94 + .06 * unfold}, ${.9 + .1 * unfold})`;
    columns.forEach((column, i) => {
      // Left/even columns descend; right/odd columns rise by a full photo sequence.
      const offset = (i % 2 ? -1 : 1) * parallax * columnCycles[i];
      column.style.transform = `translate3d(0, ${offset}px, 0)`;
    });
    hint.style.opacity = 1 - clamp(progress / .3);
  }
  function tick(time) {
    if (document.hidden) { frame = 0; previous = 0; return; }
    const {header, wallTop, introTop, startLine, openingDistance, travel} = geometry;
    const scroll = window.scrollY;
    const opening = clamp((startLine - introTop + scroll) / openingDistance);
    const columnTravel = clamp((header - wallTop + scroll) / travel);
    const target = reduced.matches ? 1 : .26 * opening + .74 * columnTravel;
    const dt = Math.min(time - (previous || time - 16.67), 64);
    previous = time;
    // Exact exponential damping: same response at 60/120 Hz, without spring jitter.
    current = reduced.matches || !nearScene ? target : current + (target - current) * (1 - Math.exp(-dt / 65));
    if (Math.abs(target - current) < .00002) current = target;
    render(clamp(current));
    if (current !== target) frame = requestAnimationFrame(tick);
    else { frame = 0; previous = 0; }
  }
  function requestUpdate() { if (!frame && geometry) frame = requestAnimationFrame(tick); }
  window.addEventListener('scroll', () => { if (nearScene) requestUpdate(); }, {passive: true});
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) { cancelAnimationFrame(frame); frame = 0; previous = 0; }
    else { measureScene(); requestUpdate(); }
  });
  window.addEventListener('resize', () => { measureScene(); requestUpdate(); }, {passive: true});
  new ResizeObserver(() => { measureScene(); requestUpdate(); }).observe(document.querySelector('main') || section);
  reduced.addEventListener('change', () => {
    section.classList.toggle('is-animating', nearScene && !reduced.matches);
    measureScene();
    requestUpdate();
  });
  mobile.addEventListener('change', buildWall);
  new IntersectionObserver(entries => {
    nearScene = entries[0].isIntersecting;
    section.classList.toggle('is-animating', nearScene && !reduced.matches);
    if (nearScene) matrix.querySelectorAll('img').forEach(image => {
      if (preparedImages.has(image)) return;
      preparedImages.add(image);
      image.loading = 'eager';
      if (image.decode) image.decode().catch(() => {});
    });
    requestUpdate();
  }, {rootMargin: '600px'}).observe(wall);
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
