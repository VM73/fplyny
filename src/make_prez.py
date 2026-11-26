import json, re, os, html
from PIL import Image
OUT_IMG="/home/claude/fplyny/pwa/prez"
DECKS=[("hlavni","/home/claude/deck1/project","/home/claude/work/shots1","https://claude.ai/artifact/J7tGqqDwT2cktV7f3nFuak","F-plyny Přeškolení – výuka","Celý rozsah přeškolení: pojmy, chladiva, 5 t CO₂e, předpisy a kategorie, oběh a diagnostika, těsnost a vakuum, bezpečnost, CO₂ a NH₃."),
       ("horlava","/home/claude/deck2/project","/home/claude/work/shots2","https://claude.ai/artifact/SToCJFScPFqZ7XkBEheVUX","Hořlavá chladiva – výuka","Navazující modul A2L / A3: LFL a praktický limit, náplň podle EN 378, detekce, úniky, pájení, zdroje zapálení, přeprava.")]
def txt(s): return html.unescape(re.sub(r"<[^>]+>"," ",s)).replace(" "," ").strip()
data=[]; total=0
for did,root,shots,url,title,desc in DECKS:
    d=json.load(open(root+"/deck.json",encoding="utf-8")); os.makedirs(f"{OUT_IMG}/{did}",exist_ok=True)
    slides=[]
    for i,sid in enumerate(d["order"]):
        h=open(f"{root}/slides/{sid}.html",encoding="utf-8").read()
        m=re.search(r"<h2>(.*?)</h2>",h,re.S) or re.search(r"<h1[^>]*>(.*?)</h1>",h,re.S)
        t=re.sub(r"\s+"," ",txt(m.group(1).replace("<br>"," "))) if m else sid
        a=re.search(r"<aside>(.*?)</aside>",h,re.S)
        fn=f"{i+1:02d}.webp"
        Image.open(f"{shots}/{sid}.png").convert("RGB").resize((1600,900),Image.LANCZOS).save(f"{OUT_IMG}/{did}/{fn}","WEBP",quality=70,method=6)
        total+=os.path.getsize(f"{OUT_IMG}/{did}/{fn}")
        slides.append({"id":sid,"t":t,"n":txt(a.group(1)) if a else ""})
    idx={s["id"]:i for i,s in enumerate(slides)}
    secs=[{"t":re.sub(r"^Kapitola (\d+): ",r"\1 · ",v["description"]).split(" – ")[0],"i":idx[v["start"]]} for v in d["sections"].values() if v["start"] in idx]
    secs.sort(key=lambda x:x["i"])
    data.append({"id":did,"title":title,"desc":desc,"url":url,"sec":secs,"s":slides})
js="// Prezentace – generováno skriptem make_prez.py (obrázky v prez/<id>/NN.webp)\nconst PREZ = "+json.dumps(data,ensure_ascii=False)+";\n"
open("/home/claude/fplyny/prez.js","w",encoding="utf-8").write(js)
print("obrázky MB", round(total/1e6,2), "js KB", len(js.encode())//1024)
for x in data: print(x["id"],len(x["s"]),[(s["t"],s["i"]) for s in x["sec"]])
