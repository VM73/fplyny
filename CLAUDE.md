# F-plyny Přeškolení

Osobní PWA pro přípravu na přeškolení F-plynů: kat. I/II → A1/A2 a nově B (CO₂) a C (NH₃) podle nařízení (EU) 2024/573 a prov. nař. 2024/2215.

## Zadání
- Kdo: Vladan (iPhone, PC); případně kolegové – každý má vlastní pokrok.
- Kde běží: GitHub Pages (repo VM73/fplyny) + osobní Supabase projekt `klpcgnivfvczvvyoqzal` (mtb-servis), schéma `fplyny`.
- Hotovo když: ikona na ploše iPhonu otevře appku v prohlížeči (ne v aplikaci Claude) a pokrok je stejný na iPhonu i PC.

## Stack a nasazení
- `prez/` obrázky slajdů; `index.html` (vše v jednom; otázky, lekce, tahák, tabulky sytosti CoolProp vložené), `sw.js` (cache `fplyny-N`), `manifest.webmanifest`, ikony (varianta B – modrá rodina).
- Zdroj je ve složce `src/` (app.html, questions.js, content.js, prez.js, sat.json, build.py, build_pwa.py, make_prez.py, prezentace/). Kořen repa je nasazený výstup. Postup buildu v `src/README.md`.
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
- Verze 12: okruhy 1–14 přílohy I prov. nař. 2024/2215 (`src/okruhy.js`: `OKRUHY`, `OKR_CAT`, výchozí okruh podle modulu `OKR_DEF` + výjimky podle indexu otázky `OKR_OVR`; build vkládá přes `/*OKRUHY*/`). Každá otázka má `q.o`, okruh je vidět v hlavičce otázky. Skóre připravenosti pro A1/A2, B, C (průměr okruhů zkoušky; otázka box≥3 = 1, box 2 = ½), nejslabší okruh s tlačítkem procvičit – mini karta v Učení, detail navrch v Celkovém pokroku. Volba kategorie v localStorage `fplyny-rcat` (nesynchronizuje se). Nová otázka bez výjimky dostane výchozí okruh modulu – při přidávání doplnit `OKR_OVR`.
- Verze 13: +21 vlastních otázek (indexy 243–263): kondenzátory 6 (okruh 7), výparníky 6 (8), kompresory 5 (6) v modulu `kom`, prostředí 4 (2) v `env`. Inspirace témat zkouska-fplyny.cz, znění vlastní. Celkem 264 otázek. Počty po okruzích: 1:47, 2:12, 3:30, 4:17, 5:19, 6:13, 7:11, 8:8, 9:19, 10:22, 11:12, 12:33, 13:11, 14:10.
- Verze 14: Praxe – klikací schéma chladicího okruhu (vlastní SVG, `SCH` v app.html: 11 dílů + 4 úseky potrubí s funkcí, stavem chladiva a okruhem přílohy I). Režimy Prozkoumat (s popisky) a Najdi díl (kvíz bez popisků, skóre jen v paměti). 
- Verze 15: Praxe – simulátor poruch podle tlaků (`SIM` v app.html): 7 poruch + normální provoz (nedostatek, přeplnění, zanesený kondenzátor, ucpaný filtr, TEV nedodává/přeplavuje, nekondenzující plyny, namrzlý výparník). R32/R410A split, R134a vitrína; tlaky z `SAT` (sání = rosný bod, výtlak = bod varu), ukazuje přehřátí, podchlazení, teploty vzduchu a 1 indicii. Vysvětlení s naměřenými rozdíly, „jak by vypadala“ zvolená porucha, štítek okruhu 6–9 a tlačítko Procvičit okruh (`okrPractice`). Skóre jen v paměti, bez změny dat. Hodnoty modelové, tabulka příznaků ověřená proti lekci „Diagnostika podle tlaků“ na zkouska-fplyny.cz (nekondenzující plyny = podchlazení normální až nízké, ucpání = velké přehřátí + velké podchlazení); texty vlastní. Další nápady do Praxe: vakuum a nárůst tlaku, manometry + log p-h.
- Výukové prezentace jsou artefakty v Claude: hlavní (49 slajdů) a Hořlavá chladiva (31). Po změně prezentace: vyrenderovat slajdy (harness render.py) → `make_prez.py` (obrázky + prez.js) → build → push.
