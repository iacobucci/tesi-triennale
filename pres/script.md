# 0

buongiorno a tutti sono valerio iacobucci

e presento la mia tesi di laurea in tecnologie web t con il professor bellavista

dal titolo sviluppo e analisi delle prestazioni di applicazioni web **nuxt-based** in cloud aws

# 15

gli obiettivi di questa tesi sono stati quello di allestire un **ambiente sviluppo** per applicazioni web mirato a migliorare la **qualità e la scalabilità** del codice con attenzione alle **prestazioni ed alla sicurezza**.

sono stati eseguiti dei test su applicazioni di esempio con interesse su metriche di **search engine optimization, first e largest contentful paint, cumulative layout shift e prestazioni generali** per l'utente finale.

# 20

nuxt è un framework per applicazioni web full stack basato sulla libreria di **componenti reattivi vue.js** e sul server **http nitro**.

segue il **pattern architetturale** mvc, model, view, controller, la quale view segue a sua volta il pattern mvvm, model view, view model.

il compito di nuxt è appunto quello di gestire la **coerenza tra i due models**: il modello del database e il modello dei dati nella memoria del browser, quando l'app è in esecuzione

nuxt permette di fare ciò proponendo delle **convenzioni** di progettazione e di sviluppo, a partire dal file system routing ed all'importazione automatica dei componenti.

# 1:00

un'esempio dell'api nuxt:

in alto viene definito lato server un **handler** dell'endpoint users by last name, che **aspetta di ricevere il body** da una richiesta post, per poi fare **parsing usando un generic** che viene condiviso anche con il frontend.

poi si fa un accesso a database e si restituisce il risultato in una return, che consente di **tipizzare la risposta** come un oggetto con campi status e body.

sotto invece c'è una pagina che consuma questa api

nella pagina è presente una input box che **aggiorna una variabile reattiva tipizzata con lo stesso generic di sopra**.

al cambiamento di questa viene eseguita una **fetch** che restituisce una variabile reattiva data, utilizzata nella direttiva v-for per scorrere i risultati ed inserirli in componenti personalizzati.

# 1:00

le modalità di rendering supportate da nuxt sono molteplici

a sinistra è descritto il classico **client side rendering che soffre maggiormente di problemi di prestazioni**:

alla richiesta iniziale al server di contenuti statici viene seguita una risposta con un **DOM minimo ed un bundle javascript che viene assemblato interamente lato client**, e che poi si occupa di fare richieste asincrone per i dati.

a destra invece è descritto il server side rendering di nuxt, dove il **server frontend ha una parte attiva nel generare all'istante la pagina html completa** da fornire al browser. questo permette di **ridurre i problemi legati alle metriche di interesse**.

un'app nuxt si comporta come una **single page application per i cambiamenti di pagina quindi usa il routing client-side**. l'aggiunta di nuxt è nelle possibilità di prefetching di pagine e di **chunking di codice**, in modo da caricare solo i componenti necessari per la nuova pagina.

# 45

typeorm è la libreria di object relational mapping scelta per la gestione dei dati.

supporta vari dbms relazionali o a documenti tramite **adattatori javascript**.

rende disponibile una **command line interface per le migrazioni, con possibilità di rollback**.

le entità typeorm sono definite **a partire da classi Typescript**, ed i tipi delle colonne vengono inferiti dai tipi delle classi.

anche le relazioni sono definite automaticamente, tramite **decoratori, e le tabelle e le colonne di join sono create automaticamente**.

# 45

qui vediamo degli esempi delle api typeorm, per operazioni di create e di read.

a sinistra c'è query builder, che permette di **assemblare statement sql** con metodi concatenabili seguendo il design **pattern builder**. questo migliora la **leggibilità del codice** ma rimane la possibilità di **fare errori di battitura nelle stringhe letterali**.

a destra le stesse query sono state **tradotte** nel pattern active record, che si propone di rendere type safe anche le query con join. l'inconveniente è dal **lato delle prestazioni**, dal momento che in certi casi bisogna scorrere in memoria tutti gli oggetti per poi appiattirli e rimuovere i duplicati.

# 45

AWS è la piattaforma cloud scelta, ed offre servizi internet, tra cui servizi di calcolo, storage, database, e che **ho studiato durante il tirocinio curriculare**.

l'esempio in basso è uno snippet di un template cloudformation, che **crea o aggiorna** delle risorse database o di calcolo connesse in maniera programmatica.

# 30

le due architetture in **configurazione base** proposte proposte sono quella basata su container e quella serverless.

la prima funziona con elastic container service, un servizio che permette di **orchestrare container docker** in un cluster di macchine virtuali, anche in base al traffico, ma delle quali almeno **una deve rimanere sempre attiva e questo comporta un costo fisso**.

questo servizio è di tipo **stateful** perché l'applicativo esegue per periodi indefiniti, e questo permette di **mantenere connessioni aperte con il database**.

la seconda è basata su funzioni lambda, cioè su macchine virtuali che vengono **avviate immediatamente su richiesta** e terminano dopo brevi periodi di inattività e che soffrono del così detto problema di **cold start** per la latenza di avvio.

**i costi si calcolano in base all'attività effettiva** e il tipo di servizio è **stateless**. le connessioni al database vengono fatte ad ogni richiesta e per questo motivo è utile **aggiungere un pool di connessioni** per evitare di **aspettare handshake** ogni volta.

# 45

è stato predisposto un sistema di integrazione continua con gihtub actions. **ospitando il codice delle app su github è possibile avviare dei workflow** che si occupano di aggiornare l'infrastruttura cloud in base al codice appena caricato.

# 30

sono state realizzate delle applicazioni di esempio nelle due architetture che **simulano un social network al quale sono stati aggiunti dei dati di esempio** e delle pagine di navigazione, di profili utente e di post con reazioni.

è stata aggiunta una pagina che fa **le query descritte in entrambe le versioni** nell'esempio di typeorm per finalità di test.

il codice delle applicazioni con le due architetture è reso **disponibile su github**.

# 30

dall'analisi di prestazioni si può vedere come su richieste leggere l'architettura ecs si comporta meglio nelle metriche di rendering di una pagina **sotto carico lieve**. la **lambda a freddo in questo caso è carente nello speed index, per via del cold start**.

per carichi di lavoro **più pesanti invece la lambda è più performante, principalmente per la presenza del pool di connessioni**, invece ecs in configurazione base ha molta più variabilità.

il costo degli esperimenti che sono andati avanti per circa **due giorni** è **comune di due dollari e diciassette per la vpc**, al quale si aggiungono un dollaro e quarantasette per l'ecs e un centesimo approssimato per eccesso per le lambda.

# 1:00

in conclusione, le tecnologie scelte danno **risultati soddisfacenti quando usate in combinazione**.

estensioni possibili vanno in direzione di **ampliare l'infrastruttura cloud** delle applicazioni di esempio o di aggiungere funzionalità alle librerie stesse per la loro natura open source.

# 30
