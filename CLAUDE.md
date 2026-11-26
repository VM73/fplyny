# F-plyny Přeškolení

Osobní PWA pro přípravu na přeškolení F-plynů: kat. I/II → A1/A2 a nově B (CO₂) a C (NH₃) podle nařízení (EU) 2024/573 a prov. nař. 2024/2215.

## Zadání
- Kdo: Vladan (iPhone, PC); případně kolegové – každý má vlastní pokrok.
- Kde běží: GitHub Pages (repo VM73/fplyny) + osobní Supabase projekt `klpcgnivfvczvvyoqzal` (mtb-servis), schéma `fplyny`.
- Hotovo když: ikona na ploše iPhonu otevře appku v prohlížeči (ne v aplikaci Claude) a pokrok je stejný na iPhonu i PC.

## Stack a nasazení
- `prez/` obrázky slajdů; `index.html` (vše v jednom; otázky, lekce, tahák, tabulky sytosti CoolProp vložené), `sw.js` (cache `fplyny-N`), `manifest.webmanifest`, ikony (varianta B – modrá rodina).
- Zdroj se generuje mimo repo (`build.py` + `build_pwa.py`); v repu jen výstup.
- Supabase JS 2.45.4 z cdn.jsdelivr.net, Publishable key v `index.html`. Nikdy secret / service_role.
- Nasazení: soubory do kořene repa; zvýšit `VERZE` (viditelné dole v appce) i `CACHE` v `sw.js`.

## Data
- `fplyny.pokrok`: jeden řádek na uživatele (`user_id` = auth.uid()), `data` jsonb = box, seen, tm (časy odpovědí), tests, prax, mods, upd.
- RLS: každý čte a mění jen svůj řádek. SQL v `supabase/schema.sql` (lze spustit opakovaně).
- Schéma `fplyny` musí být v Supabase přidané mezi Exposed schemas (Data API).
- Přihlášení: e-mail + heslo, stejné účty jako MTB servis. Bez přihlášení appka funguje, pokrok jen v localStorage.

## Pravidla
- Dopad na náklady a limity u každé úpravy (Claude tokeny, GitHub Pages, Supabase free tier). Tato appka: 1 malý řádek na uživatele, bez Edge Functions a Storage.
- Diagnostika: `?debug=1` nebo při chybě JS se ukáže panel s logem.
- UI česky, iOS vzhled, od 320 px. Nejde o oficiální zkušební otázky.

## Stav
- Verze 7: přesun z artefaktu claude.ai na GitHub Pages + Supabase sync.
- Verze 8: modul Hořlavá chladiva +30 otázek (podklad SCHKT, EN 378), lekce, tahák „Hořlavá chladiva (EN 378)“, slovníček. Nové otázky jsou na konci banky – id stávajících se nemění (id = modul + pořadí).
- Verze 9: sekce Prezentace – prohlížeč slajdů (WebP 1600×900 v `prez/<id>/NN.webp` + poznámky v `PREZ`), celá obrazovka s otočením na telefonu, „Stáhnout offline“, z lekce okruhu tlačítko „Slajdy k okruhu“ (`PREZ_MAP`). Pozice čtení v localStorage `fplyny-prez` (nesynchronizuje se).
- Verze 10: SW ověřuje stránku na serveru (cache: no-cache) – aktualizace na iPhonu hned po zavření a otevření.
- Verze 11 (inspirace zkouska-fplyny.cz, vlastní obsah): Výpočty – generovaná cvičení s postupem (`EXG`: CO₂e, interval, přehřátí, podchlazení, EER/COP, tlaková zkouška, recyklační láhev, doplnění náplně, převody tlaku); Praxe – seřazování kroků (`ORD`, 7 postupů); nový okruh `sit` Situace z praxe (30 otázek, přidán do A_MODS a jednorázově do S.mods přes `S.modNew`); +50 otázek (bez, ene, pot, kom A1, tes). Celkem 243 otázek. Zkoušky nanečisto beze změny složení.
- Výukové prezentace jsou artefakty v Claude: hlavní (49 slajdů) a Hořlavá chladiva (31). Po změně prezentace: vyrenderovat slajdy (harness render.py) → `make_prez.py` (obrázky + prez.js) → build → push.
