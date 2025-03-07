# Soluzioni di design

Vengono esposte delle soluzioni progettuali ed implementative per la realizzazione di un'applicazione web con le tecnologie dettagliate nel capitolo precedente, Nuxt e TypeORM, in combinazione con i servizi cloud AWS, sui quali ho lavorato durante il tirocinio curriculare presso l'azienda Soluzioni Futura s.r.l., ora Polarity s.r.l.
## Architettura del cloud e integrazione continua

### Progettazione dell'infrastruttura dei servizi cloud AWS

Amazon web services è una piattaforma cloud che offre una vasta gamma di servizi, tra cui servizi di calcolo, storage, database, machine learning, sicurezza e molti altri. Per la realizzazione di un'applicazione web, si possono utilizzare i servizi di calcolo, storage e database per creare un'infrastruttura scalabile e resiliente.

Connessione della repository ad un *role* AWS con permessi limitati mediante OpenID Connect.

> ![Setup](./res/aws-1-setup.png){width=90%}

#### Architettura ECS

> ![Infrastructure](./res/aws-2-infrastructure.png){width=90%}

> ![Service](./res/aws-3-infrastructure.png){width=90%}

#### Architettura Lambda

> ![Setup](./res/aws-4-serverless.png){width=90%}

### Continuous Integration e Continuous Deployment con Github Actions

Il team di sviluppo dovrà solamente configurare la propria repository per l'integrazione continua, aggiungendo l'ID dell'account AWS che intendono utilizzare e le credenziali del database, che potranno essere usate per connettersi al database in fase di debug.

> ![Impostazione dei secrets di github](./res/aggiunta-secrets.png){width=70%}

> ![Creazione stack](./res/actions-creazione-stack.png){width=70%}

> ![Aggiornamento stack](./res/actions-aggiornamento.png){width=70%}

## Un'applicazione di esempio con Nuxt e TypeORM

### Design patterns per il riutilizzo del modello dei dati


### Implementazione TypeORM in Nuxt


lifecycles di Nuxt



server stateful


```typescript
import { DataSource } from "typeorm";

import { Message } from "~/entities/Message";
import { Post } from "~/entities/Post";
import { User } from "~/entities/User";

// Inserire le classi delle entità qui
let entities = [User, Message, Post];

const options = {
	type: "postgres",
	host: process.env.DB_HOSTNAME,
	database: process.env.DB_NAME,
	port: parseInt(process.env.DB_PORT || "5432"),
	username: process.env.DB_USERNAME,
	password: process.env.DB_PASSWORD,
	ssl: { rejectUnauthorized: false },
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

Per servizi stateless l'approccio è diverso: ad ogni richiesta ad api bisogna attendere la connessione. Con pool di connessioni si può fare in modo che queste siano riutilizzate.

## Analisi di performance e sicurezza

### SSR su server distribuiti con ECS ed RDS

#### Test di carico

#### Audit di rendimento lato client

### SSR su CDN statica con funzioni Lambda e Aurora

#### Test di carico

soffre di cold start

#### Audit di rendimento lato client

### Query Active record e Query Builder
