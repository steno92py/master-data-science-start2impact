# EcoBot — Agenti AI per Data

**Stefano Nocco · start2impact**

EcoBot analizza la produzione solare di un’azienda e i consumi di una famiglia per EcoGrid Solutions. Permette di controllare la qualità dei dati, calcolare l’energia in un intervallo, visualizzare grafici e chiedere spiegazioni in linguaggio naturale.

## Scelte del progetto

Ho scelto un singolo agente con LangChain: per due dataset e sei strumenti non serve distribuire il lavoro fra più agenti. Il modello interpreta la domanda e sceglie gli strumenti; Python esegue i calcoli. In questo modo ogni risposta può riportare il periodo analizzato, le ore valide e i risultati delle operazioni.

La pulizia conserva l’incertezza dei dati: valori mancanti e negativi vengono esclusi dai totali, senza sostituirli con zero. Le date sono allineate all’ora nel fuso Europe/Rome. Negli intervalli, la data iniziale è inclusa e quella finale esclusa.

L’interfaccia Streamlit permette di caricare entrambi i CSV, consultare le analisi e usare la chat. L’agente conserva gli ultimi sei scambi per gestire domande successive come «E nella settimana precedente?». È possibile scaricare dati puliti, grafici PNG e un report HTML.

## Avvio

1. Estrarre lo ZIP e aprire un terminale nella cartella estratta. Usare Python 3.11.
2. Creare l’ambiente e installare le dipendenze:

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   python -m ipykernel install --user --name ecobot --display-name "Python (EcoBot)"
   ```

   Su Windows, attivare l’ambiente con `.venv\Scripts\activate`.

3. Aprire `agent.ipynb` in Jupyter o in un editor compatibile, scegliere il kernel **Python (EcoBot)** ed eseguire le celle in ordine. Il notebook crea i moduli Python e `app.py` nella cartella di lavoro.
4. Avviare l’app dal terminale con l’ambiente attivo:

   ```bash
   python -m streamlit run app.py --server.address 127.0.0.1
   ```

Il `.env` incluso è già configurato: non va sovrascritto. Nell’app, abilitare la casella di invio dei dati per usare la chat. Le chiamate al modello consumano credito. L’esecuzione ordinaria del notebook non effettua chiamate API: mostra le prove salvate; la sezione dedicata spiega come abilitarne di nuove.

## File

- `agent.ipynb`: sviluppo dell’agente, esempi e creazione dell’app Streamlit.
- `.env` e `requirements.txt`: configurazione e dipendenze.
- `streamlit_screenshot.png`: una domanda con risposta e grafico nella chat.
- `data/`: i due CSV e il manifest con le loro impronte, per ripetere le analisi sugli stessi dati.
- `evidenze/prove_api_reali.json`: cinque conversazioni salvate, lette dal notebook per mostrare risposte, piani operativi e strumenti utilizzati.

## Esempi e risultati

I CSV contengono 720 misure orarie. Sono stati generati con le formule e le anomalie della traccia, aggiungendo un seed fisso e salvando i file per rendere ripetibili gli esempi.

| Domanda | Risultato verificato |
| --- | --- |
| «Calcola la produzione totale osservata.» | 1.150,201223 kWh su 713 ore valide; 7 misure mancanti o non valide. |
| «Quanto ho consumato dal 28 settembre al 5 ottobre 2026, con fine esclusa?» | 291,75 kWh su 168 ore valide. |
| «E nella settimana precedente?» | 301,18 kWh dal 21 al 28 settembre, fine esclusa. |
| «Mostra un grafico del confronto mensile.» | PNG con produzione e consumo; settembre e ottobre sono segnalati come mesi coperti solo in parte. |
| «Quanto ho risparmiato in euro?» | EcoBot segnala che mancano tariffe e informazioni economiche per calcolarlo. |

## Limiti

I dati sono sintetici. Il confronto fra produzione aziendale e consumo familiare è uno scenario illustrativo: non misura una bolletta o l’autoconsumo reale di una comunità energetica. Le anomalie non dimostrano da sole un guasto. Le risposte del modello vanno lette insieme ai risultati dei calcoli e alla copertura dei dati.

Il pacchetto contiene una chiave API ed è destinato alla valutazione del progetto.
