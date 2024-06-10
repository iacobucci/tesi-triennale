# Linee evolutive

## Pagine statiche

Il primo modello del World Wide Web era inteso a facilitare la condivisione di documenti tra scienziati e ricercatori, permettendo ai lettori di navigare nei siti attraverso collegamenti non lineari tra pagine. Il WWW consisteva in una combinazione di applicazioni, di protocolli e di linguaggi di marcatura progettati e rilasciati presso il CERN a ridosso degli anni '90:

##### Browser e Server
Con un browser web installato nel proprio sistema informatico, un utente può visualizzare pagine web e scegliere di seguire i collegamenti ipertestuali (hyperlinks) per accedere ad altre pagine. Il server web è responsabile di fornire le pagine web richieste dai client, come i browser.

##### Protocollo HTTP
HTTP è il protocollo di comunicazione di livello applicativo (OSI 7) che permette la trasmissione di informazioni tra client e server web. Un browser contatta un server web inviando una richiesta HTTP ad un determinato URL e il server risponde con una risposta HTTP contenente i dati richiesti. HTTP è un protocollo stateless, non mantiene informazioni sullo stato della comunicazione. Sta all'applicazione gestire eventuali sessioni o autenticazioni.

##### Linguaggio HTML
Il linguaggio HTML (HyperText Markup Language) è un linguaggio di marcatura utilizzato per la creazione di pagine web. HTML definisce la struttura e il contenuto di una pagina web attraverso l'uso di tag e attributi e consente di incorporare elementi multimediali. Il browser web interpreta il codice HTML e visualizza la pagina web all'utente.


##### CGI 
I primi browser web erano in grado di visualizzare solo pagine statiche, il che significa che il contenuto di una determinata pagina non cambiava in base all'interazione dell'utente, ed i primi srever web erano in grado di fornire solo pagine statiche, cioè pagine il cui contenuto non cambiava nel tempo.

Tuttavia, tramite hyperlinks e successivamente tramite form (cioè dei moduli da compilare con opzioni selezionabili dall'utente, introdotte nel 1993) i browser potevano effettuare richieste al server inviando parametri tramite il protocollo HTTP. Il server poteva elaborare tali richieste e restituire una *nuova pagina HTML* in base ai parametri ricevuti. Questo processo era gestito da programmi detti CGI (Common Gateway Interface), da eseguire sul server per generare pagine dinamicamente, cioè al momento della richiesta.

I linguaggi di programmazione utilizzati all'epoca per scrivere programmi CGI erano principalmente:

- Linaguaggi di basso livello come C o C++, di difficile gestione e manutenzione;
	- Sono performanti ma richiedono una solida conoscenza informatica.

- Linguaggi di scripting come Perl o Shell UNIX, più facili da utilizzare ma meno efficienti;
	- Comodi per la manipolazione di stringhe e file, ma non per la gestione di strutture dati complesse.

##### Linguaggi di templating 
Successivamente, dal 1995 in poi, emersero alcuni Linguaggi di templating, come PHP o JSP, che consentono di incorporare codice dinamico all'interno di pagine HTML.

- Java Server Pages (JSP) è un'estensione di Java, quindi era possibile usare tutte le librerie di questo linguaggio molto popolare all'epoca.
- PHP è un linguaggio interpretato che ha avuto molto successo per oltre un decennio[^1] grazie alla sua semplicità.

Un esempio di pagina di autenticazione in PHP, che riflette lo stile di programmazione tipico dell'epoca:
```php
<?php
$username = $_POST["username"];
$password = $_POST["password"];

$query = sprintf( "SELECT * FROM Users WHERE username='%s' AND password='%s'", $username, $password);
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
È da notare come il codice HTML da inviare al browser sia inserito direttamente all'interno del codice da mantenere privato, rendendone difficile la manutenzione per via della *confusione tra logica di presentazione e logica di business*. Vengono poi adoperati 3 linguaggi diversi (PHP, HTML, SQL), soluzione non ottimale per la leggibilità, che si aggiunge ai problemi di sicurezza legati all'interpolazione di stringhe all'interno di query SQL.

[^1]: [Indice TIOBE per PHP](https://www.tiobe.com/tiobe-index/php/), si può vedere come il suo utilizzo sia diminuito a partire dal 2010.

## Pagine attive con Javascript

Il dinamismo delle pagine web supportato da server CGI e linguaggi di scripting era comunque limitato per via del caricamento di nuove pagine ad ogni richiesta. Non era possibile aggiornare solo una parte della pagina, ma solo l'intera pagina. Nel 1995 il browser Netscape Navigator introdusse il supporto ad un nuovo linguaggio di scripting, Javascript, per ovviare a questo problema.

##### Gestione di eventi e manipolazione del DOM

Uno script Javascript, distribuito all'interno di una pagina HTML, può essere eseguito dal browser web in risposta a determinati eventi, come il click di un bottone o la pressione di un tasto. Inizialmente il motore di esecuzione era sincrono, cioè bloccava l'esecuzione del codice fino al completamento dell'operazione, e la istruzioni per la risposta agli eventi erano inserite in funzioni dette di *callback*.

Javascript può manipolare il DOM (Document Object Model), cioè la rappresentazione ad albero della struttura della pagina, per aggiungere, rimuovere o modificare elementi HTML.

##### Richieste HTTP asincrone
Le pagine web, erano diventate *attive*, ma tutti gli script da fornire agli utenti dovevano essere inseriti nella pagina inviata come prima risposta HTTP. Nel 1999, il browser Internet Explorer 5 introdusse una estensione del linguaggio Javascript, che disponeva di un oggetto chiamato *XMLHttpRequest*, in grado effettuare richieste HTTP asincrone al server e di ricevere risposte senza dover ricaricare l'intera pagina. Così si gettavano le basi per realizzare *Single Page Applications*.

Riveste una particolare importanza la libreria jQuery, rilasciata nel 2006, che semplificava la manipolazione del DOM e le richieste HTTP, fornendo un'interfaccia più semplice e omogenea rispetto ai diversi browser, che esponevano API diverse e non ancora standardizzate.

## Node.js e Javascript lato server

La standardizzazione di Javascript seguitò attraverso le varie versioni di ECMAScript che definivano le nuove funzionalità del linguaggio e, di conseguenza, dei browser web. Nel 2008 fu rilasciata la prima versione di Google Chrome, un browser che, oltre ad includere caratteristiche appetibili per gli utenti finali, disponeva del motore di esecuzione Javascript V8. Questo *engine* apportò dei sostanziali miglioramenti di performance[^2] rispetto alla competizione e venne rilasciato come *Open source software*.

Nel 2009, Ryan Dahl iniziò a lavorare, basandosi sul codice di V8, a Node.js, un interprete di Javascript in modalità headless[^3], al quale aggiunse la capacità di accedere al filesystem, di esporre servizi HTTP e di accettare connessioni in maniera *non bloccante*.

In questo modo si poterono realizzare non solo applicazioni **frontend** ma anche **backend** con Javascript. Attorno a Node.js crebbe una comunità di sviluppatori che contribuirono, secondo i principi dell'Open source, alla creazione di un ecosistema di librerie, che potevano essere installate tramite il gestore di pacchetti NPM.

```Java
const http = require("http");
const mysql = require("mysql");

const connection = mysql.createConnection({ /* ... */ })

const server = http.createServer((req, res) => {
    if (req.method === 'POST' && req.url === '/login') {

		var username, password;
		// unmarshalling della query string ...
	
		var login = "SELECT * FROM Users WHERE username = ? AND password = ?";
		connection.query(login, [username, password], (err, rows) => {
			if (rows.length > 0) {
				res.writeHead(200, {"Content-Type": "text/html"});
				res.end("<h1>Benvenuto " + username + "</h1>");
			} else {
				res.writeHead(401, {"Content-Type": "text/html"});
				res.end("<h1>Accesso negato</h1>");
			}
		}
	}
}

server.listen(80, () => { console.log("Server in ascolto sulla porta 8080"); });
```

In questo frammento di codice è mostrato l'utilizzo della libreria "http" fornita di default da Node.js e della libreria "mysql" di Felix Geisendörfer, una delle prime per l'accesso a database da Node. È da notare l'architettura a callback, che permette di gestire in maniera asincrona le richieste HTTP e le query al database.

In questo esempio le query SQL sono parametrizzate, facendo uso di **Prepared statements**, per evitare attacchi di tipo injection, ma rimangono camblate all'interno di stringhe, rendendo il codice vulnerabile a errori di sintassi e di tipo.

Nonostante, per brevità, venga inviato l'HTML in maniera diretta, è stato fin da subito possibile utilizzare le capacità di lettura asincona di files di Node per servire pagine statiche.

[^2]: [Google Chrome announcement](https://youtu.be/LRmrMiOWdfc?si=gaHRFdA8QcYZ0NYq&t=2676), in questo video si può vedere come l'esecuzione di Javascript su Chrome sia di circa 60 volte più veloce che su Internet Explorer 8.
[^3]: Cioè senza interfaccia grafica.


## Applicazioni web orientate a componenti

Anche con Node fu possibile realizzare applicazioni web *monolitiche*, parimenti al templating PHP, usando librerie come EJS di TJ Holowaychuk.

Le tendenze di quel periodo (circa 2010) si discostarono dal modo tradizionale di scrivere applicazioni web, basate su pagine generate lato server, per passare a un modello di *client-side rendering*. Secondo questo modello il server invia al browser una pagina HTML con un DOM minimo, corredato di script Javascript che si occupano di popolare il DOM dei contenuti e di gestire le logiche di presentazione.

Le applicazioni renderizzate lato cliente potevano beneficiare di una maggiore reattività e di una migliore esperienza utente, essendo basate su una pagina unica che veniva aggiornata in maniera incrementale, aggirando i caricamenti di nuove pagine da richiedere al server. Le richieste, essendo asincrone, potevano essere gestite in modo meno invasivo rispetto a prima: mentre la comunicazione client-server avveniva in background, l'utente poteva continuare ad interagire con l'applicazione.

Il vantaggio da parte degli sviluppatori di questo paradigma era la possibilità di scrivere la logica di presentazione interamente in Javascript, sfruttando il sistema di oggetti e la modularità del linguaggio in maniera più espressiva rispetto al templating o alle API DOM. Scrivere applicazioni con jQuery, ad esempio, portava ad assumere uno stile troppo procedurale e poco manutenibile per applicazioni complesse o che dovevano essere sviluppate da più persone.

L'idea centrale della tendenza *CSR* era quella di progettare l'interfaccia utente partendo da parti più piccole, chiamate **componenti**, e riutilizzabili all'interno dell'intera applicazione. Ad ogni componente erano associati:

- un template HTML, più piccolo e gestibile rispetto ad una pagina intera
- un foglio CSS, per la stilizzazione
- il codice Javascript che ne definisce la logica di presentazione e di interazione

Tra gli esempi più noti di sistemi di componenti:

##### Angular.js
Uno dei primi framework a proporre un modello di componenti, sviluppato in Google e rilasciato nel 2010. Angular.js introduceva il concetto di *Two-way data binding*, cioè la possibilità di sincronizzare automaticamente i dati tra il modello e la vista.

##### React.js
La libreria di componenti più popolare[^4], sviluppata da un team interno di Facebook e rilasciata nel 2013. React introduceva il concetto di *Virtual DOM*, una rappresentazione in memoria del DOM reale, che permetteva di calcolare in maniera efficiente le differenze tra due stati del DOM e di applicare solo le modifiche necessarie.

##### Vue.js
Partito come progetto personale di Evan You e rilasciato nel 2014. Vue.js si proponeva come un'alternativa più leggera e flessibile rispetto ad Angular e React, dai quali riprende il binding bidirezionale e il Virtual DOM. È la libreria di componenti usata da Nuxt.js.

```html
<script setup>
import { RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
      <HelloWorld msg="HelloWorld" />
  </header>
  <RouterView />
</template>

<style scoped>
</style>
```

Un esempio moderno di applicazione Vue.js 3, che mostra l'utilizzo di un componente HelloWorld all'interno di un template principale, e di un RouterView per la navigazione tra le pagine. 
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
````

Il DOM minimo che viene distribuito da una applicazione Vue.js 3 servita con lo strumento *Vite*. La pagina viene assemblata lato client, a partire dal così detto *entry point*: l'elemento con id "app" in cui viene montata l'applicazione. Nel caso Javascript non sia abilitato nel client, il contenuto dell'applicazione non verrà visualizzato.

[^4]: [Github - React](https://github.com/facebook/react) - la più popolare in base numero di stars su Github.

## Typescript

Le basi di codice Javascript si allargarono dopo la 

	adozione di react in netflix, intstagam
	problemi di tipizzazine
		accesso a proprietà inesistenti
	presso microsoft
	anders hejlsberg
	tipizzazione statica


## Ritorno al server side rendering

	problemi
		search engine optimization
		velocità di caricamento pagine
	nextjs
