# Soddisfazione dei passeggeri aerei — Stefano Nocco

Analisi e classificazione del dataset Airline Passenger Satisfaction. Esecuzione completa del **9 ottobre 2026** e revisione descrittiva del **12 ottobre 2026**, mantenendo EDA, quattro algoritmi, griglie complete e approfondimenti originali.

- [Notebook completo con grafici e risultati](Progetto%20Finale%20Data%20Science%20di%20Stefano%20Nocco.ipynb): 139 celle, 60 celle di codice eseguite senza errori, circa 5,6 MB.
- [Copia senza output](versione_git/Progetto%20Finale%20Data%20Science%20di%20Stefano%20Nocco.ipynb): stesso testo e codice, per consultare le modifiche.
- [Recap tecnico](RECAP.md), [note metodologiche e controlli](NOTE_METODOLOGICHE.md), [risultati completi](risultati/riepilogo.json).
- [Pipeline di preprocessing](airline_pipeline.py), [dipendenze](requirements.txt), CSV originali `train.csv` e `test.csv`.

## Revisione descrittiva del 12 ottobre 2026

- Corretto il commento al rating 0 di Online boarding: **1.351 soddisfatti su 2.428 osservazioni, pari al 55,6%**.
- Distinte osservazioni e ipotesi nei commenti EDA, chiariti il significato della classe negativa e il confronto con la baseline.
- Aggiunte motivazioni della scelta degli algoritmi, spiegazioni degli iperparametri e sintesi dei ranking e dei risultati, con riferimenti alla documentazione scikit-learn.
- Aggiornati i messaggi sul bilanciamento e lo spazio per le etichette del relativo grafico; rieseguita soltanto quella cella.

Le altre 59 celle di codice e i loro output sono invariati. La struttura conserva 139 celle, 47 PNG e 22 grafici interattivi. Dati, pipeline, griglie e metriche restano quelli dell'esecuzione completa; il ricontrollo del 12 ottobre ha riconfermato le metriche del modello salvato tramite inferenza sull'intero test. [Verifica della revisione](evidenze/revisione_2026-10-12/verifica_descrittiva.json).

## Metodo e risultati

Il preprocessing e la selezione sono appresi dentro ogni fold di CV. La Strada 1 usa tutte le 22 variabili grezze; la Strada 2 usa esattamente quattro numeriche significative al Welch T-test. Conservo separatamente la selezione ibrida e i due confronti temporali: senza rating, e senza rating né ritardi effettivi.

| Esperimento | Modello scelto tramite CV | Accuracy CV | Accuracy test | ROC-AUC test |
| --- | --- | ---: | ---: | ---: |
| S1 | Gradient Boosting | 96.37% | 96.43% | 0.99537 |
| S2 | Gradient Boosting | 85.46% | 85.33% | 0.93228 |
| Ibrida | Gradient Boosting | 86.71% | 86.58% | 0.93610 |
| Senza rating | Gradient Boosting | 80.60% | 80.25% | 0.86880 |
| Pre-volo | Gradient Boosting | 80.15% | 79.48% | 0.85865 |

La scelta del modello deriva dalla cross-validation; il test serve al confronto finale. I risultati riguardano un **test pubblico già osservato**, non una nuova validazione esterna. La classe negativa comprende neutrali e insoddisfatti. Il dataset non dimostra causalità o benefici ambientali.

## Esecuzione

Python 3.11, notebook e CSV nella stessa cartella. Creare l'ambiente e il kernel:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --user --name finale2 --display-name "Finale 2 (Python 3.11)"
```

Aprire il notebook in Jupyter o VS Code, scegliere questo kernel e usare **Restart Kernel and Run All**. Su Windows l'attivazione è `.venv\Scripts\activate`. Per Colab sono riportate istruzioni anche nel notebook. Le griglie sono complete: 189 combinazioni, 945 fit nei cinque fold, 100 fit degli spot check e otto rifit finali. Il tempo dipende dall'hardware; `N_JOBS` limita il parallelismo senza ridurre la ricerca.

Il notebook scrive `airline_pipeline.py`, produce i CSV in `risultati/` e genera `airline_satisfaction_model.joblib`. Il modello binario e gli ZIP sono artefatti locali esclusi dal repository. Le prove di export includono dati grezzi, mancanti, categorie nuove e ricaricamento in un altro processo Python.

Per rigenerare i PNG dei grafici Plotly servono Kaleido e Chrome/Chromium; `plotly_get_chrome` permette di installare il renderer richiesto. Se manca, resta il formato interattivo. Il notebook pubblicato contiene già **47 output PNG e 22 grafici Plotly**: i PNG sono visibili senza Internet.

## Dati e fonti

I CSV contengono 103.904 righe nel train e 25.976 nel test; gli hash sono in [riepilogo.json](risultati/riepilogo.json). [Dataset indicato nel corso](https://drive.google.com/drive/folders/18MMXkE98uHDuWHDgXPpwD08Y7vyEnElk?usp=sharing) e [scheda del dataset](https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction).

Il [PDF di supporto](materiali_supporto/Analisi%20Esplorativa%20dei%20Dati%20di%20Soddisfazione%20dei%20Passeggeri.pdf) è un appunto storico: i risultati aggiornati e i grafici completi sono nel notebook.
