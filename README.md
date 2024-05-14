## Analysis of Security Threats to an Android Device 

### Descrizione
Il progetto si concentra sull'implementazione di uno strumento per l'analisi automatizzata della sicurezza delle applicazioni Android. L'obiettivo principale è fornire all'utente una visione chiara dello stato di sicurezza del proprio dispositivo Android, attraverso l'analisi delle vulnerabilità presenti nelle applicazioni installate.

### Caratteristiche Principali
- Esegue automaticamente l'analisi di sicurezza delle applicazioni Android.
- Fornisce una visualizzazione dei risultati dell'analisi orientata anche all'utente meno esperto.
- Supporta l'analisi simultanea di più applicazioni.
- Genera report dettagliati in formato PDF e JSON.

### Entità Coinvolte
- **Server**: Il server ospita gli strumenti necessari per eseguire l'analisi statica delle applicazioni Android. Funge da piattaforma centralizzata in cui gli utenti possono inviare le richieste di analisi e ricevere i risultati.
- **Client**: Il client è l'interfaccia utilizzata dagli utenti per interagire con il server, inviando richieste di analisi e visualizzando i risultati ottenuti. Questo approccio elimina la necessità per l'utente di installare e configurare manualmente lo strumento di analisi di sicurezza sul proprio computer.

### Tecnologie Utilizzate
- MobSF: Strumento open source per l'analisi di sicurezza delle applicazioni mobili.
- PyQt: Libreria Python per lo sviluppo di interfacce utente.
- REST API: Utilizzate per l'automatizzazione dell'intero processo di analisi.

### Requisiti del Progetto
- Python 3.6 o versioni successive.
- Installazione di MobSF e relative dipendenze.
