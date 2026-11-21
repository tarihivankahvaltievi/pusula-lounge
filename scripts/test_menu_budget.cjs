/* Real navigation, no-JS disclosure, RTL and mobile budget comparison checks. */
const {chromium} = require(process.env.PLAYWRIGHT_PATH || '/Users/baran/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const base = process.env.PREVIEW_URL || 'http://127.0.0.1:8893';
const out = process.argv[2] || '/tmp/pusula-menu-budget';
(async () => {
  fs.mkdirSync(out, {recursive: true});
  const browser = await chromium.launch({channel:'chrome', headless:true});
  const results=[];
  try {
    for (const javaScriptEnabled of [false,true]) {
      for (const width of [320,390,768,1440]) {
        const context=await browser.newContext({javaScriptEnabled, viewport:{width,height:900}});
        const page=await context.newPage();
        const errors=[];
        page.on('pageerror',e=>errors.push(e.message));
        page.on('console',e=>{if(e.type()==='error') errors.push(e.text());});
        for (const lang of ['tr','en','ru','ar']) {
          const route=lang==='tr'?'/menu/':`/${lang}/menu/`;
          await page.goto(base+route);
          await page.evaluate(()=>document.fonts.ready);
          const details=page.locator('#shared-breakfast-budget');
          assert.equal(await details.count(),1);
          assert.equal(await details.getAttribute('open'),null);
          const cta=page.locator(lang==='tr'?'.menu-visit-primary':'.menu-intro-actions a').first();
          assert.ok((await cta.boundingBox()).y<(await details.boundingBox()).y,'CTA before comparison');
          await details.locator('summary').focus();
          await page.keyboard.press('Enter');
          assert.equal(await details.locator('table').isVisible(),true);
          assert.equal(await details.locator('tbody tr').count(),3);
          const currency = (text) => Number(text.replace(/[^0-9.,]/g, '')
            .replace(lang === 'tr' ? /\./g : /,/g, '').replace(',', '.'));
          const totals = await page.locator('#serpme-van-kahvaltisi .portion-prices b, #serpme-van-kahvaltisi .portion-list strong').allTextContents();
          const rows = await details.locator('tbody tr').evaluateAll(items => items.map(row =>
            [...row.cells].map(cell => cell.textContent)));
          assert.equal(totals.length, 3);
          for (const [index, [guests, total, perPerson]] of rows.entries()) {
            const people = index + 2;
            const published = Number(totals[index].replace(/[^0-9]/g, ''));
            assert.equal(Number(guests), people);
            assert.equal(currency(total), published);
            assert.equal(currency(perPerson), Math.round(100 * published / people) / 100);
          }
          const intro = page.locator(lang === 'tr' ? '.menu-visit p' : '.visit-intro .lead').first();
          const shared = intro.locator('a[href="#serpme-van-kahvaltisi"]');
          assert.equal(currency(await shared.textContent()), currency(rows[0][1]));
          await shared.click();
          await page.waitForURL('**/#serpme-van-kahvaltisi');
          assert.equal(await page.locator('#serpme-van-kahvaltisi').isVisible(), true);
          assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,route+' horizontal overflow');
          if(lang==='ar') assert.equal(await page.locator('html').getAttribute('dir'),'rtl');
          if(javaScriptEnabled&&width===390){await details.scrollIntoViewIfNeeded();await page.screenshot({path:`${out}/${lang}-mobile.png`});}
          await details.locator('a[href="#kahvalti-tabagi"]').click();
          await page.waitForURL('**/#kahvalti-tabagi');
          assert.equal(await page.locator('#kahvalti-tabagi').isVisible(),true);
          results.push({route,width,javaScriptEnabled});
        }
        assert.deepEqual(errors,[]);
        await context.close();
      }
    }
    fs.writeFileSync(`${out}/checks.json`,JSON.stringify(results,null,2));
    console.log('PASS: 32 menu checks: no-JS disclosure, keyboard, price arithmetic, CTA order, dish navigation, RTL, overflow and browser/CSP errors.');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
