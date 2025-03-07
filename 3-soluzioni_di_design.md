# Soluzioni di design

Vengono esposte delle soluzioni progettuali ed implementative per la realizzazione di un'applicazione web con le tecnologie dettagliate nel capitolo precedente, Nuxt e TypeORM, in combinazione con i servizi cloud AWS, sui quali ho lavorato durante il tirocinio curriculare presso l'azienda Soluzioni Futura s.r.l., ora Polarity s.r.l.

## Architettura del cloud e integrazione continua

Amazon web services è una piattaforma che offre una _PaaS_, platform as a service, dove sono messi a disposizione servizi di calcolo, di storage e di database; ma anche una _IaaS_, infrastructure as a service, che permette di configurare reti di calcolatori virtuali accessibili via internet.

Per utilizzare AWS è necessario registrarsi (come root user dell'account) accedendo alla dashboard online ([https://aws.amazon.com/it/console/](https://aws.amazon.com/it/console/)).

### Progettazione dell'infrastruttura dei servizi cloud AWS

cloud che offre una vasta gamma di servizi, tra cui servizi di calcolo, storage, database, machine learning, sicurezza e molti altri. Per la realizzazione di un'applicazione web, si possono utilizzare i servizi di calcolo, storage e database per creare un'infrastruttura scalabile e resiliente.

Le architetture esposte di seguito possono essere personalizzate per soddisfare le esigenze di un'applicazione e del suo team di sviluppo modificando i template Cloudformation forniti nelle directory `cloudformation/` dei progetti di esempio.

Entrambe le architetture espongono servizi HTTP, ma non forniscono un DNS personalizzato. Per aggiungere un DNS personalizzato, è possibile utilizzare il servizio Route 53 di AWS.

#### Architettura basata su container

a partire da [^aws-template]

[^aws-template]: [AWS CloudFormation Starter Workflow for GitHub Actions](https://github.com/aws-samples/aws-cloudformation-starter-workflow-for-github-actions)

> ![](./res/aws-2-infrastructure.png){width=90%}

> ![Service](./res/aws-3-infrastructure.png){width=90%}

#### Architettura serverless

Con serverless si intende un'architettura che non richiede agli sviluppatori di gestire l'infrastruttura sottostante, ma si basa su servizi cloud che non necessitano configurazioni di rete[^serverless].

[^serverless]: [Serverless architectures](https://martinfowler.com/articles/serverless.html) - Articolo di Mike Roberts sul blog di Martin Fowler.

> ![Setup](./res/aws-4-serverless.png){width=90%}

### Continuous Integration e Continuous Deployment con Github Actions

Il team di sviluppo dovrà solamente configurare la propria repository per l'integrazione continua, aggiungendo l'ID dell'account AWS che intendono utilizzare e le credenziali del database, che potranno essere usate per connettersi al database in fase di debug.

Nelle repository ho realizzato

Connessione della repository ad un _role_ AWS con permessi limitati mediante OpenID Connect.

è presente anche uno script di setup che permette di creare dei roles

> ![Stack di setup per connessione OIDC alla repository](./res/aws-1-setup.png){width=90%}

> ![Impostazione dei secrets di github](./res/aggiunta-secrets.png){width=70%}

Nel caso dell'architettura basata su container, il workflow di Github Actions si occuperà di fare:

1. Checkout del codice sorgente
1. Login ad AWS
1. Deploy dello stack `infrastructure.yml` con Cloudformation
1. Login al registry ECR creato dallo stack
1. Build, tag e push dell'immagine Docker su ECR
1. Deploy dello stack `service.yml` con Cloudformation
1. Stampa dell'url del servizio e del database

Nel caso dell'architettura serverless, il workflow di Github Actions si occuperà di fare:

1. Checkout del codice sorgente
1. Login ad AWS
1. Creazione, se non esiste, di un Bucket S3 per il salvataggio del codice della Lambda
1. Installazione delle dipendenze
1. Build del progetto
1. Creazione di un file zip con il `.output` della build
1. Caricamento del file zip su S3
1. Deploy dello stack Cloudformation
1. Stampa dell'url del servizio e del database

Una prima metrica di performance della soluzione software è il tempo di completamento del workflow di Github Actions, che può essere monitorato nella dashboard "Actions" della repository.

I dati che ho rilevato sono

| Architettura | Tempo di creazione | Tempo di aggiornamento |
| :----------: | :----------------: | :--------------------: |
|  Container   |      14m 58s       | 5m 30s                 |
|  Serverless  |       6m 30s       | 1m                     |

## Un'applicazione di esempio con Nuxt e TypeORM

Nelle repositories

### Design patterns per il riutilizzo del modello dei dati

### Implementazione di TypeORM in Nuxt

lifecycles di Nuxt

Le task di ECS si comportano come server stateful, in quanto dopo l'avvio tendono a rimanere attivi fino alla loro terminazione manuale. Anche in caso di guasti, il servizio ECS si riavvia automaticamente e la continuità del servizio è garantita in quanto TypeORM si collegherà nuovamente al database.

L'istanza di DataSource è esportata per essere utilizzata in altri moduli del progetto, come una funzione asincrona `initialize()`

```typescript
const options =
	process.env.NODE_ENV === "production"
		? {
				type: "postgres",
				host: process.env.DB_HOSTNAME,
				database: process.env.DB_NAME,
				port: parseInt(process.env.DB_PORT || "5432"),
				username: process.env.DB_USERNAME,
				password: process.env.DB_PASSWORD,
				ssl: { rejectUnauthorized: false },
				synchronize: false,
				logging: true,
				entities, // array di classi delle entità
				migrations: [],
				subscribers: [],
		  }
		: {
				type: "sqlite",
				database: ":memory:",
				synchronize: true,
				logging: true,
				entities,
				migrations: [],
				subscribers: [],
		  };

export const AppDataSource = new DataSource(options);

export async function initialize() {
	try {
		if (!AppDataSource.isInitialized) {
			await AppDataSource.initialize();
			console.log("Typeorm inizializzato", {
				type: AppDataSource.options.type,
				database: AppDataSource.options.database,
			});
		}
	} catch (error) {
		console.error("Errore inizializzazione Typeorm", error);
		throw error;
	}
}
```

Un **plugin** in `~/server/plugins/typeorm.ts`:

```typescript
import { AppDataSource, initialize } from "~/server/utils/datasource";

export default defineNitroPlugin(async () => {
	initialize();
});
```

Per servizi stateless l'approccio è diverso: ad ogni richiesta ad api bisogna assicurarsi che la connessione al database sia attiva. Non basterebbe inizializzare la connessione all'avvio della funzione Lambda, per via delle sue

attendere la connessione. Con pool di connessioni si può fare in modo che queste siano riutilizzate.

## Analisi di performance e sicurezza

### SSR su server distribuiti con ECS ed RDS

#### Test di carico

#### Audit di rendimento lato client

### SSR su CDN statica con funzioni Lambda e Aurora

#### Test di carico

soffre di cold start

#### Audit di rendimento lato client

### Query Active record e Query Builder
