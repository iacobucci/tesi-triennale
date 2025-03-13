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

<!-- prettier-ignore-start -->
```typescript
export default defineEventHandler(async event => {
	const body = await readBody<UsersByLastName>(event);
	const lastName = body.lastName;
	const users = await User.find({ where: { lastName } });
	return { status: 200, body: { users } }
});
```

```html
<script setup lang="ts">
	const usersByLastName = reactive<UsersByLastName>({ lastName: "" });
	const { data, pending, error } = await useFetch("/api/users/byLastName", {
		method: "POST", body: usersByLastName, watch: [usersByLastName], lazy: true,
	});
</script>
<template>
	<input v-model="usersByLastName.lastName" />
	<ul>
		<li v-for="user in data.users">
			{{ user.firstName }} {{user.lastName}}
		</li>
	</ul>
</template>
```
<!-- prettier-ignore-end -->

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
Nuxt supporta anche altre modalità di rendering, come SSG e ISG, e queste possono essere combinate per ottenere una soluzione ibrida.
</div>

---

# TypeORM

-   Dispone di una CLI che supporta migrazioni e generazione di entità.
-   Supporta diversi adattatori per DBMS.
-   Le entità sono definite tramite classi Typescript, ed i tipi delle colonne sono inferiti dal tipo di variabile, e si possono dettagliare con decoratori.
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

Permettono di effettuare query CRUD con transazioni ACID.

<div class="horizontal" style="scale: 1.82; margin:100px">

<!-- prettier-ignore-start -->
```typescript
// CREATE
const newUser = new User();
newUser.username = "bob";
await newUser.save();

// READ
const authors = await User.find({
	where: [{ username: In("alice", "bob") }],
	relations: { posts: { likedBy: true } },
});

const usersWhoLikedAuthorsPostsWithDuplicates =
	authors.flatMap((author) =>
	author.posts.flatMap((post) => post.likedBy)
);

const usersWhoLikedAuthorsPosts = [
	...new Set(usersWhoLikedAuthorsPostsWithDuplicates),
];
```

```typescript
// CREATE
await User.createQueryBuilder()
	.insert()
	.into(User)
	.values({ username: "bob" })
	.execute();

// READ
const usersWhoLikedAuthorsPosts = await User
	.createQueryBuilder("user")
	.innerJoin("user.likedPosts", "likedPost")
	.innerJoin("likedPost.author", "author")
	.where("author.username IN (:...usernames)", {
		usernames: ["alice", "bob"],
	})
	.distinct(true)
	.getMany();
```
<!-- prettier-ignore-end -->

</div>

---

# AWS

Piattaforma cloud che offre servizi di calcolo, storage, database... usata per il deploy di applicazioni di esempio e studiata durante il Tirocinio curriculare.

<div style="max-height: 500px; scale: 0.8; translate: 0 -20px">

```yaml
Parameters:
    DBUsername:
        Type: String
    DBPassword:
        Type: String
        Description: Database master password

Resources:
    RDSInstance:
        Type: AWS::RDS::DBInstance
        Properties:
            MasterUsername: !Ref "DBUsername"
            MasterUserPassword: !Ref "DBPassword"

    EC2Instance:
        Type: AWS::EC2::Instance
        Properties:
            Environment:
                Variables:
                    DB_HOSTNAME: !GetAtt "RDSInstance.Endpoint.Address"
                    DB_USERNAME: !Ref "DBUsername"
                    DB_PASSWORD: !Ref "DBPassword"
```

</div>

---

<div class="container">

<div class="content">

## Architettura basata su container

-   **Elastic Container Service** per il deploy di container Docker: sempre attivi, quindi costi fissi, e scalabilità verticale.
-   Architettura **stateful**.
-   Database RDS, connessioni persistenti.

</div>

<div class="content">

## Architettura serverless

-   **Lambda** per l'esecuzione di funzioni serverless: costi "pay-as-you-go" e scalabilità orizzontale, ma soffrono di _cold start_.
-   Architettura **stateless**.
-   Database Aurora Serverless con proxy per pool di connessioni.

</div>

</div>

---

# Integrazione continua

Con **GitHub Actions** è possibile automatizzare il deploy su AWS.

Ad un push su `master` si attiva il workflow di CI/CD.

<div class="container">
<div class="content">
<div class="mermaid" style="width: 30%">
%%{init: {'theme': 'neutral' , 'gitGraph': {'mainBranchName': 'master'} } }%%
gitGraph
commit
branch dev
checkout dev
commit
commit
checkout master
merge dev
commit tag:"Deploy 1.0"
</div>
</div>
</div>

---

# Test di performance

<div class="horizontal">
<img src="res/100.png" style="padding:10px">
<img src="res/97.png" style="padding:10px">
<img src="res/100.png" style="padding:10px">
</div>

<div class="container">

|       Metrica        |   Server ECS    | Lambda a freddo | Lambda a caldo |
| :------------------: | :-------------: | :-------------: | :------------: |
|      FCP / LCP       |      0.4s       |      0.7s       |      0.6s      |
| Query Builder t/200r |      1.38s      |      0.38s      |     0.34s      |
| Active Record t/200r |      1.29s      |      1.00s      |     0.25s      |
|  costo esperimenti   | ($2.17) + $1.47 | ($2.17) + $0.01 |       -        |

</div>
