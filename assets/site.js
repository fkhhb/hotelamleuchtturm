/* Hotel am Leuchtturm – Konzeptentwurf
   Echte Daten: Zimmer, Ausstattung und Saisonpreise 2026 laut hotel-am-leuchtturm.de (Preise ohne Frühstück).
   Demo-Werte: Verfügbarkeit, Frühstückspreis, Kurtaxe, Spartarif, Sekt. */
(function(){
"use strict";
const ROOT = document.body.dataset.root || "";
const $ = (s, el=document) => el.querySelector(s);
const $$ = (s, el=document) => [...el.querySelectorAll(s)];

/* ---------- Daten ---------- */
const ROOMS = [
  {slug:"panorama-terrassen-doppelzimmer", name:"Panorama-Terrassen-Doppelzimmer", view:"Direkter Ostseeblick", extra:"40 m² Dachterrasse mit Strandkorb", size:"20 m²", floor:"1. Etage", bed:"Doppelbett 180 × 200 cm", max:2, prices:{N:269,Z:309,H:339}, img:"ptdz-5"},
  {slug:"panorama-doppelzimmer", name:"Panorama-Doppelzimmer", view:"Direkter Ostseeblick", extra:"2. und 3. Etage", size:"20 m²", floor:"2. und 3. Etage", bed:"Doppelbett 180 × 200 cm", max:2, prices:{N:259,Z:289,H:319}, img:"pdz-4"},
  {slug:"terrassen-doppelzimmer", name:"Terrassen-Doppelzimmer", view:"Seitlicher Ostseeblick oder Leuchtturm", extra:"12 m² Dachterrasse", size:"17–20 m²", floor:"1. Etage", bed:"Doppelbett 180 × 200 cm", max:2, prices:{N:219,Z:259,H:299}, img:"tdz-1"},
  {slug:"komfort-doppelzimmer", name:"Komfort-Doppelzimmer", view:"Seitlicher Ostseeblick oder Leuchtturm", extra:"teils Betten 2,10 m lang", size:"17–20 m²", floor:"1. bis 3. Etage", bed:"Doppelbett 180 × 200 cm", max:2, prices:{N:209,Z:239,H:279}, img:"kdz-2"},
  {slug:"doppelzimmer", name:"Doppelzimmer", view:"Dachgeschoss mit Dachfenstern", extra:"leichte Dachschräge", size:"15–18 m²", floor:"3. Etage", bed:"Doppelbett 180 × 200 cm", max:2, prices:{N:179,Z:209,H:229}, img:"dz-4"},
  {slug:"einzelzimmer", name:"Einzelzimmer", view:"Dachgeschoss mit Dachfenstern", extra:"Queensize-Bett", size:"15–18 m²", floor:"3. Etage", bed:"Bett 100 × 200 cm", max:2, prices:{N:139,Z:159,H:199}, img:"ez-1"}
];
const PARKING = 14;           // echt: Vorzugspreis Tiefgarage Kurhaus pro 24 h
const BREAKFAST = 22;         // Demo
const KURTAXE = 3;            // Demo
const SAVER = 0.10;           // Vorschlag
const EXTRAS = [
  {id:"fruehstueck", name:"Frühstücksbuffet in der Frühstückslounge", note:"pro Person und Nacht", price:BREAKFAST, per:"pn", demo:true},
  {id:"parken", name:"Parkticket Tiefgarage Kurhaus (ca. 400 m)", note:"Vorzugspreis für Hotelgäste, pro 24 h", price:PARKING, per:"n"},
  {id:"latecheckout", name:"Später Check-out bis 13 Uhr", note:"Vorschlag · nach Verfügbarkeit", price:0, per:"x"},
  {id:"sekt", name:"Flasche Sekt bei Anreise im Zimmer", note:"Vorschlag", price:29, per:"x", demo:true}
];
const roomBy = s => ROOMS.find(r => r.slug === s);
/* Echter DIRS21-Deep-Link (funktioniert heute, ermittelt aus der Buchungsmaske der Hotel-Website) */
const dirs21Url = st => "https://reservation.one.dirs21.de/hotel-am-leuchtturmde?range=" + st.arrival + "," + st.departure +
  "&sets=" + encodeURIComponent(JSON.stringify([{occupancy:{adultCount:+st.adults, children:[]}}])) + "&culture=de-DE&show_results=true";
const img = (k) => ROOT + "img/" + k + ".jpg";

/* ---------- Datum ---------- */
const D = s => new Date(s + "T12:00:00Z");
const iso = d => d.toISOString().slice(0,10);
const today = () => { const t=new Date(); return new Date(Date.UTC(t.getFullYear(), t.getMonth(), t.getDate(), 12)); };
const add = (d,n) => { const x=new Date(d); x.setUTCDate(x.getUTCDate()+n); return x; };
const nights = (a,b) => Math.max(0, Math.round((D(b)-D(a))/864e5));
const fmt = (s, o={day:"numeric", month:"short"}) => D(s).toLocaleDateString("de-DE", {...o, timeZone:"UTC"});
const euro = n => n.toLocaleString("de-DE", {style:"currency", currency:"EUR", maximumFractionDigits:0});
const validDates = (a,b) => /^\d{4}-\d{2}-\d{2}$/.test(a||"") && /^\d{4}-\d{2}-\d{2}$/.test(b||"") && b > a;

/* Saisons laut Preisliste 2026 (Tag/Monat-Muster, für 2027 fortgeschrieben) */
function season(s){
  const md = s.slice(5);
  if (md >= "12-24" || md <= "01-04") return "H";
  if (md <= "03-31") return "N";
  if (md <= "05-12") return "Z";
  if (md <= "10-03") return "H";
  if (md <= "10-31") return "Z";
  return "N";
}
const SEASON_NAME = {N:"Nebensaison", Z:"Zwischensaison", H:"Hauptsaison"};
function minStay(a){
  const s = season(a), wd = D(a).getUTCDay();
  if (s === "H") return 6;
  if (s === "Z") return 4;
  if (s === "N" && (wd === 5 || wd === 6)) return 2;
  return 1;
}
/* Demo-Verfügbarkeit: deterministisch je Zimmer und Nacht */
function freeNight(r, s){ let h=0; const k=r.slug+s; for (let i=0;i<k.length;i++) h=(h*31+k.charCodeAt(i))>>>0; return h % 6 !== 0; }
function freeStay(r, a, b){ for (let d=D(a); iso(d)<b; d=add(d,1)) if (!freeNight(r, iso(d))) return false; return true; }
function nextFree(r, n=3, count=3, from=add(today(),3)){
  const out=[]; let d=new Date(from);
  for (let i=0; i<240 && out.length<count; i++, d=add(d,1)){
    const a=iso(d), need=Math.max(n, minStay(a)), b=iso(add(d,need));
    if (freeStay(r,a,b)) { out.push([a,b]); d=add(d,need+1); }
  }
  return out;
}
function quote(r, a, b, adults, rate="flex", extras=[]){
  const n = nights(a,b); let room = 0;
  for (let d=D(a); iso(d)<b; d=add(d,1)) room += r.prices[season(iso(d))];
  const disc = rate === "saver" ? Math.round(room*SAVER) : 0;
  const kur = KURTAXE*adults*n;
  const ex = extras.map(id => EXTRAS.find(e => e.id===id)).filter(Boolean).map(e => ({...e, amount: e.per==="pn" ? e.price*adults*n : e.per==="n" ? e.price*n : e.price}));
  return {n, room, disc, kur, ex, total: room - disc + kur + ex.reduce((s,e)=>s+e.amount,0)};
}
function bookUrl(p){
  const q = new URLSearchParams();
  ["arrival","departure","adults","room","rate","extras","offer","step"].forEach(k => { if (p[k] !== undefined && p[k] !== "" && !(Array.isArray(p[k]) && !p[k].length)) q.set(k, Array.isArray(p[k]) ? p[k].join(",") : p[k]); });
  return ROOT + "buchen.html" + (q.toString() ? "?" + q : "");
}

/* ---------- Kleinteile ---------- */
function toast(t){ const el=$("#toast"); if(!el) return; el.textContent=t; el.classList.add("on"); clearTimeout(toast.t); toast.t=setTimeout(()=>el.classList.remove("on"), 3400); }
function store(k, v){ try { if (v===undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch(_) { return null; } }

function initChrome(){
  // Konzept-Hinweise
  const btn = $("#toggleNotes");
  if (store("hal-notes") === "off") document.body.classList.remove("notes");
  const label = () => { if (btn) btn.textContent = document.body.classList.contains("notes") ? "Hinweise ausblenden" : "Hinweise einblenden"; };
  label();
  if (btn) btn.onclick = () => { document.body.classList.toggle("notes"); store("hal-notes", document.body.classList.contains("notes") ? "on" : "off"); label(); };
  // Menü mobil
  const burger = $(".burger"), menu = $(".menu");
  if (burger) burger.onclick = () => { const o = menu.classList.toggle("open"); burger.setAttribute("aria-expanded", o); };
  // Toasts
  document.addEventListener("click", e => { const t=e.target.closest("[data-toast]"); if (t){ e.preventDefault(); toast(t.dataset.toast); } });
  // Lightbox
  const lb = $("#lightbox");
  if (lb){
    document.addEventListener("click", e => { const t=e.target.closest("[data-zoom]"); if (t){ $("img", lb).src = t.currentSrc || t.src; $("img", lb).alt = t.alt; lb.classList.add("on"); } });
    lb.onclick = () => lb.classList.remove("on");
    document.addEventListener("keydown", e => { if (e.key==="Escape") lb.classList.remove("on"); });
  }
  // Datumsfelder: Mindestdatum
  $$('input[type=date]').forEach(i => i.min = iso(today()));
}

/* ---------- Suchmaske (Startseite) ---------- */
function initSearch(){
  const f = $("#search"); if (!f) return;
  const a=$("#s-arr", f), b=$("#s-dep", f);
  a.addEventListener("change", () => { if (!b.value || b.value <= a.value) b.value = iso(add(D(a.value), Math.max(2, minStay(a.value)))); });
  f.addEventListener("submit", e => {
    e.preventDefault();
    if (!validDates(a.value, b.value)) { toast("Bitte Anreise und Abreise wählen."); return; }
    location.href = bookUrl({arrival:a.value, departure:b.value, adults:$("#s-ad",f).value, room:$("#s-room",f).value, step: $("#s-room",f).value ? 2 : 1});
  });
}

/* ---------- Nächste freie Termine auf Karten ---------- */
function initSlots(){
  $$("[data-slots]").forEach(box => {
    const r = roomBy(box.dataset.slots); if (!r) return;
    box.innerHTML = nextFree(r).map(([a,b]) => {
      const q = quote(r, a, b, 2);
      return `<a class="slot" href="${bookUrl({arrival:a, departure:b, adults:2, room:r.slug, step:2})}" title="${q.n} Nächte, ${euro(q.room)} Zimmerpreis">${fmt(a)}–${fmt(b)}</a>`;
    }).join("");
  });
}

/* ---------- Buchungsbox auf der Zimmerseite ---------- */
function initBookcard(){
  const c = $("[data-bookcard]"); if (!c) return;
  const r = roomBy(c.dataset.bookcard);
  const a=$("#b-arr",c), b=$("#b-dep",c), ad=$("#b-ad",c), out=$("#b-sum",c), go=$("#b-go",c);
  const first = nextFree(r)[0]; a.value = first[0]; b.value = first[1];
  function upd(){
    if (!validDates(a.value,b.value)) { out.innerHTML = "Bitte Reisedaten wählen."; go.setAttribute("aria-disabled","true"); return; }
    const n = nights(a.value,b.value), ms = minStay(a.value);
    let h = "";
    if (freeStay(r, a.value, b.value)) {
      const q = quote(r, a.value, b.value, +ad.value);
      h = `${n} ${n===1?"Nacht":"Nächte"} · ${SEASON_NAME[season(a.value)]}<br><b>Zimmer ${euro(q.room)}</b> · ohne Frühstück <span class="demo">Verfügbarkeit Demo</span>`;
      go.removeAttribute("aria-disabled");
    } else {
      const alt = nextFree(r, n, 3, D(a.value));
      h = `<b>An diesen Daten belegt.</b> Nächste freie Termine:<div class="slots">${alt.map(([x,y]) => `<a class="slot" href="#" data-pick="${x}|${y}">${fmt(x)}–${fmt(y)}</a>`).join("")}</div>`;
      go.setAttribute("aria-disabled","true");
    }
    if (n < ms) h += `<div class="warn">Mindestaufenthalt bei dieser Anreise: ${ms} Nächte. Kürzere Aufenthalte sind kurzfristig bei Verfügbarkeit buchbar.</div>`;
    out.innerHTML = h;
    go.href = bookUrl({arrival:a.value, departure:b.value, adults:ad.value, room:r.slug, step:2});
  }
  a.addEventListener("change", () => { if (b.value <= a.value) b.value = iso(add(D(a.value), Math.max(2,minStay(a.value)))); upd(); });
  b.addEventListener("change", upd); ad.addEventListener("change", upd);
  out.addEventListener("click", e => { const t=e.target.closest("[data-pick]"); if (t){ e.preventDefault(); [a.value,b.value] = t.dataset.pick.split("|"); upd(); } });
  go.addEventListener("click", e => { if (go.getAttribute("aria-disabled")) { e.preventDefault(); toast("Bitte freie Reisedaten wählen."); } });
  upd();
}

/* ---------- Buchungsstrecke ---------- */
function initBooking(){
  const app = $("#booking"); if (!app) return;
  const st = {arrival:"", departure:"", adults:2, room:"", rate:"flex", extras:["fruehstueck"], offer:"", step:1};
  const p = new URLSearchParams(location.search);
  if (validDates(p.get("arrival"), p.get("departure"))) { st.arrival=p.get("arrival"); st.departure=p.get("departure"); }
  st.adults = p.get("adults")==="1" ? 1 : 2;
  st.room = roomBy(p.get("room")||"") ? p.get("room") : "";
  st.rate = p.get("rate")==="saver" ? "saver" : "flex";
  if (p.has("extras")) st.extras = p.get("extras").split(",").filter(id => EXTRAS.some(e=>e.id===id));
  st.offer = p.get("offer")==="wintertage" ? "wintertage" : "";
  st.step = Math.min(4, Math.max(1, parseInt(p.get("step")||"1",10)||1));
  if (!validDates(st.arrival, st.departure)) { const s=add(today(),14); st.arrival=iso(s); st.departure=iso(add(s,3)); }
  if (st.step > 1 && !st.room) st.step = 1;

  const write = () => {
    const url = bookUrl({arrival:st.arrival, departure:st.departure, adults:st.adults, room:st.room, rate: st.step>=3?st.rate:"", extras: st.step>=4?st.extras:"", offer:st.offer, step:st.step});
    history.replaceState(null, "", url.replace(ROOT, ""));
    $$(".js-url").forEach(el => el.textContent = location.href);
  };
  const go = (step) => { st.step = step; history.pushState(null, "", ""); render(); write(); window.scrollTo({top: app.offsetTop - 110, behavior:"smooth"}); };
  window.addEventListener("popstate", () => location.reload());

  function render(){
    const r = roomBy(st.room);
    const n = nights(st.arrival, st.departure), ms = minStay(st.arrival);
    // Stepper
    $$("#stepper a").forEach((a,i) => { a.className = i+1 < st.step ? "done" : i+1 === st.step ? "on" : ""; a.onclick = e => { e.preventDefault(); if (i+1 < st.step || (r && i+1 <= 4)) go(i+1); }; });
    // Datum/Gäste
    $("#k-arr").value = st.arrival; $("#k-dep").value = st.departure; $("#k-ad").value = st.adults;
    const body = $("#step");
    if (st.step === 1){
      body.innerHTML = `<h2 class="caps" style="font-size:28px">Zimmer wählen</h2>
        <p class="lead" style="font-size:16px;margin-top:8px">${fmt(st.arrival,{weekday:"short",day:"numeric",month:"long"})} – ${fmt(st.departure,{weekday:"short",day:"numeric",month:"long",year:"numeric"})} · ${n} ${n===1?"Nacht":"Nächte"} · ${st.adults} ${st.adults===1?"Erwachsener":"Erwachsene"} · ${SEASON_NAME[season(st.arrival)]}</p>
        ${n < ms ? `<p class="warn">Mindestaufenthalt bei dieser Anreise: ${ms} Nächte. Kürzere Aufenthalte sind kurzfristig bei Verfügbarkeit buchbar.</p>` : ""}
        <div style="margin-top:18px">${ROOMS.map(x => {
          const free = freeStay(x, st.arrival, st.departure), q = quote(x, st.arrival, st.departure, st.adults);
          return `<label class="opt roomopt" ${free?"":'style="opacity:.75"'}>
            <img src="${img(x.img)}" alt="${x.name}" loading="lazy">
            <div><input type="radio" name="room" value="${x.slug}" ${x.slug===st.room?"checked":""} ${free?"":"disabled"} style="position:absolute;opacity:0">
              <b style="color:var(--navy);font-size:17px">${x.name}</b><small>${x.view} · ${x.size} · ${x.extra}</small>
              ${free ? "" : `<small style="color:#9a3b12">Belegt – nächste freie Termine: ${nextFree(x, n, 2, D(st.arrival)).map(([a,b]) => `<a href="#" data-alt="${x.slug}|${a}|${b}">${fmt(a)}–${fmt(b)}</a>`).join(", ")}</small>`}</div>
            <div class="p">${free ? euro(q.room) + '<small style="font-weight:400">Zimmer, ohne Frühstück</small>' : "—"}</div></label>`;}).join("")}</div>
        <p class="slots-h">Preise laut Preisliste 2026 (ab-Preise je Saison). Verfügbarkeit ist im Entwurf simuliert <span class="demo">Demo</span></p>
        <div class="note" data-n="1"><b>Jeder Schritt hat eine eigene URL.</b> Schauen Sie in die Adresszeile: Daten, Gäste und – ab Schritt 2 – Zimmer, Rate und Extras stehen darin. Neu laden, kopieren oder per WhatsApp schicken: derselbe Stand erscheint.</div>`;
      $$('input[name=room]', body).forEach(i => i.closest("label").addEventListener("click", e => { if (e.target.closest("[data-alt]") || i.disabled) return; st.room = i.value; go(2); }));
      $$("[data-alt]", body).forEach(a => a.onclick = e => { e.preventDefault(); e.stopPropagation(); const [s,x,y]=a.dataset.alt.split("|"); st.room=s; st.arrival=x; st.departure=y; go(2); });
    }
    if (st.step === 2 && r){
      const flex = quote(r, st.arrival, st.departure, st.adults, "flex").room;
      const saver = flex - Math.round(flex*SAVER);
      body.innerHTML = `<h2 class="caps" style="font-size:28px">Rate wählen</h2>
        <div style="margin-top:18px">
        <label class="opt"><input type="radio" name="rate" value="flex" ${st.rate==="flex"?"checked":""}><div><b style="color:var(--navy)">Flexibel</b><small>Kostenfrei stornierbar bis 14 Tage vor Anreise · Zahlung im Hotel (EC-Karte, bar) oder per Vorauszahlung</small></div><span class="p">${euro(flex)}</span></label>
        <label class="opt"><input type="radio" name="rate" value="saver" ${st.rate==="saver"?"checked":""}><div><b style="color:var(--navy)">Spartarif −10 %</b> <span class="demo">Vorschlag</span><small>Nicht erstattbar · Zahlung bei Buchung</small></div><span class="p">${euro(saver)}</span></label>
        </div>
        <div class="note" data-n="2"><b>Zwei klare Raten, nicht mehr.</b> Die Stornoregel (14 Tage) steht heute nur auf der Preisseite. Hier steht sie direkt an der Rate – und sollte auf allen Portalen gleich lauten.</div>
        <div class="navbtns"><button class="btn btn-line" type="button" data-step="1">Zurück</button><button class="btn btn-navy" type="button" data-step="3">Weiter zu den Extras</button></div>`;
      $$('input[name=rate]', body).forEach(i => i.onchange = () => { st.rate = i.value; renderSummary(); write(); });
    }
    if (st.step === 3 && r){
      body.innerHTML = `<h2 class="caps" style="font-size:28px">Extras</h2>
        <div style="margin-top:18px">${EXTRAS.map(e => { const a = e.per==="pn" ? e.price*st.adults*n : e.per==="n" ? e.price*n : e.price;
          return `<label class="opt"><input type="checkbox" value="${e.id}" ${st.extras.includes(e.id)?"checked":""}><div><b style="color:var(--navy)">${e.name}</b><small>${e.note}${e.demo?' · <span class="demo">Demo-Preis</span>':""}</small></div><span class="p">${a?euro(a):"inklusive"}</span></label>`; }).join("")}</div>
        <div class="note" data-n="3"><b>Zusatzleistungen direkt in der Buchung:</b> Das Parkticket für die Kurhaus-Tiefgarage (14 € / 24 h) muss heute vor Ort an der Rezeption gekauft werden. Hier ist es mit einem Klick dabei.</div>
        <div class="navbtns"><button class="btn btn-line" type="button" data-step="2">Zurück</button><button class="btn btn-navy" type="button" data-step="4">Weiter zur Übersicht</button></div>`;
      $$('input[type=checkbox]', body).forEach(i => i.onchange = () => { st.extras = $$('input:checked', body).map(x=>x.value); renderSummary(); write(); });
    }
    if (st.step === 4 && r){
      body.innerHTML = `<h2 class="caps" style="font-size:28px">Übersicht</h2>
        <p style="margin-top:12px">Bitte prüfen Sie Ihre Auswahl. Rechts sehen Sie den Gesamtpreis inklusive aller gewählten Leistungen und der Kurtaxe.</p>
        <div class="opt" style="cursor:default;display:block;background:var(--paper)">
          <b style="color:var(--navy)">In der echten Buchung folgt hier:</b>
          <ul class="ticks" style="margin-top:8px"><li>ein kurzes Formular: Name, E-Mail, Telefon</li><li>Zahlung über das Buchungssystem (DIRS21)</li><li>sofortige Bestätigung per E-Mail mit Link „Meine Buchung verwalten“</li></ul>
          <p style="margin:12px 0 0"><b>In diesem Entwurf endet der Ablauf hier.</b> Die echte Verfügbarkeit für Ihre Daten können Sie schon heute direkt im Buchungssystem des Hotels prüfen – per Link, ohne Umweg:</p>
          <p style="margin:12px 0 0"><a class="btn btn-line" href="${dirs21Url(st)}" target="_blank" rel="noopener">Echte Verfügbarkeit bei DIRS21 prüfen ↗</a></p></div>
        <div class="share"><span>Diese Auswahl teilen:</span><code class="js-url"></code><button type="button" data-copy>Link kopieren</button></div>
        <div class="note" data-n="4"><b>Teilbarer Buchungslink:</b> Genau diese Adresse kann die Rezeption per E-Mail oder WhatsApp schicken, ein KI-Assistent einem Gast übergeben oder eine Anzeige als Ziel verwenden.</div>
        <div class="navbtns"><button class="btn btn-line" type="button" data-step="3">Zurück</button><button class="btn btn-navy" type="button" disabled>Weiter zur Zahlung</button></div>`;
    }
    $$("[data-step]", body).forEach(bt => bt.onclick = () => go(+bt.dataset.step));
    renderSummary();
  }
  function renderSummary(){
    const box = $("#summary"), r = roomBy(st.room);
    const n = nights(st.arrival, st.departure);
    if (!r){ box.innerHTML = `<h3 style="font-size:22px">Ihre Reise</h3><p style="margin-top:8px">${fmt(st.arrival)} – ${fmt(st.departure)} · ${n} ${n===1?"Nacht":"Nächte"} · ${st.adults} ${st.adults===1?"Person":"Personen"}</p><p class="slots-h">Wählen Sie links ein Zimmer.</p>`; return; }
    const q = quote(r, st.arrival, st.departure, st.adults, st.rate, st.step>=3 ? st.extras : []);
    box.innerHTML = `<img src="${img(r.img)}" alt="${r.name}"><h3 style="font-size:22px">${r.name}</h3>
      <p class="slots-h" style="margin:4px 0 10px">${fmt(st.arrival)} – ${fmt(st.departure,{day:"numeric",month:"short",year:"numeric"})} · ${n} ${n===1?"Nacht":"Nächte"} · ${st.adults} ${st.adults===1?"Person":"Personen"}${st.step>=2?" · "+(st.rate==="saver"?"Spartarif":"Flexibel"):""}</p>
      <div class="line"><span>Zimmer</span><span>${euro(q.room)}</span></div>
      ${q.disc?`<div class="line"><span>Spartarif −10 %</span><span>−${euro(q.disc)}</span></div>`:""}
      ${q.ex.map(e=>`<div class="line"><span>${e.name.split(" (")[0]}</span><span>${e.amount?euro(e.amount):"inklusive"}</span></div>`).join("")}
      <div class="line"><span>Kurtaxe <span class="demo">Demo</span></span><span>${euro(q.kur)}</span></div>
      <div class="line tot"><span>Gesamt</span><span>${euro(q.total)}</span></div>
      <p class="slots-h">${st.rate==="flex"?"Kostenfrei stornierbar bis "+fmt(iso(add(D(st.arrival),-14)),{day:"numeric",month:"long"}):"Nicht erstattbar"} · Preise inkl. MwSt.</p>`;
    const mb = $("#mbar-txt"); if (mb) mb.innerHTML = `<b>${euro(q.total)} gesamt</b>${fmt(st.arrival)}–${fmt(st.departure)}`;
  }
  // Datum ändern
  $("#k-form").addEventListener("submit", e => {
    e.preventDefault();
    const a=$("#k-arr").value, b=$("#k-dep").value;
    if (!validDates(a,b)) { toast("Bitte eine Abreise nach der Anreise wählen."); return; }
    st.arrival=a; st.departure=b; st.adults=+$("#k-ad").value; go(1);
  });
  $("#k-arr").addEventListener("change", () => { const a=$("#k-arr").value, b=$("#k-dep"); if (!b.value || b.value<=a) b.value = iso(add(D(a), Math.max(2,minStay(a)))); });
  document.addEventListener("click", async e => { if (e.target.closest("[data-copy]")) { try { await navigator.clipboard.writeText(location.href); toast("Link kopiert – öffnen Sie ihn in einem anderen Fenster."); } catch(_) { toast("Bitte die Adresse markieren und kopieren."); } } });
  if (st.offer === "wintertage") toast("Arrangement „Wintertage in Warnemünde“: Preis laut Angebot ab 105 € p. P./Nacht inkl. Frühstück, Kurtaxe und Parken.");
  render(); write();
}

initChrome(); initSearch(); initSlots(); initBookcard(); initBooking();
window.HAL = {ROOMS, quote, nextFree, season, minStay};
})();
