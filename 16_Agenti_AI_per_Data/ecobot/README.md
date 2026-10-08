# EcoBot — Stefano Nocco

Assistente per analizzare produzione solare aziendale e consumi domestici, con strumenti Python, agente LangChain e interfaccia Streamlit.

## Avvio

Usare Python 3.11 e un ambiente virtuale. Dalla cartella `ecobot`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
python -m streamlit run app.py --server.address 127.0.0.1
```

Compilare `OPENAI_API_KEY` nel proprio `.env` oppure inserirla nel campo password dell’app. Il modello predefinito è `gpt-4.1-mini`. Le analisi Python e i grafici funzionano senza API; la chat richiede la casella di consenso nell’app e può consumare credito dell’account.

## Notebook

Aprire `agent.ipynb` dalla cartella del progetto ed eseguirlo in ordine. Contiene setup, generatore ufficiale, strumenti, agente LangChain, verifiche numeriche e una seconda parte che crea `app.py` con `%%writefile`. Le celle scrivono le copie dei moduli incluse nel notebook: personalizzare i file prima di rigenerare il notebook con `build_notebook.py`.

Il notebook è stato eseguito integralmente con un vero kernel Jupyter Python 3.11 in una cartella temporanea isolata: **16 celle di codice su 16 nella verifica finale**, senza errori. Gli output sono conservati in `agent.ipynb` e il riepilogo in `evidenze/esecuzione_notebook_finale_2026-10-08.json`. Nel passaggio precedente della stessa revisione sono state eseguite **5 conversazioni API reali**, salvate in `evidenze/prove_api_reali.json`. L’esecuzione finale è offline: la cella dedicata legge queste evidenze e mostra i piani operativi pubblici e i tool effettivamente usati. Non presenta la rilettura locale come una nuova chiamata al modello. Installazione e avvio server erano disattivati. Le simulazioni restano etichettate. Per ripetere le chiamate avvia Jupyter con `ECOBOT_RUN_REAL_API=1`; senza questa variabile il notebook non usa l’API.

## Dati e risultati riproducibili

I due CSV sotto `data/` sono generati dalle formule della traccia, con seed 42 e 720 campioni orari. `data/manifest.json` conserva data e hash. Il file solare contiene 6 NaN e un valore negativo introdotti dalla consegna. Non rigenerare i file per ripetere gli stessi risultati.

La pulizia allinea gli orari (contando i timestamp arrotondati), rende sconosciuti i valori negativi, non numerici e non finiti, segnala i timestamp invalidi e gestisce i duplicati. Non sostituisce i mancanti con zero. Ogni somma mostra copertura e periodo; l'estremo finale è escluso. Il fuso è Europe/Rome, compreso il cambio d'ora con offset espliciti. La griglia comune include anche ore assenti in entrambi i file. I grafici distinguono la copertura della selezione da quella di giorni o mesi interi e segnalano quando mostrano soltanto gli ultimi 90 periodi.

Risultati locali sul dataset archiviato:

| Misura | Valore | Copertura |
| --- | ---: | --- |
| Produzione osservata | 1.150,201223 kWh | 713/720 ore, totale parziale |
| Consumo osservato | 1.292,323970 kWh | 720/720 ore |
| Coincidenza potenziale produzione/consumo | 495,384477 kWh | 713 coppie valide |

Il confronto è illustrativo: produzione aziendale e consumo familiare non misurano da soli autoconsumo o fatturazione di una comunità energetica. Non sono disponibili tariffe, quote, accumulo o fattori emissivi. Nessuna stima monetaria o raccomandazione d'acquisto è prodotta.

## Architettura e limiti

Un singolo agente è sufficiente per due dataset e sei strumenti: mantiene il flusso comprensibile e verificabile senza richiedere coordinamento fra agenti. LangChain gestisce `ChatOpenAI`, messaggi e function calling. Sei strumenti Python consentiti espongono qualità, totali, confronto, aggregazioni e grafici PNG. La pulizia viene applicata prima di ogni analisi. L'agente può correggere argomenti errati, mantiene gli ultimi sei scambi e si ferma dopo sei richieste al modello o dieci operazioni. Non esegue codice arbitrario generato dal modello.

L'app accetta due upload, mostra grafici nella chat e permette di esportare CSV puliti, PNG, report HTML e tracce JSON. Le tracce conservano argomenti, risultati, breve piano operativo se fornito dal modello, tempi e token. I percorsi locali dei PNG non vengono inviati al modello. Il tracing esterno LangSmith è disabilitato.

Il modello riceve domanda, contesto recente, profilo e risultati calcolati, che possono includere dati caricati. Per le prove preparate usare esclusivamente i CSV sintetici. Ambiguità, causalità e istruzioni ingannevoli sono state verificate nella suite di 13 casi; le ultime precisazioni linguistiche del prompt sono coperte da altre 3 prove mirate e dalle 5 conversazioni del notebook. Le prove non garantiscono correttezza su tutte le possibili domande. Copertura e limiti del confronto vengono aggiunti direttamente dai risultati Python, anche se il modello li omette.

## Esempi provati con successo

- «Ci sono anomalie nei sensori?» — distingue i valori mancanti/negativi da una diagnosi certa di guasto.
- «Calcola la produzione totale osservata e indica le ore mancanti.» — 1.150,201223 kWh su 713/720 ore.
- «Mostra un grafico del confronto mensile.» — PNG con settembre e ottobre esplicitamente parziali.
- «Quanto ho risparmiato in euro?» — spiega quali dati economici mancano.
- Su dati noti: «Calcola il consumo dal 1 luglio 2026 01:00 al 1 luglio 2026 03:00, fine esclusa», poi «E nelle due ore successive?» — rispettivamente 2 e 5 kWh.

## Revisione dell’8 ottobre

Le [evidenze tecniche](evidenze/validazione_api.json) riepilogano test locali, prove API e verifiche del notebook.

Un errore del servizio interrompe l’analisi ma conserva i calcoli già eseguiti; i token riportati coprono soltanto le risposte effettivamente ricevute. I file di dati originali e i loro hash sono invariati. I test includono giorni di 23 e 25 ore, intervalli disgiunti e recupero dagli errori. L’installazione da `requirements.txt` è stata verificata in un nuovo ambiente Python 3.11.

## Verifiche

```sh
python -m pytest tests -q
```

La suite comprende 36 test locali. Le evidenze conservano anche 13 casi API, 3 prove mirate e 5 conversazioni del notebook. Sono esecuzioni storiche, distinte dai test offline.

`python verifica_api.py --confirm-api` ripete le prove reali con dati sintetici e richiede una chiave API. I controlli automatici sugli strumenti vanno accompagnati dalla lettura delle risposte.

La [relazione tecnica](RELAZIONE.md) descrive scelte, risultati e limiti. Lo [screenshot](streamlit_screenshot.png) mostra l’interfaccia con domanda, risposta e grafico.
