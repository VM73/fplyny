"""Náhled prezentace: složí slajdy do HTML s lokálními fonty, zkontroluje přetečení a udělá náhledy."""
import json, os, re, sys
from playwright.sync_api import sync_playwright

ROOT = "/tmp/claude-0/-home-claude/f491fb96-a910-5c47-9c15-8b98fcb8fe28/scratchpad/deck/project"
SVG = "/home/claude/prez/svg"
HERE = os.path.dirname(os.path.abspath(__file__))
BLOBS = {
 "3045f55636f3dcdd9beaccc1eebe9bd3":"certifikat","dd06a0593d1ffe3056348f2665076ef4":"co2","d49b6dd3b830979c6fd9881b9b629637":"d_co2fazy",
 "e7676daeadd3470170bd20a5a8f82bec":"d_mistnost","b26c5a611e75be020feaea5ce2d310b5":"d_obeh","8e2715ab50a8c3f44ed9675cdcf80f27":"d_vakuum",
 "7297a3594ed4e6bde5ddcdf7d7a4940f":"detektor","2c7a26b263b91211d5b582d81b8d78fe":"kalendar","4e7e36d2cda0e1054f34cf90280f1e20":"kapka",
 "304afc2607b5a954d8ad7549e13f021b":"kompresor","f6770a9ccceaeaa3048fae4fce3fc718":"lahev","165c2dcb12e619e09c2f67a8d1e6c52e":"lahev_dusik",
 "c4e38e5809bf920cadbf6f6b80beb85a":"lahev_propan","f6ac8052e18e300e174ee0b0448c20b2":"lahev_recyklace","0bdba362b8ac0f9f3b4fc561e1ec3fc9":"manometr_cerveny",
 "011b7d55966ee717f95e369fa1e41202":"manometr_modry","46bfc8365d240853be2a8b00686dd77f":"maska","91868dd6d452db8f9d0b09ef2f9a5994":"nh3",
 "f45d3c3d88fd5595a24a61d2c96b7965":"oopp","a06a744c23daac85281b597df610acec":"ozon","24d13700bec6244a20d48802fea62369":"plamen",
 "ae3ffc0801ea6076b214325fb0f9161e":"potrubi","42a55f9e7515f773bb5205f3f34765a6":"pozor","e6f1fa2ad1806adf0598381923b8e7bb":"predpis",
 "21679719c3f9d0188e9ff85f07dd854c":"vahy","0b9cef2ae2a4876f25933c38e768655d":"vazeni","4161491b0f9867300c6781ee5c921412":"venkovni",
 "2e26a20181223dc660a2f7e981518cfd":"vnitrni","40d742bcd1a25d2a7e15bc78d25a6c37":"vyveva","04c5381271866c74ecb9d488e1451d75":"zeme_teplo"}

deck = json.load(open(f"{ROOT}/deck.json", encoding="utf-8"))
only = sys.argv[1:]
order = [s for s in deck["order"] if os.path.exists(f"{ROOT}/slides/{s}.html") and (not only or s in only)]
css = open(f"{ROOT}/deck.css", encoding="utf-8").read()
fonts = "".join(f'<link rel="stylesheet" href="node_modules/@fontsource/{f}">' for f in
                ["montserrat/600.css","montserrat/800.css","montserrat/900.css","nunito-sans/400.css","nunito-sans/700.css","nunito-sans/800.css","nunito-sans/900.css"])
body = ""
for s in order:
    h = open(f"{ROOT}/slides/{s}.html", encoding="utf-8").read()
    h = re.sub(r'/_blob/([0-9a-f]{32})', lambda m: "file://" + SVG + "/" + BLOBS[m.group(1)] + ".svg", h)
    h = re.sub(r"<aside>.*?</aside>", "", h, flags=re.S)
    h = h.replace("<x-shape", '<div data-shape="1"').replace("</x-shape>", "</div>")
    body += h
html = f"""<!doctype html><html><head><meta charset="utf-8">{fonts}<style>
*{{margin:0;padding:0;box-sizing:content-box}} ul{{padding-left:36px}}
{css}
section{{width:1920px;height:1080px;position:relative;overflow:hidden;box-sizing:border-box;margin-bottom:20px}}
.rise{{animation:none!important}}
[data-shape]{{clip-path:polygon(0 30%,60% 30%,60% 0,100% 50%,60% 100%,60% 70%,0 70%)}}
table{{border-collapse:collapse;width:100%}} td,th{{padding:0.35em 0.6em;border:1px solid #CBD2D9;text-align:left}}
</style></head><body style="margin:0;background:#888">{body}</body></html>"""
open(f"{HERE}/preview.html", "w", encoding="utf-8").write(html)

CHECK = """() => {
 const out=[];
 for (const sec of document.querySelectorAll('section')) {
   const sr=sec.getBoundingClientRect(); const probs=[];
   for (const el of sec.querySelectorAll('*')) {
     if (el.classList.contains('hose')) continue;
     const r=el.getBoundingClientRect(); if(!r.width) continue;
     if (r.bottom - sr.top > 1080-96) probs.push('pod okrajem '+Math.round(r.bottom-sr.top)+' '+el.tagName+' '+(el.textContent||'').trim().slice(0,40));
     if (r.right - sr.left > 1920-100) probs.push('vpravo '+Math.round(r.right-sr.left)+' '+el.tagName+' '+(el.textContent||'').trim().slice(0,40));
     if ((el.tagName==='P'||el.tagName==='H3'||el.tagName==='TD') && el.scrollWidth>el.clientWidth+2) probs.push('slovo přetéká '+el.tagName+' '+el.textContent.trim().slice(0,40));
   }
   if (probs.length) out.push(sec.id+': '+[...new Set(probs)].slice(0,4).join(' || '));
 }
 return out;
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto("file://" + f"{HERE}/preview.html")
    pg.wait_for_timeout(800)
    pg.evaluate("document.fonts.ready")
    for line in pg.evaluate(CHECK): print("PROBLÉM", line)
    os.makedirs(f"{HERE}/shots", exist_ok=True)
    for s in order:
        pg.locator(f"section#{s}").screenshot(path=f"{HERE}/shots/{s}.png")
    b.close()
print("slajdů", len(order))
