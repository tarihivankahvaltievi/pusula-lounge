const {JSDOM}=require(process.env.JSDOM_PATH || '/tmp/pusula-reservation-qa/node_modules/jsdom');
const fs=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const code=fs.readFileSync(require('node:path').join(process.argv[2],'seo-events.js'),'utf8');
for(const lang of ['tr','en','ru','ar','ko','zh']){
  const dom=new JSDOM(`<html lang="${lang}"><body></body></html>`,{url:`https://www.pusulalounge.com/${lang}/`});
  const {window}=dom,events=[];
  window.addEventListener('pusula:interaction',event=>events.push(event.detail));
  vm.runInNewContext(code,{window,document:window.document,location:window.location,URL,CustomEvent:window.CustomEvent});
  function click(href){const link=window.document.createElement('a');link.href=href;link.innerHTML='<span>Open</span>';link.addEventListener('click',e=>e.preventDefault());window.document.body.append(link);link.firstChild.click();}
  const reservation=lang==='tr'?'/rezervasyon/':`/${lang}/reservation/`;
  click(reservation);
  assert.equal(events.at(-1).name,'reservation_page_click');
  if(!['ko','zh'].includes(lang)){
    click(lang==='tr'?'/menu/':`/${lang}/menu/`);
    assert.equal(events.at(-1).name,'menu_click');
  }
  click('https://wa.me/905078162994?text=Private+guest+information');
  assert.equal(events.at(-1).name,'reservation_whatsapp_open');
  assert.ok(events.every(e=>Object.keys(e).sort().join(',')==='language,name,path'));
  assert.ok(events.every(e=>e.language===lang && !JSON.stringify(e).includes('Private')));
  const count=events.length;click('https://example.com/en/menu/');assert.equal(events.length,count);
}
console.log('PASS: all six reservation languages, four menus and private interaction events.');
