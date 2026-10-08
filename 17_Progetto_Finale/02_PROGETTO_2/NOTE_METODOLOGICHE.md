# Note metodologiche

Revisione tecnica del notebook originale di Stefano Nocco, svolta il 7 ottobre 2026. Il notebook pubblicato conserva testo e codice originali.

## Verifica svolta

Sono state eseguite in una cartella temporanea 47 delle 57 celle di codice, fino alla definizione delle metriche. Caricamento, analisi esplorativa, encoding, imputazione, scaling e selezione sono terminati senza errori. Cross-validation, tuning e addestramento finale non sono stati rieseguiti in questa verifica; le metriche citate nel testo restano risultati storici.

I CSV contengono 103.904 e 25.976 righe, senza duplicati esatti né identificativi condivisi. I mancanti originali riguardano `Arrival Delay in Minutes`: 310 nel train, 83 nel test. L’ambiente verificato usava Python 3.11.14 e scikit-learn 1.7.2.

## Interpretazione dei risultati

- Il modello chiamato “pre-volo” usa i ritardi effettivi di partenza e arrivo. L’accuracy storica dell’80,28% non dimostra capacità predittiva prima del volo.
- Imputazione, scaling e selezione delle variabili sono appresi sull’intero training set prima della cross-validation. I fold di validazione influenzano quindi queste trasformazioni; l’impatto sulle metriche non è stato quantificato.
- Il vincitore è indicato confrontando l’accuracy sul test, mentre l’esportazione sceglie esplicitamente Gradient Boosting. Il test non rappresenta una valutazione indipendente dalla selezione del modello.
- L’interpretazione dei rating zero come “non applicabile” è un’ipotesi; `Class_Business` distingue Business dalle altre classi e unisce Eco ed Eco Plus.
- Il dataset non misura emissioni, consumi di carburante o effetti causali degli interventi. L’accuracy è la quota di classificazioni corrette, non varianza spiegata.
- Il modello serializzato storico usa dati già trasformati e non costituisce una pipeline completa dai dati grezzi. Le versioni delle dipendenze e il parametro AdaBoost `algorithm='SAMME'` richiedono attenzione alla compatibilità dell’ambiente.

Queste osservazioni qualificano anche i risultati e le interpretazioni conservati nel recap originale.
