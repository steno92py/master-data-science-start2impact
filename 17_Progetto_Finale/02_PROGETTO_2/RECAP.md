# RECAP — Progetto Finale: Airline Passenger Satisfaction

Documento aggiornato dopo l'esecuzione completa del 9 ottobre e la revisione descrittiva del 12 ottobre 2026. Mantengo analisi, approfondimenti e griglie del lavoro originale; integro la Strada 2 richiesta e correggo il metodo di validazione.

## 1. Contesto e obiettivo

Classifico `satisfied` contro `neutral or dissatisfied` per una compagnia aerea attenta al servizio e all'impatto ambientale. Il target negativo comprende anche i neutrali. Il dataset descrive survey: il modello completo serve soprattutto a una lettura post-volo, non a prevedere da informazioni già tutte note alla prenotazione.

Il [notebook completo](Progetto%20Finale%20Data%20Science%20di%20Stefano%20Nocco.ipynb) contiene codice, grafici e risultati della nuova esecuzione. Il PDF nella cartella di supporto resta un appunto storico.

## 2. Dataset

Mantengo `train.csv` (103.904 righe) e `test.csv` (25.976 righe), già separati dalla fonte. Le 22 feature comprendono sei dati demografici/di contesto, due ritardi effettivi e 14 rating. ID, indice e target non entrano nei predittori.

Arrival Delay ha 310 mancanti nel train e 83 nel test. Non ci sono duplicati di contenuto né ID condivisi fra i due file. Gli hash dei CSV sono invariati. L'unità di Flight Distance non è specificata nella scheda consultata: non la chiamo km o miglia.

Il test era già stato osservato nel progetto originale e nella revisione: non lo presento come campione nuovo. Nella nuova esecuzione fisso modelli e parametri sul train prima di valutarli sul test.

## 3. Decisioni metodologiche

### 3.1 Preprocessing e validazione

L'EDA conserva le dimostrazioni di imputazione, encoding e scaling sull'intero train. I modelli ripartono invece dai dati grezzi: `Pipeline(select, prepare, model)` apprende tutte le trasformazioni all'interno dei fold. Non uso gli oggetti già fittati nell'EDA per la cross-validation.

### 3.2 Outlier e scaling

Conservo gli estremi plausibili senza eliminare righe automaticamente. RobustScaler sui due ritardi; StandardScaler su Age, Flight Distance e 14 rating. Lo scaling non elimina gli outlier né rende normali le distribuzioni. Per gli alberi non è necessario; permette una preparazione comune alla baseline lineare.

### 3.3 Zeri nei rating

La scheda Kaggle documenta `0 = Not Applicable` per il Wi-Fi. Per gli altri rating applico la stessa policy come ipotesi dichiarata, da confermare con il dizionario completo. Nella Strada 1 separo gli zeri in flag e imputo i rating con la mediana dei valori 1–5 del training del fold. Le flag vengono create solo se quel fold contiene zeri. Sul train completo sono 13.

Nel T-test escludo mancanti e zeri dei rating, senza imputarli prima del confronto delle medie. Questo aggiorna anche il ranking: rispetto al vecchio T-test che includeva lo zero, il Wi-Fi entra nelle prime quattro variabili. L'importanza di una flag non dimostra il significato della codifica.

### 3.4 Categoriche

Mantengo la spiegazione di LabelEncoder nell'EDA. Nella pipeline uso OneHotEncoder con `drop='if_binary'`, che produce una colonna per ogni binaria e tre per Class sul train completo. Gestisco categorie non viste con `handle_unknown='ignore'`; il blocco tutto zero è un limite da monitorare, soprattutto per le binarie dove coincide con la categoria di riferimento.

### 3.5 Bilanciamento e metriche

Circa 57/43 nel train: non applico ricampionamento. Accuracy è la metrica principale richiesta; riporto anche precision, recall, F1, AUC, matrice di confusione e report per entrambe le classi. Classe positiva = satisfied. La baseline maggioritaria sul test è **56.10%**.

### 3.6 Multicollinearità

I due ritardi sono fortemente correlati (circa 0,97). Mantenerli non invalida automaticamente gli alberi, ma le importanze possono distribuirsi fra predittori correlati; non le interpreto come effetti indipendenti o causali.

### 3.7 Feature selection

Confronto Welch T-test, Chi-square/Cramér's V e Mutual Information. Nella MI dichiaro rating e colonne codificate come discreti; le quattro numeriche continue restano continue per l'estimatore. Le scale dei tre punteggi non sono confrontabili direttamente.

- **S1**: tutte le 22 variabili grezze, 37 colonne dopo la preparazione sul train completo.
- **S2**: quattro numeriche con `p < 0,05`, ordinate per `|t|`, selezionate di nuovo dentro ogni fold. Sul train completo: `Online boarding`, `Inflight entertainment`, `Inflight wifi service`, `Seat comfort`. Nessuna flag aggiuntiva: il classificatore riceve esattamente quattro colonne.
- **Ibrida aggiuntiva**: mantengo due numeriche da T-test e due categoriche da Chi-square/Cramér's V. Class viene ridotta a Business/resto, perdendo Eco/Eco Plus. Anche questa selezione viene appresa nei fold; non sostituisce S2.

Il T-test sui rating ordinali è un'approssimazione. La soglia è esplorativa e non corretta per test multipli; p-value pari a zero per underflow non significa probabilità esattamente nulla. La graduatoria univariata non garantisce la migliore combinazione predittiva.

### 3.8 Modelli e tuning

Conservo Logistic Regression, Random Forest, AdaBoost e Gradient Boosting, cinque fold stratificati con shuffle/seed 0, e tutte le griglie originali. In S1, S2 e Ibrida ottimizzo i migliori due algoritmi dello spot check; nei due controlli temporali ottimizzo il migliore, come nell'esperimento aggiuntivo originale.

Griglie: LR 8 combinazioni, RF 18, AdaBoost 12, GB 27. Questa esecuzione comprende 189 combinazioni di iperparametri, 945 fit di CV nelle griglie e 8 rifit sul train completo; 100 fit negli spot check (5 esperimenti × 4 algoritmi × 5 fold). Il miglior score GridSearch è interno alla ricerca e può essere ottimista; non ho svolto nested CV.

Il modello principale, scelto dalla CV fra S1 e S2, è **S1 - Gradient Boosting**. Importanze ed export seguono quella scelta. Il primo sul test nel confronto descrittivo è **S1 - Gradient Boosting**; nessun tuning viene rifatto dopo la lettura del test.

### 3.9 Disponibilità delle informazioni

- **Senza rating**: sei variabili di contesto più i due ritardi effettivi. Conservo l'analisi originale, chiamandola correttamente post-volo senza rating.
- **Pre-volo**: Age, Flight Distance, Gender, Customer Type, Type of Travel e Class; escludo rating e ritardi effettivi. Il dataset non documenta timestamp o disponibilità operativa: resta un confronto sul benchmark, non un modello già validato in produzione.

La differenza di accuracy fra questi esperimenti non è una stima dell'effetto causale dei servizi.

## 4. Risultati effettivamente ricalcolati

| Esperimento | Modello scelto tramite CV | Accuracy CV | Accuracy test | ROC-AUC test |
| --- | --- | ---: | ---: | ---: |
| S1 | Gradient Boosting | 96.3707% | 96.4275% | 0.99537 |
| S2 | Gradient Boosting | 85.4577% | 85.3326% | 0.93228 |
| Ibrida | Gradient Boosting | 86.7108% | 86.5838% | 0.93610 |
| Senza rating | Gradient Boosting | 80.6042% | 80.2510% | 0.86880 |
| Pre-volo | Gradient Boosting | 80.1538% | 79.4772% | 0.85865 |

Tutti i modelli ottimizzati, senza selezionare soltanto il miglior risultato sul test:

| Modello | Accuracy | Precision | Recall | F1 | ROC-AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| S1 - Random Forest | 0.96262 | 0.97238 | 0.94159 | 0.95674 | 0.99405 |
| S1 - Gradient Boosting | 0.96427 | 0.97206 | 0.94580 | 0.95875 | 0.99537 |
| S2 - Random Forest | 0.85367 | 0.82604 | 0.84451 | 0.83518 | 0.93209 |
| S2 - Gradient Boosting | 0.85333 | 0.82407 | 0.84662 | 0.83519 | 0.93228 |
| Ibrida - Random Forest | 0.86584 | 0.87505 | 0.81005 | 0.84130 | 0.93624 |
| Ibrida - Gradient Boosting | 0.86584 | 0.87505 | 0.81005 | 0.84130 | 0.93610 |
| Senza rating - Gradient Boosting | 0.80251 | 0.77083 | 0.78286 | 0.77680 | 0.86880 |
| Pre-volo - Gradient Boosting | 0.79477 | 0.77425 | 0.75164 | 0.76278 | 0.85865 |

Parametri CV completi, metriche e versioni sono in `risultati/riepilogo.json`; tutte le combinazioni tentate sono nei CSV `grid_*`. Le predizioni non derivano dagli artefatti vecchi: i modelli sono stati riaddestrati da zero.

## 5. Architettura del notebook

Conservo tutte le 135 posizioni originali, aggiornandone il contenuto dove necessario. Il notebook finale contiene 139 celle, di cui 60 di codice:

1. Introduzione, ambiente e fonti.
2. EDA completa delle 22 feature; mancanti, duplicati, outlier, encoding, zeri, scaling, bilanciamento, correlazioni e tre metodi di selezione.
3. Metriche e significato degli errori.
4. Due strade richieste, selezione ibrida e controlli temporali; spot check e griglie complete.
5. Confronto sul test, matrici, ROC, importanze e disponibilità delle informazioni.
6. Conclusioni, ipotesi aziendali, sostenibilità e limiti; riepilogo numerico generato dagli esperimenti.
7. Export della pipeline completa e verifica di inferenza, anche da un nuovo processo Python.

## 6. Limiti da ricordare

Il test pubblico è già noto; serve una valutazione su nuovi dati. Il modello completo usa la stessa survey del target. Il pre-volo è teorico finché non verifico la disponibilità reale delle sei variabili. Il significato dello zero è documentato soltanto esplicitamente per il Wi-Fi nella fonte consultata. T-test e importanze non dimostrano causalità. Non ho carburante, emissioni o esperimenti aziendali: le proposte ambientali e di servizio rimangono ipotesi.

## 7. File e versioni

- `Progetto Finale Data Science di Stefano Nocco.ipynb`: elaborato eseguito, con grafici e risultati.
- `airline_pipeline.py`: trasformazioni leggibili e importabili; il notebook lo rigenera.
- `airline_satisfaction_model.joblib`: Pipeline completa generata dalla sezione finale del notebook; il binario rimane escluso dal repository.
- `train.csv`, `test.csv`: dataset invariati.
- `requirements.txt`: ambiente Python riproducibile.
- `risultati/`: metriche, parametri, griglie e controlli dei fold.
- `versione_git/`: copia con codice e testo identici ma senza output.

Non occorre uno scaler isolato: le mediane e tutti gli scaler sono ora inclusi nella pipeline finale.

## 8. Come rieseguire e modificare

Creare l'ambiente descritto nel README, selezionare il kernel e avviare **Restart Kernel and Run All**. Le celle dipendono dalle precedenti; il modulo scritto all'inizio deve essere importabile anche per i processi paralleli. Le griglie sono complete: il tempo varia con hardware e parallelismo, senza una promessa di pochi minuti. `N_JOBS` controlla soltanto i processi, non riduce la ricerca.

Se cambio feature, preprocessing, griglie o selezione, rieseguo l'intero percorso e rigenero l'artefatto. Il riepilogo finale legge i risultati correnti. Non sostituisco i numeri manualmente.

Errori da riconoscere: CSV mancanti (controllare directory), librerie/versioni diverse (ricreare l'ambiente), modulo non trovato in inferenza (tenere `airline_pipeline.py` accanto al modello), renderer PNG indisponibile (installare Kaleido/Chrome oppure usare il formato Plotly). I PNG già salvati restano visibili.

## 9. Errori in cui non voglio ricadere

1. Non usare il preprocessing fittato su tutto il train dentro la CV.
2. Non sostituire la Strada 2 richiesta dal T-test con l'ibrida: posso presentarle entrambe.
3. Non chiamare pre-volo un modello che usa ritardi effettivi o rating della survey.
4. Non dire che l'accuracy misura varianza spiegata, o che un'associazione prova un intervento efficace.
5. Non descrivere il test già esaminato come nuovo e non ottimizzare parametri in base a quel risultato.
6. Non esportare un classificatore che richiede trasformazioni esterne non salvate.
7. Non fissare a mano il nome del vincitore in conclusioni, importanze ed export.

## 10. Se devo raccontare il lavoro

- **Perché il modello completo va bene?** Usa informazioni ricche della survey post-volo. La sua utilità è diversa da quella del confronto pre-volo.
- **Perché due strade?** Per confrontare tutte le variabili con quattro significative al T-test, come richiesto; l'ibrida è un approfondimento personale aggiuntivo.
- **Perché cambia la top 4?** Ora il T-test esclude gli zeri trattati come N/A: il Wi-Fi entra nel ranking. La regola resta dichiarata e ripetuta nei fold.
- **Come ho corretto il leakage?** Passo alla CV la Pipeline con dati grezzi; i controlli registrano le righe di fit di selezione e preprocessing in ogni fold.
- **Perché RF e AdaBoost?** Li richiede la traccia; confronto anche GB e una baseline lineare.
- **Cosa farei dopo?** Nuovi dati temporali, verifica del dizionario e disponibilità degli input, analisi degli errori per gruppo e prove aziendali controllate. Nessuna promessa di migliorare ambiente o soddisfazione senza misurarli.

## 11. Revisione descrittiva del 12 ottobre 2026

Il rating 0 di Online boarding comprende 1.351 soddisfatti su 2.428 osservazioni (55,6%): il commento è stato corretto per distinguerlo dai rating 1–3. L'EDA separa osservazioni e possibili spiegazioni aziendali, evitando di ricavare effetti causali o soglie operative dai grafici. Sono state ampliate le motivazioni del confronto fra algoritmi e le spiegazioni degli iperparametri, con sintesi dei ranking e delle differenze fra modelli.

La revisione interessa 36 celle di testo. Nella cella sul bilanciamento sono stati precisati tre messaggi e il margine verticale del grafico; è l'unica cella rieseguita. Ordine delle celle, calcoli, pipeline e risultati dei modelli sono conservati. Il ricontrollo dell'inferenza sul test completo conferma accuracy 96,43% e ROC-AUC 0,99537. Il test pubblico resta già noto: non si tratta di una nuova validazione esterna.
