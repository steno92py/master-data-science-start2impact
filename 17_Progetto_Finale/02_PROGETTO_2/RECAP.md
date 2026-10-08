# RECAP — Progetto Finale: Airline Passenger Satisfaction

Appunti sul progetto. Per interpretare metriche e conclusioni leggere le [note metodologiche](NOTE_METODOLOGICHE.md). Serve a ritrovare velocemente
contesto, scelte fatte, risultati e file presenti nella cartella, senza dover
rileggere tutto il notebook da capo.

---

## 1. Contesto del progetto

- **Master**: progetto finale, modulo di Machine Learning.
- **Brief**: compagnia aerea attenta a qualità del servizio e impatto ambientale.
  Vuole analizzare i dati di soddisfazione dei passeggeri per ottimizzare
  servizi in volo e a terra.
- **Task**: classificazione binaria della label `satisfaction`
  (`satisfied` vs `neutral or dissatisfied`).
---

## 2. Dataset

- Sorgente: dataset pubblico Airline Passenger Satisfaction (Kaggle).
- Pre-separato in `train.csv` (103.904 record) e `test.csv` (25.976 record),
  proporzione ~80/20, distribuzione del target coerente (~43% satisfied).
- 22 feature di input + 1 target:
  - **Demografiche/contesto**: Gender, Customer Type, Age, Type of Travel,
    Class, Flight Distance.
  - **Operative**: Departure Delay in Minutes, Arrival Delay in Minutes.
  - **Rating di servizio (0–5)**: Inflight wifi service,
    Departure/Arrival time convenient, Ease of Online booking, Gate location,
    Food and drink, Online boarding, Seat comfort, Inflight entertainment,
    On-board service, Leg room service, Baggage handling, Checkin service,
    Inflight service, Cleanliness.

Sul train ci sono 310 NaN su `Arrival Delay in Minutes` (0.30%) e 83 NaN sul test.
Imputati con la mediana del **training set**.

---

## 3. Decisioni metodologiche chiave (con il perché)

### 3.1 Split train/test
Mantengo la partizione pre-separata della sorgente. L'analisi esplorativa
è fatta SOLO su `train.csv`; `test.csv` è intoccato fino alla valutazione finale.

### 3.2 Outlier
- Age e Flight Distance: outlier marginali e plausibili → mantenuti.
- Departure/Arrival Delay: 13–14% di outlier IQR ma sono casi reali (un volo
  con 6 ore di ritardo conta). Mantenuti.
- Strategia di mitigazione: **RobustScaler** sui due delay,
  **StandardScaler** sulle altre 16 numeriche. Niente eliminazione di righe.

### 3.3 Valori "0" nei rating
Durante l'EDA ho notato che alcuni rating con valore `0` mostrano un tasso
di soddisfazione anomalo (es. Wi-Fi rating 0 → 99.7% satisfied).
Interpretazione: `0 = non applicabile / non usato`, non "pessimo".

Trattamento applicato:
1. Per ogni rating con almeno uno `0`, creo una flag binaria `<feature>_zeroflag`.
2. Sostituisco lo `0` con NaN, poi imputo con la mediana 1–5 del train.
3. Aggiungo le flag come colonne extra nel dataset modellabile.

**Validazione a posteriori**: `Inflight wifi service_zeroflag` finisce in top 5
della feature importance del Gradient Boosting (importanza 0.048). La scelta
era corretta.

### 3.4 Variabili categoriche
- Binarie (Gender, Customer Type, Type of Travel): LabelEncoder.
- Multi-classe (Class): One-Hot con 3 colonne (Business, Eco, Eco Plus).

### 3.5 Bilanciamento
Rapporto 57/43, ratio 1.31. Nessun resampling. Accuracy resta affidabile.

### 3.6 Multicollinearità
`Departure Delay` ↔ `Arrival Delay`: r = 0.97. Mantenute entrambe perché i
modelli vincenti sono tree-based (non risentono di collinearità). Andrebbero
deduplicate in un setup con modelli lineari.

### 3.7 Feature selection
Tre metodi complementari applicati al training set:
- **T-test** (numeriche): top 4 = Online boarding, Inflight entertainment,
  Seat comfort, On-board service.
- **Chi-square + Cramér's V** (categoriche): Class (V=0.505), Type of Travel
  (V=0.449), Customer Type (V=0.188), Gender (V=0.012).
- **Mutual Information** (tutte): conferma Online boarding, Wi-Fi, Class,
  Type of Travel come top.

**Selezione ibrida per la Strada 2**: top 2 numeriche dal T-test + top 2
categoriche dal Chi-square →
`['Online boarding', 'Inflight entertainment', 'Class_Business',
'Type of Travel_encoded']`.

Motivo: prendere solo le top 4 dal T-test escludeva proprio Class e
Type of Travel, che sono le variabili più discriminanti del dataset secondo
gli altri due test.

### 3.8 Metriche
Accuracy principale + Precision, Recall, F1, AUC-ROC sempre riportate.

### 3.9 Modelli
- **Spot-check con 5-fold StratifiedKFold** su 4 modelli: Logistic Regression,
  Random Forest, AdaBoost, Gradient Boosting.
- **Top 2 → GridSearchCV** con stessa CV (Random Forest e Gradient Boosting
  in entrambe le strade).
- **Valutazione finale sul test set** (mai usato prima).

### 3.10 Strada 1 vs Strada 2 vs Pre-volo
- **Strada 1**: tutte le 37 feature.
- **Strada 2**: 4 feature dalla selezione ibrida.
- **Modello operativo pre-volo**: SOLO variabili note prima del volo
  (Age, Customer Type, Type of Travel, Class, Flight Distance, Gender,
  ritardi). Niente rating post-volo.

Motivo del pre-volo: i rating sono raccolti POST-volo sulla stessa survey
della target. Il modello completo a 96% è uno scoring diagnostico, non un
predittore operativo. Il pre-volo è la baseline realistica.

---

## 4. Risultati numerici (test set)

| Modello                          | Accuracy | Precision | Recall | F1     | AUC-ROC |
|----------------------------------|----------|-----------|--------|--------|---------|
| **S1 – Gradient Boosting** (vincitore) | **0.9637** | 0.972     | 0.945  | 0.958  | **0.9954** |
| S1 – Random Forest               | 0.9624   | 0.972     | 0.941  | 0.957  | 0.9939  |
| S2 – Random Forest               | 0.866    | 0.875     | 0.810  | 0.841  | 0.936   |
| S2 – Gradient Boosting           | 0.866    | 0.875     | 0.810  | 0.841  | 0.936   |
| **Pre-volo – Gradient Boosting** | **0.8028** | 0.771     | 0.783  | 0.777  | 0.8667  |

**Iperparametri del modello vincitore (S1 – Gradient Boosting)**:
`learning_rate=0.1`, `max_depth=7`, `n_estimators=300`.

**Top 5 feature importance del vincitore**:
1. Online boarding (0.416)
2. Type of Travel_encoded (0.163)
3. Inflight wifi service (0.132)
4. Inflight wifi service_zeroflag (0.048)
5. Customer Type_encoded (0.043)

---

## 5. Architettura del notebook

```
# 0.0 Introduzione
# 1.0 Setup dell'Ambiente
  ## 1.1 Librerie Utili
  ## 1.2 Loading dei dati  (+ nota sullo split)
# 2.0 Exploratory Data Analysis
  ## 2.1 Valori Duplicati
  ## 2.2 Valori Mancanti
  ## 2.3 Esploriamo le Features
  ## 2.4 Features vs Target  (### 2.4.1 – 2.4.22, una sezione per feature)
  ## 2.5 Outliers
  ## 2.6 Analisi delle Variabili Categoriche
  ## 2.7 Gestione dello "0" nei rating come valore "non applicabile"
  ## 2.8 Standardizzazione delle Features
  ## 2.9 Bilanciamento del Dataset
  ## 2.10 Correlazione tra Features
  ## 2.11 Feature Selection
  ## 2.12 Pipeline Dati Unificato
# 3.0 Scelta della Metrica di Valutazione
# 4.0 Modelli, Training e Ottimizzazione
  ## 4.1 Strada 1 (tutte le features)
  ## 4.2 Strada 2 (4 feature, selezione ibrida)
# 5.0 Valutazione Finale e Confronto
  ## 5.1 Feature importance del modello vincitore
  ## 5.2 Modello operativo "pre-volo" (controllo leakage)
# 6.0 Conclusione
# 7.0 Persistenza del modello finale
```

Totale celle: 135 (78 markdown + 57 code).

---

## 6. Limiti dichiarati (sono già scritti in Conclusione, ma li ripeto qui)

1. **Leakage dei rating post-volo**: il modello al 96% usa rating raccolti
   dopo il volo, sulla stessa survey della target. Per uso predittivo reale
   pre-volo, riferirsi al modello operativo a 80%.
2. **Collinearità delay**: r=0.97 tra Departure e Arrival Delay; le tengo
   entrambe perché sono tree-based.
3. **Interpretazione dello "0"**: trattato come "non applicabile" — supportata
   dai dati ma non dal data dictionary ufficiale.

---

## 7. File nella cartella di progetto

- `versione_git/Stefano Nocco PROGETTO FINALE 2.ipynb` — notebook senza output.
- `train.csv` / `test.csv` — dataset originali richiesti dal notebook.
- `RECAP.md` — appunti sul progetto.
- `NOTE_METODOLOGICHE.md` — limiti delle analisi e delle metriche storiche.

---

## 8. Se in futuro devo rimettere mano al notebook

### Ordine di esecuzione obbligato
Il notebook va eseguito **dall'inizio in sequenza**. Diverse celle dipendono
da variabili definite nelle precedenti:
- `raw_data_train_clean`, `zero_flag_cols`, `median_imputation_map` →
  definiti in 2.7 e usati in 2.8 e nella Pipeline.
- `robust_scaler`, `standard_scaler` → definiti in 2.8 e usati nella Pipeline
  e nella persistenza.
- `top4_features` → definito in 2.11 e usato in Strada 2 e Pipeline.
- `cv`, `models_dict`, `param_grids` → definiti in 4.1 e usati anche in 5.2
  (pre-volo).

### Tempo di esecuzione
Tutto il notebook gira in ~5–10 minuti su una macchina decente. Il collo di
bottiglia sono i due GridSearchCV (RF e GB) che insieme valgono il 70% del
tempo. AdaBoost e Gradient Boosting sono single-thread su sklearn.

### Se cambio un iperparametro o aggiungo una feature
1. Modifico la cella interessata.
2. Eseguo da quella cella in poi (Run from cell).
3. Sezione 7.0: rigenera `airline_satisfaction_model.joblib` con i nuovi
   pesi/scaler.

### Errori di esecuzione tipici
- **`NameError` su `top4_features`** → vuol dire che la cella di
  feature selection (2.11) non è stata eseguita prima della Pipeline (2.12).
- **`KeyError: 'Class_Business'`** → la cella di feature selection o la
  pipeline non sono allineate; ricontrollare l'ordine.

---

## 9. Cose da NON rifare (errori in cui non voglio ricadere)

1. **Non scegliere le feature per la Strada 2 dal solo T-test**: esclude
   Class e Type of Travel, che sono le variabili più discriminanti. La
   selezione ibrida (T-test + Chi-square) è quella corretta.
2. **Non rimuovere fisicamente gli outlier dei delay**: si perde proprio
   l'informazione più predittiva. RobustScaler sì, dropna no.
3. **Non trattare i rating == 0 come "pessimo"**: si distorce lo scaling e
   le feature importance. Vanno trattati come "non applicabile".
4. **Non spacciare il modello al 96% come predittore pre-volo**: contiene
   rating post-volo (leakage strutturale). Per uso operativo reale, il
   benchmark è il modello pre-volo a 80%.
5. **Non scordare di applicare lo stesso preprocessing al test set**: in
   particolare le `_zeroflag` e gli scaler `RobustScaler`/`StandardScaler`
   vanno fittati sul train e solo `transform`-ati sul test.

---

## 10. Linee guida per un'eventuale presentazione orale

Se mi chiedono di difendere il progetto, le domande probabili sono:

- **"Perché 96% di accuracy?"** → Perché il modello usa rating post-volo.
  È uno scoring diagnostico. Il modello operativo pre-volo, più onesto per
  uso reale, è a 80%.
- **"Perché due strade?"** → Per confrontare un modello completo con uno
  parsimonioso. Mostra che 4 feature ben scelte spiegano già 86% della
  varianza (vs 96% con 37).
- **"Perché RandomForest e AdaBoost?"** → Richiesti dalla traccia. Ho aggiunto
  GradientBoosting come terzo ensemble e LogReg come baseline lineare.
- **"Cosa cambieresti?"** → (1) Eseguirei feature importance via SHAP per
  un'interpretazione locale (per singolo passeggero), non solo globale.
  (2) Testerei XGBoost/LightGBM, generalmente più performanti di GB nativo.
  (3) Costruirei una variabile sintetica per i delay invece di tenerli
  entrambi.

---

*Ultimo aggiornamento del recap: dopo l'esecuzione finale del notebook con
tutte le correzioni applicate (pulizia testuale, numerazione, feature
selection ibrida, pre-volo, persistenza, conclusione estesa).*
