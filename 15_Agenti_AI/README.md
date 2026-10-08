# Agenti AI — Assistente Telegram

Progetto di Stefano Nocco: assistente n8n per gestire email e appuntamenti da messaggi Telegram testuali o vocali. Usa Airtable come rubrica, Gmail per le email e Google Calendar per gli eventi.

- [Workflow portabile](workflow.json), inattivo e senza credenziali.
- [Guida di configurazione](GUIDA_SETUP.md) e [relazione tecnica](RELAZIONE.md).
- [Presentazione PDF](consegna/Progetto%20Agenti%20AI%20di%20Stefano%20Nocco.pdf).
- [Demo video di 2:30](https://www.loom.com/share/6df5343a8a194c3f88e6df64413976ac).
- [Prove reali](evidenze/prove_reali.json), [demo](evidenze/demo_video_2026-10-08.json) e [12 controlli locali](evidenze/test_workflow.json).

## Funzionamento

Il filtro della chat privata precede l’agente. Testo e trascrizione confluiscono nello stesso ingresso; la memoria conserva il contesto recente della chat. Il prompt richiede una nuova lettura della rubrica per ogni richiesta di email o evento e distingue le bozze dalle azioni.

Le istruzioni al modello non sono vincoli deterministici sugli strumenti. La relazione documenta prove effettuate e limiti osservati.

## Sorgenti e verifiche

`workflow_mcp.ts` conserva la rappresentazione del workflow. `contatti_demo.csv` è un esempio per la rubrica. `aggiorna_workflow.py` è lo strumento storico di trasformazione dell’export originale: richiede `originale_recuperato/workflow.json`, conservato nell’archivio locale. Il workflow pubblicato è già disponibile e non richiede questo passaggio.

`test_workflow.cjs` usa i moduli compilati di una copia locale di n8n 2.37.0, indicata da `N8N_REPO`:

```sh
N8N_REPO=/percorso/n8n node test_workflow.cjs
```

Il test verifica struttura, espressioni e filtro della chat senza attivare il workflow.
