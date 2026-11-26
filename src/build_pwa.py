"""Sestaví PWA verzi appky F-plyny pro GitHub Pages (repo VM73/fplyny).
Vstup: fplyny.html (verze pro Claude). Výstup: pwa/ (index.html, sw.js, manifest, ikony).
Úložiště Claude se nahradí Supabase (osobní projekt, schéma fplyny, tabulka pokrok)."""
import os, re, shutil
VERZE = "verze 18"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "pwa")
os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(HERE, "fplyny.html"), encoding="utf-8").read()

def rep(a, b, s):
    assert s.count(a) == 1, ("nenalezeno / vícekrát", a[:60])
    return s.replace(a, b)

# 1) synchronizace: Claude úložiště → Supabase
start = src.index("async function initCloud(){")
end = src.index("const shuffle=")
cloud = r'''const SUPABASE_URL="https://klpcgnivfvczvvyoqzal.supabase.co";
const SUPABASE_KEY="sb_publishable_6mo7Xg3GQ4GTi9Qu7AAeKw_HKPSXacV";
const sb=(window.supabase&&supabase.createClient)?supabase.createClient(SUPABASE_URL,SUPABASE_KEY,{db:{schema:"fplyny"}}):null;
let userEmail="";
function sbRef(uid){return{
  async get(){const {data,error}=await sb.from("pokrok").select("data").eq("user_id",uid).maybeSingle();if(error)throw error;log("načteno z účtu: "+(data?"ano":"zatím nic"));return{exists:!!data,data:()=>data&&data.data}},
  async set(d){const {error}=await sb.from("pokrok").upsert({user_id:uid,data:d,updated_at:new Date().toISOString()});if(error)throw error;log("uloženo k účtu")}
}}
async function initCloud(){
  try{
    if(!sb){setSync("Pokrok: jen v tomto zařízení (Supabase nedostupný)","err");log("supabase-js se nenačetl");return}
    const {data:{session}}=await sb.auth.getSession();
    if(!session){cloud=null;setSync("Pokrok: jen v tomto zařízení · klepni a přihlas se");return}
    userEmail=session.user.email||"";
    const ref=sbRef(session.user.id);
    setSync("Pokrok: načítám z účtu…");
    const snap=await Promise.race([ref.get(),new Promise((_,rej)=>setTimeout(()=>rej(new Error("timeout 10 s")),10000))]);
    cloud=ref;
    const changed=snap.exists?mergeRemote(snap.data()):false;
    try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}
    setSync("Pokrok: uložen k účtu","on");
    if(!snap.exists||changed)pushCloud();
    if(changed){const cur=document.querySelector('#nav button[aria-pressed="true"]');if(cur&&!document.querySelector("#next,.opt:disabled,#clock"))go(cur.dataset.v)}
  }catch(e){log("chyba synchronizace: "+(e.message||e));setSync("Pokrok: účet nedostupný, ukládá se v tomto zařízení","err")}
}
document.addEventListener("visibilitychange",async()=>{if(document.visibilityState!=="visible"||!cloud)return;
  try{const s2=await cloud.get();if(s2.exists&&mergeRemote(s2.data())){try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}}}catch(e){log("načtení při návratu selhalo: "+(e.message||e))}});
function account(){
  document.querySelectorAll("#nav button").forEach(b=>b.setAttribute("aria-pressed",false));
  if(cloud){view.innerHTML=`<div class="card"><p class="label">Účet</p><p class="hint">Přihlášen: <b>${esc(userEmail)}</b>. Pokrok se ukládá k účtu i v tomto zařízení.</p><button class="btn ghost" id="logout">Odhlásit</button></div>`;
    $("#logout").onclick=async()=>{await sb.auth.signOut();cloud=null;userEmail="";setSync("Pokrok: jen v tomto zařízení · klepni a přihlas se");go("learn")};return}
  view.innerHTML=`<form class="card" id="lf"><p class="label">Přihlášení</p><p class="hint">Stejný účet jako v MTB servisu. Bez přihlášení appka funguje, pokrok zůstane jen v tomto zařízení.</p>
  <div class="calc" style="grid-template-columns:1fr"><label for="lEmail">E-mail<input id="lEmail" type="email" autocomplete="username" required></label>
  <label for="lHeslo">Heslo<input id="lHeslo" type="password" autocomplete="current-password" required></label></div>
  <p class="hint" id="lErr" style="color:var(--bad)"></p><button class="btn" type="submit">Přihlásit</button></form>`;
  $("#lf").onsubmit=async e=>{e.preventDefault();if(!sb){$("#lErr").textContent="Supabase se nenačetl – zkontroluj připojení.";return}
    $("#lErr").textContent="";const {error}=await sb.auth.signInWithPassword({email:$("#lEmail").value.trim(),password:$("#lHeslo").value});
    if(error){log("přihlášení: "+error.message);$("#lErr").textContent="Přihlášení se nepovedlo: "+error.message;return}
    await initCloud();go("learn")};
}
// diagnostika (?debug=1 nebo při chybě JS)
const DEBUG=/[?&]debug=1/.test(location.search);const LOG=[];
function log(m){LOG.push(new Date().toLocaleTimeString("cs-CZ")+" "+m);if(DEBUG||showLog)renderLog()}
let showLog=false;
function renderLog(){let p=document.getElementById("dbg");if(!p){p=document.createElement("pre");p.id="dbg";document.body.appendChild(p)}p.textContent=LOG.slice(-40).join("\n")}
window.addEventListener("error",e=>{showLog=true;log("JS chyba: "+e.message+" ("+(e.lineno||"")+")")});
window.addEventListener("unhandledrejection",e=>{showLog=true;log("Promise: "+((e.reason&&e.reason.message)||e.reason))});
'''
src = src[:start] + cloud + src[end:]

# 2) řádek se stavem je klikací → účet / přihlášení
src = rep('<p class="sync" id="sync"><i></i><span>Pokrok: jen v tomto zařízení</span></p>',
          '<button class="sync" id="sync" type="button"><i></i><span>Pokrok: jen v tomto zařízení</span></button>', src)
src = rep("\ninitCloud();", '\ninitCloud();\n$("#sync").onclick=account;\nif("serviceWorker" in navigator&&location.protocol==="https:")navigator.serviceWorker.register("sw.js").catch(e=>log("SW: "+e.message));\nif(DEBUG)renderLog();', src)
src = src.replace("Pokrok se ukládá k tvému účtu claude.ai a zároveň v prohlížeči.", "Pokrok se ukládá v tomto zařízení a po přihlášení i k účtu. " + VERZE + ".")
src = rep(".sync i{", ".sync{background:none;border:0;padding:0;font:inherit;font-size:12px;cursor:pointer;text-align:left}\n#dbg{position:fixed;left:0;right:0;bottom:0;max-height:40vh;overflow:auto;margin:0;padding:8px 12px calc(8px + env(safe-area-inset-bottom,0px));background:#111;color:#9f9;font:11px/1.4 ui-monospace,Menlo,monospace;z-index:50;white-space:pre-wrap}\n.sync i{", src)

# 3) plný dokument pro GitHub Pages
src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
head = f'''<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#1f6fd1">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="F-plyny">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="favicon-32.png" sizes="32x32">
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js"></script>
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}</style>
'''
src = head + src.replace("</style>\n", "</style>\n</head>\n<body>\n", 1) + "\n</body>\n</html>\n"
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(src)

open(os.path.join(OUT, "manifest.webmanifest"), "w", encoding="utf-8").write('''{
  "name": "F-plyny Přeškolení",
  "short_name": "F-plyny",
  "description": "Příprava na přeškolení F-plynů A1/A2 a kategorie B a C",
  "lang": "cs",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#eef2f5",
  "theme_color": "#1f6fd1",
  "icons": [
    {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
    {"src": "icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]
}
''')
open(os.path.join(OUT, "sw.js"), "w", encoding="utf-8").write(f'''// F-plyny – service worker: soubory appky ze sítě, při výpadku z cache. Supabase se necachuje.
const CACHE = 'fplyny-{VERZE.split()[-1]}';
const SOUBORY = ['./', 'index.html', 'manifest.webmanifest', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png', 'favicon-32.png'];
self.addEventListener('install', e => {{ e.waitUntil(caches.open(CACHE).then(c => c.addAll(SOUBORY)).then(() => self.skipWaiting())); }});
self.addEventListener('activate', e => {{ e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== CACHE).map(x => caches.delete(x)))).then(() => self.clients.claim())); }});
self.addEventListener('fetch', e => {{
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin) return;
  const fresh = !/\.(webp|png)$/.test(u.pathname); // stránka a skripty vždy ověřit na serveru (obejde 10min cache GitHub Pages)
  e.respondWith(fetch(e.request, fresh ? {{cache: 'no-cache'}} : {{}}).then(r => {{ const k = r.clone(); caches.open(CACHE).then(c => c.put(e.request, k)); return r; }})
    .catch(() => caches.match(e.request).then(r => r || caches.match('index.html'))));
}});
''')
ik = os.path.join(HERE, "ikona")
for a, b in [("icon-192.png", "icon-192.png"), ("icon-512.png", "icon-512.png"), ("icon-maskable-512.png", "icon-512-maskable.png"),
             ("apple-touch-icon.png", "apple-touch-icon.png"), ("favicon-32.png", "favicon-32.png")]:
    shutil.copy(os.path.join(ik, a), os.path.join(OUT, b))
print("hotovo", sorted(os.listdir(OUT)))
