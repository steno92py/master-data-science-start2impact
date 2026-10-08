# Configurazione e prove

## Istanza di Stefano già operativa

Il [workflow](https://stenopymeana.app.n8n.cloud/workflow/vjsParWnqMG15FS0) è attivo. Scrivere o inviare una nota vocale a [stenopy_bot](https://t.me/stenopy_bot); non occorre premere Execute workflow. È ammessa soltanto la chat privata verificata di Stefano.

- Gmail e Calendar: `stefano.nocco.meana@gmail.com`.
- Destinatario delle prove: `Contatto Prova S2I`, `stefano.nocco@outlook.it`.
- Airtable: base `Agenti AI - Rubrica Stefano`, tabella `Contatti`; OAuth collegato. Il PAT locale, verificato separatamente, non è usato dal workflow.
- OpenAI: chat `gpt-4o-mini` e trascrizione mediante Gateway credits n8n. La chiave locale EcoBot non è stata copiata.
- Fuso: `Europe/Rome`; evento personale senza invitati già verificato.

Le credenziali sono conservate in n8n; copia configurata e log sono in `config_locale/`, esclusa dai pacchetti. Non importare l'export portabile sopra al workflow operativo: i suoi riferimenti agli account sono intenzionalmente vuoti.

## Configurazione su una nuova istanza

Importare `workflow.json`, inizialmente inattivo, e associare:

| Credenziale | Nodi |
| --- | --- |
| Telegram Bot API | Telegram Trigger, Get Voice File, Telegram Send, Formato non supportato |
| OpenAI API o Gateway credits disponibili | OpenAI Chat Model, OpenAI (trascrizione) |
| Gmail OAuth2 | invio email |
| Google Calendar OAuth2 | calendario |
| Airtable OAuth2 | rubrica contatti |

Nel nodo `Solo Stefano`, sostituire `INSERISCI_CHAT_ID` con l'ID della propria chat privata. Il valore non configurato genera un errore esplicito; altre chat e gruppi vengono esclusi. Creare una tabella Airtable con `Nome`, `Email`, `Telefono`, `Note`, concedere lettura e selezionare base/tabella. Per usare un PAT selezionare l'autenticazione corrispondente nel nodo e una credenziale con accesso alla base. Il CSV portabile contiene esempi fittizi, da sostituire con un destinatario di prova autorizzato.

Selezionare il calendario di destinazione. Pubblicare soltanto dopo avere verificato chat, credenziali e risorse. Il trigger Telegram richiede un endpoint HTTPS raggiungibile; l'istanza cloud lo fornisce. Non collegare contemporaneamente un secondo trigger allo stesso bot, perché il webhook è unico.

## Esiti delle prove del 7 ottobre 2026

| Caso | Esecuzione | Esito |
| --- | --- | --- |
| Avvio | 1 | Risposta Telegram ricevuta |
| Rubrica | 2 | Contatto di prova trovato |
| Bozza testo | 3 | Nessuna chiamata Gmail/Calendar |
| Invio e memoria | 4 | Una email ricevuta; contatto riusato dalla memoria |
| Calendario | 5 | Rubrica prima del tool; 8 ottobre, 15:00-15:30, nessun invitato |
| Bozza voce | 6 | Trascrizione e bozza corrette; nessun invio |
| Contatto assente | 7 | Assenza segnalata, nessun invio |
| Orario mancante | 8 | Domanda di chiarimento, nessun evento |
| Sticker | 9 | Fallback testo/nota vocale, senza modello |
| Omonimi, errore servizio, invitati | - | Non eseguiti online |

Il prompt è stato rafforzato dopo l'esecuzione 4 per richiedere una nuova lettura della rubrica a ogni azione, anche con contatto in memoria. Verificato nelle esecuzioni 10 e 11 dell’8 ottobre: Airtable precede rispettivamente Gmail e Calendar. Per eventuali prove di errore usare un ambiente isolato, senza revocare credenziali personali. Non ripetere automaticamente operazioni con esito incerto.

## Prove conservate

`evidenze/prove_reali.json` contiene risultati e tempi. Le immagini mostrano email ricevuta, evento nel calendario e bozza vocale. L'email è inizialmente finita nello spam: Stefano l'ha spostata in Posta in arrivo. Il footer automatico n8n è presente nel corpo. La memoria non garantisce persistenza attraverso riavvii.

## Riferimenti tecnici

- [n8n: download file Telegram](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.telegram/file-operations/).
- [OpenAI: gpt-4o-mini](https://developers.openai.com/api/docs/models/gpt-4o-mini).
- Contratti dei parametri ed espressioni verificati sul codice n8n 2.37.0 già presente sul Mac; integrazioni verificate dalle esecuzioni cloud.
