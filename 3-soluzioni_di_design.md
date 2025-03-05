# Soluzioni di design

## Architettura del cloud e integrazione continua

### Progettazione dell'infrastruttura dei servizi cloud AWS

> ![Setup](./res/aws-1-setup.png){width=90%}

> ![Infrastructure](./res/aws-2-infrastructure.png){width=90%}

> ![Service](./res/aws-3-infrastructure.png){width=90%}

### Continuous Integration e Continuous Deployment con Github Actions

> ![Impostazione dei secrets di github](./res/aggiunta-secrets.png){width=70%}

> ![Creazione stack](./res/actions-creazione-stack.png){width=70%}

> ![Aggiornamento stack](./res/actions-aggiornamento.png){width=70%}

## Un'applicazione di esempio con Nuxt e TypeORM

### Implementazione di un plugin Nuxt per TypeORM

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

```typescript
import { AppDataSource, initialize } from "~/server/utils/datasource";

export default defineNitroPlugin(async () => {
	initialize();
});
```

### Design patterns per il riutilizzo del modello dei dati

## Analisi di performance e sicurezza

### SSR su server distribuiti con ECS ed RDS

#### Test di carico

#### Audit di rendimento lato client

### SSG su CDN statica con funzioni Lambda e Aurora
