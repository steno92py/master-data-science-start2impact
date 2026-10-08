# Agenti AI - Assistente personale Telegram

Progetto di Stefano Nocco, recuperato dal lavoro in `progetto_n8n_s2i` e verificato il 7 ottobre 2026.

**Workflow operativo e presentazione completata.** 11 esecuzioni reali, 2 email ricevute e 2 eventi creati. [Video finale su Loom](https://www.loom.com/share/6df5343a8a194c3f88e6df64413976ac) di **2:30**, con avatar personale HeyGen e riprese reali. [PDF di consegna](Progetto%20Agenti%20AI%20di%20Stefano%20Nocco.pdf) approfondito, 10 pagine.
Il [workflow n8n Cloud](https://stenopymeana.app.n8n.cloud/workflow/vjsParWnqMG15FS0) contiene 14 nodi, usa `Europe/Rome` e accetta soltanto la chat privata di Stefano. È stato configurato tramite MCP ufficiale con OAuth autorizzato. Non serve importarlo nuovamente o premere Execute workflow: è pubblicato e riceve i messaggi di [stenopy_bot](https://t.me/stenopy_bot).

## Risultati verificati

- Testo, ricerca in Airtable e bozza senza invio: esecuzioni 1-3.
- Invio della bozza mantenuta in memoria: esecuzione 4. Email ricevuta in Outlook; inizialmente nello spam, poi spostata in Posta in arrivo da Stefano.
- Evento personale: esecuzione 5, 8 ottobre 2026 dalle 15:00 alle 15:30, senza invitati. Consultazione Airtable prima di Google Calendar e riscontro visivo nel calendario.
- Nota vocale di Stefano: esecuzione 6, trascrizione e bozza corrette, nessun invio né evento.
- Contatto assente, orario mancante e sticker: esecuzioni 7-9, nessuna azione Gmail/Calendar; lo sticker riceve la risposta per formato non supportato senza chiamare il modello.

Il [registro delle prove](evidenze/prove_reali.json) contiene tempi, strumenti, output e limiti. Le 9 esecuzioni non costituiscono una misura statistica di affidabilità. Nell'invio 4 il modello ha riusato il contatto già letto nei turni precedenti: il prompt è stato poi rafforzato per richiedere una nuova lettura a ogni azione. La nuova lettura Airtable è verificata prima di Gmail nell’esecuzione 10 e prima di Calendar nell’11. Il [registro della demo](evidenze/demo_video_2026-10-08.json) integra le nove prove storiche.

## Account e portabilità

Telegram, Gmail, Google Calendar e Airtable OAuth sono collegati. Il modello `gpt-4o-mini` e la trascrizione utilizzano i Gateway credits n8n, verificati nelle chiamate reali. La chiave OpenAI del progetto EcoBot non è stata trasferita al workflow. L'eventuale esaurimento dei crediti richiederà un provider abilitato.

La [rubrica Airtable](https://airtable.com/appDywFtvczqawZkY/tbl4kdQVmhaEYPVkH) contiene il solo contatto di prova. `workflow.json` è l'export portabile, inattivo e senza credenziali o riferimenti agli account; `workflow_mcp.ts` è la sorgente SDK. La copia configurata, i segreti e i log integrali sono in `config_locale/`, esclusa dai pacchetti.

## File principali

- [GUIDA_SETUP.md](GUIDA_SETUP.md): funzionamento attuale e configurazione per una nuova istanza.
- [RELAZIONE.md](RELAZIONE.md): architettura, prove e limiti.
- [CONFORMITA.md](CONFORMITA.md): confronto con la traccia ufficiale.
- [SCENEGGIATURA_VIDEO.md](SCENEGGIATURA_VIDEO.md): testo e schermate per la registrazione.
- [evidenze/test_workflow.json](evidenze/test_workflow.json): 12 controlli locali con il motore n8n 2.37.0.
- originale_recuperato (file nell’archivio locale): i tre file iniziali conservati byte per byte; provenienza e hash in [recupero.json](recupero.json).

## Verifica tecnica

L'importazione e la riesportazione CLI sono riuscite nell'ambiente isolato `/tmp/s2i-n8n-verifica-20261007`. I 12 controlli locali verificano espressioni, collegamenti, testo/voce, date, invitati, input vuoti, escape Telegram e filtro della chat. Le prove cloud verificano separatamente i servizi reali.

Per rigenerare l'export: `python3 aggiorna_workflow.py`. Per i controlli locali: `N8N_REPO=/percorso/n8n node test_workflow.cjs`. L'export generato richiede la configurazione descritta nella guida; non sostituire con esso il workflow cloud già operativo.

## Stato della consegna

Video e PDF pronti. Il video mostra l’apertura dei 14 nodi, due richieste Telegram, email ricevuta ed evento del 9 ottobre 2026, 16:00-16:30 Europe/Rome. Accesso Loom verificato senza login. Avatar e voce sintetici sono dichiarati a schermo. Nessun caricamento su start2impact effettuato.

Il file finale è Progetto_Agenti_AI_Stefano_Nocco_3_MINUTI.mp4 (file nell’archivio locale), Full HD a 30 fps. Manifest di produzione (file nell’archivio locale), timeline (file nell’archivio locale) e script riproducibile (file nell’archivio locale). Il precedente montaggio Voicebox di 4:15 resta materiale preparatorio storico.

Non sono stati provati online omonimi, guasti dei servizi o inviti a terzi. Le 11 esecuzioni non misurano statisticamente l’affidabilità del modello.
