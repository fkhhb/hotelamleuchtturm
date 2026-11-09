// Prüft alle Seiten des Entwurfs (Desktop + Handy): 4xx, kaputte Bilder, horizontales Scrollen, interne Links, EN-Buchung, Sprachwechsel.
// Aufruf: python3 -m http.server 8772 (im Repo-Root) und dann: node quelle/tests/test_site.js
const { chromium } = require('playwright');
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'../..'), BASE='http://localhost:'+(process.env.PORT||8772)+'/';
const pages=[]; (function walk(d){for(const f of fs.readdirSync(d)){const p=path.join(d,f);if(fs.statSync(p).isDirectory()){if(!/^(\.git|quelle|img|assets)$/.test(f))walk(p);}else if(f.endsWith('.html'))pages.push(path.relative(ROOT,p));}})(ROOT);
(async()=>{
  const b=await chromium.launch(); const errs=[]; const bad=new Set(); const links=new Set();
  for (const [name,vp] of [['desk',{width:1366,height:900}],['mob',{width:375,height:812}]]) {
    const ctx=await b.newContext({viewport:vp,isMobile:name==='mob',hasTouch:name==='mob',locale:'en-GB',timezoneId:'Europe/Berlin'});
    const p=await ctx.newPage(); p.on('pageerror',e=>errs.push(name+' '+p.url()+' '+e.message));
    p.on('response',r=>{if(r.url().startsWith(BASE)&&r.status()>=400)bad.add(r.status()+' '+r.url());});
    await p.route(/openstreetmap/,r=>r.abort());
    for (const pg of pages){
      await p.goto(BASE+pg,{waitUntil:'load'}); await p.waitForTimeout(150);
      const ov=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
      if(ov>0) errs.push(`${name} overflow ${ov}px ${pg}`);
      const broken=await p.evaluate(()=>[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&i.getAttribute('src')).map(i=>i.getAttribute('src')));
      if(broken.length) errs.push(`${name} broken img ${pg}: ${broken}`);
      if(name==='desk'){ (await p.evaluate(()=>[...document.querySelectorAll('a[href]')].map(a=>a.href).filter(h=>h.startsWith(location.origin)))).forEach(l=>links.add(l.split('#')[0].split('?')[0])); }
    }
    await ctx.close();
  }
  const c=await b.newContext(); const rq=await c.newPage();
  for (const u of links){ const r=await rq.request.get(u); if(r.status()>=400) bad.add(r.status()+' link '+u); }
  // EN booking flow
  const q=await c.newPage(); q.on('pageerror',e=>errs.push('flow '+e.message));
  await q.goto(BASE+'en/index.html'); await q.fill('#s-arr','2027-06-07'); await q.fill('#s-dep','2027-06-14'); await q.click('#search button[type=submit]'); await q.waitForLoadState('load'); await q.waitForTimeout(300);
  console.log('EN search ->', q.url().replace(BASE,''), '|', await q.textContent('#step h2'));
  await q.locator('label.roomopt:has(input:not([disabled]))').first().click(); await q.waitForTimeout(300);
  await q.click('[data-step="3"]'); await q.waitForTimeout(200); await q.check('input[value=parken]'); await q.click('[data-step="4"]'); await q.waitForTimeout(300);
  const enUrl=q.url(), enTot=await q.textContent('.line.tot'); console.log('EN step4 ->', enUrl.replace(BASE,''), '|', enTot, '| dirs21:', (await q.getAttribute('a[href*=dirs21]','href')).includes('culture=en-GB'));
  // language switch keeps state
  await q.click('.lang a[hreflang=de]'); await q.waitForLoadState('load'); await q.waitForTimeout(300);
  console.log('switch to DE ->', q.url().replace(BASE,''), '|', await q.textContent('.line.tot'), '|', await q.textContent('#stepper a.on'));
  // DE flow still fine
  await q.goto(BASE+'zimmer/einzelzimmer.html'); await q.waitForTimeout(200); console.log('DE bookcard:', (await q.textContent('#b-sum')).slice(0,60));
  await q.click('.lang a[hreflang=en]'); await q.waitForLoadState('load'); console.log('DE room -> EN:', q.url().replace(BASE,''), '|', await q.textContent('h1'));
  console.log('pages tested:', pages.length, '| links checked:', links.size);
  console.log('BAD:', [...bad]); console.log('ERRORS:', errs.length?errs:'none');
  await b.close();
})();
