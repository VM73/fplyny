# F-plyny Přeškolení

Osobní PWA pro přípravu na přeškolení F-plynů: kat. I/II → A1/A2 a nově B (CO₂) a C (NH₃) podle nařízení (EU) 2024/573 a prov. nař. 2024/2215.

## Zadání
- Kdo: Vladan (iPhone, PC); případně kolegové – každý má vlastní pokrok.
- Kde běží: GitHub Pages (repo VM73/fplyny) + osobní Supabase projekt `klpcgnivfvczvvyoqzal` (mtb-servis), schéma `fplyny`.
- Hotovo když: ikona na ploše iPhonu otevře appku v prohlížeči (ne v aplikaci Claude) a pokrok je stejný na iPhonu i PC.

## Stack a nasazení
- `index.html` (vše v jednom; otázky, lekce, tahák, tabulky sytosti CoolProp vložené), `sw.js` (cache `fplyny-N`), `manifest.webmanifest`, ikony (varianta B – modrá rodina).
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
- Výukové prezentace jsou samostatné artefakty v Claude: hlavní (48 slajdů) a navazující Hořlavá chladiva.
