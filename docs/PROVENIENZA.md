# Provenienza e integrità degli elaborati

Verifica eseguita l’8 ottobre 2026 sulle pagine personali del master start2impact. Il [catalogo](catalogo_progetti.json) distingue l’esito del progetto dal risultato del test teorico e contiene nome della consegna, data, dimensione e SHA-256.

## Metodo di recupero

Sono state consultate 22 sezioni progetto, comprese le due consegne di Google Analytics 4, le due prove finali e le attività opzionali. Per i 16 elaborati indicati come **Superato** è stato scaricato l’allegato dell’invio associato alla correzione. Ogni allegato è stato confrontato con l’archivio locale tramite SHA-256.

Otto allegati di consegna non erano presenti nella stessa versione: Excel, Looker Studio, i due progetti GA4, Introduzione alla Data Analysis, Advanced Analytics, lo ZIP Machine Learning e il PDF della prova finale 1. È stato recuperato anche un workbook GA4 annotato dal docente, conservato solo localmente. Gli altri otto allegati coincidono con file già presenti; tre copie archiviate sono state rese facilmente consultabili in `consegna_piattaforma/`.

Non sono stati inviati progetti, eseguiti test didattici o modificati gli elaborati valutati. Le schermate integrali della piattaforma e i feedback privati restano nei registri locali, esclusi dal repository.

## Differenze che contano

| Progetto | Risultato del confronto |
| --- | --- |
| Introduzione Data Analysis | Il PDF approvato è di 30 pagine, circa 2,4 MB. La presentazione locale da circa 36 MB è una variante, conservata sul Mac. |
| Excel Advanced | Il file locale con suffisso `2` è identico alla consegna ufficiale senza suffisso. |
| Python / Orizon | La copia approvata era nell’archivio storico. La copia in `progetto/` differisce nel codice. Entrambe conservano 30 celle. |
| Wine EDA | La copia approvata era tra i file recuperati da Kaggle. La copia locale ha modifiche, incluso il percorso dei dati; entrambe hanno 191 celle. |
| Tableau | `Correzioni Tableau.pdf` è la presentazione inviata dall’autore e approvata, non la correzione privata del docente. |
| Advanced Analytics | Le 109 celle di testo e codice coincidono; il file scaricato differisce dalla copia locale nei metadati/output. |
| File Organizer | Codice, notebook ed esempi utili coincidono con i membri dello ZIP approvato. Il checkpoint automatico non è proposto come versione corrente. |
| Machine Learning / Advanced | Tutti i file utili estratti coincidono con i membri dei rispettivi ZIP approvati. |
| Prova finale 1 | Recuperato il PDF realmente inviato il 13 ottobre 2025; correzione del 19 ottobre 2025, 1500/1500. Notebook locale e Tableau restano materiali di lavoro collegati. |

## Originali e copie per Git

Gli originali delle prove finali hanno dimensioni elevate perché contengono tutti gli output. Sono rimasti invariati sul Mac. Le copie in `versione_git/` rimuovono soltanto output e contatori di esecuzione; tipo, ordine e sorgente delle celle coincidono con gli originali. La prima ha 125 celle, la seconda 135.

Gli hash nel catalogo si riferiscono al **file effettivamente scaricato**. Per le consegne ZIP l’hash identifica il pacchetto locale; `artifact_path` indirizza invece al notebook estratto e verificato, pubblicato su GitHub. Non va quindi confrontato l’hash dello ZIP con quello del notebook.

## Limiti della verifica

Un progetto superato rappresenta una valutazione didattica storica, non una certificazione del software in produzione. La verifica del recupero controlla identità dei file, stato della piattaforma e struttura dell’archivio. Le dipendenze e tutti i modelli storici non sono stati nuovamente installati o addestrati. I progetti Agenti AI, EcoBot e la seconda prova finale hanno le proprie evidenze e pendenze documentate separatamente.

## Collocazione corrente

L’accorpamento successivo ha riunito i materiali per corso ufficiale. Le cartelle `consegna_piattaforma/` sono confluite in `consegna/`, senza cambiare i byte degli elaborati. Gli originali importati sono negli archivi dei rispettivi corsi. I registri di recupero restano storici; il catalogo corrente e la [mappa degli spostamenti](../00_STATO_MASTER/riordino/accorpamento_corsi_2026-10-08.json) indicano i percorsi attuali.
