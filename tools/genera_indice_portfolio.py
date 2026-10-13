"""Genera un indice offline dei soli file selezionati per il portfolio pubblico."""
from pathlib import Path
from datetime import date
from urllib.parse import quote
import html
import json
import os

ROOT = Path(__file__).resolve().parents[1]
from verifica_archivio import candidate_paths


def category(rel):
    p = Path(rel)
    parts = set(p.parts)
    if parts & {'archivio', 'versioni_precedenti', 'storico', 'originale_recuperato'}:
        return 'Storico'
    if 'versione_git' in parts:
        return 'Copie senza output'
    if 'materiali_supporto' in parts and '02_PROGETTO_2' in parts:
        return 'Storico'
    if p.parts[0] == '98_ARCHIVIO_ORIGINALI':
        return 'Storico'
    if '00_STATO_MASTER' in parts or parts & {'evidenze', 'revisioni'} or p.name.startswith(('AUDIT_', 'RECAP', 'REVISIONE_')):
        return 'Registri e verifiche'
    if 'consegna' in parts or (p.suffix == '.zip' and '02_PROGETTO_2' in parts):
        return 'Consegne'
    if p.suffix in {'.py', '.ipynb', '.sql', '.cjs', '.ts', '.command', '.sh'}:
        return 'Codice e notebook'
    if p.suffix in {'.csv', '.xlsx', '.npy', '.joblib', '.pkl', '.safetensors', '.twb', '.twbx'}:
        return 'Dati e modelli'
    if p.suffix.lower() in {'.mp4', '.mov', '.wav', '.mp3', '.m4a', '.png', '.jpg', '.jpeg', '.gif', '.srt'}:
        return 'Multimedia'
    return 'Documentazione'


def scan():
    rows = []
    for rel in sorted(candidate_paths()):
        p = ROOT/rel
        if not p.is_file() or p.is_symlink() or p.name.startswith('.') or rel == 'INDICE_PORTFOLIO.html':
            continue
        rows.append({'path':rel, 'name':p.name, 'course':Path(rel).parts[0],
                     'category':category(rel), 'size':p.stat().st_size})
    return rows


def main():
    projects = json.loads((ROOT/'docs/catalogo_progetti.json').read_text())
    courses = [c for c in json.loads((ROOT/'docs/indice_corsi.json').read_text()) if c['folder']]
    today = date.today().isoformat()
    rows = scan()
    cards = []
    for c in courses:
        related = [p for p in projects if p['course_slug'] == c['slug']]
        title = c['title'] if c['folder'] != '17_Progetto_Finale' else 'Progetto finale — le due prove'
        links = [f'<a href="{quote(c["folder"]+"/README.md",safe="/")}">Guida del corso</a>']
        for p in related:
            target = p['artifact_path']
            label = 'Apri elaborato'
            if len(related)>1: label += ' · '+p['title'].split('—')[-1].strip()
            links.append(f'<a href="{quote(target,safe="/")}">{html.escape(label)}</a>')
        status = ' '.join(p.get('description','') for p in related)
        cards.append(f'<article><span class="number">{c["folder"][:2]}</span><h3>{html.escape(title)}</h3><p>{html.escape(status)}</p><nav>{"".join(links)}</nav></article>')
    data = json.dumps(rows,ensure_ascii=False).replace('<','\\u003c')
    options = ''.join(f'<option value="{html.escape(c["folder"])}">{html.escape(c["folder"].replace("_"," "))}</option>' for c in courses)
    page = '''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Master Data Science & AI — Stefano Nocco</title>
<style>
:root{color-scheme:light;--ink:#18332e;--muted:#526962;--line:#d8e3dc;--paper:#f5f7f3;--accent:#096b51}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,sans-serif}
main{max-width:1220px;margin:auto;padding:40px 28px}header{border-bottom:1px solid var(--line);padding-bottom:28px}
h1{font-size:clamp(28px,4vw,44px);line-height:1.12;margin:12px 0}h2{font-size:25px;margin-top:36px}h3{font-size:19px;line-height:1.3;margin:8px 0}
p{max-width:85ch}.eyebrow,.number{font-size:13px;font-weight:700;letter-spacing:.08em;color:var(--accent)}.muted{color:var(--muted)}
a{color:var(--accent);text-underline-offset:3px}a:hover{color:#063c2e}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #e0ac28;outline-offset:3px}
.toplinks{display:flex;flex-wrap:wrap;gap:12px}.toplinks a{padding:8px 13px;border:1px solid var(--line);border-radius:8px;background:white}
.notice{background:#e6efe7;border-left:4px solid var(--accent);padding:14px 18px;margin-top:22px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}article{padding:21px;background:white;border:1px solid var(--line);border-radius:12px}
article p{font-size:14px;color:var(--muted)}article nav{display:grid;gap:7px;font-size:14px}
.filters{display:grid;grid-template-columns:2fr 1fr 1fr;gap:14px;padding:18px;background:white;border:1px solid var(--line);border-radius:10px}
label{font-size:14px;font-weight:600}input,select{display:block;margin-top:6px;width:100%;padding:11px;border:1px solid #98afa5;border-radius:6px;font:inherit;color:var(--ink);background:white}
.results{border:1px solid var(--line);border-radius:10px;background:white;overflow:hidden}.file{display:grid;grid-template-columns:1fr 150px 80px;gap:12px;padding:13px 18px;border-bottom:1px solid var(--line)}
.file:last-child{border:0}.file a{font-weight:600;overflow-wrap:anywhere}.path{display:block;font-size:12px;overflow-wrap:anywhere;color:var(--muted)}.tag,.size{font-size:12px;color:var(--muted)}
.pagination{display:flex;align-items:center;gap:15px;margin:18px 0}button{padding:9px 16px;border:1px solid var(--line);border-radius:6px;background:white;color:var(--ink);font:inherit;cursor:pointer}button:disabled{opacity:.4;cursor:default}
footer{margin-top:35px;border-top:1px solid var(--line);padding-top:20px;font-size:13px;color:var(--muted)}
@media(max-width:700px){main{padding:25px 16px}.filters{grid-template-columns:1fr}.file{grid-template-columns:1fr}.tag,.size{display:none}}
</style></head><body><main>
<header><div class="eyebrow">STEFANO NOCCO · START2IMPACT</div><h1>Esplora il portfolio.</h1>
<p class="muted">17 cartelle di corso · 19 progetti. Cerca gli elaborati e consulta codice, dati e documentazione del repository.</p>
<nav class="toplinks"><a href="docs/PERCORSO.md">Indice dei progetti</a><a href="docs/ORGANIZZAZIONE.md">Come è organizzato</a><a href="README.md">Presentazione</a><a href="GITHUB.md">Verifiche</a></nav></header>
<section aria-labelledby="courses"><h2 id="courses">I corsi e gli elaborati</h2><div class="cards">__CARDS__</div></section>
<section aria-labelledby="find"><h2 id="find">Trova un file</h2><p class="muted">Cerca anche nel percorso: per esempio “Titanic”, “train.csv”, “video” o “Tableau”. Scegli Copie senza output per i notebook leggeri, oppure Registri e verifiche per le evidenze pubblicate.</p>
<div class="filters"><label>Cerca<input id="query" type="search" placeholder="Nome del file o parola chiave" autocomplete="off"></label>
<label>Corso<select id="course"><option value="">Tutto il portfolio</option>__OPTIONS__</select></label>
<label>Materiali<select id="category"><option>Correnti</option><option>Tutti</option><option>Consegne</option><option>Codice e notebook</option><option>Dati e modelli</option><option>Documentazione</option><option>Multimedia</option><option>Copie senza output</option><option>Storico</option><option>Registri e verifiche</option></select></label></div>
<p id="count" aria-live="polite"></p><div id="results" class="results"></div><div class="pagination"><button id="previous">Precedenti</button><span id="page"></span><button id="next">Successivi</button></div>
<noscript>Per la ricerca attivare JavaScript. I collegamenti dei corsi qui sopra funzionano anche senza JavaScript.</noscript></section>
<footer>Indice generato il __DATE__ · Funziona offline, senza servizi esterni. L’elenco comprende soltanto i file selezionati dalle regole del repository. I file restano nelle loro cartelle; il browser può aprirli o scaricarli secondo il formato.<br>Per aggiornare l’elenco: <code>python3 tools/genera_indice_portfolio.py</code>. <a href="docs/ORGANIZZAZIONE.md">Guida alla navigazione</a>.</footer>
</main><script>
const files=__DATA__;
const q=document.querySelector('#query'), course=document.querySelector('#course'), category=document.querySelector('#category'), results=document.querySelector('#results');
let page=0;const limit=60;
const norm=s=>s.toLocaleLowerCase('it').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
function render(){
 const words=norm(q.value).trim().split(/\s+/).filter(Boolean),kind=category.value;
 const found=files.filter(f=>(!course.value||f.course===course.value)&&(kind==='Tutti'||(kind==='Correnti'?!['Storico','Registri e verifiche','Copie senza output'].includes(f.category):kind===f.category))&&words.every(w=>norm(f.path+' '+f.category).includes(w)));
 const pages=Math.max(1,Math.ceil(found.length/limit));page=Math.min(page,pages-1);results.replaceChildren();
 for(const f of found.slice(page*limit,(page+1)*limit)){
  const row=document.createElement('div');row.className='file';const main=document.createElement('div'),a=document.createElement('a'),path=document.createElement('span'),tag=document.createElement('span'),size=document.createElement('span');
  a.textContent=f.name;a.href=f.path.split('/').map(encodeURIComponent).join('/');path.textContent=f.path;path.className='path';tag.className='tag';tag.textContent=f.category;size.className='size';size.textContent=f.size>=1e6?(f.size/1e6).toFixed(2)+' MB':Math.max(1,Math.ceil(f.size/1000))+' KB';main.append(a,path);row.append(main,tag,size);results.append(row);
 }
 document.querySelector('#count').textContent=found.length+' file trovati'+(found.length?' · '+(page*limit+1)+'–'+Math.min((page+1)*limit,found.length):'');
 if(!found.length){const p=document.createElement('p');p.style.padding='0 18px';p.textContent='Nessun risultato. Prova un altro termine o scegli Tutti.';results.append(p)}
 document.querySelector('#page').textContent='Pagina '+(page+1)+' di '+pages;document.querySelector('#previous').disabled=page===0;document.querySelector('#next').disabled=page>=pages-1;
}
q.addEventListener('input',()=>{page=0;render()});for(const e of [course,category])e.addEventListener('change',()=>{page=0;render()});
document.querySelector('#previous').onclick=()=>{page--;render()};document.querySelector('#next').onclick=()=>{page++;render()};render();
</script></body></html>'''
    for marker, value in {'__CARDS__':''.join(cards),'__OPTIONS__':options,'__DATE__':today,'__DATA__':data}.items():
        page=page.replace(marker,value)
    (ROOT/'INDICE_PORTFOLIO.html').write_text(page)
    print(json.dumps({'courses':len(courses),'projects':len(projects),'searchable_files':len(rows),'output':'INDICE_PORTFOLIO.html'},ensure_ascii=False))


if __name__ == '__main__':
    main()
