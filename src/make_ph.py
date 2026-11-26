import json
from CoolProp.CoolProp import PropsSI as P
R=["R32","R410A","R134a","R290"]
out={}
T0=list(range(-25,16,5)); SH=[2,5,10,15,20]; TK=list(range(30,61,5)); ETA=0.7
for k in R:
  K=lambda t:t+273.15
  tc=P("Tcrit","",0,"",0,k)-273.15; pc=P("pcrit","",0,"",0,k)/1e5
  ts=[t for t in range(-40,int(tc)) ]
  if ts[-1]<tc-0.5: pass
  dome={"t":[],"pl":[],"hl":[],"pv":[],"hv":[]}
  for t in list(range(-40,int(tc)-1,2))+[round(tc-0.6,1)]:
    dome["t"].append(t)
    dome["pl"].append(round(P("P","T",K(t),"Q",0,k)/1e5,3)); dome["hl"].append(round(P("H","T",K(t),"Q",0,k)/1e3,1))
    dome["pv"].append(round(P("P","T",K(t),"Q",1,k)/1e5,3)); dome["hv"].append(round(P("H","T",K(t),"Q",1,k)/1e3,1))
  h1=[];h2=[];t2=[]
  for t0 in T0:
    p0=P("P","T",K(t0),"Q",1,k)
    r1=[];r2=[];r3=[]
    for sh in SH:
      h=P("H","T",K(t0+sh),"P",p0,k); s=P("S","T",K(t0+sh),"P",p0,k); r1.append(round(h/1e3,1))
      a=[];b=[]
      for tk in TK:
        pk=P("P","T",K(tk),"Q",0,k); hs=P("H","P",pk,"S",s,k); hh=h+(hs-h)/ETA
        a.append(round(hh/1e3,1)); b.append(round(P("T","P",pk,"H",hh,k)-273.15,1))
      r2.append(a);r3.append(b)
    h1.append(r1);h2.append(r2);t2.append(r3)
  out[k]={"tc":round(tc,1),"pc":round(pc,2),"hc":round(P("H","T",K(tc-0.01),"Q",0,k)/1e3,1),"d":dome,"h1":h1,"h2":h2,"t2":t2}
js="// log p-h data z CoolProp: dóm (bar abs, kJ/kg), h1[t0][sh], h2/t2[t0][sh][tk] při izoentropické účinnosti 0,7\nconst PH="+json.dumps(out,separators=(",",":"))+",PH_T0="+json.dumps(T0)+",PH_SH="+json.dumps(SH)+",PH_TK="+json.dumps(TK)+";\n"
open("ph.js","w").write(js)
print(len(js), {k:(out[k]["tc"],out[k]["pc"]) for k in out}, out["R32"]["h1"][5][1], out["R32"]["h2"][5][1][3], out["R32"]["t2"][5][1][3])
