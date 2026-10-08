# Video finale - 2:30

Completato l’8 ottobre 2026. [Video Loom](https://www.loom.com/share/6df5343a8a194c3f88e6df64413976ac), accessibile senza login. Tre parti definitive HeyGen, nessuna generazione di prova. Tutti i 14 nodi sono aperti nelle riprese; la demo documenta le nuove esecuzioni 10 e 11.

Il copione (file nell’archivio locale) contiene 298 parole. La timeline effettiva (file nell’archivio locale) e il manifest (file nell’archivio locale) riportano durate misurate e controlli. Il video dura 150,135 secondi, entro il vincolo di tre minuti. La scaletta sottostante è storica e non descrive attività ancora da completare.

## Scaletta precedente, conservata come riferimento tecnico

I tempi 4:45 della versione seguente sono superati dal vincolo di tre minuti. Restano utili le indicazioni sui parametri da mostrare e le verifiche dei risultati.

Revisione dell’8 ottobre 2026 sui requisiti riportati da Stefano. Servono schermo e commento parlato, apertura di **tutti i 14 nodi**, richiesta email in Telegram e messaggio ricevuto, richiesta di aggiunta dello stesso appuntamento e verifica nel calendario. Limite assoluto: **5:00**.

Il montaggio precedente (file nell’archivio locale), di 4:15, contiene screenshot e uno schema ricostruito: resta materiale preparatorio. Questa scaletta descrive le nuove riprese, non attesta che siano già state effettuate. L’accesso all’editor n8n tramite browser è riuscito nella verifica dell’8 ottobre.

## Preparazione fuori registrazione

- Aprire il [workflow esistente](https://stenopymeana.app.n8n.cloud/workflow/vjsParWnqMG15FS0), la chat Telegram `stenopy_bot`, la [rubrica Airtable](https://airtable.com/appDywFtvczqawZkY/tbl4kdQVmhaEYPVkH), Outlook del destinatario e Google Calendar del mittente.
- Verificare che il workflow sia pubblicato; nella verifica dell’8 ottobre lo era. Non premere **Execute workflow**: i messaggi arrivano dal trigger di produzione.
- Espandere i gruppi se necessario, chiudere i pannelli superflui e rendere leggibili nomi e parametri. Ogni nodo va aperto, non soltanto indicato sul canvas. Non modificarne i parametri durante la presentazione.
- Mostrare il record `Contatto Prova S2I`, associato alla casella di prova di Stefano. Nel messaggio Telegram usare il nome senza incollare l’indirizzo: si vede così il motivo della ricerca in Airtable.
- Tenere pronta la casella del destinatario e il calendario sul **9 ottobre 2026**. L’appuntamento scelto è **16:00–16:30, Europe/Rome**, diverso dalla prova precedente. Se si registra dopo questa data, sostituirla coerentemente nei due messaggi e nella vista del calendario.
- Copiare in anticipo i due messaggi sotto. Limitare l’inquadratura alle applicazioni utili, con testo leggibile e credenziali chiuse. Provare audio e spiegazione dei nodi senza ripetere invii o creazioni.
- Con la propria voce, registrare il commento insieme allo schermo. Con la voce sintetica già usata, sincronizzare la narrazione alle riprese effettive e dichiararla brevemente nel video.

## 0:00–0:15 — Obiettivo e panoramica

**Schermo:** workflow completo, gruppi espansi.

**Con la propria voce:**

> Sono Stefano Nocco. Questo assistente riceve richieste da Telegram, cerca i contatti in Airtable e usa Gmail e Google Calendar. Mostro i nodi, poi invio un’email e aggiungo al calendario l’appuntamento descritto nel messaggio.

**Alternativa per voce sintetica:**

> Progetto Agenti AI di Stefano Nocco, con narrazione sintetica. L’assistente collega Telegram, rubrica Airtable, Gmail e Google Calendar. Vedremo i nodi, l’invio di un’email e la creazione dello stesso appuntamento nel calendario.

## 0:15–2:15 — Aprire ogni singolo nodo

Aprire il nodo, mostrare il parametro indicato e tornare al canvas. Le frasi spiegano **a cosa serve e perché è presente**. I tempi sono obiettivi, non durate già misurate su un nuovo video.

| Tempo | Nodo da aprire | Cosa mostrare | Frase da pronunciare |
| --- | --- | --- | --- |
| 0:15–0:22 | Telegram Trigger | Evento `message` | «Telegram Trigger avvia il flusso quando arriva un messaggio al bot: è l’ingresso dell’assistente.» |
| 0:22–0:29 | Solo Stefano | Controllo della chat privata nel codice | «Questo filtro accetta soltanto la mia chat privata, prima di consentire l’accesso al modello e agli strumenti.» |
| 0:29–0:37 | Switch | Uscite Testo, Audio, Fallback | «Lo Switch distingue testo, note vocali e formati non supportati, perché richiedono trattamenti diversi.» |
| 0:37–0:44 | Get Voice File | Operazione sul file Telegram e download | «Per un vocale, questo nodo scarica il file audio da Telegram e lo passa alla trascrizione.» |
| 0:44–0:51 | OpenAI | Transcribe Recording | «Questo nodo trascrive l’audio, rendendo una richiesta vocale utilizzabile come testo.» |
| 0:51–0:59 | Normalizza input | Campo `input_text` nel codice | «Normalizza input porta messaggio e trascrizione nello stesso campo. L’agente riceve così un input uniforme.» |
| 0:59–1:06 | Formato non supportato | Risposta Telegram | «Il ramo alternativo chiede testo o voce: evita di chiamare il modello per un formato non gestito.» |
| 1:06–1:24 | AI Agent | Prompt, system message e data in Europe/Rome | «L’agente interpreta la richiesta e sceglie gli strumenti. Il prompt richiede la rubrica prima delle azioni, distingue bozza e invio e chiede chiarimenti sui dati mancanti. La data corrente nel fuso di Roma aiuta a interpretare le date relative.» |
| 1:24–1:32 | OpenAI Chat Model | Modello `gpt-4o-mini` | «Questo è il modello linguistico usato dall’agente per interpretare le richieste e decidere quale strumento chiamare.» |
| 1:32–1:42 | Window Buffer Memory | Chiave per chat e finestra 10 | «La memoria conserva il contesto recente, separato per chat, con finestra dieci. Permette richieste successive sullo stesso appuntamento; non è un archivio permanente.» |
| 1:42–1:51 | rubrica contatti | Airtable, Search, base e tabella | «Airtable fornisce gli indirizzi associati ai nomi. L’agente deve cercare il contatto, evitando di inventarne l’email.» |
| 1:51–1:59 | invio email | Gmail, destinatario, oggetto e corpo | «Gmail esegue l’invio. Destinatario, oggetto e corpo sono compilati dall’agente in base alla richiesta e alla rubrica.» |
| 1:59–2:08 | calendario | Create, inizio, fine, titolo e invitati | «Google Calendar crea l’evento con titolo, inizio e fine. Il flusso gestisce anche invitati, se richiesti e trovati in rubrica.» |
| 2:08–2:15 | Telegram Send | Chat di destinazione e output | «Infine Telegram Send restituisce l’esito alla stessa chat. Il prompt richiede di confermare solo dopo il successo dello strumento.» |

## 2:15–3:35 — Richiesta Telegram e email ricevuta

**2:15–2:25:** mostrare il record `Contatto Prova S2I` in Airtable, poi la chat del bot.

> Il destinatario è già in rubrica. Gli scrivo usando soltanto il nome: il recupero dell’indirizzo spetta all’agente.

**Da incollare e inviare una sola volta in Telegram durante la ripresa:**

```text
Invia una sola email a Contatto Prova S2I. Oggetto: Demo Agenti AI - appuntamento 9 ottobre. Testo: Ciao, questo è un messaggio di prova per il progetto start2impact. L'appuntamento dimostrativo è il 9 ottobre 2026 dalle 16:00 alle 16:30, fuso Europe/Rome. Non è richiesta alcuna azione. Per ora invia soltanto l'email, senza creare eventi.
```

**2:25–2:55:** mostrare il messaggio inviato e la risposta effettiva del bot.

> La richiesta specifica destinatario, oggetto e testo, e autorizza soltanto l’invio dell’email. Il calendario sarà aggiornato con un secondo messaggio.

**2:55–3:35:** aprire l’email appena ricevuta nella casella del destinatario: oggetto, mittente, destinatario, data e contenuto leggibile.

> Ecco l’email ricevuta: oggetto e contenuto corrispondono alla richiesta, compresi giorno e orario dell’appuntamento. Questo riscontro verifica il risultato anche fuori da Telegram.

Pronunciare la frase solo dopo aver visto il messaggio. Controllare anche lo spam se necessario; non ripetere l’invio per la sola assenza in Posta in arrivo. L’ispezione dettagliata dell’esecuzione n8n può avvenire dopo le riprese; inserirla nel video solo se rimane tempo. Non dichiarare una nuova chiamata Airtable prima di Gmail finché il log non l’ha confermata: nella prima prova storica il modello aveva riusato il contatto dalla memoria.

## 3:35–4:35 — Aggiungere lo stesso appuntamento e mostrarlo

**3:35–3:55:** tornare alla stessa chat e inviare una sola volta:

```text
Aggiungi anche al mio calendario l'appuntamento descritto nell'email appena inviata: 9 ottobre 2026, dalle 16:00 alle 16:30, fuso Europe/Rome. Titolo: Demo Agenti AI - appuntamento. Descrizione: Appuntamento dimostrativo del progetto start2impact, comunicato a Contatto Prova S2I. Crea un solo evento personale, senza invitati e senza inviare altre email.
```

> Chiedo ora di aggiungere lo stesso appuntamento. Ripeto data e orari per rendere la richiesta precisa; l’evento è personale e non prevede invitati.

**3:55–4:35:** mostrare la risposta del bot e aprire l’evento appena creato in Google Calendar. Rendere visibili **titolo, 9 ottobre, 16:00–16:30 e descrizione**, con fuso di Roma coerente con la richiesta.

> Nel calendario vediamo lo stesso appuntamento dell’email, con titolo, data e durata di trenta minuti. L’evento non contiene invitati. La richiesta parte da Telegram e il risultato è verificabile nel servizio finale.

Descrivere l’esito soltanto se i dettagli corrispondono. Se il bot chiede un chiarimento, rispondere esplicitamente; se l’azione fallisce, non montare una conferma di successo sopra un risultato diverso.

## 4:35–4:45 — Chiusura

**Schermo:** evento aperto oppure panoramica n8n.

> La demo mostra il percorso completo: richiesta in Telegram, email ricevuta ed evento creato. Le istruzioni guidano il modello; per questo verifico sempre anche il risultato nei servizi collegati.

Restano **15 secondi di margine**. Dare priorità ai clic su tutti i nodi e ai risultati leggibili. Le prove aggiuntive di voce, sticker, contatto assente e i conteggi storici sono documentati nella relazione e non servono in questa scaletta.

## Controllo del video finito

- [ ] Durata misurata non superiore a 5:00; obiettivo 4:45.
- [ ] Audio comprensibile e sincronizzato con lo schermo.
- [ ] Tutti i 14 nodi aperti, compresi filtro, normalizzazione e ramo non supportato.
- [ ] Collegamenti e parametri leggibili; spiegazione del motivo dei passaggi.
- [ ] Contatto visibile in Airtable e richiesta Telegram per nome.
- [ ] Invio della richiesta email visibile, risposta del bot ed email ricevuta aperta.
- [ ] Seconda richiesta Telegram visibile ed evento aperto in Google Calendar.
- [ ] Date, orari e titolo coerenti fra richieste, email ed evento.
- [ ] Eventuali tagli eliminano attese o navigazione superflua senza alterare l’ordine delle azioni o far apparire riuscito un errore.
- [ ] Nuove esecuzioni verificate e annotate separatamente dalle nove prove storiche.

## Finalizzazione della consegna

Rendere il video accessibile tramite un link verificato anche senza autenticazione. Dopo aver controllato video e collegamento, dalla cartella del progetto:

```sh
../.venv-agenti-ai/bin/python crea_pdf.py --video-url 'https://URL-REALE-DEL-VIDEO'
```

Il comando inserisce il link nel PDF; non pubblica il video né ne verifica l’accessibilità. Conservare il PDF con suffisso BOZZA finché manca il video completo o il link verificato. I due messaggi sono da eseguire durante le nuove riprese: la scaletta da sola non ne attesta l’invio.
