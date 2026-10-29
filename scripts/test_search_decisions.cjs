/* Check the visitor journey, including readable HTML without JavaScript. */
const { chromium } = require(process.env.PLAYWRIGHT_PATH || '/Users/baran/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.PREVIEW_URL || 'http://127.0.0.1:8875';
const output = process.argv[2] || '/tmp/pusula-search-decisions';

(async () => {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  const results = [];
  try {
    for (const javaScriptEnabled of [false, true]) {
      for (const width of [320, 390, 768, 1440]) {
        const context = await browser.newContext({ javaScriptEnabled, viewport: { width, height: 900 }, reducedMotion: 'reduce' });
        const page = await context.newPage();
        const errors = [];
        page.on('pageerror', error => errors.push(error.message));
        page.on('console', message => {
          if (message.type() === 'error') errors.push(message.text());
        });
        for (const route of ['/menu/', '/kahvalti/', '/en/breakfast/']) {
          await page.goto(base + route);
          await page.evaluate(() => document.fonts.ready);
          assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, route + ' overflow at ' + width);
          if (route === '/menu/') {
            assert.equal(await page.locator('h1').count(), 1);
            assert.equal(await page.locator('h1').isVisible(), true);
            const cta = page.locator('.menu-visit-primary');
            const box = await cta.boundingBox();
            assert.ok(box.y + box.height < 900 && box.height >= 44, 'Visible early table request');
            await cta.focus();
            assert.equal(await cta.evaluate(el => el === document.activeElement), true);
            if (javaScriptEnabled) {
              await page.evaluate(() => {
                window.__events = [];
                window.addEventListener('pusula:interaction', e => window.__events.push(e.detail));
                document.querySelector('.menu-visit-primary').addEventListener('click', e => e.preventDefault(), { once: true });
              });
              await cta.click();
              const events = await page.evaluate(() => window.__events);
              assert.deepEqual(events.map(e => e.name), ['reservation_page_click']);
              assert.deepEqual(Object.keys(events[0]).sort(), ['language', 'name', 'path']);
              await cta.click();
              await page.waitForURL('**/rezervasyon/?visit=breakfast');
              assert.equal(await page.locator('[name=visitType]').inputValue(), 'breakfast');
              await page.goto(base + route);
              await page.locator('#menu-query').fill('menemen');
              assert.equal(await page.locator('#sade-menemen').isVisible(), true);
              assert.equal(await page.locator('#peynirli-gozleme').isVisible(), false);
              await page.locator('#menu-query').fill('zzzz-no-dish');
              assert.equal(await page.locator('.search-empty').isVisible(), true);
              await page.locator('.search-empty button').click();
              assert.equal(await page.locator('#peynirli-gozleme').isVisible(), true);
            } else {
              await cta.click();
              await page.waitForURL('**/rezervasyon/?visit=breakfast');
              assert.equal(await page.locator('main').isVisible(), true);
              await page.goto(base + route);
            }
          } else {
            const table = page.locator('.breakfast-options');
            assert.equal(await table.locator('tbody tr').count(), 5);
            assert.equal(await table.locator('caption').isVisible(), true);
            const href = await table.locator('a[href$="#sade-menemen"]').getAttribute('href');
            await table.locator('a[href$="#sade-menemen"]').click();
            await page.waitForURL(base + href);
            assert.equal(await page.locator('#sade-menemen').isVisible(), true);
            if (route.startsWith('/en/')) assert.equal(await page.locator('html').getAttribute('lang'), 'en');
            await page.goto(base + route);
            await table.scrollIntoViewIfNeeded();
          }
          if (javaScriptEnabled && [390, 1440].includes(width)) {
            await page.screenshot({ path: path.join(output, route.replaceAll('/', '_') + width + '.png') });
          }
          results.push({ route, width, javaScriptEnabled });
        }
        assert.deepEqual(errors, [], 'Browser/CSP errors');
        await context.close();
      }
    }
    fs.writeFileSync(path.join(output, 'checks.json'), JSON.stringify(results, null, 2));
    console.log('PASS: 24 page checks; no-JS HTML, mobile/desktop layout, dish links, search/reset, private events and breakfast request prefill.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
