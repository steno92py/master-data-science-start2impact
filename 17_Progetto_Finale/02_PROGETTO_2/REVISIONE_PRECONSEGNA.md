# Seconda prova: cosa manca prima della consegna

Verifica del 7 ottobre 2026 sul notebook corrente di Stefano Nocco, di 135 celle. **Il progetto esiste ed è sostanzialmente sviluppato. Restano alcune correzioni metodologiche, l'esecuzione completa della versione corretta e il caricamento.** Non risulta necessario ricostruire il progetto da zero.

Questa è una revisione tecnica locale, non una valutazione del docente. La traccia ufficiale e lo stato dell'account non sono stati verificati: l'accesso alla piattaforma è stato negato dal browser. Il `RECAP.md` originale riporta la scelta di consegnare direttamente il notebook e l'obbligo di includere Random Forest e AdaBoost, ma queste indicazioni attendono confronto con la traccia.

## Controlli completati

Sono state eseguite in ordine **47 delle 57 celle di codice**, dall'inizio fino alla definizione delle metriche, in una directory temporanea con copie dei dataset. Caricamento, EDA, encoding, imputazione, scaling e selezione delle variabili sono terminati senza errori. Non sono stati rieseguiti cross-validation, addestramento, ricerca degli iperparametri, valutazione finale o esportazione del modello. Le metriche già presenti nel notebook restano quindi risultati salvati dall'esecuzione precedente.

| Controllo | Esito |
| --- | --- |
| Struttura del notebook | Valida; 135 celle, di cui 57 di codice |
| Training set | 103.904 righe, 25 colonne |
| Test set | 25.976 righe, 25 colonne |
| Duplicati esatti all'interno dei CSV | Nessuno |
| Identificativi condivisi fra train e test | Nessuno |
| Valori mancanti originali | Solo `Arrival Delay in Minutes`: 310 nel train, 83 nel test |
| Matrici preparate dal codice originale | 37 colonne, nessun valore mancante, stesso numero di righe dei CSV |
| Variabili della Strada 2 | `Online boarding`, `Inflight entertainment`, `Class_Business`, `Type of Travel_encoded` |

L'ambiente di verifica usa Python 3.11.14, pandas 2.2.3, NumPy 2.2.6, SciPy 1.15.3, scikit-learn 1.7.2 e Plotly 6.2.0. L'esito macchina (file nell’archivio locale) registra versioni, celle eseguite e hash dei file verificati. Non sono stati modificati notebook, dataset, recap o modelli originali; nessun oggetto pickle/joblib preesistente è stato deserializzato.

## Correzioni prioritarie

I numeri indicano la posizione della cella, **contata da 1**, non il contatore di esecuzione di Jupyter.

### 1. Correggere il modello chiamato “pre-volo”

**Dove:** sezione 5.2, celle 131–132; conclusione, cella 133.

Il modello usa `Departure Delay in Minutes` e `Arrival Delay in Minutes`. Il codice prende i ritardi dal dataset: non costruisce stime disponibili prima del volo. In particolare, il ritardo all'arrivo non è un'informazione osservabile prima del volo. L'accuracy salvata di **80,28% non dimostra quindi una capacità predittiva pre-volo**.

**Da fare:** per mantenere l'obiettivo pre-volo, escludere entrambi i ritardi effettivi, oltre ai rating, e rieseguire confronto e tuning. In alternativa, descrivere questa analisi come “modello senza rating, con dati operativi post-volo”, eliminando ogni promessa di uso pre-volo. Aggiornare le conclusioni e, nella versione revisionata, le spiegazioni del recap. Il confronto fra accuracy misura una differenza predittiva fra questi modelli, non l'effetto causale dell'esperienza a bordo.

### 2. Spostare preprocessing e selezione dentro la cross-validation

**Dove:** gestione degli zero e scaling, celle 101 e 105; selezione, cella 113; CV e tuning, celle 120–125 e 132.

Mediane, scaler e selezione delle variabili sono calcolati sull'intero training set prima di creare i fold. La selezione usa anche le etichette delle righe che poi diventano validazione. Nel primo fold, il preprocessing ha già visto tutte le **20.781 righe di validazione**: per esempio, la media di `Age` usata dallo scaler è 39,379706, mentre quella del solo sottoinsieme di addestramento del fold è 39,409995.

Questo riguarda la validazione interna: il controllo non ha rilevato identificativi condivisi fra i CSV e il codice applica al test trasformazioni apprese sul training set. Non è stata quantificata l'influenza dell'errore sulle metriche.

**Da fare:** racchiudere imputazione, encoding, scaling e selezione appresa dai dati in trasformatori e in una `Pipeline`, passata a `cross_val_score` e `GridSearchCV`. Ogni fold deve apprendere queste operazioni solo dalle proprie righe di addestramento. La feature selection può restare nell'EDA come analisi descrittiva, ma quella usata per valutare la Strada 2 deve essere appresa dentro ogni fold. [Documentazione scikit-learn sul data leakage](https://scikit-learn.org/stable/common_pitfalls.html).

### 3. Scegliere il modello usando la validazione

**Dove:** confronto finale, cella 128; persistenza, cella 135.

Il codice usa `comparison_df["Accuracy"].idxmax()` sui risultati del test per nominare il vincitore e raccomandarlo per il deployment. Inoltre, il salvataggio sceglie esplicitamente Gradient Boosting, invece di usare un riferimento al modello scelto.

**Da fare:** definire la metrica e il criterio di scelta sui risultati della CV, conservare i punteggi di tuning e collegare valutazione ed esportazione al modello scelto con quel criterio. È possibile mostrare un confronto descrittivo sul test, ma non usarlo per iterare su feature, iperparametri o vincitore. Il test è già stato consultato: nella revisione non andrà descritto come un nuovo campione mai osservato. [Documentazione scikit-learn sulla separazione fra selezione e valutazione](https://scikit-learn.org/stable/modules/cross_validation.html).

### 4. Rendere le conclusioni aderenti a ciò che i dati dimostrano

**Dove:** selezione, cella 113; conclusione, cella 133; appunti nel `RECAP.md` originale.

- **Rating zero:** l'importanza della relativa flag non dimostra che zero significhi “non applicabile”. Presentare questa interpretazione come ipotesi, cercare il dizionario della fonte e, se necessario, confrontare trattamenti alternativi mediante CV.
- **Class nella Strada 2:** il codice usa soltanto `Class_Business`, quindi unisce Eco ed Eco Plus. Non è una codifica completa a tre classi né un normale `drop_first`, che conserverebbe due colonne. Descrivere precisamente la variabile binaria oppure rivedere la codifica in base alla richiesta ufficiale sulle quattro feature.
- **Sostenibilità e interventi:** il dataset non contiene misure di emissioni, carburante o effetti di interventi. Le proposte aziendali possono essere ipotesi da sperimentare; il notebook non dimostra che ridurre frequenze o migliorare il boarding produca i benefici ambientali e di soddisfazione affermati. Verificare anche l'unità di `Flight Distance` prima di scrivere soglie in km.
- **Accuracy e varianza:** nel recap, “86% della varianza” va corretto: 86% di accuracy significa percentuale di classificazioni corrette, non varianza spiegata.

## Riproducibilità e confezione

- **Esecuzione finale:** dopo le correzioni, eseguire tutto da kernel pulito con una versione documentata delle dipendenze, rigenerare risultati e grafici e controllare la coerenza del testo. L'esecuzione parziale effettuata qui non certifica il notebook completo.
- **Compatibilità AdaBoost:** la cella 120 passa `algorithm='SAMME'`. Il parametro è presente nella versione 1.7.2 usata per il controllo, ma non nella firma corrente documentata da scikit-learn. Rimuovere il parametro ormai superfluo per le versioni correnti, oppure fissare e verificare un ambiente compatibile. [API ufficiale AdaBoostClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html).
- **Peso del notebook:** 116.773.057 byte, circa 116,8 MB. Gli output HTML occupano circa 109,1 MB e contengono ripetutamente la libreria Plotly. Configurare un renderer adatto alla modalità di consegna e verificare la visualizzazione dei grafici nel file finale. Non è stato verificato alcun limite di upload della piattaforma. [Renderer Plotly](https://plotly.com/python/renderers/).
- **Mutual Information:** esplicitare quali feature sono discrete: l'attuale chiamata su una matrice densa lascia il comportamento automatico e non identifica le colonne binarie/categoriche. Il ranking va poi ricontrollato.
- **Modello esportato, extra facoltativo:** l'esempio di inferenza parte da `X_test` già trasformato. L'artefatto non è una pipeline completa dai dati grezzi e non salva esplicitamente la mediana usata per imputare il ritardo all'arrivo. Se viene mantenuto come extra, completare e verificare l'inferenza da nuove righe grezze.

## Sequenza per arrivare alla consegna

1. Recuperare la traccia ufficiale e confermare modelli obbligatori, regole delle due strade e formato di consegna. Non è stata accertata la necessità di aggiungere una presentazione PDF.
2. Preparare una revisione del notebook che corregga validazione, scelta del modello e significato dell'analisi pre-volo, conservando l'originale.
3. Eseguire integralmente la revisione e riscrivere le conclusioni con i nuovi risultati.
4. Preparare il file finale, verificare che i grafici si aprano e che i dati siano accessibili secondo le modalità richieste, quindi caricare la seconda prova.
5. Controllare sulla piattaforma valutazione, eventuali richieste di correzione e condizioni per ottenere l'attestato.

Separatamente, per completare l'archivio locale restano da recuperare `supermarket_sales.csv` e `apple_quality.csv` del modulo Advanced Analytics. La loro assenza locale **non dimostra un modulo da rifare** e non blocca l'esecuzione di questa seconda prova.
