# Verifica e accorpamento dei corsi

Verifica dell’associazione corso–materiali basata sulla pagina del master e sulle 22 sezioni progetto acquisite l’8 ottobre 2026. I registri integrali restano locali in `00_STATO_MASTER/download_master/`; l’[indice pubblico](indice_corsi.json) riporta i 24 corsi e attività, compresi quelli senza un elaborato locale. Non è stata effettuata una nuova consultazione della piattaforma durante questo riordino.

**17 corsi con materiali, 19 elaborati, 16 approvati e 3 non inviati.** L’accorpamento usa lo slug della pagina ufficiale del corso, confrontato con nome, contenuto e hash dei file, non il solo prefisso numerico o il software impiegato.

## Esito corso per corso

| Corso / attività | Collocazione unica | Verifica e accorpamento |
| --- | --- | --- |
| Prima di Iniziare | Nessuna cartella: nessun elaborato locale | Sezione introduttiva senza elaborato progettuale. |
| Introduzione alla Data Analytics | [01_Introduzione_Data_Analytics](../01_Introduzione_Data_Analytics/README.md) | PDF approvato e variante locale riuniti nel corso; variante conservata in archivio. |
| Introduzione alla Data Science e AI | [02_Introduzione_Data_Science_AI](../02_Introduzione_Data_Science_AI/README.md) | PDF approvato e precedente bocciato riuniti nel corso; versioni distinte. |
| AI e Prompt Engineering | Nessuna cartella: nessun elaborato locale | Test superato, 270/300; nessun elaborato da recuperare. |
| Costruisci una strategia dati | Nessuna cartella: nessun elaborato locale | Progetto di gruppo opzionale; nessun allegato inviato. |
| Excel | [03_Excel](../03_Excel/README.md) | Un workbook approvato; corso distinto da Excel Advanced. |
| Excel Advanced | [04_Excel_Advanced](../04_Excel_Advanced/README.md) | Un workbook approvato; corso distinto da Excel. |
| SQL | [05_SQL](../05_SQL/README.md) | PDF valutato, SQL e tre dataset nello stesso corso. |
| Python | [06_Python](../06_Python/README.md) | Consegna Orizon, copia di lavoro e originali MasterS2I riuniti; corso distinto da NumPy. |
| NumPy | [07_NumPy](../07_NumPy/README.md) | File Organizer appartiene a NumPy; notebook e script verificati contro lo ZIP approvato. |
| Data Manipulation and Visualization | [08_Data_Manipulation_Visualization](../08_Data_Manipulation_Visualization/README.md) | Wine Enthusiast EDA: consegna e varianti nello stesso corso. Distinto dal Wine di scikit-learn. |
| Data Studio | [09_Data_Studio](../09_Data_Studio/README.md) | Data Studio e Looker Studio sono qui lo stesso corso; un PDF approvato. |
| Data Visualization con Tableau | [10_Tableau](../10_Tableau/README.md) | Turismo globale, dati e originali MasterS2I riuniti. Turismo virtuale appartiene alla prova finale 1. |
| Google Analytics 4 | [11_Google_Analytics_4](../11_Google_Analytics_4/README.md) | Un corso con due elaborati: estrazione e strategia dati. Feedback privato conservato solo sul Mac. |
| Advanced Analytics | [12_Advanced_Analytics](../12_Advanced_Analytics/README.md) | Consegna approvata, copia locale, dataset e checkpoint recuperato riuniti. |
| Machine Learning | [13_Machine_Learning](../13_Machine_Learning/README.md) | Titanic appartiene a Machine Learning, anche se il nome dei file contiene ML_Advanced. |
| Machine Learning Advanced | [14_Machine_Learning_Advanced](../14_Machine_Learning_Advanced/README.md) | Wine di scikit-learn: consegna, varianti e originale MasterS2I riuniti. |
| Agenti AI | [15_Agenti_AI](../15_Agenti_AI/README.md) | Assistente Telegram: PDF in consegna, video in video e vecchi ZIP in archivio/pacchetti_preparatori. |
| Agenti AI per Data | [16_Agenti_AI_per_Data](../16_Agenti_AI_per_Data/README.md) | EcoBot: ZIP finale in consegna/pacchetto_riservato, vecchi ZIP e prototipo in archivio. Corso distinto da Agenti AI. |
| Realizza l’analisi completa di un dataset e genera previsioni sul futuro | [17_Progetto_Finale](../17_Progetto_Finale/README.md) | Un corso con due prove; originali MasterS2I riuniti negli archivi delle rispettive prove. |
| Trovare Lavoro | Nessuna cartella: nessun elaborato locale | Corso opzionale; nessun allegato progettuale da recuperare. |
| LinkedIn per il Personal Branding | Nessuna cartella: nessun elaborato locale | Corso opzionale; sezione progetto presente, nessun allegato inviato. |
| Networking | Nessuna cartella: nessun elaborato locale | Corso opzionale; nessun allegato progettuale da recuperare. |
| Public Speaking | Nessuna cartella: nessun elaborato locale | Corso opzionale; sezione progetto presente, nessun allegato inviato. |

## Associazioni che evitano equivoci

- **Data Studio / Looker Studio:** un solo corso e una sola consegna.
- **Google Analytics 4:** un solo corso, due elaborati conservati distinti.
- **Progetto finale:** un solo corso, due prove conservate distinte.
- **Excel / Excel Advanced**, **Python / NumPy**, **Machine Learning / Machine Learning Advanced** e **Agenti AI / Agenti AI per Data** hanno pagine ufficiali e valutazioni separate: ciascuno mantiene il proprio contenitore.
- Il progetto Titanic ha nomi di file contenenti `ML_Advanced`, ma appartiene a **Machine Learning**. L’EDA Wine Enthusiast appartiene a **Data Manipulation and Visualization**; il Wine di scikit-learn a **Machine Learning Advanced**.

## Conservazione e verifica

Le consegne recuperate sono confluite in `consegna/`; gli originali del vecchio archivio MasterS2I sono negli archivi dei rispettivi corsi. I pacchetti dei due progetti Agenti AI sono nei loro corsi, con la versione finale EcoBot distinta dagli ZIP preparatori. Nessun elaborato, dataset, video o pacchetto è stato riscritto o eliminato.

La [mappa degli spostamenti](../00_STATO_MASTER/riordino/accorpamento_corsi_2026-10-08.json) traduce i percorsi precedenti. I registri storici mantengono i nomi validi alla data delle rispettive operazioni; il catalogo e l’indice correnti usano quelli nuovi. I dettagli di integrità restano nel registro locale del riordino.

`python3 tools/verifica_corsi.py` controlla unicità delle cartelle, appartenenza di ogni elaborato, esistenza dei file e hash delle consegne approvate. `verifica_archivio.py` controlla separatamente la selezione pubblicabile.

## Attività ancora aperte

Agenti AI ed EcoBot risultano pronti, non inviati. La seconda prova finale richiede revisione metodologica. Per EcoBot e la seconda prova finale le evidenze della piattaforma segnalano prerequisiti per l’invio: il riordino non modifica tale stato. Il master risultava all’84%; non viene dichiarato concluso.
