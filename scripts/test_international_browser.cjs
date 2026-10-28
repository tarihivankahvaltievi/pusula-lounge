// Exercise actual rendered pages with CSP enforced by preview_seo.py.
const {chromium}=require(process.env.PLAYWRIGHT_PATH || '/Users/baran/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const root=process.argv[2],output=process.argv[3] || '/tmp/pusula-seo-20261028';
const base=process.env.PREVIEW_URL || 'http://127.0.0.1:8874';
fs.mkdirSync(output,{recursive:true});
const routes=[...fs.readFileSync(path.join(root,'sitemap.xml'),'utf8').matchAll(/<loc>https:\/\/www.pusulalounge.com([^<]+)<\/loc>/g)].map(m=>m[1]);
(async()=>{
  const browser=await chromium.launch({headless:true,channel:'chrome'}),results=[];
  for(const width of [320,390,768,1440]){
    const page=await browser.newPage({viewport:{width,height:900}});
    let errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('response',r=>{if(r.status()>=400)errors.push(r.status()+' '+r.url());});
    page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
    for(const route of routes){
      errors=[];
      const response=await page.goto(base+route);
      assert.equal(response.status(),200,route);
      await page.evaluate(()=>document.fonts.ready);
      const result=await page.evaluate(()=>({
        overflow:document.documentElement.scrollWidth>innerWidth,
        h1:document.querySelectorAll('h1').length,
        language:document.documentElement.lang,
        direction:getComputedStyle(document.body).direction,
        bodyFont:getComputedStyle(document.body).fontFamily,
        brokenImages:[...document.images].filter(i=>i.getAttribute('src')&&i.loading!=='lazy'&&!i.hasAttribute('data-src')&&(!i.complete||i.naturalWidth===0)).map(i=>i.src),
        languageNavs:document.querySelectorAll('nav.site-languages').length,
        fontsReady:document.fonts.status==='loaded'
      }));
      assert.equal(result.h1,1,JSON.stringify({route,width,result}));
      assert.equal(result.overflow,false,JSON.stringify({route,width,result}));
      assert.equal(result.brokenImages.length,0,JSON.stringify({route,width,result}));
      assert.equal(result.languageNavs,1,route);
      assert.deepEqual(errors,[],JSON.stringify({route,width,errors}));
      if(route.startsWith('/ar/'))assert.equal(result.direction,'rtl');
      results.push({route,width,...result});
    }
    if(width===390 || width===1440){
      for(const [name,route] of [['ar-home','/ar/'],['ar-menu','/ar/menu/'],['ru-menu','/ru/menu/'],['article','/en/blog/what-is-van-breakfast/']]){
        await page.goto(base+route);await page.evaluate(()=>document.fonts.ready);
        await page.screenshot({path:path.join(output,`${name}-${width}.png`),fullPage:true});
      }
    }
    await page.close();
  }
  const page=await browser.newPage({viewport:{width:390,height:844}});
  for(const lang of ['ru','ar']){
    await page.goto(base+'/en/menu/');
    await page.locator(`.site-languages a[lang=${lang}]`).click();
    assert.equal(new URL(page.url()).pathname,`/${lang}/menu/`);
    await page.locator(`main a.visit-button[href="/${lang}/reservation/"]`).first().click();
    assert.equal(new URL(page.url()).pathname,`/${lang}/reservation/`);
    await page.locator(`header a[href="/${lang}/menu/"]`).click();
    assert.equal(new URL(page.url()).pathname,`/${lang}/menu/`);
  }
  await page.goto(base+'/ar/');await page.keyboard.press('Tab');
  assert.equal(await page.evaluate(()=>document.activeElement.className),'skip');
  await page.keyboard.press('Enter');
  assert.equal(await page.evaluate(()=>location.hash),'#content');
  await browser.close();
  fs.writeFileSync(path.join(output,'browser.json'),JSON.stringify({checks:results.length,nativeLanguageJourneys:true,keyboardSkip:true,results},null,2));
  console.log(`PASS ${results.length} page/viewport checks with CSP, images and fonts; RU/AR menu-booking journeys; keyboard skip.`);
})().catch(e=>{console.error(e);process.exit(1);});
