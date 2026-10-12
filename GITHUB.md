# Repository del portfolio

[steno92py/master-data-science-start2impact](https://github.com/steno92py/master-data-science-start2impact) raccoglie 19 progetti personali di Stefano Nocco e i relativi materiali di lavoro.

## Verifiche

Dalla radice del repository:

```sh
python3 tools/verifica_corsi.py
python3 tools/verifica_consegne.py
python3 tools/verifica_archivio.py --output /tmp/master-verifica-git.json
```

I controlli verificano l’associazione fra corsi ed elaborati, i file e gli hash delle consegne approvate, la selezione pubblicabile, le dimensioni e alcuni formati di credenziali. La scansione automatica non è una garanzia universale di assenza di informazioni riservate.

## Aggiornamenti

Le cartelle pubblicabili sono elencate esplicitamente in `.gitignore`. Per aggiungere un progetto personale aggiornare i cataloghi e le regole di selezione, poi eseguire le verifiche e controllare `git diff`. Le configurazioni personali, i registri interni, gli archivi privati e i materiali di riferimento di altri studenti restano esclusi dalla pubblicazione.

Le consegne approvate conservano i byte originali: eventuali modifiche vanno effettuate in una copia di lavoro distinta. Gli hash del catalogo identificano i file valutati.

Per esportare il portfolio in una cartella nuova o vuota:

```sh
python3 tools/prepara_repository.py /tmp/portfolio-export
```

L’export applica la selezione pubblicabile e verifica ogni copia. Rifiuta destinazioni non vuote e non esegue commit o push.

## Revisioni descrittive dei notebook

Per aggiornare il progetto sui passeggeri, mantenere sincronizzati notebook completo, copia senza output, README, recap e note metodologiche. Il catalogo deve riportare dimensione e SHA-256 del notebook pubblicato. Distinguere la data dell'ultima esecuzione integrale da quella delle revisioni del testo e documentare eventuali celle rieseguite separatamente. Le evidenze storiche conservano la loro data e i loro hash; la revisione del 12 ottobre 2026 è identificata da una verifica dedicata.
