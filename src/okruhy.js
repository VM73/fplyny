// Okruhy přílohy I prov. nař. (EU) 2024/2215 a přiřazení otázek.
// Zkouška: vždy 1–5, 10, 11 + podle kategorie 12 (A1/A2), 13 (B), 14 (C) + aspoň jeden z 6–9 (předem nevíš který).
const OKRUHY = {
  1:"Legislativa a základy termodynamiky",
  2:"Vliv chladiv na prostředí a předpisy",
  3:"Kontroly před uvedením do provozu, po opravě a za provozu",
  4:"Kontrola těsnosti",
  5:"Šetrné zacházení se systémem a chladivem",
  6:"Kompresory",
  7:"Kondenzátory",
  8:"Výparníky",
  9:"Expanzní ventily a další komponenty",
  10:"Potrubí – těsný systém",
  11:"Alternativní technologie a bezpečné zacházení",
  12:"Uhlovodíky – instalace a servis",
  13:"CO₂ (R744) – instalace a servis",
  14:"NH₃ (R717) – instalace a servis"
};
const OKR_CAT = {
  "A1/A2":[1,2,3,4,5,6,7,8,9,10,11,12],
  "B":[1,2,3,4,5,6,7,8,9,10,11,13],
  "C":[1,2,3,4,5,6,7,8,9,10,11,14]
};
// výchozí okruh podle modulu
const OKR_DEF = {leg:1,env:2,fyz:1,kom:9,tes:3,hor:12,co2:13,nh3:14,pot:10,bez:5,ene:3,sit:3};
// výjimky podle pořadí otázky v bance (index = číslo za pomlčkou v id)
const OKR_OVR = {
  // env
  37:11,38:11,39:1,41:11,
  // kom
  54:6,55:6,57:10,221:6,225:6,226:6,227:6,230:6,231:6,
  // tes
  59:4,62:5,63:5,65:5,99:4,100:5,101:5,102:4,239:4,240:4,241:4,242:5,
  // hor
  70:11,113:11,114:11,145:11,146:11,148:4,149:4,150:4,151:4,152:4,153:3,154:3,
  // bez
  121:11,124:3,195:3,196:3,197:3,198:11,201:11,
  // ene
  125:7,127:8,204:8,
  // sit
  163:4,167:4,168:4,170:7,171:7,172:9,173:11,174:1,175:5,176:1,177:12,178:5,179:4,180:4,
  182:7,183:4,184:10,186:12,187:1,189:5,190:7,191:9,192:5
};
