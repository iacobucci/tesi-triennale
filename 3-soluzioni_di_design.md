# Soluzioni di design

## Architettura del cloud e integrazione continua

AWS scelto per la sua flessibilità e scalabilità, e per continuazione di tirocinio

### Infrastruttura dei servizi cloud AWS

cloudformation

> ![Setup](./res/aws-1-setup.png){width=90%}

> ![Infrastructure](./res/aws-2-infrastructure.png){width=90%}

> ![Service](./res/aws-3-infrastructure.png){width=90%}

### Continuous Integration e Continuous Deployment con Github Actions

github actions

> ![Impostazione dei secrets di github](./res/aggiunta-secrets.png){width=70%}

tempi di provisioning

> ![Creazione stack](./res/actions-creazione-stack.png){width=70%}

> ![Aggiornamento stack](./res/actions-aggiornamento.png){width=70%}

## Un'applicazione di esempio con Nuxt e TypeORM

utilizzo di componenti shadcn

### Implementazione di un plugin Nuxt per TypeORM

scelte di progetto

### Design patterns per il riutilizzo del modello dei dati

## Analisi di performance e sicurezza

### Deploy dell'applicazione SSR su server distribuiti con ECS ed RDS

scala orizzontale, aggiunta di nodi

### Deploy dell'applicazione SSG su CDN statica con funzioni Lambda e Aurora

scala verticale, parallelismo [^serverless]

[^serverless]: [Serverless architectures](https://martinfowler.com/articles/serverless.html) - Articolo di Mike Roberts sul blog di Martin Fowler che descrive

### Analisi di performance

In questo capitolo si illustrano alcune soluzioni di design per la realizzazione di applicazioni web con Nuxt in combinazione con TypeORM.
