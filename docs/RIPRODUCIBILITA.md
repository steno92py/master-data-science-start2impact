# Consultare e riprodurre i progetti

Il portfolio raccoglie lavori realizzati in ambienti diversi. Non esiste un unico file di dipendenze che riproduca fedelmente tutto il master. Per conservare il valore storico delle consegne, i notebook approvati non sono stati riscritti durante il recupero.

## Consultazione rapida

I PDF delle consegne, i workbook Excel e le esportazioni HTML di Machine Learning permettono di vedere i risultati senza avviare i programmi. I notebook con output conservano le esecuzioni storiche; la copia del notebook sul turismo virtuale ha gli output rimossi per dimensioni.

## Ambiente Python

Usare un ambiente virtuale per ogni progetto e lavorare su una copia degli elaborati valutati. Per aprire un notebook locale è sufficiente un ambiente con Jupyter; installare poi le librerie importate dal singolo notebook. Le versioni originali dei corsi storici non sono state ricostruite con un lockfile, quindi non è dichiarata una riproducibilità completa.

| Progetto | Requisiti e dati | Attenzione |
| --- | --- | --- |
| Python / Orizon | Python, Jupyter; libreria standard; esempio `test.json` | La consegna approvata e la copia adattata sono distinte. |
| File Organizer | Python, NumPy e librerie importate dal notebook | Lavora sui file e può spostarli: usare una cartella di prova. |
| Wine EDA | pandas, NumPy, Matplotlib, Seaborn, Plotly, Unidecode, NLTK, WordCloud | Ripristinare il CSV Wine Enthusiast; può essere necessario scaricare risorse NLTK. |
| Advanced Analytics | pandas, NumPy, SciPy, Matplotlib, scikit-learn, XGBoost | Notebook predisposto per Colab/Drive; ripristinare i due CSV nei percorsi documentati. |
| Titanic | Librerie importate dal notebook, dati e PDF in `progetto/` | Controllare eventuali sorgenti dati esterne prima di eseguire. |
| ML Advanced / Wine | scikit-learn e librerie importate dal notebook | Il dataset è quello fornito da scikit-learn. |
| Prova finale 1 | Notebook, CSV Travel e Tableau | Directory di lavoro: `17_Progetto_Finale/01_PROGETTO_1`, anche aprendo la copia in `versione_git/`. |

Gli elenchi descrivono le dipendenze osservate e i punti d’ingresso, non un ambiente reinstallato e certificato durante questa attività.

## Dashboard, workbook e dati esterni

Per Excel usare il workbook originale, così da conservare formule e pivot. I progetti Tableau possono richiedere di riconnettere i CSV se contengono percorsi storici di Windows. Il PDF Looker Studio conserva il collegamento al report; la disponibilità live dipende dal servizio e dalle relative fonti.

I due CSV Advanced Analytics sono stati recuperati dalle fonti collegate dal corso e conservati localmente. La [guida ai dataset](../12_Advanced_Analytics/dataset/README.md) contiene link, dimensioni e hash per ripristinarli. Il dataset Wine voluminoso, i modelli binari, gli ZIP e i video rimangono nell’archivio locale. Il repository non attribuisce licenze ai dati di terzi.


## Agenti AI e passeggeri aerei

- [Assistente Telegram](../15_Agenti_AI/GUIDA_SETUP.md): importare il workflow n8n e configurare chat, credenziali e servizi. L’export è inattivo e portabile.
- [EcoBot](../16_Agenti_AI_per_Data/ecobot/README.md): Python 3.11, dipendenze in `requirements.txt`, due CSV inclusi. Analisi e test locali non richiedono chiamate API; la chat richiede una propria configurazione.
- [Passeggeri aerei](../17_Progetto_Finale/02_PROGETTO_2/README.md): directory di lavoro `17_Progetto_Finale/02_PROGETTO_2`, dove si trovano `train.csv` e `test.csv`, anche aprendo il notebook in `versione_git/`. Consultare le note metodologiche prima di interpretare le metriche storiche.
