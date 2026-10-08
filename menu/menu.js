(() => {
 const links = [...document.querySelectorAll('.category-nav a')];
 const sections = [...document.querySelectorAll('.menu-section')];
 const items = [...document.querySelectorAll('.menu-item')];
 const nav = document.querySelector('.category-nav');
 const rail = document.querySelector('.category-inner');
 const toggle = document.querySelector('.search-toggle');
 const panel = document.querySelector('.menu-search');
 const form = document.querySelector('.search-form');
 const input = document.querySelector('#menu-query');
 const clear = document.querySelector('.clear-search');
 const status = document.querySelector('.search-status');
 const empty = document.querySelector('.search-empty');
 const viewToggle = document.querySelector('.view-toggle');
 const skip = document.querySelector('.skip-link');
 const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
 const normalize = value => value.toLocaleLowerCase('tr').replace(/ı/g, 'i').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
 const searchable = new Map(items.map(item => [item, normalize(item.closest('.menu-section').querySelector('h2').textContent + ' ' + [...item.querySelectorAll('h3,.item-detail p')].map(node => node.textContent).join(' '))]));
 let scheduled = false;
 let active;
 function update() {
  const visible = sections.filter(section => !section.hidden);
  const threshold = nav.getBoundingClientRect().bottom + 40;
  let current = visible[0];
  visible.forEach(section => { if (section.getBoundingClientRect().top <= threshold) current = section; });
  if (scrollY > 0 && document.documentElement.scrollHeight > innerHeight + 4 && innerHeight + scrollY >= document.documentElement.scrollHeight - 4) current = visible.at(-1);
  links.forEach(link => {
   if (current && link.hash === '#' + current.id) link.setAttribute('aria-current', 'true');
   else link.removeAttribute('aria-current');
  });
  const selected = links.find(link => link.hasAttribute('aria-current'));
  if (selected && selected !== active) {
   const bounds = selected.getBoundingClientRect();
   const container = rail.getBoundingClientRect();
   if (bounds.left < container.left || bounds.right > container.right) {
    rail.scrollTo({left: rail.scrollLeft + bounds.left - container.left - 16, behavior: reducedMotion.matches ? 'instant' : 'smooth'});
   }
  }
  active = selected;
  scheduled = false;
 }
 function measure() {
  const height = document.body.classList.contains('is-searching') ? panel.getBoundingClientRect().height : 0;
  document.documentElement.style.setProperty('--search-height', height + 'px');
  update();
 }
 function filter() {
  const words = normalize(input.value.trim()).split(/\s+/).filter(Boolean);
  let count = 0;
  items.forEach(item => {
   item.hidden = !words.every(word => searchable.get(item).includes(word));
   if (!item.hidden) count++;
  });
  sections.forEach(section => { section.hidden = ![...section.querySelectorAll('.menu-item')].some(item => !item.hidden); });
  clear.hidden = !input.value;
  empty.hidden = count > 0;
  status.textContent = words.length ? `${count} ürün bulundu · Tüm kategorilerde` : '';
  document.body.classList.toggle('is-searching', words.length > 0);
  const first = sections.find(section => !section.hidden);
  skip.href = first ? '#' + first.id : '#menu-search';
  measure();
 }
 function reset() { input.value = ''; filter(); }
 function focusSearch() {
  panel.scrollIntoView({block:'center', behavior:'instant'});
  input.focus({preventScroll:true});
 }
 toggle.addEventListener('click', focusSearch);
 input.addEventListener('input', filter);
 form.addEventListener('submit', event => { event.preventDefault(); input.blur(); });
 form.addEventListener('reset', event => { event.preventDefault(); reset(); focusSearch(); });
 input.addEventListener('keydown', event => { if (event.key === 'Escape') { reset(); input.blur(); } });
 empty.querySelector('button').addEventListener('click', () => { reset(); focusSearch(); });
 viewToggle.addEventListener('click', () => {
  const compact = document.body.classList.toggle('prices-only');
  viewToggle.setAttribute('aria-pressed', String(compact));
  measure();
 });
 links.forEach(link => link.addEventListener('click', () => {
  if (input.value) reset();
  input.blur();
 }));
 addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(update); } }, { passive: true });
 addEventListener('resize', measure);
 new ResizeObserver(measure).observe(panel);
 document.fonts.ready.then(measure);
 measure();
})();
