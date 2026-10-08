# Repository GitHub

Repository pubblica: [steno92py/master-data-science-start2impact](https://github.com/steno92py/master-data-science-start2impact).

## Archivio locale e copia versionata

La cartella del master conserva tutti gli originali, le versioni precedenti e i materiali privati. La copia di lavoro Git pubblicabile è separata, in `00_STATO_MASTER/github/master-data-science-start2impact/`. In questo modo i file storici voluminosi e le configurazioni locali rimangono disponibili sul Mac.

La repository contiene i file ammessi dalle regole `.gitignore`: progetti, notebook, documentazione, relazioni personali, dati di lavoro selezionati ed evidenze curate. Non contiene credenziali, feedback privati, tracce complete del corso, ZIP di consegna, video o modelli serializzati. La disponibilità pubblica del codice non attribuisce licenze ai dati o alle opere di terzi.

## Verifiche

Dalla radice del master oppure dalla copia Git:

```sh
python3 tools/verifica_consegne.py
python3 tools/verifica_archivio.py --output /tmp/master-verifica-git.json
```

Il primo comando verifica gli hash dei 16 elaborati pubblicati rispetto al catalogo. Il secondo applica le esclusioni Git, elenca i candidati e controlla dimensioni e alcuni formati di credenziali. Non stampa segreti e non invia dati in rete; non è una garanzia universale di assenza di informazioni riservate.

Le copie delle due prove finali in `versione_git/` mantengono celle, testo e codice originali, senza output né contatori. Gli originali completi restano sul Mac. I file approvati recuperati dalla piattaforma mantengono i byte originali.

## Aggiornamenti futuri

Modificare i file nella copia Git, controllare `git diff` e le verifiche prima di commit e push. Non copiare automaticamente `.env`, ZIP o intere cartelle di configurazione. Quando si cambia un elaborato approvato, conservare la consegna originale e creare una versione di lavoro distinta: gli hash del catalogo descrivono i file effettivamente valutati.

Per creare un nuovo export dell’archivio locale in una **cartella vuota**:

```sh
python3 tools/prepara_repository.py /tmp/master-export-nuovo
```

L’export copia solo la selezione ammessa e verifica l’identità di ogni copia; rifiuta destinazioni non vuote. Non cancella file, non sovrascrive la copia Git esistente e non esegue commit o push.

## Perimetro della pubblicazione

Il recupero e la pubblicazione documentano il lavoro presente. Non costituiscono una nuova consegna su start2impact né una nuova esecuzione dei modelli storici. Lo [stato del master](00_STATO_MASTER/STATO_MASTER.md) identifica le attività ancora aperte.
