const {JSDOM}=require(process.env.JSDOM_PATH || '/tmp/pusula-reservation-qa/node_modules/jsdom');
const fs=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const code=fs.readFileSync(require('node:path').join(process.argv[2],'seo-events.js'),'utf8');
const home=new JSDOM(fs.readFileSync(require('node:path').join(process.argv[2],'index.html'),'utf8')).window.document;
assert.equal(home.querySelector('.hero-rating').dataset.interaction,'reviews');
assert.equal(new URL(home.querySelector('.menu-directions').href).pathname,'/maps/dir/');
const english=new JSDOM(fs.readFileSync(require('node:path').join(process.argv[2],'en/index.html'),'utf8')).window.document;
assert.equal(english.querySelector('.visit-intro a[data-interaction=reviews]').hostname,'share.google');
assert.equal(english.querySelectorAll('[data-home-visit]').length,1);
for(const lang of ['tr','en','ru','ar','ko','zh']){
  const dom=new JSDOM(`<html lang="${lang}"><body></body></html>`,{url:`https://www.pusulalounge.com/${lang}/`});
  const {window}=dom,events=[];
  window.addEventListener('pusula:interaction',event=>events.push(event.detail));
  vm.runInNewContext(code,{window,document:window.document,location:window.location,URL,CustomEvent:window.CustomEvent});
  function click(href,interaction){const link=window.document.createElement('a');link.href=href;if(interaction)link.dataset.interaction=interaction;link.innerHTML='<span>Open</span>';link.addEventListener('click',e=>e.preventDefault());window.document.body.append(link);link.firstChild.click();}
  const reservation=lang==='tr'?'/rezervasyon/':`/${lang}/reservation/`;
  click(reservation);
  assert.equal(events.at(-1).name,'reservation_page_click');
  if(!['ko','zh'].includes(lang)){
    click(lang==='tr'?'/menu/':`/${lang}/menu/`);
    assert.equal(events.at(-1).name,'menu_click');
  }
  click('https://wa.me/905078162994?text=Private+guest+information');
  assert.equal(events.at(-1).name,'reservation_whatsapp_open');
  click('https://www.google.com/maps/dir/?api=1&destination=Private+starting+point');
  assert.equal(events.at(-1).name,'directions_click');
  click('https://share.google/l1BSBLDwv6suQkW7Y','reviews');
  assert.equal(events.at(-1).name,'reviews_click');
  click('https://www.google.com/search?q=Pusula+Lounge+Yorumlar','reviews');
  assert.equal(events.at(-1).name,'reviews_click');
  click('https://share.google/l1BSBLDwv6suQkW7Y');
  assert.equal(events.at(-1).name,'map_profile_click');
  assert.ok(events.every(e=>Object.keys(e).sort().join(',')==='language,name,path'));
  assert.ok(events.every(e=>e.language===lang && !JSON.stringify(e).includes('Private')));
  const count=events.length;
  for(const href of ['https://example.com/en/menu/','https://notgoogle.com/maps/dir/','https://google.com.example.com/maps/'])click(href,'reviews');
  click('https://www.google.com/maps-misleading');
  assert.equal(events.length,count);
}
console.log('PASS: all six reservation languages, four menus and private interaction events.');
