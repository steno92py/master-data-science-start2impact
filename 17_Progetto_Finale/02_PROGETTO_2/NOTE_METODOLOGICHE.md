# Progetto finale 2 — metodo e verifiche

Il progetto è stato revisionato e rieseguito integralmente il 9 ottobre 2026, mantenendo EDA, quattro algoritmi, griglie originali e selezione ibrida come approfondimento.

## Cosa è cambiato

| Punto | Intervento verificato |
| --- | --- |
| Strada 2 | Quattro numeriche significative al Welch T-test, p < 0,05 e ordine per valore assoluto di t, ricalcolate nei fold. |
| Selezione ibrida | Conservata e rieseguita come approfondimento distinto, con spot check e tuning completi. |
| Preprocessing | Mediane, categorie, scaler, flag e selezione appresi nella Pipeline durante ogni fit di CV. |
| Ranking T-test | Zeri dei rating esclusi come N/A prima del test statistico: la top 4 diventa `Online boarding`, `Inflight entertainment`, `Inflight wifi service`, `Seat comfort`. |
| Confronti temporali | Conservato il modello senza rating con ritardi; aggiunto quello senza rating né ritardi effettivi. |
| Mutual Information | Mask esplicita per rating e feature categoriche/binarie discrete. |
| Interpretazione | Target negativo completo, unità della distanza non inventata, associazioni separate da causalità e sostenibilità non misurata. |
| Scelta del modello | CV per selezione; confronto test descrittivo separato. Importanze e export seguono il modello realmente scelto. |
| Compatibilità | Rimossi `algorithm='SAMME'`, vecchio argomento `labels` dei boxplot e soppressione generale dei warning; ambiente versionato. |
| Export | Pipeline completa da input grezzi, inclusa imputazione di Arrival Delay, con prova in processo separato. |
| Notebook | Nome richiesto dalla traccia, output conservati e bundle Plotly ripetuti eliminati. |

## Verifiche dell’esecuzione completa del 9 ottobre 2026

- Notebook completo: **60 celle di codice su 60**, contatori sequenziali, nessun output di errore. Tutte le 135 celle originali sono conservate nelle loro posizioni relative; il totale è ora 139.
- Modelli: 189 combinazioni di iperparametri, 945 fit di CV nelle griglie e 8 rifit sul train completo; 100 fit negli spot check (5 esperimenti × 4 algoritmi × 5 fold). Nessun artefatto originale è stato caricato per produrre questi risultati.
- Sei test tecnici dedicati: fit dei fold isolato, selezione supervisionata locale, quattro colonne S2, inferenza da dati grezzi/colonne riordinate, conservazione dell'ibrida e assenza di ritardi nel pre-volo. I warning della prova con categoria sconosciuta sono attesi e non nascosti globalmente.
- CSV invariati; assenza di ID e righe di contenuto condivisi fra train e test.
- Roundtrip joblib e inferenza in un nuovo processo Python; prova con mancanti, zero nei rating e categoria nuova.
- Grafici verificati anche come immagini: 47 output PNG, 22 grafici Plotly mantenuti. Dimensione da 116.8 a 5.6 MB; nessuna sezione rimossa per ridurre il peso.

## Revisione e ricontrollo del 12 ottobre 2026

La revisione descrittiva ha corretto Online boarding con rating 0 (55,6% di soddisfatti), precisato le interpretazioni dell'EDA e aggiunto spiegazioni di algoritmi, iperparametri e sintesi dei confronti. Non cambia le feature, le griglie o la selezione dei modelli.

Sono stati ripetuti i sei test tecnici, il calcolo del T-test sul train e l'inferenza del modello esportato su tutte le 25.976 righe del test. Accuracy 0,9642747151 e ROC-AUC 0,9953694073 coincidono con il riepilogo. Per il notebook sono stati verificati struttura, assenza di errori salvati, coerenza della copia senza output e conservazione dei risultati.

È stata rieseguita soltanto la cella 108 sul bilanciamento, per aggiornare tre messaggi e il margine del grafico. Le altre 59 celle di codice e i rispettivi output sono identici alla versione precedente. Nessun nuovo addestramento completo o nuova installazione dell'intero ambiente è dichiarato. La [verifica descrittiva](evidenze/revisione_2026-10-12/verifica_descrittiva.json) identifica la versione pubblicata e distingue questo intervento dall'esecuzione integrale.

## Risultati

| Esperimento | Modello scelto tramite CV | Accuracy CV | Accuracy test | ROC-AUC test |
| --- | --- | ---: | ---: | ---: |
| S1 | Gradient Boosting | 96.3707% | 96.4275% | 0.99537 |
| S2 | Gradient Boosting | 85.4577% | 85.3326% | 0.93228 |
| Ibrida | Gradient Boosting | 86.7108% | 86.5838% | 0.93610 |
| Senza rating | Gradient Boosting | 80.6042% | 80.2510% | 0.86880 |
| Pre-volo | Gradient Boosting | 80.1538% | 79.4772% | 0.85865 |

Il modello principale è **S1 - Gradient Boosting**, scelto prima del confronto finale sul test. Baseline maggioritaria: **56.10%**. Tutti i risultati dei modelli ottimizzati sono nel recap e nei CSV, compresi quelli non selezionati come principali.

La top 4 differisce da quella riportata nella prima revisione perché il vecchio calcolo manteneva gli zeri dei rating dentro il T-test. Ora applico coerentemente la policy N/A prima del confronto statistico e dichiaro questa scelta; non scelgo manualmente una lista dopo aver visto l'accuracy.

## Limiti

Il test pubblico era già noto, la CV del tuning non è nested e la disponibilità temporale degli input resta da verificare in un contesto reale. Non sono dimostrati effetti causali, risparmi ambientali o prestazioni in produzione. Questi limiti sono riportati anche nel notebook.

## Ripetere i controlli tecnici

Dalla cartella di questo progetto, dopo aver installato `requirements.txt`:

```bash
python -m pip install pytest==8.4.2
python -m pytest evidenze/correzioni_2026-10-09/test_finale2_pipeline.py -q
```

I sei test verificano la pipeline su un sottoinsieme del train e non ripetono le griglie complete. `evidenze/correzioni_2026-10-09/verifica_finale.json` è un’evidenza storica del 9 ottobre: il suo hash del codice precede le modifiche ai messaggi e al margine del grafico. Documenta l'esecuzione integrale delle 60 celle, le 189 combinazioni di tuning e la verifica dell'export; `requirements_ambiente_completo.txt` registra anche le dipendenze transitive dell'ambiente usato.
