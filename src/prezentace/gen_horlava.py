import json, os
OUT="/home/claude/deck2/project"
S={}; ORDER=[]
def sec(id, kicker, title, body, tag, aside, cls=""):
    ORDER.append(id)
    S[id]=f'''<section id="{id}"{(' class="'+cls+'"') if cls else ''}>
<div class="hose"></div>
<div class="head"><p class="kicker">{kicker}</p><h2>{title}</h2></div>
{body}
<p class="tag">{tag}</p>
<aside>{aside}</aside>
</section>
'''
def tile(c,i,h,t,st=""): return f'<div class="tile {c} rise" style="--i:{i};{st}"><h3>{h}</h3><p class="txt">{t}</p></div>'
def rem(t): return f'<div class="remember"><p class="rlab">ZAPAMATUJ SI</p><p class="rtxt">{t}</p></div>'
def table(head, rows, fs=27, widths=None):
    w=widths or [None]*len(head)
    h="".join(f'<th{(" style=%swidth:%s%s"%(chr(34),x,chr(34))) if x else ""}>{c}</th>' for c,x in zip(head,w))
    r="".join(f'<tr class="r{1+i%2}">'+"".join(f"<td>{c}</td>" for c in row)+"</tr>" for i,row in enumerate(rows))
    return f'<table class="tab" style="font-size:{fs}px">\n<tr class="thead">{h}</tr>\n{r}\n</table>'
def quiz(id, k, title, qs, ans, aside_q, aside_a):
    cards="".join(f'<div class="qcard rise" style="--i:{i+1}"><p class="num">{i+1}</p><p class="qtext">{q}</p>'+"".join(f'<p class="opt"><b>{"ABCD"[j]}</b> {o}</p>' for j,o in enumerate(opts))+'</div>' for i,(q,opts) in enumerate(qs))
    sec("q"+id, f"Kapitola {k} · kontrolní otázky", f'Otestuj se: <span class="hl">{title}</span>', f'<div class="grid c3">{cards}</div>\n<p class="sub">Odpovědi s vysvětlením jsou na dalším slajdu.</p>', "Otázky", aside_q)
    cards="".join(f'<div class="qcard rise" style="--i:{i+1}"><p class="qsmall">{i+1} · {a[0]}</p><p class="ans">{a[1]}</p><p class="why">{a[2]}</p></div>' for i,a in enumerate(ans))
    sec("a"+id, f"Kapitola {k} · odpovědi", f'Odpovědi: <span class="hl">{title}</span>', f'<div class="grid c3">{cards}</div>', "Odpovědi", aside_a)

# ── titul
ORDER.append("cover")
S["cover"]='''<section id="cover" class="cover" data-transition="fade" style="justify-content:center">
<div class="hose"></div>
<div class="row" style="align-items:center; gap:64px">
<div class="col" style="width:930px; gap:28px">
<p class="kicker">Navazující modul · přeškolení A1 / A2</p>
<h1 style="font-size:118px">Hořlavá<br><span class="hl">chladiva</span></h1>
<p class="sub" style="font-size:40px; color:#1E2A3A"><b>A2L</b> (R32, HFO) a <b>A3</b> (R290, R600a, R1270)<br>náplň, detekce, těsnost, servis</p>
<p class="sub">4 kapitoly · u každé 3 kontrolní otázky s odpověďmi</p>
</div>
<div class="col fill" style="gap:16px">
<div class="tile rose rise" style="--i:1; padding:16px 28px"><div class="row" style="align-items:center; gap:24px"><p class="big" style="font-size:54px; width:270px">0,038</p><p class="txt fill" style="font-size:30px">kg/m³ – LFL propanu R290</p></div></div>
<div class="tile sand rise" style="--i:2; padding:16px 28px"><div class="row" style="align-items:center; gap:24px"><p class="big" style="font-size:54px; width:270px">20 %</p><p class="txt fill" style="font-size:30px">LFL – praktický limit</p></div></div>
<div class="tile sky rise" style="--i:3; padding:16px 28px"><div class="row" style="align-items:center; gap:24px"><p class="big" style="font-size:54px; width:270px">25 %</p><p class="txt fill" style="font-size:30px">LFL – alarm pevné detekce</p></div></div>
<div class="tile peach rise" style="--i:4; padding:16px 28px"><div class="row" style="align-items:center; gap:24px"><p class="big" style="font-size:54px; width:270px">3 m</p><p class="txt fill" style="font-size:30px">bez zdrojů zapálení kolem zařízení</p></div></div>
</div>
</div>
<p class="tag">Studium</p>
<aside>Navazuje na hlavní prezentaci F-plyny Přeškolení (kapitola 7). Zdroj: školicí podklad SCHKT „Hořlavá chladiva – teorie“ pro doškolení na certifikát A1/A2 (vychází z programu REAL Alternatives 4 LIFE) a ČSN EN 378. Hodnoty LFL, PL a ATEL/ODL jsou podle EN 378-1. Výpočty náplně jsou ukázkové – v praxi je dělá projektant podle úplného znění normy.</aside>
</section>
'''
sec("obsah","Obsah",'Čtyři kapitoly <span class="hl">+ shrnutí</span>','''<div class="grid c4">
<div class="tile sky rise" style="--i:1"><p class="num">1</p><h3>Chladiva a pojmy</h3><p class="txt" style="font-size:31px">LFL, PL, ATEL/ODL, přehled A2L a A3, vlastnosti</p></div>
<div class="tile mint rise" style="--i:2"><p class="num">2</p><h3>Náplň a umístění</h3><p class="txt" style="font-size:31px">odpovědnost, kategorie A/B/C, třídy I–IV, výpočty, detekce</p></div>
<div class="tile sand rise" style="--i:3"><p class="num">3</p><h3>Těsnost a úniky</h3><p class="txt" style="font-size:31px">kdy a jak hledat, metody, tlaková zkouška</p></div>
<div class="tile peach rise" style="--i:4"><p class="num">4</p><h3>Práce na okruhu</h3><p class="txt" style="font-size:31px">pracoviště, nářadí, pájení, zdroje zapálení, rizika, přeprava, normy</p></div>
</div>''',"Obsah","Kapitoly odpovídají modulu Hořlavá chladiva v appce F-plyny Přeškolení – od verze 8 v něm je 43 otázek, rozšířená lekce a tabulka v Taháku.")

K="Kapitola 1 · Chladiva a pojmy"
sec("proc",K,'Proč <span class="hl">hořlavá chladiva</span>',f'''<div class="row">
<div class="col" style="width:820px">
{tile("sky",1,"Nízké GWP","Nařízení 2024/573 tlačí na chladiva s co nejnižším GWP.")}
{tile("rose",2,"Pod GWP ≈ 650 většinou hořlavá","Nehořlavé náhrady s nízkým GWP skoro nejsou – zbývají A2L a A3.")}
{tile("sand",3,"Riziko se řídí postupy","Konstrukce, umístění, náplň a servis musí počítat s hořlavostí.")}
</div>
<div class="tile paper fill rise" style="--i:4">
<h3>Bezpečnostní značení (EN 378)</h3>
<p class="txt"><b>A</b> = netoxické · <b>B</b> = toxické</p>
<p class="txt"><b>1</b> nehořlavé</p>
<p class="txt"><b>2L</b> mírně hořlavé – R32, R1234yf, R1234ze</p>
<p class="txt"><b>2</b> hořlavé – běžně se nepoužívají</p>
<p class="txt"><b>3</b> vysoce hořlavé až výbušné – R290, R600a, R1270</p>
<p class="txt" style="margin-top:8px; font-weight:800">A2L = syntetická (HFC, HFO), A3 = uhlovodíky – obě netoxické.</p>
</div>
</div>''',"Pojmy","GWP vztažený k CO₂ (100 let). R32 má podle nařízení 2024/573 GWP 675, HFO a uhlovodíky jen jednotky. Třída 2L je podskupina třídy 2 s rychlostí hoření nejvýše 10 cm/s.")

sec("pojmy",K,'Mezní <span class="hl">koncentrace</span>','''<div class="grid c3">
<div class="tile rose rise" style="--i:1"><h3>LFL</h3><p class="txt">dolní mez hořlavosti – od této koncentrace se směs se vzduchem zapálí. % obj. nebo kg/m³.</p></div>
<div class="tile peach rise" style="--i:2"><h3>UFL</h3><p class="txt">horní mez hořlavosti – nad ní je směs příliš bohatá a nehoří.</p></div>
<div class="tile sand rise" style="--i:3"><h3>PL – praktický limit</h3><p class="txt">nejvyšší koncentrace, která se smí krátkodobě objevit. U hořlavých ≈ 20 % LFL.</p></div>
<div class="tile lilac rise" style="--i:4"><h3>RCL</h3><p class="txt">limitní koncentrace chladiva – zohledňuje toxicitu i hořlavost.</p></div>
<div class="tile sky rise" style="--i:5"><h3>ATEL / ODL</h3><p class="txt">limit akutní toxicity / nedostatku kyslíku pro dýchání.</p></div>
<div class="tile mint rise" style="--i:6"><h3>Rychlost hoření, spalné teplo</h3><p class="txt">cm/s a MJ/kg. A2L hoří pomalu (do 10 cm/s), HC kolem 45 cm/s.</p></div>
</div>''',"Pojmy","Z LFL se počítá dovolená náplň pro místnost, z PL praktický limit, z LFL a ATEL/ODL úroveň alarmu detektoru. Hodnoty v kg/m³ jsou podle EN 378-1.")

sec("prehled",K,'Přehled <span class="hl">A2L a A3</span>',table(["Chladivo","Druh","Třída","GWP","Bod varu","LFL kg/m³","PL kg/m³","ATEL/ODL","Zápalná t."],[
["R32","HFC","A2L","675","−52 °C","0,307","0,061","0,30","648 °C"],
["R1234yf","HFO","A2L","&lt; 1","−29,5 °C","0,289","0,058","0,47","405 °C"],
["R1234ze(E)","HFO","A2L","≈ 1","−19 °C","0,303","0,061","0,28","368 °C"],
["R600a","HC isobutan","A3","3","−12 °C","0,043","0,011","0,059","460 °C"],
["R290","HC propan","A3","3","−42 °C","0,038","0,008","0,09","470 °C"],
["R1270","HC propen","A3","3","−48 °C","0,046","0,008","0,0017","455 °C"]],27,["13%","13%","8%","8%","11%","12%","11%","12%","12%"])+"\n"+rem("Propan se zapálí při zhruba 8× menším množství chladiva v m³ než R32."),"Přehled","Hodnoty z podkladu SCHKT a EN 378-1. GWP: R32 podle nařízení 2024/573; pro HFO a uhlovodíky uvádí 2024/573 hodnoty v jednotkách až setinách (např. R1234ze 1,37, R290 0,02), starší podklady 3–7. Rychlost hoření: R32 6,7 cm/s, HFO 1,2–1,5 cm/s, HC 41–46 cm/s. Pozor u R1270: velmi nízké ATEL/ODL – rozhoduje o úrovni alarmu.")

sec("vlastnosti",K,'A2L vs. <span class="hl">A3</span>','''<div class="grid c2">
<div class="tile sand rise" style="--i:1"><h3>A2L – R32, R1234yf, R1234ze</h3>
<ul class="txt"><li>syntetická, F-plyny → platí nařízení 2024/573</li><li>zatím dražší, možná budoucí omezení</li><li><b>zplodiny hoření velmi toxické</b> (fluorovodík)</li><li>R32 a R1234yf v klimatizacích, R1234ze v chillerech</li></ul></div>
<div class="tile rose rise" style="--i:2"><h3>A3 – R290, R600a, R1270</h3>
<ul class="txt"><li>uhlovodíky, levné, nejsou F-plyny</li><li>netoxické i zplodiny hoření</li><li>ve směsi se vzduchem až výbušné</li><li>bílá technika, plug-in chlazení, venkovní chillery, monobloky</li></ul></div>
</div>
''' + rem("Všechna alternativní chladiva kromě R717 jsou těžší než vzduch – hromadí se u podlahy."),"A2L / A3","R717 (čpavek, B2L) je lehčí než vzduch – podklad ho uvádí jen pro srovnání. HFO jsou často součástí směsí HFC/HFO (R448A, R454B, R454C).")

sec("chladiva",K,'Co vědět <span class="hl">o jednotlivých</span>',f'''<div class="grid c3">
{tile("sand",1,"R32 · GWP 675","Tlaky a výkon jako R410A (max. typicky ~35 bar), ale <b>není drop-in</b> za R410A. Elektrika v jednotce nejiskřící.")}
{tile("mint",2,"R1234yf / ze · HFO","Jednosložková, A2L, GWP v jednotkách. yf hlavně auta a klima, ze chillery. Elektrika nejiskřící.")}
{tile("rose",3,"R600a · isobutan","Bod varu −12 °C → <b>ne pro nízké teploty</b> (vypařoval by se v podtlaku). Domácí a malé komerční chlazení.")}
{tile("rose",4,"R290 · propan","−42 °C, charakteristika podobná R22, tlaky jako R404A. Chillery, komerční chlazení, TČ.")}
{tile("rose",5,"R1270 · propen","−48 °C, nejvhodnější HC pro nízké teploty. Velmi nízké ATEL/ODL.")}
{tile("paper",6,"Velikost náplně","U HC omezuje použití hlavně na integrovaná zařízení a venkovní chillery.")}
</div>''',"Chladiva","Do zařízení navrženého pro nehořlavé chladivo se hořlavé chladivo nesmí plnit. U R32 podklad uvádí, že hořlavost omezuje náplň komfortních klimatizací bez dalších opatření zpravidla na nízké jednotky kg – konkrétní limit plyne z výpočtu podle EN 378 (kapitola 2).")

quiz("1",1,"chladiva",[("Jaká je LFL propanu R290?",["0,307 kg/m³","0,038 kg/m³","0,38 kg/m³","3,8 kg/m³"]),("Praktický limit hořlavého chladiva je přibližně…",["5 % LFL","50 % LFL","20 % LFL","100 % LFL"]),("Proč R600a nepoužít pro mrazicí aplikace?",["je toxický","bod varu −12 °C – vypařoval by se v podtlaku","má vysoké GWP","je A2L"])],
[("LFL R290","B · 0,038 kg/m³","0,307 kg/m³ je R32 – propan se zapálí při zhruba 8× menší koncentraci."),("Praktický limit","C · 20 % LFL","Pro R290: 0,2 × 0,038 ≈ 0,008 kg/m³."),("R600a","B · bod varu −12 °C","Pro nízké teploty R290 (−42 °C) nebo R1270 (−48 °C).")],
"Podobné otázky najdeš v appce v okruhu Hořlavá chladiva A2L / A3.","Rozdíl mezi A2L a A3 je hlavně v LFL a rychlosti hoření: R32 hoří rychlostí 6,7 cm/s, propan kolem 46 cm/s.")

K="Kapitola 2 · Náplň a umístění"
sec("odpovednost",K,'Kdo za co <span class="hl">odpovídá</span>',f'''<div class="grid c2">
{tile("sky",1,"Výrobce","Bezpečná konstrukce a provoz – shoda s normami, značka CE nebo prohlášení o shodě.")}
{tile("mint",2,"Provozovatel","Bezpečné a správné umístění. Často je nutné požárně bezpečnostní řešení.")}
{tile("sand",3,"Firma stavějící zařízení na míru","Zařízení z jednotlivých dílů musí splnit normy a mít prohlášení o shodě – odpovídá ten, kdo staví a uvádí do provozu.")}
{tile("peach",4,"Servis","Jen proškolená osoba, díly určené pro hořlavé chladivo, větrání, nejiskřící odsávačky a vývěvy.")}
</div>
{rem("Konstrukce, umístění i množství chladiva musí odpovídat normám (ČSN EN 378). Prostory určuje projektant s provozovatelem a požárními techniky.")}''',"Odpovědnost","Zařízení pro obsazené prostory bývají kompletně hotová a naplněná ve výrobě – výrobci se snaží náplň co nejvíc omezit. Pro A2L F-plyny (R32, HFO a jejich směsi) navíc platí povinnosti nařízení 2024/573.")

sec("pristupnost",K,'Přístupnost a <span class="hl">umístění</span>','''<div class="row">
<div class="col" style="width:880px; gap:18px">
<div class="tile rose rise" style="--i:1; padding:20px 28px"><h3>A – veřejnost</h3><p class="txt" style="font-size:31px">lidé mohou spát, počet osob se nekontroluje: nemocnice, hotely, divadla, supermarkety, restaurace</p></div>
<div class="tile sand rise" style="--i:2; padding:20px 28px"><h3>B – omezený počet osob</h3><p class="txt" style="font-size:31px">část seznámena s bezpečností: kanceláře, laboratoře, výrobní prostory</p></div>
<div class="tile mint rise" style="--i:3; padding:20px 28px"><h3>C – jen oprávněné osoby</h3><p class="txt" style="font-size:31px">chladírny, jatka, rafinerie, neveřejné části supermarketů</p></div>
</div>
<div class="col fill" style="gap:18px">
<div class="tile paper rise" style="--i:4; padding:20px 28px"><h3>I</h3><p class="txt" style="font-size:31px">vše v prostoru s osobami</p></div>
<div class="tile paper rise" style="--i:5; padding:20px 28px"><h3>II</h3><p class="txt" style="font-size:31px">kompresory ve strojovně nebo venku</p></div>
<div class="tile paper rise" style="--i:6; padding:20px 28px"><h3>III</h3><p class="txt" style="font-size:31px">celé zařízení ve strojovně nebo venku</p></div>
<div class="tile paper rise" style="--i:7; padding:20px 28px"><h3>IV</h3><p class="txt" style="font-size:31px">ve větraném krytu</p></div>
</div>
</div>''',"EN 378","Maximální náplň závisí na kombinaci kategorie přístupnosti a třídy umístění (AI, AII … CIV) a na tom, zda dominuje toxicita (NH₃, dušení CO₂) nebo hořlavost. Úplné tabulky jsou v ČSN EN 378-1.")

sec("vypocet",K,'Jak se počítá <span class="hl">náplň</span>','''<div class="grid c3">
<div class="tile sky rise" style="--i:1"><p class="lbl">Bez výpočtu do</p><p class="big" style="font-size:44px">m₁ = 4 m³ × LFL</p><p class="txt">× 1,5 u třídy 2L. R290: 0,15 kg · R32: 1,84 kg</p></div>
<div class="tile rose rise" style="--i:2"><p class="lbl">Objem místnosti</p><p class="big" style="font-size:44px">m = 0,2 × LFL × V</p><p class="txt">tj. praktický limit × objem (např. HC, jiná použití)</p></div>
<div class="tile sand rise" style="--i:3"><p class="lbl">Klimatizace, komfort</p><p class="big" style="font-size:40px">2,5 × LFL<sup>1,25</sup> × h × √A</p><p class="txt">h = výška jednotky, A = plocha podlahy</p></div>
</div>
<div class="tile paper rise" style="--i:4; padding:20px 32px"><p class="txt"><b>Výška h:</b> 0,6 m parapetní · 1,0 m okenní · 1,8 m nástěnná · 2,2 m podstropní. Čím výš, tím víc se únik zředí, než dosáhne podlahy.</p></div>
''' + rem("Výpočty náplně dělá projektant podle ČSN EN 378. Vyšší náplň jen s doplňkovými opatřeními."),"Výpočet","Vyšší náplně norma dovoluje s doplňkovými opatřeními: trvalé nebo detektorem spouštěné větrání, výstroj v nevýbušném provedení, automatické uzavírací ventily. Trvale instalovaný a přezkušovaný detektor by měl být samozřejmostí. U uhlovodíků platí v EN 378 pro kategorii A limit 150 g na okruh; EN 60335-2-89 (2019) u samostatných komerčních spotřebičů dovoluje 494 g (13 × LFL) – podle podkladu to EN 378 zatím nepřevzala.")

sec("priklady",K,'Tři <span class="hl">příklady</span>','''<div class="grid c3">
<div class="tile rose rise" style="--i:1"><h3>Chladírna, R290</h3><p class="txt" style="font-size:30px">kat. B, umístění II, kondenzační jednotka venku<br>3,5 × 3 × 2,5 m = 26,25 m³</p><p class="txt" style="font-size:30px">0,2 × 0,038 × 26,25</p><p class="big" style="font-size:60px">0,20 <span class="unit">kg</span></p><p class="txt" style="font-size:28px">a zároveň max. 2,5 kg</p></div>
<div class="tile sand rise" style="--i:2"><h3>Split, R32</h3><p class="txt" style="font-size:30px">kat. A, podstropní jednotka h = 2,2 m<br>místnost 9 × 5,5 m = 49,5 m²</p><p class="txt" style="font-size:30px">2,5 × 0,307<sup>1,25</sup> × 2,2 × √49,5</p><p class="big" style="font-size:60px">8,84 <span class="unit">kg</span></p><p class="txt" style="font-size:28px">limit 26 m³ × LFL × 1,5 = 12 kg</p></div>
<div class="tile mint rise" style="--i:3"><h3>Pult, 350 g R1270</h3><p class="txt" style="font-size:30px">kat. A, umístění I, integrovaná skříň<br>hledáme nejmenší objem</p><p class="txt" style="font-size:30px">0,35 / (0,2 × 0,046)</p><p class="big" style="font-size:60px">38 <span class="unit">m³</span></p><p class="txt" style="font-size:28px">menší místnost nevyhoví</p></div>
</div>''',"Příklady","Příklad 1 v podkladu počítá s objemem 25,2 m³ (0,192 kg); 3,5 × 3 × 2,5 m je ale 26,25 m³, tedy 0,20 kg – výsledek se prakticky nemění. Příklady jsou ukázkové; úplné podmínky viz ČSN EN 378.")

sec("detekce",K,'Pevná <span class="hl">detekce úniku</span>',f'''<div class="row">
<div class="col" style="width:820px">
{tile("sky",1,"Kam","Senzory nízko nad podlahou, dostatečný počet – i v místnostech, kudy vede potrubí chladiva.")}
{tile("mint",2,"Test","Nejméně 1× ročně. Na alarm reagovat okamžitě.")}
</div>
<div class="tile sand fill rise" style="--i:3"><h3>Úroveň alarmu</h3>
<p class="big" style="font-size:62px">25 % LFL</p><p class="txt">nebo</p><p class="big" style="font-size:62px">50 % ATEL/ODL</p><p class="txt">platí <b>nižší</b> z obou hodnot</p>
<p class="txt" style="font-size:30px">R290: 25 % × 0,038 = 0,0095 kg/m³ (rozhoduje LFL)<br>R1270: 50 % × 0,0017 = 0,00085 kg/m³ (rozhoduje ATEL/ODL)</p></div>
</div>''',"Detekce","Přenosný detektor technika má hlásit při 20 % LFL a nesmí se nulovat v prostoru, kde už může být uniklé chladivo.")

quiz("2",2,"náplň",[("Hotel, nemocnice nebo supermarket patří do kategorie přístupnosti…",["kategorie A","kategorie B","kategorie C","třída IV"]),("Chladírna 26 m³, R290 (LFL 0,038), limit 0,2 × LFL × V. Max. náplň?",["asi 2 kg","asi 0,2 kg","asi 1 kg","asi 0,04 kg"]),("Alarm pevné detekce se nastaví na…",["100 % LFL","50 % LFL","25 % LFL nebo 50 % ATEL/ODL, nižší z nich","10 % PL"])],
[("Přístupnost","A · kategorie A","Kdokoli, bez seznámení s bezpečností, lidé mohou spát. B = kanceláře, C = jen oprávnění."),("Chladírna","B · asi 0,2 kg","0,2 × 0,038 × 26 ≈ 0,20 kg. Proto se HC chladírny dělají jako monobloky s malou náplní."),("Alarm","C · nižší z 25 % LFL a 50 % ATEL/ODL","Senzory nízko, test 1× ročně.")],
"V appce najdeš i příklady s minimálním objemem místnosti a vzorcem pro split.","Pozor na zaokrouhlení: zkouškové příklady počítají s LFL v kg/m³, ne v % obj.")

K="Kapitola 3 · Těsnost a úniky"
sec("tesnost",K,'Kdy a kde <span class="hl">hledat úniky</span>',f'''<div class="row">
<div class="col" style="width:860px">
{tile("sky",1,"Uhlovodíky (HC)","Kontrola při uvedení do provozu a po zásahu do okruhu. Pravidelné intervaly zákon nestanoví – může je určit výrobce.")}
{tile("sand",2,"A2L F-plyny (R32, HFO)","Kontroly a opravy podle nařízení 2024/573 – opravu ověřit do 1 měsíce.")}
{tile("paper",3,"Kdo","Kontroly i opravy jen proškolená osoba.")}
</div>
<div class="tile rose fill rise" style="--i:4"><h3>Kde uniká nejčastěji</h3>
<ul class="txt"><li>spoje a ohyby potrubí přes 90°</li><li>trubky a díly s rizikem poškození</li><li>připojení presostatů a pojistných ventilů</li><li>chvějící se a dotýkající se díly</li></ul>
<h3 style="margin-top:12px">Prevence</h3><ul class="txt"><li>nepřidávat spoje ani díly</li><li>před Schrader ventilek kulový ventil</li></ul></div>
</div>''',"Těsnost","Únik u hořlavého chladiva je hlavně otázka bezpečnosti; jinak jsou důsledky stejné jako u nehořlavých: menší výkon, vyšší spotřeba energie, náklady na doplňování a ztráta renomé servisní firmy.")

sec("metody",K,'Metody <span class="hl">detekce</span>',table(["Metoda","Vhodnost","Pozor na"],[
["Detekční sprej","A2L i HC","jen tam, kde je <b>přetlak</b> proti atmosféře"],
["Elektronický detektor","A2L i HC","citlivý na daný typ chladiva; u HC v provedení bezpečném pro hořlavé plyny; kontrola před použitím, min. 1× ročně"],
["UV aditivum","dobrá","kompatibilita s olejem; někteří výrobci neuznají záruku; olejový odlučovač ho zachytí; oddělené hadice"],
["Ultrazvuk","dobrá","jakékoli chladivo i dusík, funguje i v <b>podtlaku</b>; nejlépe při vysokém tlaku"],
["Vizuální kontrola","doplněk","olejové skvrny, nasáklá izolace, koroze, indikátor otevření pojistného ventilu"]],29,["24%","16%","60%"])+"\n"+rem("Nepřímé znaky úniku: nižší sací a výtlačný tlak, větší přehřátí, menší podchlazení."),"Metody","Pro elektronický detektor si pořiď lahvičku „referenční únik“ – nenahrazuje roční kontrolu. Pojistný ventil, který už jednou odpustil, nemusí znovu správně těsnit. Olejové skvrny po opravě očistit, jinak dávají falešnou indikaci.")

sec("jak-hledat",K,'Jak hledat <span class="hl">správně</span>',f'''<div class="grid c2">
{tile("rose",1,"VT strana","Systém v provozu, kondenzační tlak co nejvyšší. U reverzibilních TČ testovat obě strany.")}
{tile("sky",2,"NT strana","Systém vypnutý – tlak se vyrovná. R290: výparník −30 °C = 0,6 bar g, po odstavení při 20 °C = 7,4 bar g.")}
{tile("sand",3,"Proudění vzduchu","Ventilátory na nezbytnou dobu vypnout – ale nesmí vypnout VT presostat ani otevřít pojistný ventil.")}
{tile("mint",4,"Těžší než vzduch","Kontrolovat spodní stranu spojů, dno skříní se stoupačkami, vzduch nad podlahou za dveřmi.")}
</div>
{rem("Hlásí-li detektor únik hořlavého chladiva: nejdřív důkladně vyvětrat. První nalezený únik nemusí být jediný.")}''',"Postup","Systém s odmrazováním horkými parami kontroluj na NT straně v režimu odmrazování. Při vypnutém větrání strojovny hlídej, aby se v prostoru nevytvořila hořlavá atmosféra.")

sec("tlakova",K,'Tlaková <span class="hl">zkouška</span>',f'''<div class="row">
<div class="col" style="width:860px">
{tile("sky",1,"Dusík do PS","Pomalu napouštět až po maximální dovolený tlak. Pak každý spoj sprejem, <b>nebo</b> nejméně 12 h bez poklesu tlaku.")}
{tile("mint",2,"Formovací plyn","Dusík s do 5 % vodíku (nebo helia) + speciální elektronický detektor – velmi citlivá metoda.")}
</div>
<div class="tile sand fill rise" style="--i:3"><h3>Vliv teploty okolí</h3>
<p class="big" style="font-size:66px">p₂ = p₁ × T₂ / T₁</p>
<p class="txt">absolutní tlaky v bar, teploty v K</p>
<p class="big" style="font-size:60px; margin-top:16px">10 K ≈ 3,5 %</p>
<p class="txt">Příklad: 30 bar g (31 bar abs) při 25 °C → při 15 °C asi 29,96 bar abs, tedy pokles o 1 bar bez úniku.</p></div>
</div>''',"Zkouška","Gay-Lussacův zákon: tlak plynu v uzavřeném objemu je úměrný absolutní teplotě. Při dvanáctihodinové zkoušce přes noc musíš pokles tlaku přepočítat na stejnou teplotu.")

quiz("3",3,"úniky",[("Jak kontrolovat těsnost NT strany?",["v provozu při nejnižším tlaku","při vypnutém systému","ve vakuu","nezáleží"]),("Kde nelze použít detekční sprej?",["na VT straně","na spojích","v podtlaku","na ventilech"]),("Teplota okolí klesne o 10 K. Tlak dusíku…",["klesne asi o 3,5 %","klesne asi o 10 %","nezmění se","stoupne"])],
[("NT strana","B · systém vypnutý","Tlak se vyrovná a stoupne – R290 z 0,6 na 7,4 bar g."),("Sprej","C · v podtlaku","Tam pomůže ultrazvuk, který funguje i pod atmosférickým tlakem."),("Teplota","A · asi o 3,5 %","p₂ = p₁ × T₂ / T₁ v absolutních hodnotách.")],
"Podobné otázky jsou v appce v okruzích Hořlavá chladiva a Těsnost, vakuum, plnění.","Při hledání úniku hořlavého chladiva vždy začni detektorem nad podlahou – chladivo je těžší než vzduch.")

K="Kapitola 4 · Práce na okruhu"
sec("pracoviste",K,'Bezpečné <span class="hl">pracoviště</span>',f'''<div class="grid c3">
{tile("sky",1,"OOP","Rukavice a ochranné brýle. Kontinuální monitorování prostoru detektorem.")}
{tile("rose",2,"3 m","Žádný zdroj zapálení do 3 m od systému a připojených zařízení.")}
{tile("mint",3,"Větrání","Přirozené nebo ventilátor v nevýbušném provedení.")}
{tile("sand",4,"Hasicí přístroj","Práškový min. 2 kg nebo CO₂ se srovnatelným výkonem.")}
{tile("peach",5,"Detektor","Vhodný pro HC, alarm při 20 % LFL, nenulovat v kontaminovaném prostoru.")}
{tile("paper",6,"Hodnocení rizik","Před prací; při vysokém riziku přesunout zařízení na dobu opravy ven.")}
</div>''',"Pracoviště","Hodnocení rizik ve 4 krocích: identifikovat ohrožení, kdo může být ohrožen (technik, jiní pracovníci, veřejnost), zhodnotit pravděpodobnost a závažnost a přijmout opatření, zaznamenat výsledky. Protokol patří do dokumentace o provedené práci.")

sec("naradi",K,'Nářadí a <span class="hl">chladivo</span>',f'''<div class="grid c2">
{tile("mint",1,"Lze použít","Manometrické soupravy. Většinu vývěv – potenciálně nebezpečný je jen hlavní vypínač; vývěvu do větraného prostoru.")}
{tile("rose",2,"Nelze použít","Běžné odsávací / plnicí stanice. Jen v nevýbušném provedení.")}
{tile("sand",3,"A2L F-plyny","R32, R1234yf, R1234ze před opravou odsát k opětovnému použití nebo likvidaci.")}
{tile("sky",4,"Uhlovodíky","Malou náplň lze podle podkladu vypustit do větraného prostoru.")}
</div>
{rem("Sběrnou láhev vyvakuovat, označit druhem chladiva a štítkem hořlavé látky. Hořlavá chladiva nemíchat s jinými.")}''',"Nářadí","Detektory musí být citlivé na příslušné chladivo. Plnit jen čistým chladivem v chlaďařské kvalitě. Těsnění musí odolat danému chladivu – i vložky Schrader ventilků.")

sec("rozpajeni",K,'Rozpájení, pájení, <span class="hl">plnění</span>','''<div class="grid c4" style="gap:20px">
<div class="tile sky rise" style="--i:1"><p class="num">1</p><h3>Odsát</h3><p class="txt" style="font-size:30px">detektor a větrání po celou dobu; odsávat do vakua</p></div>
<div class="tile sky rise" style="--i:2"><p class="num">2</p><h3>Dusík 0,1 bar</h3><p class="txt" style="font-size:30px">suchý, bez kyslíku; připojit hadici a otevřít ven</p></div>
<div class="tile sky rise" style="--i:3"><p class="num">3</p><h3>Odpájet</h3><p class="txt" style="font-size:30px">pak ověřit NT i VT stranu, že v okruhu nic nezůstalo</p></div>
<div class="tile mint rise" style="--i:4"><p class="num">4</p><h3>Zapájet</h3><p class="txt" style="font-size:30px">jeden servisní bod otevřený, proplach suchým dusíkem</p></div>
<div class="tile sand rise" style="--i:5"><p class="num">5</p><h3>Vakuum</h3><p class="txt" style="font-size:30px">důkladně – zbytek vzduchu může po spuštění vybuchnout</p></div>
<div class="tile sand rise" style="--i:6"><p class="num">6</p><h3>Plnit vážením</h3><p class="txt" style="font-size:30px">tolerance ±5 %, množství podle výrobce; hadice propláchnout</p></div>
<div class="tile peach rise" style="--i:7"><p class="num">7</p><h3>Díly</h3><p class="txt" style="font-size:30px">elektrika a kompresory jen stejného typu, nic neupravovat ani nepřemisťovat</p></div>
<div class="tile peach rise" style="--i:8"><p class="num">8</p><h3>Uzavřít</h3><p class="txt" style="font-size:30px">rozvaděče znovu správně utěsnit</p></div>
</div>''',"Postup","Celé schéma: odsát → dusík → odpájet → zapájet s proplachem → vakuum → plnit vážením. Elektrické díly se nahrazují prvky stejné bezpečnostní třídy.")

sec("zdroje",K,'Zdroje <span class="hl">zapálení</span>',f'''<div class="row">
<div class="tile paper rise" style="--i:1; width:820px"><h3>Nejčastější v chladicích zařízeních</h3>
<ul class="txt"><li>spínače on/off a stykače</li><li>relé (ovladače, jednofázové kompresory)</li><li>tlakové spínače, termostaty</li><li>tepelné ochrany přetížení</li><li>motory ventilátorů, čerpadla kondenzátu</li><li>jističe (MCB)</li></ul></div>
<div class="col fill">
{tile("rose",2,"Horké povrchy","Topení pro odmrazování a jiné povrchy max. zápalná teplota − 100 K, u HC asi <b>360 °C</b>.")}
{tile("sand",3,"Snižování rizik","Elektrika s označením Ex, přemístit ji mimo hořlavé zóny, trvalé větrání.")}
</div>
</div>
{rem("V potenciálně hořlavém prostředí nikdy nerozpojuj elektrické obvody pod napětím.")}''',"Zapálení","Teplota topení se ověřuje testem při maximální zátěži za předpokladu, že selhalo ukončení odmrazování. A2L, B2L i A3 chladiva lze zapálit otevřeným plamenem nebo jiskrou z nekrytých elektrických prvků.")

sec("preprava",K,'Přeprava <span class="hl">(ADR)</span>','''<div class="grid c3">
<div class="tile rose rise" style="--i:1"><p class="lbl">Hořlavý plyn v nádobách</p><p class="big">333 <span class="unit">kg</span></p><p class="txt">do tohoto množství bez dalších opatření ADR</p></div>
<div class="tile mint rise" style="--i:2"><p class="lbl">Naplněné zařízení</p><p class="big">&lt; 12 <span class="unit">kg</span></p><p class="txt">náplň pod 12 kg – ADR se nevztahuje (max. 1000 ks na vozidlo)</p></div>
<div class="tile sky rise" style="--i:3"><p class="lbl">Hasicí přístroj</p><p class="big">2 <span class="unit">kg</span></p><p class="txt">aspoň jeden ve vozidle</p></div>
</div>
<div class="tile paper rise" style="--i:4; padding:20px 32px"><p class="txt">Řidič zná bezpečnou manipulaci a hašení · vozidlo dobře větrané · ventily zavřené, adaptéry odpojené · nádoby zajištěné a jasně označené · doporučeno označení vozidla a údaj v přepravních dokladech.</p></div>''',"Přeprava","Po železnici platí obdobně RID. Láhve neohřívat a nepřevážet volně ležící.")

sec("normy",K,'Normy a <span class="hl">předpisy</span>',table(["Dokument","Co řeší pro hořlavá chladiva"],[
["ISO 817","označení chladiv a bezpečnostní třídy A1–B3"],
["EN 378-1","praktický limit, maximální náplně, kategorie přístupnosti"],
["EN 378-2 / -3","konstrukce, větrané kryty · strojovny, detektory chladiva"],
["EN 378-4","opravy systémů s hořlavými chladivy, kompetence personálu"],
["EN 60079 (-0, -10-1, -14, -15)","výbušná prostředí, zóny, elektroinstalace, krytí „nevýbušné“"],
["EN 60335-2-24 / -2-40 / -2-89","domácí chlazení · klimatizace a TČ · komerční chlazení s hořlavým chladivem"],
["ADR · RID · ATEX","přeprava po silnici a železnici · pracoviště s výbušnou atmosférou"]],29,["34%","66%"]),"Normy","Podklad uvádí vydání EN 378:2016 a starší vydání EN 60335 a EN 60079; v praxi platí aktuální vydání ČSN. Nařízení 2024/573 se týká A2L F-plynů (R32, HFO), ne uhlovodíků.")

quiz("4",4,"práce",[("Do jaké vzdálenosti od zařízení nesmí být zdroj zapálení?",["0,5 m","3 m","10 m","jen v jednotce"]),("Jak se okruh připraví k rozpájení?",["vypustí se a pájí","natlakuje se 10 bar N₂","odsaje do vakua, 0,1 bar N₂, otevřená hadice","pájí se za provozu"]),("Max. povrchová teplota topení u HC chladiv?",["100 °C","asi 360 °C","600 °C","není omezena"])],
[("Zdroje zapálení","B · 3 m","Plus větrání, detektor a hasicí přístroj v dosahu."),("Rozpájení","C · vakuum, 0,1 bar N₂, hadice ven","Dusík bez kyslíku, celou dobu hlídat prostor detektorem."),("Topení","B · asi 360 °C","Zápalná teplota HC (≈ 460 °C) mínus 100 K.")],
"V appce: Hořlavá chladiva a Bezpečnost práce.","Zapamatuj si pořadí: odsát → dusík → odpájet → zapájet s proplachem → vakuum → plnit vážením.")

ORDER.append("shrnuti")
S["shrnuti"]='''<section id="shrnuti" class="dark">
<div class="hose"></div>
<div class="head"><p class="kicker">Shrnutí</p><h2>Zapamatuj si <span style="color:#F2C230">před zkouškou</span></h2></div>
<div class="grid c2" style="gap:20px">
<div class="dtile rise" style="--i:1"><p class="dh">LFL R32 0,307 · R290 0,038</p><p class="dt">kg/m³; praktický limit ≈ 20 % LFL</p></div>
<div class="dtile rise" style="--i:2"><p class="dh">Alarm 25 % LFL / 50 % ATEL</p><p class="dt">nižší z hodnot; senzory nízko, test 1× ročně</p></div>
<div class="dtile rise" style="--i:3"><p class="dh">A / B / C · I–IV</p><p class="dt">přístupnost a umístění určují max. náplň</p></div>
<div class="dtile rise" style="--i:4"><p class="dh">0,2 × LFL × V</p><p class="dt">split: 2,5 × LFL^1,25 × h × √A</p></div>
<div class="dtile rise" style="--i:5"><p class="dh">VT v provozu, NT vypnuté</p><p class="dt">sprej jen v přetlaku, ultrazvuk i v podtlaku</p></div>
<div class="dtile rise" style="--i:6"><p class="dh">Dusík 12 h · 10 K ≈ 3,5 %</p><p class="dt">přepočet tlaku na teplotu okolí</p></div>
<div class="dtile rise" style="--i:7"><p class="dh">3 m · 360 °C · 2 kg</p><p class="dt">bez zdrojů zapálení · max. povrch · hasicí přístroj</p></div>
<div class="dtile rise" style="--i:8"><p class="dh">ADR 333 kg · zařízení &lt; 12 kg</p><p class="dt">nádoby · naplněná zařízení mimo ADR</p></div>
</div>
<p class="tag" style="background:#F2C230; color:#1E2A3A">Shrnutí</p>
<aside>Procvičuj v appce F-plyny Přeškolení v okruhu Hořlavá chladiva A2L / A3 (od verze 8 má 43 otázek); tabulka hodnot je v Taháku. Hlavní prezentace F-plyny Přeškolení pokrývá legislativu, oběh, těsnost a kategorie B a C.</aside>
</section>
'''
os.makedirs(OUT+"/slides",exist_ok=True)
for k,v in S.items(): open(f"{OUT}/slides/{k}.html","w",encoding="utf-8").write(v)
order=["cover","obsah"]+[x for x in ORDER if x not in("cover","obsah","shrnuti")]+["shrnuti"]
deck={"v":5,"createdOnFiles":{"v":1,"at":"2026-11-26T12:00:00Z"},"lists":"css","format":{"v":1,"shared":["project/deck.css"]},"title":"Hořlavá chladiva – výuka","cover":"cover","order":order,
"sections":{"s0":{"description":"Úvod a obsah","start":"cover"},"s1":{"description":"Kapitola 1: chladiva A2L a A3, pojmy LFL, PL, ATEL/ODL","start":"proc"},"s2":{"description":"Kapitola 2: odpovědnost, přístupnost a umístění, výpočet náplně, pevná detekce","start":"odpovednost"},"s3":{"description":"Kapitola 3: těsnost, metody detekce, tlaková zkouška","start":"tesnost"},"s4":{"description":"Kapitola 4: pracoviště, nářadí, pájení, zdroje zapálení, přeprava, normy","start":"pracoviste"},"s5":{"description":"Shrnutí","start":"shrnuti"}},
"faces":{"montserrat":{"family":"Montserrat","href":"https://fonts.googleapis.com/css2?family=Montserrat:wght@600..900&display=swap"},"nunito-sans":{"family":"Nunito Sans","href":"https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400..900&display=swap"}},"designSystems":[]}
json.dump(deck,open(OUT+"/deck.json","w",encoding="utf-8"),ensure_ascii=False)
print(len(order))
