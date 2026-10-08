# Configurare l’assistente Telegram

Importare `workflow.json` in n8n. L’export è inattivo e richiede la configurazione dei servizi.

1. Collegare il proprio bot Telegram ai nodi di ricezione, download dei vocali e risposta.
2. Nel nodo `Solo Stefano`, sostituire `INSERISCI_CHAT_ID` con l’identificativo della chat privata autorizzata.
3. Configurare il modello chat e la trascrizione con credenziali proprie o con il gateway disponibile nell’istanza n8n.
4. Collegare Gmail, Google Calendar e Airtable mediante le credenziali dell’istanza.
5. Scegliere base e tabella della rubrica Airtable. `contatti_demo.csv` mostra le colonne `Nome`, `Email`, `Telefono` e `Note`.
6. Selezionare il calendario e controllare il fuso `Europe/Rome`.
7. Provare testo, voce e ricerca di un contatto; controllare il destinatario e i dettagli prima di richiedere una vera email o un evento. Attivare il workflow quando la configurazione è verificata.

Il workflow distingue bozze e azioni tramite le istruzioni al modello. Le prove e i limiti di questo comportamento sono descritti nella [relazione](RELAZIONE.md).
