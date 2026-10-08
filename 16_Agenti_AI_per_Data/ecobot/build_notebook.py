"""Sincronizza nel notebook il codice verificato, evitando copie divergenti."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parent
notebook = nbf.read(ROOT / "agent.ipynb", as_version=4)
cells = []
md = lambda value: cells.append(nbf.v4.new_markdown_cell(value))
code = lambda value: cells.append(nbf.v4.new_code_cell(value))

md("""# EcoBot — analisi dei dati energetici
**Stefano Nocco · Agenti AI per Data · start2impact**

EcoBot è un assistente per EcoGrid Solutions: analizza la produzione solare di un’azienda e i consumi di una famiglia, risponde alle domande sui dati e propone indicazioni pratiche.

Il notebook è diviso in due parti. Nella prima preparo i dati, definisco gli strumenti di calcolo e costruisco l’agente. Nella seconda uso gli stessi componenti per creare l’interfaccia Streamlit.

## Parte 1 — dati, strumenti e agente
### 1. Ambiente
Uso Python 3.11 e le librerie elencate in `requirements.txt`. Se non sono ancora installate, impostare `INSTALL_DEPENDENCIES=True` nella prossima cella.

Il file `.env` contiene la configurazione del modello e della chiave API. Deve restare nella cartella del notebook; le celle leggono la configurazione senza mostrare la chiave.
""")
code("""INSTALL_DEPENDENCIES = False
if INSTALL_DEPENDENCIES:
    get_ipython().run_line_magic('pip', 'install -r requirements.txt')
from pathlib import Path
import os, json
from dotenv import load_dotenv
ROOT = Path.cwd()
assert (ROOT / 'requirements.txt').exists(), 'Apri il notebook dalla cartella ecobot'
load_dotenv(ROOT / '.env', override=False)
print('Chiave configurata:', bool(os.getenv('OPENAI_API_KEY')))
print('Le prove API richiedono attivazione esplicita; i test locali non consumano token.')
""")
md("""### 2. Dati
I due CSV descrivono 720 intervalli orari:

- `timestamp`: inizio dell’intervallo, interpretato in Europe/Rome quando manca l’offset.
- `kwh_produced`: energia prodotta dall’azienda nell’ora.
- `kwh_consumed`: energia consumata dalla famiglia nell’ora.

Ho mantenuto le formule e le anomalie previste dalla traccia: sei valori mancanti e un valore negativo nella produzione solare. Ho aggiunto un seed fisso e salvato i CSV per poter ripetere le analisi. Il manifest conserva le impronte dei file.

La cella seguente scrive il generatore. I dati vengono generati soltanto se non sono già presenti: per ritrovare i risultati degli esempi, usare i CSV inclusi.
""")
code("%%writefile generate_data.py\n" + (ROOT / "generate_data.py").read_text())
code("""from generate_data import generate
dataset_files = [ROOT/'data/solar_production_raw.csv', ROOT/'data/household_consumption.csv', ROOT/'data/manifest.json']
if not any(path.exists() for path in dataset_files):
    generate(ROOT / 'data')
elif not all(path.exists() for path in dataset_files):
    raise FileNotFoundError('Dataset incompleto: ripristina entrambi i CSV e il manifest originali, oppure sposta i file rimasti prima di rigenerare la coppia.')
manifest = json.loads((ROOT / 'data/manifest.json').read_text())
print(json.dumps(manifest, ensure_ascii=False, indent=2))
""")
md("""### 3. Pulizia e strumenti di calcolo
Prima dell’analisi, `load_and_clean` allinea i timestamp all’ora e controlla valori mancanti, negativi, infiniti e duplicati. I valori non validi restano sconosciuti: sostituirli con zero farebbe apparire completo un totale che non lo è.

Le due serie vengono allineate su una griglia oraria comune. Ogni risultato indica il periodo selezionato, le ore attese e quelle con una misura valida.

L’agente può usare sei strumenti: `quality`, `production_total`, `consumption_total`, `compare_energy`, `trend` ed `energy_chart`. Le operazioni sono definite in Python; il modello sceglie quale chiamare e con quali parametri.
""")
code("%%writefile energy_tools.py\n" + (ROOT / "energy_tools.py").read_text())
code("""from energy_tools import EnergyTools
data = EnergyTools((ROOT/'data/solar_production_raw.csv').read_bytes(),
                   (ROOT/'data/household_consumption.csv').read_bytes(), ROOT/'grafici')
print(json.dumps(data.quality(), ensure_ascii=False, indent=2))
""")
md("""### 4. Verifica con valori noti
Prima di collegare il modello, controllo i calcoli su un piccolo dataset. La produzione valida deve essere 6 kWh, con due misure sconosciute. Il confronto usa soltanto le ore valide in entrambe le serie.

Un intervallo privo di misure valide restituisce `None`: non equivale a un consumo o a una produzione pari a zero.
""")
code("""import pandas as pd
dates = pd.date_range('2026-07-01', periods=5, freq='h')
prod = pd.DataFrame({'timestamp':dates,'kwh_produced':[0,2,None,-5,4]}).to_csv(index=False).encode()
cons = pd.DataFrame({'timestamp':dates,'kwh_consumed':[1,1,1,2,3]}).to_csv(index=False).encode()
known = EnergyTools(prod, cons, ROOT/'grafici')
assert known.production_total()['total_kwh_observed'] == 6
assert known.production_total()['unknown_hours'] == 2
assert known.compare_energy()['potential_coincidence_kwh'] == 4
assert known.production_total(start='2025-07-01',end='2025-07-02')['total_kwh_observed'] is None
print('Verifiche numeriche indipendenti: superate')
pd.DataFrame([data.production_total(), data.consumption_total()])
""")
md("""### 5. Grafici e indicazioni dai dati
Il grafico giornaliero mostra l’energia osservata per ciascun giorno. La tabella successiva riassume i mesi. Per giorni e mesi uso somme; per il profilo delle ore del giorno uso medie.

I periodi ai margini del dataset possono essere incompleti. Per questo i risultati riportano sia la copertura della selezione sia quella del periodo di calendario. Se ci sono più di 90 periodi, il grafico mostra gli ultimi 90 e lo segnala.

Il confronto individua anche le ore con surplus medio positivo: possono aiutare a valutare quando spostare alcuni consumi, tenendo conto delle abitudini e della disponibilità effettiva dell’energia.
""")
code("""from IPython.display import Image, display
chart = data.energy_chart('day')
display(Image(filename=chart['chart_path']))
pd.DataFrame(data.trend('month')['data'])
""")
code("""comparison = data.compare_energy()
print(json.dumps(comparison, ensure_ascii=False, indent=2))
""")
md("""### 6. Agente e memoria
Ho scelto un singolo agente LangChain perché il compito riguarda due dataset e un insieme limitato di operazioni. Il modello interpreta la richiesta, propone un breve piano, chiama gli strumenti e spiega i risultati.

Il ciclo conserva strumenti, parametri e risultati. Se uno strumento riceve argomenti errati, l’errore torna al modello per consentire una correzione. Ogni domanda ha un limite di sei richieste al modello e dieci operazioni.

La memoria mantiene gli ultimi sei scambi, compresi i periodi analizzati, così da interpretare i riferimenti delle domande successive. La prova con `ControlledModel` qui sotto è una simulazione del ciclo; le prove con API reale sono nella sezione seguente.
""")
code("%%writefile ecobot_agent.py\n" + (ROOT / "ecobot_agent.py").read_text())
code("""from langchain_core.messages import AIMessage
from ecobot_agent import ask, make_model
class ControlledModel:
    # Simulazione dichiarata: verifica il ciclo, non l'accuratezza di un LLM reale.
    def __init__(self): self.step = 0
    def bind_tools(self, *args, **kwargs): return self
    def invoke(self, messages, **kwargs):
        self.step += 1
        if self.step == 1:
            return AIMessage(content='Piano: calcolo la produzione e controllo le ore mancanti.',
                tool_calls=[{'id':'demo_1','type':'tool_call','name':'production_total',
                  'args':{'start':None,'end':None,'hour_start':0,'hour_end':24}}])
        return AIMessage(content='6 kWh osservati su 3 ore valide; 2 ore senza misura. Totale parziale.')
simulation = ask(ControlledModel(), 'Quanto è stato prodotto?', known)
assert simulation.completed
print('SIMULAZIONE DEL MODELLO — non è una prova API')
print(simulation.text)
print(json.dumps(simulation.trace, ensure_ascii=False, indent=2))
""")
md("""### 7. Prove con il modello
La cella seguente prova cinque domande: anomalie, produzione totale, grafico mensile, risparmio economico e relazione fra produzione e consumi. Registra risposte, strumenti utilizzati, tempi e token.

Le chiamate API sono disattivate nell’esecuzione ordinaria. Per ripeterle, avviare Jupyter con la variabile `ECOBOT_RUN_REAL_API=1`. Le chiamate consumano credito dell’account configurato nel `.env`.

Per valutare una risposta confronto i numeri con i calcoli precedenti e controllo che siano spiegati i limiti dei dati. Per la memoria, un esempio utile è chiedere il consumo di una settimana e poi «E nella settimana precedente?».
""")
code("""RUN_REAL_API = os.getenv('ECOBOT_RUN_REAL_API', '0') == '1'
if RUN_REAL_API:
    from dataclasses import asdict
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        raise ValueError('Configura .env in locale prima delle prove reali')
    model_name = os.getenv('OPENAI_MODEL','gpt-4.1-mini')
    model = make_model(key, model_name)
    real_turns = []
    for question in ['Ci sono anomalie nei sensori?',
                     'Calcola la produzione totale osservata e indica le ore mancanti.',
                     'Mostra un grafico del confronto mensile.',
                     'Quanto ho risparmiato in euro?',
                     'La produzione solare causa un calo dei consumi?']:
        answer = ask(model, question, data, real_turns)
        record = asdict(answer)
        record['answer'] = record.pop('text')
        record.update(question=question,model=model_name,validation='API reale, revisione numerica da effettuare')
        real_turns.append(record)
        print(question, '\\n', answer.text, '\\nToken:', answer.usage)
        if answer.error_kind == 'api_error':
            break  # Conserva le evidenze senza insistere su un account non disponibile.
    (ROOT/'evidenze').mkdir(exist_ok=True)
    (ROOT/'evidenze/prove_api_reali.json').write_text(json.dumps(real_turns,ensure_ascii=False,indent=2))
else:
    print('Prove API NON ESEGUITE. Nessun risultato reale dichiarato.')
""")
md("""### Esempi salvati: dal piano agli strumenti
Il file `evidenze/prove_api_reali.json` contiene cinque conversazioni già eseguite. La cella seguente le legge senza chiamare nuovamente il modello e mostra i piani operativi registrati, gli strumenti scelti e i parametri.

Nel JSON sono conservate anche le risposte complete e i risultati dei calcoli. Quando una risposta non richiede strumenti, come una spiegazione sui dati mancanti per stimare il risparmio, viene indicato esplicitamente.
""")
code("""from pathlib import Path
import json
import pandas as pd
from IPython.display import display
saved_path = Path.cwd() / 'evidenze/prove_api_reali.json'
if saved_path.exists():
    saved_turns = json.loads(saved_path.read_text())
    print('EVIDENZE API ARCHIVIATE — lettura locale, nessuna nuova chiamata')
    for turn in saved_turns:
        print('Domanda:', turn['question'])
        plans = list(dict.fromkeys(step['public_plan'] for step in turn['trace'] if step.get('public_plan')))
        for plan in plans:
            print('Piano operativo registrato:', plan)
        if turn['trace']:
            display(pd.DataFrame([{'Strumento':step['tool'],
                                   'Parametri':json.dumps(step['arguments'], ensure_ascii=False),
                                   'Esito':'errore' if 'error' in step['result'] else 'calcolo completato'}
                                  for step in turn['trace']]))
        else:
            print('Nessuno strumento chiamato: risposta sui limiti dei dati.')
else:
    print('Nessuna evidenza API archiviata; esegui prima le prove reali se desideri acquisirla.')
""")
md("""### Confronto fra fasce orarie
Confronto i consumi delle ore 19–22 con quelli delle ore 11–14. Prima di interpretare i totali, controllo che le due fasce abbiano lo stesso numero di ore valide.
""")
code("""pd.DataFrame([data.consumption_total(hour_start=19,hour_end=22),
              data.consumption_total(hour_start=11,hour_end=14)])
""")
md("""## Parte 2 — interfaccia Streamlit
L’app riutilizza gli strumenti e l’agente definiti sopra. La barra laterale permette di caricare entrambi i CSV; in assenza di upload vengono usati quelli inclusi nel progetto.

La chat mostra risposte e grafici PNG e conserva i riferimenti delle domande successive. Quando cambiano i dati, la conversazione viene azzerata. Dalla scheda “Report e prove” si possono esportare la conversazione in HTML e i dettagli delle operazioni in JSON.

Le prossime due celle creano il modulo del report e `app.py`.
""")
code("%%writefile report.py\n" + (ROOT / "report.py").read_text())
code("%%writefile app.py\n" + (ROOT / "app.py").read_text())
md("""### Avvio dell’app
Dopo aver eseguito le celle precedenti, usare il comando stampato qui sotto in un terminale con l’ambiente Python attivo. In alternativa, impostare `START_STREAMLIT=True` per avviare il processo dal notebook e usare `server.terminate()` per fermarlo.

Nell’app, abilitare la casella di invio dei dati per usare la chat. `streamlit_screenshot.png` mostra una richiesta di confronto mensile con la risposta e il grafico generato.
""")
code("""import subprocess, sys
command = [sys.executable,'-m','streamlit','run','app.py','--server.address','127.0.0.1',
           '--server.port','8518','--browser.gatherUsageStats','false']
START_STREAMLIT = False
if START_STREAMLIT:
    server = subprocess.Popen(command, cwd=ROOT)
else:
    print(' '.join(command))
""")
md("""## Risultati e limiti
Sui CSV inclusi, la produzione osservata è 1.150,201223 kWh su 713 ore valide e il consumo è 1.292,323970 kWh su 720 ore. La produzione è quindi un totale parziale: sette misure sono mancanti o non valide.

I dati sono sintetici e il confronto riguarda un’azienda e una famiglia. La coincidenza fra produzione e consumo è uno scenario illustrativo, non una misura di autoconsumo o una bolletta. Mancano tariffe, stato di accumulo e quote della comunità energetica: EcoBot deve spiegare questi limiti quando la domanda richiede informazioni non disponibili. Anche una correlazione nei dati non dimostra un rapporto di causa ed effetto.

Gli esempi salvati e lo screenshot mostrano il funzionamento dell’agente. La correttezza delle risposte va valutata insieme agli strumenti chiamati, ai risultati e alla copertura temporale.

Riferimenti: [consegna del progetto](https://talent.start2impact.it/corsi/agenti-ai-per-data/progetto/b9577a46-370f-4d9f-8cbf-6a570d18ca84), [modelli e strumenti LangChain](https://docs.langchain.com/oss/python/langchain/models), [ChatOpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai).
""")
notebook.cells = cells
notebook.metadata.kernelspec = {"display_name":"Python 3 (EcoBot)","language":"python","name":"python3"}
nbf.validate(notebook)
nbf.write(notebook, ROOT / "agent.ipynb")
print(f"Notebook sincronizzato: {len(cells)} celle")
