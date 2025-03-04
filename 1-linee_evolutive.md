# Linee evolutive

Il Web è la piattaforma software più estesa al mondo e la sua evoluzione è stata guidata da una serie di innovazioni tecnologiche che hanno permesso di realizzare applicazioni sempre più complesse e performanti. Questo capitolo ripercorre brevemente le linee evolutive del web, partendo dalle pagine statiche fino ad arrivare alle applicazioni web moderne.

## Pagine statiche

Il primo modello del World Wide Web era orientato a facilitare la condivisione di documenti, permettendo ai lettori di esplorarli attraverso collegamenti tra le pagine. Il WWW consisteva in una combinazione di applicazioni, di protocolli e di linguaggi di marcatura progettati e rilasciati presso il CERN, principalmente ad opera di Tim Berners Lee e Robert Calliau, a ridosso degli anni '90:

**Browser e Server:** Con un browser web installato nel proprio sistema informatico, un utente può visualizzare pagine web e scegliere di seguire i collegamenti ipertestuali per accedere ad altre pagine. Il server web è responsabile di fornire le pagine web richieste dai client, come i browser.

**Protocollo HTTP:** È il protocollo di comunicazione di livello applicativo (OSI 7) che permette la trasmissione di informazioni tra client e server web. Un browser contatta un server web inviando una richiesta HTTP ad un determinato URL e il server risponde con una risposta HTTP contenente i dati richiesti. HTTP è un protocollo stateless, non mantiene informazioni sullo stato della comunicazione, quindi sta all'applicazione gestire eventuali sessioni o autenticazioni.

**Linguaggio HTML:** (HyperText Markup Language) è un linguaggio di marcatura utilizzato per la realizzazione di pagine web. HTML definisce la struttura e il contenuto di una pagina web attraverso l'uso di tag e attributi e consente di incorporare elementi multimediali. Il browser web interpreta il codice HTML e mostra la pagina web all'utente.

Nel 1993, il primo browser web grafico, Mosaic, introdusse il supporto per le immagini, per i form (dei moduli compilabili dall'utente con opzioni) e per i collegamenti ipertestuali, e successivamente Netscape Navigator 1.0 introdusse il supporto per CSS, il linguaggio che permise da subito agli sviluppatori di personalizzare la resa grafica della loro pagina. Queste innovazioni contribuirono a rendere il web più accessibile e visivamente attraente per un pubblico maggiore.

## Pagine dinamiche

I primi browser web erano in grado di visualizzare solo pagine statiche, il che significa che il contenuto di una determinata pagina non cambiava in base all'interazione dell'utente[^css].

[^css]: Gli unici effetti che si potevano apprezzare immediatamente dopo un'interazione dell'utente erano quelli di CSS, ad esempio il cambio di colore di un link al passaggio del mouse.

Le prime realizzazioni di pagine dinamiche furono rese possibili grazie agli hyperlinks ed ai form, con i quali i browser potevano effettuare richieste al server inviando i parametri forniti dall'utente. Il server poteva elaborare tali richieste e restituire una _nuova pagina HTML_ in base ai parametri ricevuti. Questo processo era gestito da programmi detti **CGI** (Common Gateway Interface), da eseguire sul server per generare pagine dinamicamente, cioè al momento della richiesta.

I linguaggi di programmazione utilizzati all'epoca per scrivere programmi CGI erano principalmente:

##### Linguaggi di basso livello o di scripting

-   Linguaggi di basso livello come C o C++, sono performanti ma di difficile progettazione e manutenzione.

-   Linguaggi di scripting come Perl o Shell UNIX, erano più facili da utilizzare ma meno efficienti: comodi per la manipolazione di stringhe e file, ma non per la gestione di strutture dati complesse.

##### Linguaggi di templating

Successivamente, dal 1995 in poi, emersero alcuni Linguaggi di templating che consentono di incorporare codice dinamico all'interno di pagine HTML dal lato server.

-   Java Server Pages (JSP) è un'estensione di Java, quindi era possibile usare tutte le librerie di questo linguaggio molto popolare all'epoca.

-   PHP è un linguaggio interpretato che ha avuto molto successo per oltre un decennio[^tiobe] grazie alla sua semplicità.

```php
<?php
$username = $_POST["username"];
$password = $_POST["password"];

$query = sprintf( "SELECT * FROM Users WHERE username='%s' AND password='%s'",
	$username, $password);
$result = mysql_query($query, $conn);

if (mysql_num_rows($result) > 0){
?>
	<h1>Benvenuto <?php echo $username; ?></h1>
	...
<?php
	} else {
	?>
		<h1>Accesso negato</h1>
		<p>Torna alla <a href="login">pagina di login</a></p>
	<?php
	}
?>
```

> Un esempio di pagina di autenticazione in PHP, che riflette lo stile di programmazione tipico dell'epoca[^mysqlphp]. È da notare come il codice HTML da inviare al browser sia inserito direttamente all'interno del codice da mantenere privato nel lato server, rendendone difficile la manutenzione per via della _confusione tra logica di presentazione e logica di business_. Vengono poi adoperati 3 linguaggi diversi (PHP, HTML, SQL), soluzione non ottimale per la leggibilità, che si aggiunge ai problemi di sicurezza legati all'_interpolazione_ di stringhe all'interno di query SQL.

[^tiobe]: [Indice TIOBE per PHP](https://www.tiobe.com/tiobe-index/php/), si può vedere come il suo utilizzo sia diminuito a partire dal 2010.
[^mysqlphp]: La libreria mysql di Micheal Widenius per PHP 2 risale al 1996.

## Pagine attive con Javascript

Il dinamismo delle pagine web supportato da server CGI e linguaggi di scripting era comunque limitato per via del caricamento di nuove pagine ad ogni richiesta. Non era possibile aggiornare parzialmente la pagina, ma solo scaricarne una nuova. Nel 1995 il Netscape Navigator 2.0 introdusse il supporto ad un nuovo linguaggio di scripting, che successivamente venne chiamato Javascript, realizzato da Brendan Eich, per ovviare a questo problema.

**Gestione di eventi e manipolazione del DOM:** Uno script Javascript, distribuito all'interno di una pagina HTML, può essere eseguito dal browser web in risposta a determinati eventi dell'utente. Inizialmente il motore di esecuzione era sincrono, cioè bloccava l'esecuzione del codice fino al completamento dell'operazione, e le possibilità di Javascript si limitavano alla manipolazione a _runtime_[^runtime] del DOM (Document Object Model), quindi ad aggiungere, rimuovere o modificare elementi HTML.

**Richieste HTTP asincrone:** Le pagine web, erano diventate _attive_, ma tutte le risorse da fornire agli utenti dovevano essere inserite nella pagina inviata come prima risposta HTTP. Nel 1999 però, il browser Internet Explorer 5 introdusse un'estensione del linguaggio Javascript, che disponeva di un oggetto chiamato _XMLHttpRequest_, in grado effettuare richieste HTTP asincrone al server e dunque ricevere risposte senza dover ricaricare l'intera pagina. Così si gettavano le basi per la realizzazione di _Single Page Applications_.

La libreria jQuery, rilasciata nel 2006, ha rivestito una particolare importanza perché semplificava la manipolazione del DOM e le richieste HTTP, fornendo un'interfaccia più semplice e omogenea rispetto ai diversi browser, che esponevano API diverse e non ancora standardizzate.

```javascript
$("#update").click(function () {
	$.ajax({
		// scaricamento asincrono
		url: "data.json",
		type: "GET",
		dataType: "json",
		success: function (data) {
			var content = "";
			for (var i = 0; i < data.length; i++) {
				content += "<p>" + data[i].name + "</p>";
			}
			$("#content").html(content);
		},
	});
});
```

> Nel frammento di codice jQuery, è messo in evidenza uno stile _imperativo_ di definizione del comportamento dell'interfaccia utente, poco manutenibile per applicazioni complesse.

[^runtime]: Il momento in cui la pagina è resa attiva con Javascript.

## Node.js e Javascript lato server

La standardizzazione di Javascript procedette attraverso le varie versioni di ECMAScript che definivano le nuove funzionalità del linguaggio e, di conseguenza, dei browser web. Nel 2008 fu rilasciata la prima versione di Google Chrome, un browser che, oltre ad includere caratteristiche appetibili per gli utenti finali, disponeva del motore di esecuzione Javascript V8. Questo _engine_ apportò dei sostanziali miglioramenti di prestazioni[^prestazioniv8] rispetto alla competizione e venne rilasciato come _Open source software_.

Nel 2009, Ryan Dahl iniziò a lavorare, basandosi sul codice di V8, a Node.js, un interprete di Javascript in modalità headless[^headless], al quale aggiunse la capacità di accedere al filesystem, di esporre servizi HTTP e di accettare connessioni in maniera _non bloccante_.

In questo modo si poterono realizzare non solo applicazioni **frontend** ma anche **backend** con Javascript, abilitando sempre più novizi alla creazione di siti web completi. Attorno a Node crebbe una comunità di sviluppatori che contribuirono, secondo i principi dell'Open source, alla creazione di un ecosistema di librerie, che potevano essere installate tramite il gestore di pacchetti NPM.

```javascript
const http = require("http");
const mysql = require("mysql");

const connection = mysql.createConnection({
	/* ... */
});

const server = http.createServer((req, res) => {
	if (req.method === "POST" && req.url === "/login") {
		var username, password;
		// unmarshalling della query string ...
		var login = "SELECT * FROM Users WHERE username = ? AND password = ?";
		connection.query(login, [username, password], (err, rows) => {
			if (rows.length > 0) {
				res.writeHead(200, { "Content-Type": "text/html" });
				res.end("<h1>Benvenuto " + username + "</h1>");
			} else {
				res.writeHead(401, { "Content-Type": "text/html" });
				res.end("<h1>Accesso negato</h1>");
			}
		});
	}
});
server.listen(80, () => {
	console.log("Server in ascolto alla porta 8080");
});
```

> In questo frammento di codice è mostrato l'utilizzo della libreria "http" fornita di default da Node e della libreria "mysql" di Felix Geisendörfer, una delle prime per l'accesso a database da Node. È da notare l'architettura a callback, che permette di gestire in maniera asincrona le richieste HTTP e le query al database.

> In questo esempio le query SQL sono parametrizzate, facendo uso di _Prepared statements_, per evitare attacchi di tipo injection, ma rimangono cablate all'interno di stringhe, rendendo il codice vulnerabile a errori di sintassi e di tipo.

[^prestazioniv8]: [Google Chrome announcement:](https://youtu.be/LRmrMiOWdfc?si=gaHRFdA8QcYZ0NYq&t=2676) in questo video si può vedere come l'esecuzione di Javascript su Chrome sia di circa 60 volte più veloce che su Internet Explorer 8.
[^headless]: Cioè senza interfaccia grafica.

## Applicazioni web orientate a componenti

Anche con Node fu possibile realizzare applicazioni web _monolitiche_, parimenti al templating PHP, usando librerie come EJS di TJ Holowaychuk.

Tuttavia le tendenze di quel periodo (circa 2010) si discostarono dal modo tradizionale di scrivere applicazioni web, basate su pagine generate lato server, per passare a un modello di **client-side rendering**. Secondo questo modello il server invia al browser una pagina HTML con un DOM minimo, corredato di script JS che si occupano di popolare a runtime il DOM con contenuti e di gestire le logiche di presentazione.

Le applicazioni renderizzate lato cliente potevano beneficiare di una maggiore _reattività_ e di una migliore esperienza utente, essendo basate su una pagina unica che veniva aggiornata in maniera incrementale, aggirando i caricamenti di nuove pagine da richiedere al server. Le richieste al server, essendo asincrone, potevano essere gestite in modo meno invasivo rispetto a prima: mentre la comunicazione avveniva in background, l'utente poteva continuare ad interagire con l'applicazione.

Il vantaggio di questo paradigma da parte degli sviluppatori era la possibilità di scrivere la logica di presentazione interamente in Javascript, sfruttando il sistema di oggetti e la modularità del linguaggio in maniera più espressiva rispetto al templating o all'uso imperativo delle API DOM.

L'idea centrale delle nuove tendenze _CSR_ era quella di progettare l'interfaccia utente partendo da parti più piccole, chiamate **componenti**, e riutilizzabili all'interno dell'intera applicazione. Lo stile assunto era _dichiarativo_[^dichiarativo]. Ad ogni componente sono associati:

[^dichiarativo]: In questo contesto, uno stile dichiarativo è riferito ad un approccio alla programmazione in cui si descrive cosa il programma deve fare piuttosto che come farlo. Con jQuery si dovevano specificare esplicitamente i passaggi per manipolare il DOM, mentre i componenti permettono di definire il comportamento dell'interfaccia utente attraverso delle dichiarazioni più astratte e concise.

-   un template HTML, più piccolo e gestibile rispetto ad una pagina intera.
-   un foglio CSS, per la stilizzazione.
-   il codice Javascript che ne definisce la logica di interazione.

Tra gli esempi più noti di sistemi di componenti:

##### Angular.js

Uno dei primi framework a proporre un modello di componenti, sviluppato in Google e rilasciato nel 2010. Angular.js introduceva il concetto di _two-way data binding_, cioè la possibilità di sincronizzare automaticamente i dati tra il modello e la vista.

##### React.js

La libreria di componenti sviluppata da un team interno di Facebook e rilasciata nel 2013. React introduceva il concetto di _Virtual DOM_, una rappresentazione in memoria del DOM reale, che permetteva di calcolare in maniera efficiente le differenze tra due stati del DOM e di applicare solo le modifiche necessarie. Per questi miglioramenti nella performace venne adottato moltissimo[^react]. Da React in poi, lo sviluppo di pagine web ha riguardato un livello più astratto rispetto all'esecuzione del classico codice Javascript che manipola direttamente il DOM. Inteso così, il browser diventa l'interprete di un codice intermedio sul quale gli sviluppatori non mettono mano direttamente.

[^react]: [Github - React](https://github.com/facebook/react) - la più popolare in base numero di stelle su Github.

##### Vue.js

Partito come progetto personale di Evan You e rilasciato nel 2014, Vue si proponeva come un'alternativa più flessibile e meno verbosa rispetto ad Angular e React, dai quali riprende il binding bidirezionale e il Virtual DOM. È la libreria di componenti usata da Nuxt.

```html
<script setup>
	import { RouterView } from "vue-router";
	import HelloWorld from "./components/HelloWorld.vue";
</script>

<template>
	<HelloWorld msg="Ciao mondo" />
	<RouterView />
</template>

<style scoped>
	background-color: #f0f0f0;
</style>
```

> Un esempio moderno di applicazione Vue 3, che mostra l'utilizzo di un componente "HelloWorld" all'interno di un template principale, e di un RouterView per la navigazione tra le pagine. Questi componenti sono definiti in file distinti, per favorire la separazione delle preoccupazioni, ed importati nel file principale come se fossero moduli Javascript. Ogni volta che compaiono in un template assumono un comportamento dettato dalla loro definizione (il loro template) e dal loro _stato_ di istanza. Si noti come il componente HelloWorld sia parametrizzato con un attributo `msg`, che ne consente un utilizzo più flessibile.

```html
<html lang="en">
	<head>
		<title>Vite App</title>
	</head>
	<body>
		<div id="app"></div>
		<script type="module" src="/src/main.js"></script>
	</body>
</html>
```

> Il DOM minimo che viene distribuito da una applicazione Vue 3. La pagina viene assemblata lato client, a partire dal così detto _entry point_: l'elemento con id "app", in cui viene montata l'applicazione. Si noti che nel caso che Javascript non sia abilitato nel client il contenuto dell'applicazione non verrà visualizzato affatto.

## Typescript e ORM

Le basi di codice Javascript iniziarono a diventare sempre più complesse quando anche i team di sviluppatori di grandi compagnie iniziarono ad adottare i framework a componenti. A partire dal 2014 anche applicazioni web come Instagram, Netflix e Airbnb incorporarono React nei loro stack tecnologici per realizzare interamente l'interfaccia utente.

Javascript, essendo un linguaggio interpretato e debolmente tipizzato, non era in grado di garantire la correttezza del codice e i test di unità erano fatti in modo _behavior driven_, cioè basati sul comportamento dell'applicazione e non sulla tipizzazione dei dati. Questo spesse volte portava ad errori, difficili da individuare e correggere, soprattutto in applicazioni di grandi dimensioni.

Nel 2012 Anders Hejlsberg ed il suo team interno a Microsoft iniziarono a lavorare al linguaggio Typescript, una estensione di Javascript, realizzando un **compilatore** in grado di rilevare errori di tipo in con analisi statica. Typescript permette anche di sfruttare le funzionalità delle nuove versioni di ECMAScript in modo _retrocompatibile_, cioè facendo _transpiling_[^transpiling] verso una specifica di ECMA inferiore, per usarle anche sui browser deprecati.

[^transpiling]: [Wikipedia - Source-to-source compiler](https://en.wikipedia.org/wiki/Source-to-source_compiler) - il transpiling è il processo di traduzione automatica di codice sorgente da un linguaggio ad un altro.

L'adozione di Typescript è stata pressoché immediata, per il motivo che la conversione di basi di codice a partire da Javascript vanilla[^vanilla] era a costo zero: ogni sorgente Javascript è valido Typescript. Typescript ha avuto successo non solo lato client, ma anche lato server. Sono comparse infatti alcune librerie di supporto all'accesso a database basate sul pattern **ORM**, _Object-relational mapping_, quindi capaci di mappare il modello dei dati presente nel database a strutture dati proprie di Typescript. Librerie notevoli di questo tipo sono:

[^vanilla]: Con "vanilla" ci riferisce a Javascript senza estensioni, quindi al codice che può eseguire nativamente sui browser conformi alle specifiche ECMA. Typescript invece è un _superset_, quindi ha un insieme di espressioni sintattiche più grande ma che comprende interamente quello di Javascript.

##### Sequelize

È stata una delle prime, il progetto è iniziato nel 2010 quindi funzionava con Javascript vanilla, ma si è evoluta fino a supportare le migliorie di Typescript ed una moltitudine di DBMS.

##### TypeORM

Offre supporto a Typescript nativamente. È illustrata con dettaglio nel [capitolo 2](#typeorm).

L'evoluzione dei sistemi per fare query a basi di dati da Javascript è poi diramata in direzioni diverse, da quelli che usano protocolli applicativi binari (basati ad esempio su gRPC) a quelli che usano linguaggi di query specifici (come GraphQL), ad ORM che introducono nuovi linguaggi di definizione dei modelli (come Prisma).

## Ritorno al server-side rendering

Dal lancio di React sempre più applicazioni web hanno fatto uso della tecnica CSR per via della migliorata esperienza utente e di sviluppo. Questo approccio ha portato però una serie di nuovi problemi e limitazioni legate al meccanismo di rendering.

##### Performance su dispositivi lenti

I _bundle_ Javascript che vengono generati per le applicazioni CSR sono spesso onerosi in termini di risorse, e la loro esecuzione su dispositivi con capacità di calcolo limitate può risultare lenta e insoddisfacente per l'utente.

##### Search engine optimization

I siti web che fanno uso di CSR sono più difficilmente indicizzabili dai _crawler_ dei motori di ricerca, questo può portare a problemi di esposizione e di traffico ridotti.

##### First contentful paint

È il tempo che intercorre tra la cattura della risposta HTTP del server e il momento in cui viene visualizzato a schermo dal browser il primo elemento di contenuto significativo per l'utente. Nelle applicazioni CSR questa durata spesso eccede quella massima suggerita da Google[^corewebvitals].

##### Cumulative layout shift

Per il motivo che gli aggiornamenti dell'interfaccia vengono vengono resi graficamente in maniera sequenziale nel browser, potrebbero esserci dei fastidiosi spostamenti di elementi visivi nell'interfaccia durante la fase di caricamento.

##### Accessibility

Per gli stessi motivi che portano al cumulative layout shift, ci potrebbero essere degli impedimenti di accessibilità per chi usa metodi di input alternativi o per gli screen-reader che aiutano le persone non vedenti nella fruizione delle pagine web.

Per questi motivi, a partire dal 2016, sono emerse delle nuove tendenze che hanno portato ad un ritorno al server-side rendering, in combinazione con i sistemi basati su componenti, per unire i vantaggi di entrambi i modelli.
Esempi di framework che supportano il SSR sono: Angular Universal, Next.js per React e Nuxt per Vue, che verrà illustrato nel [capitolo 2](#nuxt).

[^corewebvitals]: [Google developers - Core web vitals](https://developers.google.com/search/docs/appearance/core-web-vitals?hl=it) - Al 10 maggio 2023, la durata massima ammissibile per il FCP è di 2.5s.

## Servizi cloud e containerizzazione

Le tecniche di rilascio di applicazioni web si sono evolute di pari passo alle tecnologie di sviluppo.

Il primo modello era quello _monolitico_, in cui l'applicazione web viene distribuita su un server fisico, con un indirizzo IP statico, e che necessita di configurazioni manuali.

Poi, attorno all'inizio degli anni 2000, sono emersi i primi **provider di cloud**, come Amazon Web Services, Google Cloud Platform, Microsoft Azure e IBM Cloud, che non solo offrivano servizi di hosting di _virtual private server_, traducendo quindi il paradigma monolitico su macchine virtuali, ma anche servizi di _infrastrucure as a service_, permettendo ai progettisti di app web di modificare le risorse di calcolo e di archiviazione secondo necessità e di automatizzare il processo di rilascio.

Una tecnologia in particolare si è affermata come standard per la distribuzione di applicazioni web attraverso l'infrastruttura cloud, il **container**, e la sua implementazione più popolare, Docker.

Docker è un sistema di virtualizzazione di risorse a livello di sistema operativo, che permette di isolare i processi di un'applicazione in un ambiente chiuso che condivide il kernel del sistema operativo host.
Questa tecnica è diversa da quelle di virtualizzazione classiche, che mirano ad emulare un intero sistema operativo, come fa ad esempio KVM, o un intero sistema hardware, come fa QEMU. Docker è più leggero e più veloce, e permette di avere un ambiente di esecuzione riproducibile e portabile, che può essere distribuito su qualsiasi macchina che abbia Docker installato. [^docker]

[^docker]: [Docker - What is a container?](https://www.docker.com/resources/what-container) In questo articolo vengono comparate le tecnologie di virtualizzazione tradizionali con Docker.

Il ruolo degli informatici coinvolti nello sviluppo di applicazioni web si è quindi differenziato tra gli _architetti di cloud_ e gli _ingegneri di sviluppo_. Tuttavia, una volta che l'infrastruttura è pronta, il processo di rilascio di un'aggiornamento dell'applicazione si semplifica notevolmente, grazie ai metodi di di **continuous integration** come Travis CI, Circle CI e Github Actions, che permettono di automatizzare il processo di build e di test, e di rilasciare su cloud con la stessa facilità con cui si fa un commit sul repository di codice.
