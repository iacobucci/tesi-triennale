---
marp: true
paginate: true
description: Sviluppo ed analisi delle prestazioni di applicazioni web basate su Nuxt e TypeORM su servizi cloud AWS
---

<!-- _paginate: false -->

<h1>Sviluppo ed analisi delle prestazioni di applicazioni web basate su Nuxt e TypeORM su servizi cloud AWS</h1>

<script src="../node_modules/mermaid/dist/mermaid.min.js"></script>
<script>mermaid.initialize({startOnLoad:true, theme:"neutral", mirrorActors:false});</script>

<link rel="stylesheet" href="res/styles.css">
<link rel="stylesheet" href="../node_modules/@fortawesome/fontawesome-free/css/fontawesome.min.css">

<div class="container">
<div class="horizontal">
<img src="res/nuxt.png" alt="Nuxt logo" style="max-width: 240px">
<img src="res/typeorm.png" alt="TypeORM logo" style="max-width: 240px">
<img src="res/aws.png" alt="AWS logo" style="max-width: 240px">
</div>
</div>

---

## Obiettivi

### Allestimento di un framework di sviluppo mirato a

-   Uso dei componenti come unità di codice riutilizzabile.
-   Separazione delle preoccupazioni tra programmazione dell'app e mantenimento dell'infrastruttura.
-   Utilizzo di linguaggi e pattern type-safe.

### Ottimizzazione di metriche di rendimento del frontend

-   Search Engine Optimization (SEO).
-   First/Largest Contentful Paint ([F/L]CP).
-   Cumulative Layout Shift (CLS).

---

# Nuxt

Framework per Applicazioni Web full-stack basato su Vue.js e Nitro.

<div class="container">
<div class="content">

```txt
components/
composables/
layouts/
pages/
public/

server/
	api/
	functions/
	plugins/

test/
app.vue
nuxt.config.ts
package.json
```

</div>
<div class="content">
<div class="mermaid" style="width: 60%">
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
flowchart TB
subgraph vue[**View**]
direction LR
vueview[**View**]
vueviewmodel[**ViewModel**]
vuemodel[**Model**]
vueview <--> vueviewmodel
vueviewmodel --> vuemodel
vuemodel -.-> vueviewmodel
end
model[**Model** ]
controller[**Controller**]
controller -- Accesso CRUD --> model
model -.-> controller
vue -- Richiesta utente --> controller
controller -.-> vue
</div>
</div>
</div>

---

<h2 style="translate: 0px -30px">Modalità di rendering</h2>

<div class="container">
<div class="horizontal">

<div class="content">
<div style="translate:-50px -110px">
Client Side Rendering
</div>

<div class="mermaid" style="width: 70%; padding-right: 60px">
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
sequenceDiagram
participant client as Client
participant frontend as CDN
participant backend as Server API
client->>frontend: Richiesta pagina
frontend-->>client: DOM minimo
frontend-->>client: Bundle Javascript
client->>client: Esecuzione dell'app Vue
client->>backend: Richieste dati o assets
backend-->>client: Dati JSON o binari
client->>client: Aggiornamento della pagina
</div>
</div>

<div class="content">
<div style="translate:50px -110px">
Server Side Rendering
</div>

<div class="mermaid" style="width: 70%; padding-left: 60px">
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
sequenceDiagram
participant client as Client
participant frontend as Server Frontend
participant backend as Server API
client->>frontend: Richiesta pagina
frontend->>backend: Richieste dati
backend-->>frontend: Dati JSON
frontend->>frontend: Rendering HTML completo
frontend-->>client: HTML completo + JS bundle
client->>client: Hydration (interattività)
client->>backend: Richieste dati o assets
backend-->>client: Dati JSON o binari
client->>client: Aggiornamento della pagina
</div>
</div>
</div>
</div>

<div style="translate: 0px 40px">
Nuxt supporta anche altre modalità di rendering, come Static Site Generation (SSG), e queste possono essere combinate per ottenere una soluzione ibrida.
</div>

---

# TypeORM

-   Dispone di una CLI che supporta migrazioni e generazione di entità.
-   Supporta diversi adattatori per DBMS.
-   Le entità sono definite tramite classi Typescript, ed i tipi delle colonne sono inferiti dal tipo di variabile.
-   Si possono definire relazioni `@ManyToOne`, `@OneToMany`, `@ManyToMany` e `@OneToOne`. A queste si associano delle colonne o tabelle di join con `@JoinTable` e `@JoinColumn`.

<div class="container">
<div class="horizontal">
<img src="res/sqlite.png" alt="Nuxt logo" style="max-width: 240px">
<img src="res/sqljs.png" alt="Nuxt logo" style="max-width: 240px">
<img src="res/mysql.png" alt="Nuxt logo" style="max-width: 240px">
<img src="res/postgresql.png" alt="Nuxt logo" style="max-width: 240px">
<img src="res/mongodb.png" alt="Nuxt logo" style="max-width: 240px">
</div>
</div>

---

## Active Record e Query Builder

<div class="horizontal">

```typescript

```

```typescript
const usersWhoLikedAuthorsPosts = await User.createQueryBuilder("user")
	.innerJoin("user.likedPosts", "likedPost")
	.innerJoin("likedPost.author", "author")
	.where("author.username IN (:...usernames)", {
		usernames: ["alice", "bob"],
	})
	.distinct(true)
	.getMany();
```

</div>

---

# AWS

---

## Architettura basata su container

---

## Architettura serverless

---

# Integrazione continua

---

# Test di performance

-   ***
