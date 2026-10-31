# Fabrique la page perso « Mon assiette » (mes-proteines/) à partir de Georges (index.html).
# Georges lui-même ne contient AUCUNE calorie : tout le module calories est ajouté ici, seulement dans la page perso.
# À relancer après chaque modification de index.html :  python3 build-perso.py
import json, re

h = open('index.html', encoding='utf-8').read()

def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (a[:70], h.count(a))
    h = h.replace(a, b)

# ---------- En-tête, icônes, chemins ----------
rep('<meta charset="utf-8">', '<meta charset="utf-8">\n<script>window.PERSO_MODE=1</script>')
rep('<meta name="apple-mobile-web-app-title" content="Georges">', '<meta name="apple-mobile-web-app-title" content="Mon assiette">')
rep('href="icon.png?v=7"', 'href="plante-512.png?v=3"')
h = re.sub(r'<link rel="icon" href="icon-512.png\?v=\d+">', '<link rel="icon" href="plante-192.png?v=3">', h)
h = re.sub(r'<title>.*?</title>', '<title>Mon assiette</title>', h, count=1)
rep('fetch("version.json?t="', 'fetch("../version.json?t="')
rep('<h1>Georges</h1>', '<h1>Mon assiette</h1>')
rep('<div class="gport xs"></div>', '<img src="plante-192.png?v=3" alt="" style="width:58px;height:58px;border-radius:50%;flex:none">')
rep('navigator.serviceWorker.register("sw.js")', 'navigator.serviceWorker.register("../sw.js")')
rep('show("<strong>Accueille Georges sur ton téléphone.</strong> Il aura sa propre icône sur ton écran d\'accueil."',
    'show("<strong>Installe « Mon assiette » sur ton téléphone.</strong>"')
rep('go.hidden=!btn;', 'go.hidden=!btn;go.textContent="Installer";')

# ---------- Styles : masquer la navigation de Georges, afficher les calories ----------
rep('<style>.gate{display:none!important}[hidden]{display:none!important}</style>',
    '<style>.gate{display:none!important}[hidden]{display:none!important}'
    '.bnav,.apphead .atag,.apphead .asig{display:none!important}'
    '.nut .kc{font-weight:600}'
    'section[aria-label="Résumé du jour"] .settings{display:none!important}</style>')

# ---------- Carte « Mes calories du jour » ----------
rep('''  <div id="pane-s" class="pane" role="tabpanel" aria-labelledby="tab-s">
''', '''  <div id="pane-s" class="pane" role="tabpanel" aria-labelledby="tab-s">
    <section class="card" aria-labelledby="kcT" id="kcCard">
      <h2 id="kcT">Mes calories du jour<span id="kScore"></span></h2>
      <div class="settings">
        <label for="pT">Taille <input id="pT" type="number" inputmode="numeric" min="130" max="210" value="163"> cm</label>
        <label for="pA">Âge <input id="pA" type="number" inputmode="numeric" min="16" max="99" value="39"> ans</label>
        <label for="pK">Poids <input id="pK" type="number" inputmode="decimal" min="35" max="180" step="0.1" value="60"> kg</label>
        <label for="pG">Objectif <input id="pG" type="number" inputmode="decimal" min="35" max="180" step="0.1" value="55"> kg</label>
        <label for="pS">Muscu <select id="pS"><option value="0">0 séance</option><option value="1">1 séance</option><option value="2">2 séances</option><option value="3">3 séances</option><option value="3.5" selected>3 à 4 séances</option><option value="5">5 séances</option><option value="6">6 séances</option></select> / sem.</label>
      </div>
      <div class="sumtop">
        <svg class="ring" viewBox="0 0 100 100" aria-hidden="true">
          <circle class="bgc" cx="50" cy="50" r="42"/>
          <circle class="fgc" id="kArc" cx="50" cy="50" r="42" transform="rotate(-90 50 50)" stroke-dasharray="263.9" stroke-dashoffset="263.9"/>
          <text id="kTot" x="50" y="52" text-anchor="middle">0</text>
          <text class="small" x="50" y="68" text-anchor="middle">kcal</text>
        </svg>
        <div class="stats">
          <b id="kLeft">—</b>
          <div class="meta" id="kGoal"></div>
        </div>
      </div>
      <p class="meta colnote" id="kNote"></p>
    </section>
''')

# ---------- Œuf dur (page perso uniquement) ----------
rep('  ["tofu","Tofu ferme au calcium","100 g",14,2.7,1.5,350,0,0.3],', '  ["oeuf","Petit œuf dur (de ma poule)","1 petit œuf, 40 g",5,0.7,0.5,22,0,0.03,58],\n  ["tofu","Tofu ferme au calcium","100 g",14,2.7,1.5,350,0,0.3],')

# ---------- Calories des aliments ajoutés soi-même ----------
rep('''        <label for="aO">Oméga-3 (g)<input id="aO" inputmode="decimal" placeholder="0"></label>
''', '''        <label for="aO">Oméga-3 (g)<input id="aO" inputmode="decimal" placeholder="0"></label>
        <label for="aK">Calories (kcal)<input id="aK" inputmode="decimal" placeholder="0"></label>
''')
rep('v("aP"),v("aFe"),v("aZn"),v("aCa"),v("aC"),v("aO")]', 'v("aP"),v("aFe"),v("aZn"),v("aCa"),v("aC"),v("aO"),v("aK")]')

# ---------- Table des calories et calcul du déficit ----------
rep('const FOODMAP=()=>Object.fromEntries(allFoods().map(f=>[f[0],f]));', '''const FOODMAP=()=>Object.fromEntries(allFoods().map(f=>[f[0],f]));
// kcal par portion (valeurs moyennes Ciqual/USDA, arrondies)
const KCAL={laitS:85,laitA:40,yaS:65,avoine:150,painC:95,cacah:95,pureeA:200,tahini:90,tofu:130,tempeh:190,tvp:165,lent:230,soupeL:180,pateL:270,
 poisC:245,haric:190,houmous:140,edam:120,petitsP:80,seitan:140,poudre:115,courge:170,chanvre:115,chia:100,lin:55,tourn:175,sesame:52,amande:175,
 cajou:170,noix:200,bresil:66,olive:120,colza:120,quinoa:180,riz:195,rizC:185,sarrasin:140,pates:185,patesB:235,patesSG:200,patateD:180,pdt:170,
 avocat:120,radis:8,carotte:40,epinard:35,kale:25,pakchoi:13,brocoli:35,chouF:25,poivron:23,tomate:22,courgette:25,haricV:45,betterave:45,champi:22,
 salade:13,persil:5,nori:15,orange:65,jusO:90,kiwi:45,citron:10,grenade:70,raisin:105,raisinS:90,fraise:32,framb:52,myrtille:55,papaye:65,mangue:90,
 ananas:75,banane:105,pomme:80,figue:100,abricotS:75,datte:70,choco:115};
const kcalOf=f=>f[9]!=null?f[9]:(KCAL[f[0]]||0);
let pp=Object.assign({t:163,a:39,k:60,g:55,s:3.5},load("perso",{}));
function persoPlan(){
  const bmr=10*pp.k+6.25*pp.t-5*pp.a-161;            // Mifflin-St Jeor, femme
  const tdee=bmr*(1.375+0.025*pp.s);                  // marche quotidienne + séances de muscu
  const lose=pp.k-pp.g>0.3;
  const goal=lose?Math.max(1400,Math.round((tdee-300)/10)*10):Math.round(tdee/10)*10;   // déficit doux d'environ 300 kcal
  return {tdee:Math.round(tdee),goal,lose,prot:Math.round(pp.k*1.6)};               // 1,6 g de protéines par kilo
}
[["pT","t"],["pA","a"],["pK","k"],["pG","g"],["pS","s"]].forEach(([id,k])=>{const el=document.getElementById(id);el.value=pp[k];
  el.addEventListener(el.tagName==="SELECT"?"change":"input",()=>{const v=parseFloat(String(el.value).replace(",","."));if(v>0){pp[k]=v;store("perso",pp);render();}});});
function renderPerso(T){
  const P=persoPlan(),k=Math.round(T.k);
  document.getElementById("kArc").setAttribute("stroke-dashoffset",(263.9*(1-Math.min(1,k/P.goal))).toFixed(1));
  document.getElementById("kArc").style.stroke=k>P.goal+100?"var(--iron)":"";
  document.getElementById("kTot").textContent=k;
  document.getElementById("kLeft").textContent=k<=P.goal?`Encore ${P.goal-k} kcal`:`${k-P.goal} kcal au-dessus`;
  document.getElementById("kGoal").textContent=`Objectif : ${P.goal} kcal par jour${P.lose?" pour perdre du gras":""} · ${P.prot} g de protéines`;
  document.getElementById("kScore").textContent=P.lose?`déficit d'environ ${P.tdee-P.goal} kcal`:"";
  const weeks=P.lose?Math.ceil((pp.k-pp.g)/0.3):0,end=new Date();end.setDate(end.getDate()+weeks*7);
  document.getElementById("kNote").textContent=P.lose
    ?`Ton corps dépense environ ${P.tdee} kcal par jour. Avec ${P.goal} kcal et tes protéines atteintes, tu perds environ 0,25 à 0,35 kg de gras par semaine en gardant ton muscle : ${fmt(pp.g)} kg vers ${end.toLocaleDateString("fr-FR",{day:"numeric",month:"long"})}. Un jour au-dessus ne change rien : c'est la semaine qui compte. Mets à jour ton poids une fois par semaine, le matin à jeun.`
    :`Tu es à ton objectif : ${P.goal} kcal par jour pour rester stable.`;
}''')

# ---------- Totaux du jour avec calories, objectif protéines perso ----------
rep('const G=goals(),T={p:0,fe:0,zn:0,ca:0,c:0,o3:0},ate=[];', 'const G=goals(),T={p:0,fe:0,zn:0,ca:0,c:0,o3:0,k:0},ate=[];')
rep('T.p+=k*f[3];T.fe+=k*f[4];', 'T.p+=k*f[3];T.k+=k*kcalOf(f);T.fe+=k*f[4];')
rep('const [fl,ft]=ACT[prof.act],lo=Math.round(prof.kg*fl),target=Math.round(prof.kg*ft);',
    'const [fl,ft]=ACT[prof.act],lo=Math.round(prof.kg*fl),target=persoPlan().prot;')
rep('  window.__T=T;if(window.__vivReady)renderExtras();', '  renderPerso(T);\n  window.__T=T;if(window.__vivReady)renderExtras();')
rep('const T=window.__T||{p:0,fe:0,ca:0,c:0},G=goals(),target=Math.round(prof.kg*ACT[prof.act][1]);',
    'const T=window.__T||{p:0,fe:0,ca:0,c:0},G=goals(),target=persoPlan().prot;')

# ---------- Calories sur les aliments, recettes et menus ----------
rep('function nutHTML(f){\n  return [f[3]?', 'function nutHTML(f){\n  return [`<span class="kc">${kcalOf(f)} kcal</span>`,f[3]?')
rep('function recTotals(r){const M=FOODMAP(),t={p:0,fe:0,ca:0,c:0};\n  r.ing.forEach(([id,q])=>{const f=id&&M[id];if(f){t.p+=q*f[3];',
    'function recTotals(r){const M=FOODMAP(),t={p:0,fe:0,ca:0,c:0,k:0};\n  r.ing.forEach(([id,q])=>{const f=id&&M[id];if(f){t.k+=q*kcalOf(f);t.p+=q*f[3];')
rep('<div class="nut"><span class="p">${fmt(t.p)} g protéines</span><span class="f">fer ${fmt(t.fe)} mg</span>',
    '<div class="nut"><span class="kc">${Math.round(t.k)} kcal</span><span class="p">${fmt(t.p)} g protéines</span><span class="f">fer ${fmt(t.fe)} mg</span>')
rep('<span class="meta">${r.time} · ${fmt(t.p)} g de protéines</span>', '<span class="meta">${r.time} · ${fmt(t.p)} g de protéines · ${Math.round(t.k)} kcal</span>')

# ---------- Ouverture directe sur l'Assiette, sans message de Georges ----------
rep('if(true){gate.hidden=true;if(load("georges_vu","")!==today)showGeorges();}', 'if(true){gate.hidden=true;}')
rep('showTab(H==="mediter"?"m":H==="assiette"?"a":H==="journal"?"n":H==="aujourdhui"?"j":"g");', 'showTab("a");')

open('mes-proteines/index.html', 'w', encoding='utf-8').write(h)
json.dump({"id": "/mes-proteines/", "name": "Mon assiette", "short_name": "Mon assiette", "start_url": "./", "scope": "./",
           "display": "standalone", "background_color": "#eaf6f6", "theme_color": "#0a8379",
           "icons": [{"src": "plante-192.png?v=3", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                     {"src": "plante-512.png?v=3", "sizes": "512x512", "type": "image/png", "purpose": "any"}]},
          open('mes-proteines/manifest.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('mes-proteines/index.html régénéré')
