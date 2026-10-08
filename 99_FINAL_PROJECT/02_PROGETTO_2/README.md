# Seconda prova finale Machine Learning

**Stato aggiornato l’8 ottobre 2026: PREPARATA, da revisionare prima della consegna.**

Notebook corrente di 135 celle, dati e modelli conservati invariati. Le criticità già note sono in REVISIONE_PRECONSEGNA.md. La copia senza output in versione_git non sostituisce il file da consegnare.

[Copia leggera per Git](versione_git/) - codice e testo identici, senza output.


Progetto di Stefano Nocco sulla soddisfazione dei passeggeri aerei. **La prova è già svolta e resta da caricare**, secondo quanto indicato da Stefano il 7 ottobre 2026.

Il file corrente locale è `Stefano Nocco PROGETTO FINALE 2.ipynb`; la [copia consultabile su GitHub](versione_git/Stefano%20Nocco%20PROGETTO%20FINALE%202.ipynb) mantiene lo stesso testo e codice senza output, indicato come file da consegnare nel [RECAP originale](RECAP.md). Contiene 135 celle, di cui 57 di codice, tutte con un contatore di esecuzione; non contiene output di errore salvati. Questo controllo non sostituisce una nuova esecuzione completa o il confronto con la traccia ufficiale.

**Prima del caricamento:** la [revisione preconsegna](REVISIONE_PRECONSEGNA.md) ha individuato correzioni nella cross-validation, nella scelta del modello e nell'analisi chiamata “pre-volo”. Sono state rieseguite senza errori 47 celle di codice, fino alla preparazione dei dati e alla definizione delle metriche; addestramento e valutazione finale restano da rieseguire dopo le correzioni. Gli elaborati originali sono invariati.

## File correnti

| File | Funzione |
| --- | --- |
| `Stefano Nocco PROGETTO FINALE 2.ipynb` | Notebook corrente recuperato dalla cartella, 135 celle. |
| `train.csv` e `test.csv` | Dati letti dal notebook tramite percorsi relativi. |
| `airline_satisfaction_model.joblib` | Modello e informazioni di preprocessing salvati. Copiato senza caricarlo in Python. |
| `standard_scaler.pkl` | Scaler salvato; il recap lo descrive come residuo della precedente analisi. Copiato senza deserializzarlo. |
| `RECAP.md` | Appunti originali su obiettivi, metodo, risultati e modalità di consegna scelta. |
| `materiali_supporto/Analisi Esplorativa dei Dati di Soddisfazione dei Passeggeri.pdf` | Materiale di supporto all'analisi; il recap indica la consegna diretta del notebook. |

Aprire il notebook con questa cartella come directory di lavoro, mantenendo `train.csv` e `test.csv` accanto al notebook. Il codice, gli output e i modelli non sono stati modificati o rieseguiti durante il riordino.

## Versioni conservate

| Posizione | Contenuto |
| --- | --- |
| Cartella principale | Notebook corrente di 135 celle, coerente con il recap. |
| `versioni_precedenti/backup_cartella` | Backup di 123 celle. Il checkpoint della cartella sorgente era identico a questo backup. |
| `versioni_precedenti/zip_originale` | Tutti i 7 file estratti dallo ZIP, inclusi notebook di 111 celle e checkpoint distinto. |
| `versioni_precedenti/PROGETTO_FINALE_02_originale.zip` | Archivio originale integro, che conserva la versione di 111 celle. |
| `supporto_tecnico` | Manifesti Node e configurazione dell'editor archiviata senza attivarla. |

Il riferimento al backup nel recap descrive la vecchia disposizione: ora il file è in `versioni_precedenti/backup_cartella`. Le dipendenze `node_modules` sono conservate nella cartella originale `98_ARCHIVIO_ORIGINALI/MasterS2I_pythonProject/PROGETTO FINALE 02`, senza copiarle nel progetto Python.

La pagina della prova è stata verificata l’8 ottobre 2026: nessun allegato presente in Invio e nessuna approvazione. Il caricamento risulta bloccato da un messaggio sui prerequisiti. Prima della consegna occorre completare la revisione metodologica e verificare lo sblocco nella piattaforma.
