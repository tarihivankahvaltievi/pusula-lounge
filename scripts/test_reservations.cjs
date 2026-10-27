// Pure DOM tests: no network requests or WhatsApp messages are sent.
const {JSDOM} = require(process.env.JSDOM_PATH || '/tmp/pusula-reservation-qa/node_modules/jsdom');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = process.argv[2];
const routes = {tr:'/rezervasyon/', en:'/en/reservation/', ru:'/ru/reservation/',ko:'/ko/reservation/',ar:'/ar/reservation/',zh:'/zh/reservation/'};
const code = fs.readFileSync(path.join(root,'rezervasyon/reservation.js'),'utf8');
class FixedDate extends Date { constructor(...args) { super(...(args.length ? args : ['2026-10-27T08:00:00Z'])); } }
function mount(lang, ios=false) {
  const html=fs.readFileSync(path.join(root,routes[lang],'index.html'),'utf8');
  const dom=new JSDOM(html,{url:'https://www.pusulalounge.com'+routes[lang]});
  const document=dom.window.document, nav=[],events=[],clipboard=[];
  const navigator={userAgent:ios?'iPhone':'Android',platform:ios?'iPhone':'Linux',maxTouchPoints:ios?1:0,clipboard:{writeText:async value=>clipboard.push(value)}};
  const window={location:{assign:url=>nav.push(url)}, addEventListener:()=>{},dispatchEvent:e=>events.push(e.detail)};
  vm.runInNewContext(code,{window,document,navigator,location:{pathname:routes[lang]},Intl,Date:FixedDate,CustomEvent:dom.window.CustomEvent});
  return {dom,document,form:document.querySelector('form'),nav,events,clipboard,navigator,copy:JSON.parse(document.getElementById('reservation-copy').textContent)};
}
function submit(x) {x.form.dispatchEvent(new x.dom.window.Event('submit',{bubbles:true,cancelable:true}));}
function fill(x) {
 for (const [k,v] of Object.entries({date:'2026-10-28',time:'10:30',guests:'5',name:'Deneme 李 & اختبار',phone:'+90 (507) 816-2994',note:'A&B + ? # / مرحبا 한국어 中文 <script>not executable</script>\nSecond line'})) x.form.elements[k].value=v;
}
(async()=>{
 for(const lang of Object.keys(routes)) {
  const x=mount(lang,lang==='ar');
  assert.equal(x.form.elements.date.min,'2026-10-27');
  assert.equal(x.document.querySelector('[type=submit]').disabled,false);
  submit(x);assert.equal(x.nav.length,0);assert.equal(x.document.activeElement.id,'date');
  fill(x);x.form.elements.date.value='2026-10-26';submit(x);assert.equal(x.document.getElementById('date-error').textContent,x.copy.dateError);
  fill(x);x.form.elements.date.value='2026-10-27';x.form.elements.time.value='10:59';submit(x);assert.equal(x.document.getElementById('time-error').textContent,x.copy.timeError);
  fill(x);x.form.elements.phone.value='abcdefghijk';submit(x);assert.equal(x.nav.length,0);assert.equal(x.document.activeElement.id,'phone');
  fill(x);x.form.elements.name.value='   ';submit(x);assert.equal(x.nav.length,0);
  fill(x);x.form.elements.guests.value='1.5';submit(x);assert.equal(x.nav.length,0);
  fill(x);x.form.elements.guests.value='1000';submit(x);assert.equal(x.nav.length,0);
  fill(x);submit(x);assert.equal(x.nav.length,1);
  const url=new URL(x.nav[0]);assert.equal(url.hostname,'wa.me');assert.equal(url.pathname,'/905078162994');
  const msg=url.searchParams.get('text');assert.ok(msg.startsWith(x.copy.intro));assert.ok(msg.includes('2026-10-28'));assert.ok(msg.includes('10:30 (Europe/Istanbul)'));assert.ok(msg.includes('A&B + ? # / مرحبا 한국어 中文 <script>not executable</script>\nSecond line'));
  assert.equal(x.document.getElementById('request-text').value,msg);
  assert.equal(x.document.getElementById('request-summary').hidden,false);assert.equal(x.form.hidden,true);
  assert.ok(x.document.getElementById('sms-request').getAttribute('href').includes(lang==='ar'?'&body=':'?body='));
  assert.equal(x.events[0].name,'reservation_whatsapp_open');assert.deepEqual(Object.keys(x.events[0]).sort(),['language','name','path']);
  x.document.getElementById('copy-request').click();await new Promise(r=>setImmediate(r));assert.equal(x.clipboard[0],msg);
  x.navigator.clipboard=null;x.document.getElementById('copy-request').click();await new Promise(r=>setImmediate(r));assert.equal(x.document.getElementById('copy-status').textContent,x.copy.copyFallback);
  x.document.getElementById('edit-request').click();assert.equal(x.form.hidden,false);assert.equal(x.form.elements.name.value,'Deneme 李 & اختبار');
  x.form.elements.guests.value='1';x.document.getElementById('guest-minus').click();assert.equal(x.form.elements.guests.value,'1');
  x.form.elements.guests.value='999';x.document.getElementById('guest-plus').click();assert.equal(x.form.elements.guests.value,'999');
  fill(x);x.form.elements.phone.value='+٩٠ ٥٠٧ ٨١٦ ٢٩٩٤';submit(x);assert.ok(new URL(x.nav.at(-1)).searchParams.get('text').includes('+90 507 816 2994'));
  console.log('PASS',lang,'validation, Istanbul timezone, WhatsApp encoding, fallback/edit, clipboard, stepper, Arabic digits, private telemetry');
 }
})().catch(e=>{console.error(e);process.exitCode=1});
