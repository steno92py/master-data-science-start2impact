# Confronto con la consegna ufficiale

Fonte: [start2impact, Agenti AI per Data](https://talent.start2impact.it/corsi/agenti-ai-per-data/progetto/b9577a46-370f-4d9f-8cbf-6a570d18ca84), sezioni 1–7 rilette direttamente sul sito l’8 ottobre 2026 dal link fornito da Stefano. Sintesi della verifica in `evidenze/consegna_riletta_2026-10-08.json`; trascrizione precedente in `00_STATO_MASTER/tracce_ufficiali_2026-10-07.json`.

| Requisito / criterio | Implementazione ed evidenza | Stato |
| --- | --- | --- |
| EcoBot per EcoGrid, energia rinnovabile locale | Dataset azienda/famiglia, prompt e interfaccia dedicati | Implementato |
| Due CSV sintetici secondo il generatore fornito | Formule e anomalie originali; seed 42 e conservazione in `data/` aggiunti e documentati | Conforme alle formule; adattamento rispetto alla copia letterale dello script |
| Pulire NaN e valori negativi prima dell'analisi | `load_and_clean`, rapporto anomalie, nessuna imputazione silenziosa | Verificato localmente |
| Strumenti di pulizia, produzione e consumo | Funzione di pulizia + tool quality, production_total, consumption_total | Verificato localmente |
| Grafici PNG, insight e consigli comprensibili | energy_chart, compare_energy, prompt e notebook | Verificati nella suite API finale; note del notebook archiviate |
| Framework agentico | `langchain-core`, `langchain-openai`, ciclo tool calling esplicito | Verificato con API reale; il framework è a scelta nella traccia |
| Piano, strumenti, correzione errori | Piani operativi pubblici reali e parametri visibili nella cella dedicata; errori restituiti al modello | Uso reale dei tool verificato; recupero errori e limiti testati con simulazioni |
| Notebook principale, due sezioni | `agent.ipynb`, 28 celle, seconda parte `%%writefile app.py` | 16 celle verificate in ambiente pulito; 5 conversazioni API acquisite nel precedente passaggio della stessa revisione e rilette nella cella dei piani operativi |
| Streamlit: due upload laterali, chat, grafici | `app.py` | AppTest superato; app/chat/grafico controllati negli screenshot di Stefano. Caricamento manuale di entrambi i CSV verificato nello screenshot delle 12:02: tabella, grafico, totali e copertura attesi |
| Memoria e follow-up | Ultimi 6 scambi con periodo e risultati | Prove API note più chat di Stefano: 291,75 kWh dal 28/9 al 5/10 escluso, poi 301,18 kWh nella settimana precedente; numeri ricalcolati sui CSV |
| Robustezza e qualità del codice | 36 test, limiti righe/ore/tool, no exec generato | Verificato localmente |
| .env, requirements, README | `.env` configurato nel pacchetto finale riservato, versioni fissate, istruzioni | Presenti; installazione verificata. Inclusione della chiave esistente autorizzata da Stefano |
| Screenshot di interazione Streamlit | `streamlit_screenshot.png`, copia originale fornita da Stefano | Presente: domanda, risposta e PNG mensile visibili; chiave mascherata |
| ZIP NomeCognome_AgentiAIData.zip | Pacchetto finale riservato `StefanoNocco_AgentiAIData.zip` | Controlli funzionali e visivi completati; `.env` configurato su autorizzazione dell’utente |

Le lezioni pertinenti trattano LangChain, tool personalizzati, memoria, function calling, qualità dei dati, osservabilità, sicurezza, Streamlit e agenti multi-step. La traccia ammette esplicitamente una scelta di framework in funzione della complessità; Microsoft Agent Framework, RAG, Ollama e sistemi multi-agente non sono obbligatori per questi due CSV. La scelta di LangChain rende il lavoro direttamente confrontabile con i tutorial senza introdurre agenti superflui.

## Verifiche reali eseguite e attività residue

L’8 ottobre sono passati 36 test in un ambiente Python 3.11 appena installato da `requirements.txt`. La suite `evidenze/api_reale_20261008_103134.json` contiene 13 casi conformi, con risposte e strumenti revisionati. Le precisazioni successive del prompt su causalità, terminologia energetica e dati mancanti sono verificate in `evidenze/revisione_api_mirata_2026-10-08.json` (3 casi) e nelle 5 nuove conversazioni del notebook. Le note stilistiche e il filtro orario ridondante restano espliciti nelle evidenze.

Il notebook finale ha completato 16/16 celle di codice con API disattivata e lettura delle 5 conversazioni reali archiviate; tutti i moduli incorporati coincidono con i file Python. I CSV originali mantengono gli hash archiviati. Il report HTML incorpora il PNG reale; la struttura del report è controllata localmente. I grafici giornaliero, orario e mensile sono stati ispezionati come PNG, senza spacciare questa verifica per un controllo dell’interfaccia browser.

Gli output forniti da Stefano in `Downloads/ecobot_output` documentano panoramica, grafico mensile, consumo settimanale, follow-up e PNG giornaliero esportato. Valori e copertura coincidono con i CSV locali; lo screenshot mensile è copiato senza modifiche in `streamlit_screenshot.png`. Dettagli in `evidenze/verifica_output_utente_2026-10-08.json`. Report HTML/JSON della sessione verificati: dati, tool e risposte coincidono, il PNG giornaliero è incorporato e le due schermate del report ne mostrano la leggibilità con dettagli chiusi/aperti. Evidenza in `evidenze/verifica_export_utente_2026-10-08.json`. Anche l’upload manuale CSV è verificato nella nuova schermata delle 12:02: entrambi i file presenti, avviso demo assente, risultati attesi. Evidenza in `evidenze/verifica_upload_utente_2026-10-08.json`. L'accesso diretto del browser dell'assistente resta non effettuato dopo il diniego; nessun aggiramento. La traccia richiede un `.env` con chiave: Stefano ha autorizzato l’uso della chiave esistente nel pacchetto finale riservato; la versione di lavoro resta senza credenziale. Non sono stati caricati elaborati sulla piattaforma.

Nessun video è richiesto dalla consegna Data consultata. Il resoconto dei problemi corretti è in `REVISIONE_2026-10-08.txt`.

La rilettura live conferma che Colab, localtunnel, Seaborn e architetture multi-agente sono possibilità o esempi, non componenti obbligatori dell’implementazione locale scelta. La richiesta di pianificazione è documentata con piani operativi pubblici e tracce verificabili, senza divulgare ragionamenti interni privati.
