# Master Data Science & AI — Stefano Nocco

Portfolio del percorso **start2impact**, organizzato per corso ufficiale. Associazioni, consegne e materiali verificati sulle evidenze della piattaforma acquisite l’**8 ottobre 2026**; file ricontrollati dopo l’accorpamento.

**24 corsi e attività censiti, 17 cartelle con materiali, 19 elaborati.** I 16 elaborati approvati sono conservati con hash verificati. Agenti AI ed EcoBot sono pronti ma non inviati; la seconda prova finale richiede revisione. Il master non è indicato come concluso.

## Da dove iniziare

- [Agenti AI: cosa inviare](15_Agenti_AI/consegna/README.md) — PDF definitivo e video Loom.
- [Agenti AI per Data: consegna EcoBot](16_Agenti_AI_per_Data/consegna/README.md) — posizione del pacchetto locale.
- [Progetto finale](17_Progetto_Finale/README.md) — le due prove nello stesso corso.
- [Verifica completa dei corsi e criterio di accorpamento](docs/PERCORSO.md).

## Corsi con materiali

Ogni riga corrisponde a un corso ufficiale. I numeri ordinano le cartelle con materiali; non rappresentano un’identità comune fra corsi. I punteggi si riferiscono agli elaborati, non ai test teorici.

| Corso | Elaborati e stato | Cartella |
| --- | --- | --- |
| Introduzione alla Data Analytics | Superato · 200/200 | [01_Introduzione_Data_Analytics](01_Introduzione_Data_Analytics/README.md) |
| Introduzione alla Data Science e AI | Superato · 190/200 | [02_Introduzione_Data_Science_AI](02_Introduzione_Data_Science_AI/README.md) |
| Excel | Superato · 440/500 | [03_Excel](03_Excel/README.md) |
| Excel Advanced | Superato · 490/500 | [04_Excel_Advanced](04_Excel_Advanced/README.md) |
| SQL | Superato · 470/500 | [05_SQL](05_SQL/README.md) |
| Python | Superato · 500/500 | [06_Python](06_Python/README.md) |
| NumPy | Superato · 500/500 | [07_NumPy](07_NumPy/README.md) |
| Data Manipulation and Visualization | Superato · 500/500 | [08_Data_Manipulation_Visualization](08_Data_Manipulation_Visualization/README.md) |
| Data Studio | Superato · 500/500 | [09_Data_Studio](09_Data_Studio/README.md) |
| Data Visualization con Tableau | Superato · 500/500 | [10_Tableau](10_Tableau/README.md) |
| Google Analytics 4 | Due elaborati superati: 400/500 e 500/500 | [11_Google_Analytics_4](11_Google_Analytics_4/README.md) |
| Advanced Analytics | Superato · 500/500 | [12_Advanced_Analytics](12_Advanced_Analytics/README.md) |
| Machine Learning | Superato · 480/500 | [13_Machine_Learning](13_Machine_Learning/README.md) |
| Machine Learning Advanced | Superato · 480/500 | [14_Machine_Learning_Advanced](14_Machine_Learning_Advanced/README.md) |
| Agenti AI | Pronto; non inviato | [15_Agenti_AI](15_Agenti_AI/README.md) |
| Agenti AI per Data | Pronto; non inviato; invio bloccato dai prerequisiti in piattaforma | [16_Agenti_AI_per_Data](16_Agenti_AI_per_Data/README.md) |
| Progetto finale — Data Science, Analytics e AI | Prova 1: 1500/1500; prova 2 da revisionare e inviare | [17_Progetto_Finale](17_Progetto_Finale/README.md) |

## Organizzazione

Ogni corso raccoglie consegne, codice, dati, versioni precedenti e materiali recuperati che gli appartengono. Google Analytics 4 comprende due elaborati e il progetto finale due prove; rimangono sottocartelle dello stesso corso.

- `consegna/`: elaborati approvati o materiali pronti, identificati dal README del corso. Le precedenti cartelle `consegna_piattaforma/` sono confluite qui.
- `progetto/`, `dataset/`, `materiali/`: codice, dati e materiali di lavoro, dove presenti; EcoBot mantiene la propria cartella `ecobot/`.
- `archivio/` e `versioni_precedenti/`: originali importati e versioni storiche, locali ed escluse da Git.
- `00_STATO_MASTER/`: registri trasversali e copia Git del portfolio; gli ZIP dei progetti sono ora nei rispettivi corsi.
- `00_MATERIALI_MASTER/`: materiali generali del percorso.
- `98_ARCHIVIO_ORIGINALI/`: metadati e rimandi storici; i contenuti dei corsi sono stati ricollocati nei relativi archivi.

Le sette attività senza elaborati locali sono censite nell’[indice completo](docs/PERCORSO.md), senza creare cartelle vuote.

## Consultazione e verifiche

I PDF, workbook e HTML consentono di consultare molti risultati senza eseguire il codice. I notebook storici mantengono i propri contenuti e percorsi Colab/locali; seguire la [guida alla riproducibilità](docs/RIPRODUCIBILITA.md) e il README del corso prima di eseguirli. Le copie leggere delle prove finali sono in `versione_git/`.

```sh
python3 tools/verifica_corsi.py
python3 tools/verifica_consegne.py
python3 tools/verifica_archivio.py --output /tmp/master-verifica-git.json
```

[Provenienza](docs/PROVENIENZA.md) · [Catalogo degli elaborati e hash](docs/catalogo_progetti.json) · [Indice dei corsi](docs/indice_corsi.json) · [Stato del master](00_STATO_MASTER/STATO_MASTER.md) · [Gestione GitHub](GITHUB.md).

## Materiali e diritti

Portfolio personale, non materiale ufficiale di start2impact. Elaborati di Stefano Nocco; dati, software e materiali di terzi restano dei rispettivi autori. La pubblicazione non attribuisce una nuova licenza ai contenuti di terzi. Tracce integrali, correzioni private, credenziali, ZIP di consegna e configurazioni personali restano locali.

Gli output e i punteggi descrivono il lavoro storico. La verifica controlla appartenenza e integrità dei materiali; non costituisce una nuova esecuzione di tutti i modelli o una nuova consegna.
