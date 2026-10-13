# Come consultare il portfolio

Il portfolio raccoglie **19 progetti in 17 cartelle di corso**. Per orientarsi su GitHub partire dal [README](../README.md) o dall’[indice dei progetti](PERCORSO.md). Dopo aver scaricato o clonato il repository, aprire [INDICE_PORTFOLIO.html](../INDICE_PORTFOLIO.html) nel browser: la ricerca funziona offline per nome, percorso, corso e tipo di materiale.

## Dove trovare i file

| Percorso | Contenuto |
| --- | --- |
| `01_…` → `17_…` | Corsi, in ordine di percorso; ciascuno ha un README con i file principali. |
| `consegna/` | Elaborati consultabili; il README del corso ne chiarisce provenienza e versione. |
| `progetto/` | Notebook, script e materiali di lavoro, dove presenti. |
| `ecobot/` | Progetto Agenti AI per Data, con le istruzioni di avvio. |
| `dataset/` o `data/` | Dati disponibili nel repository e indicazioni sulle fonti. Alcuni notebook mantengono i dati accanto al codice. |
| `versione_git/` | Copie dei notebook finali senza output, per consultare testo e codice. |
| `evidenze/` | Risultati tecnici e verifiche selezionati per la pubblicazione. |
| `docs/` | Cataloghi, provenienza, riproducibilità e questa guida. |
| `tools/` | Strumenti per verificare, esportare e indicizzare il portfolio. |

I progetti finali mantengono notebook e dati nelle rispettive cartelle principali. Per NumPy, Machine Learning e Machine Learning Advanced, i file estratti dagli elaborati originali sono in `progetto/`: il catalogo e i README puntano al file corretto.

## Corsi con più elaborati

Google Analytics 4 comprende estrazione e strategia dati. Progetto finale comprende turismo virtuale e soddisfazione dei passeggeri aerei. Titanic appartiene a Machine Learning anche se il nome del notebook contiene `ML_Advanced`; il Wine di Machine Learning Advanced è distinto dalla Wine EDA di Data Manipulation and Visualization.

## Versioni e riproduzione

I README identificano le versioni pubblicate e le date delle verifiche. I file con output permettono di leggere i risultati senza rieseguire i modelli; le copie senza output sono raccolte separatamente nell’indice. Prima di eseguire un progetto consultare la [guida alla riproducibilità](RIPRODUCIBILITA.md) e le sue dipendenze.

Il repository è la selezione pubblica del lavoro personale. Backup, registri amministrativi e configurazioni riservate appartengono all’archivio locale e non vengono importati nell’indice pubblico.

Per aggiornare l’indice dalla radice del repository:

```sh
python3 tools/genera_indice_portfolio.py
```

Il comando applica le stesse regole di selezione usate dai [controlli del repository](../GITHUB.md) e non modifica gli elaborati.
