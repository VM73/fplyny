# Zdroj appky F-plyny Přeškolení

Kořen repa = nasazený výstup (GitHub Pages). Tady je zdroj, ze kterého se výstup generuje.

## Build appky
```
cd src
python3 build.py        # app.html + questions.js + content.js + prez.js + sat.json -> fplyny.html
python3 build_pwa.py    # fplyny.html -> pwa/ (index.html, sw.js, manifest, ikony); VERZE nastav v build_pwa.py
```
Pak zkopíruj `pwa/index.html` a `pwa/sw.js` do kořene repa a pushni (prez/ jen při změně slajdů).

- `questions.js` – banka otázek (nové vždy na konec: id = modul + pořadí)
- `content.js` – lekce, tahák, slovníček
- `prez.js` – data sekce Prezentace (generuje `make_prez.py`)
- `sat.json` – tabulky sytosti (CoolProp)
- `ikona/` – zdroj ikon

## Prezentace
- `prezentace/hlavni/` a `prezentace/horlava/` – soubory artefaktů Slides v Claude (deck.json, deck.css, slides/*.html).
  Artefakty: hlavní https://claude.ai/artifact/J7tGqqDwT2cktV7f3nFuak, hořlavá https://claude.ai/artifact/SToCJFScPFqZ7XkBEheVUX
- `harness/render.py` – vykreslí slajdy do PNG (Playwright); `make_prez.py` z nich udělá `../prez/<id>/NN.webp` a `prez.js`.
  Cesty v obou skriptech jsou absolutní z původního prostředí – před použitím je uprav.
- Obrázky v hlavní prezentaci (`/_blob/...`) jsou nahrané assety artefaktu, lokálně je nemáme.
