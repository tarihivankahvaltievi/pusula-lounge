const {chromium}=require(process.env.PLAYWRIGHT_PATH || '/Users/baran/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=process.argv[2];
const base=process.env.PREVIEW_URL || 'http://127.0.0.1:8875';
const copy=JSON.parse(fs.readFileSync(path.join(root,'scripts/arrival_copy.json'),'utf8'));
const address='Katip Mustafa Çelebi Mahallesi, Küçük Parmak Kapı Sokak, Sinek Çıkmazı No:3, Beyoğlu / İstanbul';
(async()=>{
  const browser=await chromium.launch({headless:true,channel:'chrome'});
  const results=[];
  for(const width of [320,390,768,1440]){
    const context=await browser.newContext({viewport:{width,height:900}});
    const page=await context.newPage();
    for(const lang of ['tr','en','ru','ar']){
      const route=lang==='tr'?'/konum/':`/${lang}/location/`;
      await page.goto(base+route);await page.evaluate(()=>document.fonts.ready);
      assert.equal(await page.locator('.arrival-guide').count(),1);
      assert.equal(await page.locator('main > section').first().getAttribute('id'),'arrival-guide');
      assert.equal(await page.evaluate(()=>document.querySelector('.arrival-guide').previousElementSibling.classList.contains('visit-intro')),true);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,route+' overflow '+width);
      assert.equal(await page.evaluate(()=>Boolean(document.querySelector('.visit-card').compareDocumentPosition(document.querySelector('.arrival-routes'))&Node.DOCUMENT_POSITION_FOLLOWING)),true);
      const link=new URL(await page.locator('.arrival-guide .visit-button').first().getAttribute('href'));
      assert.equal(link.searchParams.get('api'),'1');assert.equal(link.searchParams.get('travelmode'),'walking');
      assert.equal(link.searchParams.get('destination'),'Pusula Lounge, '+address);
      assert.equal(link.searchParams.has('origin'),false); // No invented starting point or geolocation.
      await page.evaluate(()=>{
        window.__events=[];
        window.addEventListener('pusula:interaction',e=>window.__events.push(e.detail));
        Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{window.__copied=value;}}});
        window.print=()=>{window.__printed=true;};
      });
      await page.locator('[data-copy-address]').click();
      await page.waitForFunction(()=>window.__copied);
      assert.equal(await page.evaluate(()=>window.__copied),address);
      assert.equal(await page.locator('.arrival-guide [role=status]').textContent(),copy[lang].copied);
      await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:undefined}));
      await page.locator('[data-copy-address]').click();
      assert.equal(await page.evaluate(()=>getSelection().toString()),address);
      assert.equal(await page.locator('.arrival-guide [role=status]').textContent(),copy[lang].fallback);
      await page.locator('[data-print-visit]').click();
      assert.equal(await page.evaluate(()=>window.__printed),true);
      const events=await page.evaluate(()=>window.__events);
      assert.ok(events.every(e=>Object.keys(e).sort().join(',')==='language,name,path'));
      assert.deepEqual(events.map(e=>e.name),['address_copy','visit_card_print']);
      await page.emulateMedia({media:'print'});
      assert.equal(await page.locator('.arrival-guide').isVisible(),true);
      assert.equal(await page.locator('main h1').isVisible(),false);
      assert.equal(await page.locator('.visit-footer').isVisible(),false);
      await page.emulateMedia({media:'screen'});
      if(lang!=='tr'){
        await page.goto(base+`/${lang}/menu/`);
        const button=page.locator('.menu-intro-actions .visit-button');
        assert.equal(await button.getAttribute('href'),`/${lang}/reservation/`);
        const box=await button.boundingBox();assert.ok(box.y<900,JSON.stringify({width,lang,box}));
      }
      results.push({width,lang,copy:true,copyFallback:true,print:true,directions:true,privateEvents:true});
    }
    await context.close();
  }
  const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}});
  const page=await context.newPage();
  for(const lang of ['tr','en','ru','ar']){
    await page.goto(base+(lang==='tr'?'/konum/':`/${lang}/location/`));
    assert.equal(await page.locator('[data-copy-address]').isVisible(),false);
    assert.equal(await page.locator('[data-print-visit]').isVisible(),false);
    assert.equal((await page.locator('[data-visit-address]').textContent()).trim(),address);
    assert.equal(await page.locator('.arrival-guide a[href^="https://www.google.com/maps/dir/"]').count(),1);
  }
  await page.goto(base+'/en/');
  assert.equal(await page.locator('.visit-intro a[href="/en/reservation/?visit=breakfast"]').isVisible(),true);
  assert.equal(await page.locator('.visit-intro a[href="/en/location/#arrival-guide"]').isVisible(),true);
  await browser.close();
  console.log(`PASS ${results.length} arrival/viewport combinations: address copy/fallback, print, directions, early menu actions and privacy; four languages also work without JavaScript.`);
})().catch(e=>{console.error(e);process.exit(1)});
