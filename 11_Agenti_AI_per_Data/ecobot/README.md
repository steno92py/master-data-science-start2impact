# EcoBot — Stefano Nocco

Progetto **Agenti AI per Data**, adeguato alla [consegna start2impact](https://talent.start2impact.it/corsi/agenti-ai-per-data/progetto/b9577a46-370f-4d9f-8cbf-6a570d18ca84) consultata il 7 ottobre 2026. EcoBot aiuta EcoGrid Solutions a spiegare produzione solare aziendale e consumi domestici.

**Revisione dell’8 ottobre: 36 test locali superati anche in un ambiente pulito, suite di 13 casi API riesaminata, 3 prove mirate dopo le precisazioni del prompt e notebook rieseguito con 5 conversazioni reali. App, grafico e follow-up verificati negli screenshot forniti da Stefano; screenshot di consegna acquisito. Export HTML/JSON verificati, compresa la resa visiva negli screenshot di Stefano. Anche l’upload manuale dei due CSV è verificato nello screenshot di Stefano delle 12:02: totali e copertura attesi. Configurazione API autorizzata da Stefano nel `.env` del pacchetto finale. Pronto alla consegna riservata al valutatore.** Il precedente Data Companion in ../archivio/prototipo_data_companion è conservato come prototipo, non è il progetto conforme da consegnare.

## Avvio

Usare Python 3.11 e un ambiente virtuale. Dalla cartella `ecobot`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
python -m streamlit run app.py --server.address 127.0.0.1
```

Il pacchetto finale include un `.env` già configurato. Non sovrascriverlo con `.env.example`. Nella versione senza credenziale, compilare `OPENAI_API_KEY` in `.env` oppure inserirla nel campo password dell’app. Il modello predefinito è `gpt-4.1-mini`; deve essere disponibile nell'account scelto. Le analisi Python e i grafici sono disponibili senza API. La chat richiede la selezione esplicita della casella di consenso nell'app e può consumare credito dell'account.

Nel workspace già predisposto, aprire `avvia_ecobot.command`: usa l'ambiente condiviso `.venv-agenti-ai`. Il server è stato avviato nuovamente l’8 ottobre 2026 su `http://127.0.0.1:8518`. L'accesso diretto del browser dell'assistente è stato rifiutato; l'interfaccia e la chat sono state poi verificate negli screenshot forniti da Stefano, senza aggirare il blocco. La chiave API è configurata nel `.env` locale con permessi 0600. Su autorizzazione di Stefano, il pacchetto finale la include nel solo `.env`; la versione di lavoro conserva il template vuoto.

## Notebook richiesto

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

Il resoconto completo è in [REVISIONE_2026-10-08.txt](REVISIONE_2026-10-08.txt); le prove sono riepilogate in [evidenze/revisione_2026-10-08.json](evidenze/revisione_2026-10-08.json). Corretti copertura dei CSV con periodi diversi, evidenze di più intervalli, conservazione dei risultati in caso di errore API e azzeramento dei grafici della vecchia chat. Migliorate le indicazioni sui periodi incompleti e la leggibilità del report HTML.

Un errore del servizio interrompe l’analisi ma conserva i calcoli già eseguiti; i token riportati coprono soltanto le risposte effettivamente ricevute. I file di dati originali e i loro hash sono invariati. I test includono giorni di 23 e 25 ore, intervalli disgiunti e recupero dagli errori. L’installazione da `requirements.txt` è stata verificata in un nuovo ambiente Python 3.11.

## Verifica e consegna

```bash
python -m pytest tests -q --junitxml=evidenze/test_locali.xml
python verifica_api.py --confirm-api
```

Il secondo comando esegue prove reali con i CSV sintetici e il piccolo dataset noto; richiede chiave e opzione esplicita. Il risultato contiene controlli automatici sui tool e casi da rivedere manualmente: non equiparare una risposta dell'LLM a un test superato senza valutarla.

Consultare [RELAZIONE.md](RELAZIONE.md) e [CONFORMITA.md](CONFORMITA.md). Il pacchetto richiesto è `StefanoNocco_AgentiAIData.zip` con notebook, `.env`, requisiti, README e `streamlit_screenshot.png`. Il pacchetto finale include il `.env` configurato con la chiave esistente, come autorizzato da Stefano, e lo screenshot originale della chat con domanda, risposta e grafico mensile. È destinato alla consegna riservata al valutatore e contiene una credenziale; non pubblicarlo su repository o link pubblici. La versione `DA_VALIDARE` conserva un `.env` senza chiave e richiede configurazione. Provenienza e verifiche sono in `evidenze/verifica_output_utente_2026-10-08.json`, `verifica_export_utente_2026-10-08.json` e `verifica_upload_utente_2026-10-08.json`.

Il comando `python prepara_consegna.py` crea la versione senza chiave `StefanoNocco_AgentiAIData_REVISIONATO_DA_VALIDARE.zip`. Il comando esplicito `python prepara_consegna.py --include-local-api-key` crea il pacchetto riservato `StefanoNocco_AgentiAIData.zip`, includendo soltanto chiave, modello e disattivazione del tracing nel `.env`. La consegna è stata riletta direttamente sul sito l’8 ottobre, incluse tutte le sette sezioni.

La versione finale usa un elenco di 9 file e il README essenziale in `materiali_consegna/README.md`. Il notebook genera i moduli Python: nella consegna eseguirlo prima di avviare Streamlit. Test, registri di revisione, report aggiuntivi e strumenti di lavoro restano fuori dallo ZIP finale.
