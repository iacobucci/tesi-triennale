# Linee evolutive

## Pagine statiche (1991 $\rightarrow$)

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

- **Linaguaggi di basso livello** come C o C++, di difficile gestione e manutenzione;
	- Sono performanti ma richiedono una solida conoscenza informatica.

- **Linguaggi di scripting** come Perl o Shell UNIX, più facili da utilizzare ma meno efficienti;
	- Comodi per la manipolazione di stringhe e file, ma non per la gestione di strutture dati complesse.

- Successivamente, dal 1995 in poi, **Linguaggi di templating** come PHP o JSP, che consentono di incorporare codice dinamico all'interno di pagine HTML.
	- Java Server Pages (JSP) è un'estensione di Java, quindi era possibile usare tutte le librerie di questo linguaggio molto popolare all'epoca.
	- PHP è un linguaggio interpretato che ha avuto molto successo per oltre un decennio[^1] grazie alla sua semplicità.

Un esempio di pagina di autenticazione in PHP:
```php
<?php
$username = $_POST["username"];
$password = $_POST["password"];

$query = sprintf( "SELECT * FROM utenti WHERE username='%s' AND password='%s'", $username, $password);
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
È da notare come il codice HTML da inviare al browser sia inserito direttamente all'interno del codice PHP, rendendone difficile la manutenzione per via della *confusione tra logica di presentazione e logica di business*. Inoltre ci sono evidenti problemi di sicurezza legati all'interpolazione di stringhe all'interno di query SQL.

[^1]: [Indice TIOBE per PHP](https://www.tiobe.com/tiobe-index/php/), si può vedere come il suo utilizzo sia diminuito a partire dal 2010.

## Pagine attive con Javascript (1995 $\rightarrow$)

Il dinamismo delle pagine web supportato da server CGI e linguaggi di scripting era comunque limitato per via del caricamento di nuove pagine ad ogni richiesta. Non era possibile aggiornare solo una parte della pagina, ma solo l'intera pagina. Nel 1995 il browser Netscape Navigator introdusse il supporto ad un nuovo linguaggio di scripting, Javascript, per ovviare a questo problema.

##### Gestione di eventi e manipolazione del DOM

Uno script Javascript, distribuito all'interno di una pagina HTML, può essere eseguito dal browser web in risposta a determinati eventi, come il click di un bottone o la pressione di un tasto. Inizialmente il motore di esecuzione era sincrono, cioè bloccava l'esecuzione del codice fino al completamento dell'operazione, e la istruzioni per la risposta agli eventi erano inserite in funzioni dette di *callback*.

Javascript può manipolare il DOM (Document Object Model) della pagina, cioè la rappresentazione ad albero della struttura della pagina, per aggiungere, rimuovere o modificare elementi HTML.

##### Richieste HTTP asincrone (1999 $\rightarrow$)
Le pagine web, erano diventate *attive*, ma tutti gli script da fornire agli utenti dovevano essere inseriti nella pagina inviata come prima risposta HTTP. Nel 1999, il browser Internet Explorer 5 introdusse una estensione del linguaggio Javascript, che disponeva di un oggetto chiamato `XMLHttpRequest`, in grado effettuare richieste HTTP asincrone al server e di ricevere risposte senza dover ricaricare l'intera pagina.



## Node.js e Javascript lato server (2009 $\rightarrow$)

## Applicazioni web orientate a componenti (2011 $\rightarrow$)

### React.js

### Vue.js

	react.js
		nato iome progetto trasversale da ingegneri di react
	angular.js
	vue.js
		nato come progetto personale di evan you



## Typescript (2012 $\rightarrow$)

	problemi di tipizzazine
		accesso a proprietà inesistenti
	presso microsoft
	anders hejlsberg
	tipizzazione statica


## Ritorno al server side rendering (2016 $\rightarrow$)

	problemi
		search engine optimization
		velocità di caricamento pagine
	nextjs
