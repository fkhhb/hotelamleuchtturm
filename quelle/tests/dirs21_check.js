// Fragt die echte DIRS21-Buchung des Hotels ab und listet Zimmertypen und Preise pro Nacht.
// Aufruf: node quelle/tests/dirs21_check.js 2026-11-10:2026-11-12 2027-07-12:2027-07-18   (AD=1 für 1 Erwachsenen)
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const r of process.argv.slice(2)){const [a,d]=r.split(':');
const p=await b.newPage({locale:'de-DE',viewport:{width:1366,height:900}});
const u=`https://reservation.one.dirs21.de/hotel-am-leuchtturmde?range=${a},${d}&sets=[{"occupancy":{"adultCount":${process.env.AD||2},"children":[]}}]&culture=de-DE&show_results=true`;
await p.goto(u,{waitUntil:'networkidle',timeout:60000}).catch(()=>{});
await p.getByRole("button",{name:/ablehnen/i}).click({timeout:8000}).catch(()=>{});
await p.getByRole('button',{name:'Suchen'}).first().click({timeout:8000}).catch(()=>{});
await p.waitForTimeout(9000);
const L=(await p.evaluate(()=>document.body.innerText)).split("\n").map(s=>s.trim()).filter(Boolean);
const out=[];let cur=null;
for(const l of L){const m=l.match(/^Allgemeine Informationen : (.*)/);if(m){cur=m[1];continue;}
 if(cur&&/€/.test(l)){out.push(cur+" = "+l);cur=null;}}
const cnt=L.find(l=>/verfügbare Zimmertypen|keine/i.test(l));
console.log(`## ${a} → ${d}: ${cnt||''}\n  `+out.join("\n  "));await p.close();}
await b.close();})();
