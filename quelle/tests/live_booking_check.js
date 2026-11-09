// Prüft auf hotel-am-leuchtturm.de, ob sich die Buchung nach "Ablehnen" bzw. "Alle zulassen" im Cookie-Banner öffnet.
// Aufruf: node quelle/tests/live_booking_check.js
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const [choice,sel] of [["decline","#CybotCookiebotDialogBodyButtonDecline"],["accept","#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]]){
const ctx=await b.newContext({locale:'de-DE',viewport:{width:1366,height:900}});const p=await ctx.newPage();
const errs=[];p.on('pageerror',e=>errs.push('PE:'+e.message));p.on('console',m=>{if(m.type()=='error')errs.push('CE:'+m.text().slice(0,140))});
const pops=[];ctx.on('page',np=>pops.push(np));
await p.goto('https://www.hotel-am-leuchtturm.de/DE/home.html',{waitUntil:'networkidle',timeout:60000}).catch(()=>{});
await p.waitForTimeout(1500);
await p.click(sel,{timeout:5000}).catch(e=>console.log(choice,'consent click fail'));
await p.waitForTimeout(2500);
const vis=await p.evaluate(()=>({title:getComputedStyle(document.querySelector('#booking-title')).display,form:getComputedStyle(document.querySelector('#booking form')).display,box:getComputedStyle(document.querySelector('#booking')).display,api:typeof window.d21_api}));
console.log(choice,'state',JSON.stringify(vis));
await p.click('#booking-title',{timeout:5000}).catch(()=>console.log('title click fail'));
await p.waitForTimeout(1500);
await p.fill('input[name=anreise]','10.11.2026').catch(()=>console.log('fill fail'));
await p.fill('input[name=abreise]','12.11.2026').catch(()=>{});
await p.click('#booking input.submit',{timeout:5000}).catch(()=>console.log('submit click fail'));
await p.waitForTimeout(10000);
const fr=p.frames().map(f=>f.url()).filter(u=>/dirs21/.test(u));
console.log(choice,'after submit: url',p.url(),'| dirs21 frames',fr.length,fr[0]||'','| popups',pops.map(x=>x.url()).join(','),'| errors',errs.slice(0,4).join(' / '));
await ctx.close();}
await b.close();})();
