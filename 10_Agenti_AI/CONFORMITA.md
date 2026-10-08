# Confronto con la consegna Agenti AI

Fonte: [consegna ufficiale start2impact](https://talent.start2impact.it/corsi/agenti-ai/progetto/a46e2d4f-c641-4a2d-ab85-94c8e79708d8), acquisita il 7 ottobre 2026 in `00_STATO_MASTER/tracce_ufficiali_2026-10-07.json`.

| Requisito | Stato ed evidenza |
| --- | --- |
| Assistente personale email e calendario in n8n | 14 nodi, workflow pubblicato e attivo |
| LLM, buffer memory, Airtable, Gmail, Google Calendar | Collegati; chiamate reali e riuso della bozza verificati |
| Rubrica prima di email e creazione eventi | Prompt rafforzato dopo esecuzione 4; Airtable prima di Gmail in 10 e prima di Calendar in 11 |
| Data corrente e date relative | Espressione n8n verificata; evento del giorno successivo corretto in Europe/Rome |
| System prompt chiaro e strumenti spiegati | Regole per destinatari, bozza/invio, orari, durata, conferme e limiti |
| Telegram testo e voce | Entrambi verificati sul bot; vocale trascritto, bozza senza invio |
| Email inviata e ricevuta | Esecuzioni 4 e 10; ricezione in Outlook verificata e mostrata nella demo 10 |
| Evento visibile in calendario | Esecuzione 11 mostrata nel video: 9 ottobre 2026 ore 16:00-16:30, senza invitati |
| Video parlato con schermo, massimo 5 minuti | Video finale 2:30 con riprese reali e avatar/voce HeyGen dichiarati |
| Clic su tutti i nodi, richiesta email e richiesta evento nel video | Presenti e verificati nel video finale |
| PDF con introduzione e link video accessibile | PDF finale approfondito di 10 pagine, con link Loom accessibile senza login |
| Nome Progetto Agenti AI di Nome Cognome | Applicato al PDF definitivo |

## Evidenze e limiti

Il registro [prove_reali.json](evidenze/prove_reali.json) descrive nove esecuzioni con stato n8n `success`: una sola email e un solo evento creati. Sono verificati anche contatto assente, orario mancante e formato non supportato, senza ulteriori azioni Gmail/Calendar. Le dodici verifiche locali coprono il codice e le espressioni, non l'affidabilità del modello su ogni richiesta.

La prima email ha usato il contatto già consultato in un turno precedente. La revisione successiva del prompt richiede una lettura Airtable nella richiesta corrente. Questo comportamento è stato osservato nuovamente nelle esecuzioni 10 e 11, per email e calendario. Contatti omonimi, guasti dei servizi e inviti ad altre persone non sono stati testati online. Non sono dichiarati come superati.

La traccia indica il completamento del system prompt come soglia minima, ma richiede una demo con azioni reali. Le schermate e i log non sostituiscono il video. Nessun progetto è stato inviato alla piattaforma e non viene dichiarato superato.

## Materiali finali

[Video Loom](https://www.loom.com/share/6df5343a8a194c3f88e6df64413976ac) e PDF definitivo completati. Il registro storico delle 9 prove va letto insieme a [demo_video_2026-10-08.json](evidenze/demo_video_2026-10-08.json): totale 11 esecuzioni, 2 email e 2 eventi. Riproduzione senza login verificata in Edge InPrivate. Nessun invio alla piattaforma effettuato.
