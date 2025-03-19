# 0
buongiorno/buonasera a tutti sono valerio iacobucci
e presento la mia tesi di laurea in tecnologie web con il professor bellavista
dal titolo sviluppo e analisi delle prestazioni di applicazioni web nuxt-based in cloud aws

# 15

gli obiettivi di questa tesi sono stati quello di allestire un ambiente sviluppo per applicazioni web mirato a migliorare la qualità e la scalabilità del codice con attenzione alle prestazioni.
sono state scelte le tecnologie nuxt come framework di sviluppo, typeorm come libreria per accesso a database e aws come fornitore di servizi cloud.
le metriche di interesse sono state quelle di sicurezza ma anche search engine optimization, first e largest contentful paint, cumulative layout shift e prestazioni generali per l'utente finale

# 20

nuxt è un framework per applicazioni web full stack basato sulla libreria di progettazione di componenti reattivi vue.js e sul server http nitro
come si può vedere dal suo diagramma architetturale, nuxt segue il pattern mvc, model, view controller, la quale view segue a sua volta il pattern mvvc, model view, view model.
il compito di nuxt è quello di gestire la comunicazione tra i due models: il modello del database e il modello dei dati nella memoria del browser, quando l'app è in esecuzione
nuxt permette di fare ciò proponendo delle convenzioni di progettazione e di sviluppo, a partire dal file system routing che permette di creare una struttura di navigazione delle pagine in base alla gerarchia di files e directories, poi all'importazione automatica dei componenti e dei layout.
anche per il lato backend le api sono organizzate in base ad una gerarchia

# 1:00

qui vediamo un'esempio di uso delle api di nuxt che tralascia molti dettagli.
lo snippet sopra è nel file /api/users/byLastName.ts e definisce un endpoint POST che
attende l'arrivo del body, tipizzato con il generic UsersByLastName
poi fa una query al database per cercare tutti gli utenti con il cognome uguale a quello passato nel body
e infine restituisce i risultati con una return, che garantisce la tipizzazione del risultato come un oggetto con campi status e body
sotto invece c'è un componente o una pagina vue che consuma questa api
c'è una variabile reattiva tipizzata nello stesso modo del backend che viene associata alla input box con v-model
poi c'è un metodo che fa una chiamata post all'api ogni volta che la variabile reattiva si aggiorna
e infine c'è una direttiva v-for che itera sui risultati della chiamata e li aggiunge come componenti personalizzati RowsUser 
questi sono incorporati in un NuxtLink, che permette di navigare tra le pagine dell'applicazione in maniera efficiente, usando il routing client-side, il prefetching di pagine e il chunking di codice, in modo da caricare solo i componenti vue necessari per la nuova pagina.

# 1:00

nel diagramma di sequenza a sinistra è descritto il client side rendering delle classiche librerie di componenti che eseguono interamente nel browser e che soffrono dei problemi menzionati nell'introduzione. ad una richiesta del browser il server risponde con un file html pressoché vuoto ed un bundle javascript con tutto il codice dell'applicazione. quando questo codice ha terminato di eseguire la pagina è pronta e utilizzabile, con richieste asincrone di dati o assets.
a destra invece è descritto il server side rendering supportato da nuxt. ad una richiesta il server frontend ha una parte attiva nell'eseguire il codice dell'applicazione vue, facendo chiamate a database se necessario e quindi permettendo una ottimizzazione con caching, per poi restituire al browser un file html completo. per le richieste asincrone di assets l'app nuxt si comporta come una single page application, ma per la richiesta di nuove pagine il server frontend è coinvolto nell'invio dei chunk mancanti

# 45

typeorm è la libreria di object relational mapping scelta per la gestione dei dati.
supporta database relazionali tramite adattatori javascript, come il database su file o in memoria sqlite, la libreria sql.js che permette di fare persistenza su local storage ed indexedDB nel browser, poi i database basati su server come mysql e postgres.
per postgres c'è un supporto alle colonne di tipo json o jsonb per memorizzare dati non strutturati.
di contro typeorm supporta anche database non relazionali come mongodb, facendo astrazione sul loro sistema di documenti per permettere di creare strutture di dati rigide in modo simile a quelle relazionali.
rende disponibile una cli per fare migrazioni, quindi per applicare modifiche allo schema del database in maniera incrementale e reversibile.
le entità sono definite tramite classi Typescript, ed i tipi delle colonne vengono inferiti tramite i tipi Typescript ma si possono dettagliare con modificatori come la lunghezza dei varchar.
si possono anche definire relazioni tra entità con varie cardinalità, senza creare manualmente le tabelle di join, ma indicando foreign key e tabelle o colonne di join sempre con decoratori.

# 45

qui vediamo degli esempi delle api typeorm
a sinistra c'è query builder, che permette di costruire query sql con metodi concatenabili seguendo il design pattern builder. questo migliora la leggibilità del codice ma rimane la possibilità di fare errori di battitura nelle stringhe che indicano i nomi delle colonne sulle quali eseguire join.
a destra le stesse query sono state tradotte nel pattern active record.
un'istanza della classe User, che estende BaseEntity, ha a disposizione metodi come save e remove per fare operazioni CRUD, ed in più è disponibile l'API repository per fare query.
si può vedere come stavolta la query è implementata in maniera completamente type safe, dal momento che anche i valori del campo where sono tipizzati con dei Partial Typescript.
l'inconveniente è che con il caricamento delle relazioni di ogni ogni post per ogni utente e di ogni utente che ha messo mi piace per ognuno di quei post si trattano molti oggetti in memoria, poi vengono appiattiti e trasformati in un set per rimuovere duplicati.

# 45

AWS la piattaforma cloud che offre servizi internet, tra cui servizi di calcolo, storage, database studiata durante il tirocinio curriculare ed usata per impostare l'infrastruttura dell'applicazione come codice di templating.
l'esempio in basso è uno snippet di un template cloudformation, che prende parametri in ingresso al momento dell'attivazione e crea un database con le credenziali inserite.
poi viene avviata una risorsa concettuale che avvia un'applicazione, passando come variabili d'ambiente le credenziali del database, oltre che l'url al quale è raggiungibile. Il database deve essere pronto per passare l'endpoint all'applicazione, quindi l'applicazione potrà connettersi da subito.

# 30

le due architetture della cloud proposte sono quella basata su container e quella serverless.
la prima funziona con elastic container service, un servizio che permette di orchestrare container docker in un cluster di macchine virtuali, anche in base al traffico, ma delle quali almeno una deve rimanere sempre attiva e questo comporta un costo fisso. il tipo di questo servizio è stateful perché l'applicativo esegue per periodi indefiniti, e questo permette di tenere connessioni aperte con il database.
la seconda è basata su funzioni lambda, cioè su macchine virtuali che vengono avviate quando c'è una richiesta e terminano dopo brevi periodi quindi soffrono del così detto problema di cold start per la latenza di avvio. I costi si calcolano in base all'attività effettiva e il tipo di servizio è stateless. le connessioni al database vengono fatte ad ogni richiesta e per questo motivo è utile aggiungere un pool di connessioni per evitare di aspettare handshake ogni volta.

# 45

è stato predisposto un sistema di integrazione continua con gihtub actions. ospitando il codice delle app su github è possibile avviare dei workflow che si occupano di fare il checkout del codice appena pushato sul branch master, per poi fare build dell'immagine per ecs o dello zip per le lambda ed attivare la creazione o l'aggiornamento degli stack cloudformation.

# 30

sono state realizzate delle applicazioni di esempio che simulano un social network al quale sono stati aggiunti degli dati mock e delle pagine di navigazione, di profili utente e di post con reazioni. La pagina userswholikedpostsbyauthors, nelle versioni active record e query builder, usa le query mostrate precedentemente. il codice delle applicazioni con le due architetture è reso disponibile su github.

# 30

le analisi delle prestazioni sono state effettuate con google lighthouse e con uno strumento per test di carico http, che ha inviato 200 richieste ad una pagina con query complesse.
l'audit di lighthouse ha mostrato come le prestazioni dell'architettura ecs siano migliori di quelle lambda, avendo risultati migliori nel rendering di una pagina sotto carico lieve. la lambda a freddo in questo caso è carente nello speed index, per via del cold start.
first contentful paint e largest contentful paint coincidono proprio perché l'app è renderizzata lato server.
per le query invece si può vedere come la lambda sia più performante, il tempo in secondi qui è una media dei tempi di risposta delle 200 richieste. ECS con la configurazione scelta ha molta più variabilità ed in generale le lambda riescono a completare la risposta in meno di un secondo al 95esimo percentile in tutti i casi tranne in quello di cold start con active record.
il costo degli esperimenti che sono andati avanti per due giorni è comune di due dollari e diciassette per la vpc, al quale si aggiungono un dollaro e quarantasette per l'ecs e un centesimo approssimato per eccesso per le lambda.

# 1:00

in conclusione, le tecnologie scelte danno risultati soddisfacenti quando usate in combinazione.
nuxt è performante e fornisce un ambiente di sviluppo completo.
typeorm è valido in termini di performance e garantisce sicurezza di tipo.
aws lambda è una scelta competitiva per progetti di dimensioni piccole o medie. su scale molto grandi l'overhead di cold start potrebbe rendere ecs più conveniente
estensioni possibili vanno in direzione di ampliare l'infrastruttura cloud delle applicazioni di esempio o di aggiungere funzionalità alle librerie stesse per la loro natura open source.

# 30