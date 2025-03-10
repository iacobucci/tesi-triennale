## TypeORM

TypeORM è una libreria per ORM (Object-Relational Mapping) basata su Typescript, che permette di rappresentare le entità e le relazioni di un database relazionale in modo dichiarativo, e di eseguire operazioni _CRUD_ (Create, Read, Update, Delete) su di esse con API type-safe.

Il progetto, avviato nel 2016 da Umed Khudoiberdiev, è attualmente mantenuto da un team di sviluppatori che accettano contributi, all'indirizzo [github.com/typeorm/typeorm](github.com/typeorm/typeorm). La versione stabile corrente è la **0.3.20**, rilasciata nel gennaio 2024, ma lo sviluppo di versioni _nightly_ è in corso. Attualmente TypeORM è usato come dipendenza in quasi 400'000 progetti su Github.

Si può installare in un progetto Node con `npm install typeorm`, e richiede `typescript` con versione 4.5 o successiva, con le dichiarazioni di tipo `@types/node`. L'uso di TypeORM come libreria in un tag script di un file HTML non è supportato.

### Command line interface

Si può avviare un progetto con la CLI di TypeORM con `npx typeorm init --database <database>`, scegliendo tra i seguenti database: `mysql`, `mariadb`, `postgres`, `cockroachdb`, `sqlite`, `mssql`, `sap`, `spanner`, `oracle`, `mongodb`, `cordova`, `react-native`, `expo`, `nativescript`. Una volta che il progetto è configurato si possono eseguire i seguenti comandi:

#### `typeorm entity:create <percorso>`

Genera il file di una nuova entità in una directory specificata. Si tratta di un file Typescript che rappresenta una tabella del database, con i campi e le relazioni definite come proprietà della classe.

#### `typeorm schema:sync`

Sincronizza il database con le entità definite nel progetto.
Il protocollo di sincronizzazione è evidenziato nel diagramma di flusso sotto.

```mermaid {height=2cm}
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
graph LR;
    A[typeorm
	schema:sync] --> B{Il database esiste?};
    B -- No --> C[Crea il database];
    B -- Sì --> D{Le tabelle esistono?};
	C --> D;
    D -- No --> E[Crea le tabelle];
    D -- Sì --> F{Le colonne esistono?};
	E --> F;
    F -- No --> G[Crea le colonne];
    F -- Sì --> H[Modifica le colonne secondo le entità];
	classDef code font-family: monospace;
	class A code
```

#### `typeorm schema:drop`

Elimina tutte le tabelle del database.

#### `typeorm schema:log`

Stampa su _stdout_ le query SQL che verranno eseguite dal comando `schema:sync`.

#### `typeorm query <query>`

Esegue una query SQL sul database, nel dialetto del DBMS specificato.

#### `typeorm cache:clear`

Svuota la cache delle query.

#### `typeorm subscriber:create <percorso>`

Crea un nuovo subscriber, cioè una funzione che viene eseguita quando si verifica un evento sul database.

#### `typeorm migration:create <percorso>`

Crea un nuovo file di migrazione, che potrà essere utilizzato per sincronizzare il database successivamente.

#### `typeorm migration:run`

Esegue tutte le migrazioni pendenti, cioè le modifiche allo schema del database che non sono state ancora applicate.

#### `typeorm migration:show`

Stampa su stdout le migrazioni pendenti.

#### `typeorm migration:revert`

Annulla l'ultima migrazione eseguita.

#### `typeorm migration:generate <percorso>`

Genera una migration a partire dalle differenze tra le entità e le tabelle del database.

```mermaid {height=6.7cm}
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
graph LR
	subgraph Migrations
		direction LR
	subgraph Modifica schema
		direction TB
		A[Modifica
		schema] --> B{Schema del database aggiornato?}
		B -- No --> C[typeorm
		migration:generate]
		C --> D[File di
		migrazione
		con SQL]
		AA[typeorm
		migration:create] --> D
		D --> E[typeorm
		migration:run]
		B -- Sì --> F[Database
		sincronizzato]
	end
	subgraph Rollback
		direction TB
		E --Esegue SQL
		sul database--> F
		F --> G{Rollback
		necessario?}
		G -- Sì --> H[typeorm migration:revert]
		H -->|Annulla ultima migrazione| F
		G -- No --> I[Operazioni completate]
	end
	end
	classDef code font-family: monospace;
	class C,AA,E,H, code
```

> Diagramma di flusso delle migrazioni in TypeORM. L'esecuzione del SQL è specifica per il DBMS scelto, e può essere differente tra i vari database supportati.

### Collegamento con il database

TypeORM consente di lavorare con diversi DBMS (Database Management Systems), tra cui:

|        DBMS:         |  Relazionale?   | Server based? | Adattatore: |
| :------------------: | :-------------: | :-----------: | :---------: |
|   MySQL o MariaDB    |       ✅        |      ✅       |  `mysql2`   |
|      PostgreSQL      |       ✅        |      ✅       |    `pg`     |
|        SQLite        |       ✅        |    su file    |  `sqlite3`  |
|        Sql.js        |       ✅        |  in memoria   |  `sql.js`   |
| Microsoft SQL Server |       ✅        |      ✅       |   `mssql`   |
|       OracleDB       |       ✅        |      ✅       | `oracledb`  |
|       MongoDB        | ❌, a documenti |      ✅       |  `mongodb`  |
|       SAP Hana       |       ✅        |  in memoria   | `hdb-pool`  |
| Google Cloud Spanner |       ✅        |      ✅       |  `spanner`  |

Per effettuare la connessione con il database occorre installare l'adattatore mediante npm, e configurare un istanza di `DataSource` con le opzioni di accesso al database.

Ad esempio, in PostgreSQL:

```typescript
import { DataSource } from "typeorm";
import type { DataSourceOptions } from "typeorm";

let options: DataSourceOptions = {
	type: "postgres",
	host: "localhost",
	port: 5432,
	database: "dev",
	username: "dev",
	password: "dev",
	ssl: true,
	connectTimeoutMS: 10000,
	synchronize: true,
	logging: true,
	entities: [],
	migrations: [],
	subscribers: [],
};

const AppDataSource = new DataSource(options);
```

Le opzioni di connessione[^data-source-options] sono specifiche per ogni adattatore, ma quelle comuni sono:

-   `type: string`: il tipo di database, tra quelli supportati da TypeORM. In base a questo campo il compilatore Typescript inferirà il tipo specifico delle opzioni.
-   `entities: EntitySchema[]`: un array di classi che rappresentano le migrazioni del database
-   `migrations: Function[]`: un array di classi che rappresentano le migrazioni del database.
-   `subscribers: Function[]`: un array di classi che rappresentano i subscriber del database.
-   `synchronize: boolean`: indica se sincronizzare il database con le entità definite nel progetto.
-   `logging: boolean | ["query", "error", "schema", "warn", "info", "log"]`
    `| AbstractLogger`: abilita la stampa su stdout delle query SQL eseguite sul database durante l'esecuzione dell'applicazione e permette di specificare quali tipi di log abilitare o di passare un logger personalizzato.
-   `cache: boolean | {type: ["database", "redis", ...],options: {...} }`: abilita la cache delle query, con la possibilità di specificare il tipo di cache, tra le quali anche Redis.

Per i DBMS che richiedono una connessione a server, si aggiungono le opzioni:

-   `host: string`: l'indirizzo IP o il nome del server.
-   `port: number`: la porta del server.
-   `database: string`: il nome del database.
-   `username: string`: l'utente del database.
-   `password: string`: la password dell'utente.
-   `ssl: boolean`: abilita la connessione sicura.

In più, per PostgreSQL, si può specificare:

-   `connectTimeoutMS: number`: il tempo massimo di attesa per la connessione al server, in millisecondi.
-   `uuidExtension: boolean`: abilita l'estensione UUID di PostgreSQL.

[^data-source-options]: È possibile consultare quali opzioni sono disponibili per i vari adattatori [qui](https://typeorm.io/data-source-options).

In un'applicazione Typescript che viene impacchettata per l'utilizzo su client (browser) si può usare il modulo `typeorm/browser` per interagire con `indexedDB`, un database locale che è supportato da tutti i browser moderni, per memorizzare i dati in locale.

```typescript
import { DataSource } from "typeorm/browser";

const AppDataSource = new DataSource({
	type: "indexeddb",
	database: "mydb",
	entities: [],
	synchronize: true,
});
```

Successivamente si può inizializzare la connessione con il database con il metodo `initialize`, per iniziare a fare queries.

```typescript
export async function initialize() {
	try {
		if (!AppDataSource.isInitialized) {
			await AppDataSource.initialize();
			console.log("Typeorm inizializzato");
		}
	} catch (error) {
		console.error("Errore inizializzazione Typeorm", error);
		throw error;
	}
}
```

Questa operazione è asincrona, quindi si può usare `await` per attendere il completamento dell'inizializzazione, ed è da preferire eseguirla all'avvio dell'applicazione, per evitare errori di connessione al database durante l'esecuzione.

### Rappresentazione di entità

#### Entità

Una delle features principali di TypeORM è la possibilità di definire le entità del database come classi Typescript con _decoratori_[^decoratori], al contrario di altri ORM che usano un formato di configurazione esterno, come Prisma, o che usano un formato di configurazione interno, come Sequelize.

[^decoratori]: I decoratori sono funzioni che modificano il comportamento di una classe o di una funzione, aggiungendo o modificando proprietà o metodi. Sono stati introdotti in ES7 e sono supportati da Typescript.

È necessario installare uno _shim_ (una libreria che si interpone tra due API) per poter usare i decoratori di TypeORM, con `npm install reflect-metadata --save`.

È inoltre necessario configurare il compilatore typescript per supportare i decoratori, aggiungendo le seguenti opzioni al file `tsconfig.json`:

```json
{
	"compilerOptions": {
		"experimentalDecorators": true,
		"emitDecoratorMetadata": true
	}
}
```

Poi bisogna importare il modulo `reflect-metadata` globalmente in un file di entry del progetto:

```typescript
import "reflect-metadata";
```

Si potrà quindi definire la tabella `user`[^naming-strategy] con la classe `User`:

[^naming-strategy]: A riguardo, il paragrafo [Strategie di naming automatico](#strategie-di-naming-automatico).

```typescript
export class User {
	public id: number;
	public firstName: string;
	public lastName: string;
	public fullName(): string {
		return `${this.firstName} ${this.lastName}`;
	}
}
```

Poi si annota la classe con il decoratore `@Entity`:

```typescript
import { Entity } from "typeorm";
@Entity()
export class User {
	// ...
}
```

E successivamente si annotano i campi che si intende tradurre in colonne della tabella con il decoratore `@Column`:

```typescript
import { Entity, Column } from "typeorm";
@Entity()
export class User {
	@Column()
	public id: number;
	@Column()
	public firstName: string;
	@Column()
	public lastName: string;
	public fullName(): string {
		return `${this.firstName} ${this.lastName}`;
	}
}
```

In questo modo il tipo di dato da assegnare alla colonna è inferito automaticamente dal tipo della proprietà, e si può continuare ad usare il metodo `fullName` per ottenere il nome completo dell'utente.

Per rendere le entità persistenti si devono aggiungere i riferimenti delle classi ad un array nel campo `entities` delle opzioni di `DataSource`.

#### Entità annidate

Un'entità può supportare delle entità annidate, che sono rappresentate come proprietà di tipo `Entity`:

```typescript
import { Name } from "./Name";

@Entity()
export class User {
	@Column()
	id: number;

	@Column(() => Name)
	name: Name;
}
```

Dove `Name` è una classe che rappresenta un nome, con delle `@Column` sui campi da annidare.

```typescript
export class Name {
	@Column()
	first: string;

	@Column()
	last: string;
}
```

In questo modo la tabella risultante sarà:

```mermaid {height=3cm}
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
erDiagram
	user {
		number id
		varchar name_first
		varchar name_last
	}

```

Quindi si potrà accedere ai campi annidati con `user.name.first` e `user.name.last`, e per ogni entità che fa uso di `Name` si otterrà una riduzione della ridondanza del codice.

#### Polimorfismo delle entità

Le entità possono essere definite in modo polimorfico, cioè con una gerarchia di classi che condividono delle proprietà comuni.

Si inizia definendo un'entità padre `User`:

```typescript
@Entity()
export class User {
	@Column()
	id: number;

	@Column()
	firstName: string;

	@Column()
	lastName: string;
}
```

Poi si definiscono le entità figlie `Admin` e `Customer`:

```typescript
@Entity()
export class Supplier extends User {
	@Column()
	companyName: string;
}
```

```typescript
@Entity()
export class Customer extends User {
	@Column()
	shippingAddress: string;
}
```

Il diagramma delle tabelle risultante sarà:

```mermaid {height=3cm}
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
erDiagram
	user {
		number id
		varchar firstName
		varchar lastName
	}

	supplier {
		number id
		varchar firstName
		varchar lastName
		varchar companyName
	}

	customer {
		number id
		varchar firstName
		varchar lastName
		varchar shippingAddress
	}
```

L'ereditarietà è supportata ad un livello di profondità arbitrario.

È possibile usare anche il pattern di _Single table inheritance_ (STI), in cui tutte le entità figlie condividono la stessa tabella, e si usa un campo `type` per distinguere i diversi tipi di entità.

```typescript
@Entity()
@TableInheritance({ column: { type: "varchar", name: "type" } })
export class User {
	...
}

export class Supplier extends User {
	...
}

export class Customer extends User {
	...
}
```

Così facendo si otterrà un'unica tabella `user` con un campo `type` che può assumere i valori `Supplier` e `Customer`:

```mermaid {height=3cm}
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
erDiagram
	user {
		number id
		varchar firstName
		varchar lastName
		varchar type
		varchar companyName
		varchar shippingAddress
	}
```

#### Schemi

È anche possibile definire uno schema per le tabelle, senza l'utilizzo di decoratori, facendo utilizzo di interfacce Typescript e di classi EntitySchema con un parametro _generic_ dell'interfaccia in considerazione. l'esempio del paragrafo [entità annidate](#entità-annidate) può essere riscritto come:

```typescript
export interface Name {
	first: string;
	last: string;
}

export const NameEntitySchema = new EntitySchema<Name>({
	name: "name",
	columns: {
		first: { type: "varchar" },
		last: { type: "varchar" },
	},
});

export interface User {
	id: string;
	name: Name;
}

export const UserEntitySchema = new EntitySchema<User>({
	name: "user",
	columns: {
		id: { primary: true, type: "int", generated: true },
	},
	embeddeds: {
		name: { schema: NameEntitySchema, prefix: "name_" },
	},
});
```

Si passa un oggetto di tipo `EntitySchemaOptions` al costruttore di `EntitySchema`, che contiene le opzioni di configurazione della tabella, tra cui:

-   `name: string`: il nome della tabella.
-   `columns: EntitySchemaOptions<T>.columns`: un oggetto che mappa i nomi delle colonne, tipizzati come string literals, ad ulteriori opzioni della colonna, cioè ad un `EntitySchemaColumnOptions`. Ognuno di questi ha i campi:
    -   `type: ColumnType`: il tipo di dato della colonna, istanza di `ColumnType`.
    -   `primary?: boolean`: se la colonna è parte della chiave primaria, `false` di default.
    -   `generated?: boolean`: se il valore della colonna è generato automaticamente, `false` di default.
    -   `default?: any`: il valore di default della colonna.
-   `embeddeds: EntitySchemaColumnOptions[]`: un oggetto che mappa i nomi delle proprietà annidate ai loro schemi e ai prefissi delle colonne annidate. Per ogni proprietà annidata si deve definire:
    -   `schema: EntitySchema`: lo schema dell'entità annidata.
    -   `prefix: string`: il prefisso delle colonne annidate.

La tipizzazione forte è garantita anche nel caso degli schemi.

#### Proprietà delle colonne

Nelle `@Entity` si possono impostare proprietà delle colonne del database sempre mediante decoratori:

-   `@PrimaryGeneratedColumn()`: Chiave primaria generata automaticamente.
-   `@PrimaryColumn()`: Chiave primaria.
-   `@Column("int")`: Tipo di dato della colonna. Un `number` Typescript può essere mappato a `int` in SQL.
-   `@Column("varchar")` oppure `@Column("text")`: Tipo di dato della colonna. Una `string` Typescript può essere mappata a `varchar` o `text` in SQL.

Si possono aggiungere delle proprietà aggiuntive passando un oggetto di opzioni, di tipo `ColumnOptions`, al decoratore `@Column(options: ColumnOptions)`:

Alcune delle opzioni più comuni per PostgreSQL sono:

-   `type: ColumnType`: Il tipo di dato della colonna, istanza di `ColumnType`, tra i quali:
    -   `"int"`: Un intero a 32 bit.
    -   `"bigint"`: Un intero a 64 bit.
    -   `"varchar"`: Una stringa di lunghezza variabile.
    -   `"text"`: Una stringa di lunghezza arbitraria.
    -   `"boolean"`: Un valore booleano.
    -   `"date"`: Una data senza orario, in TypeScript un oggetto `Date`.
    -   `"timestamp"`: Una data e un orario, in TypeScript un oggetto `Date`.
    -   `"json"`: Un oggetto JSON. Con questo tipo si possono memorizzare oggetti complessi, come array e oggetti annidati, ma per le operazioni di ricerca e ordinamento. È preferibile usare un tipo di dato nativo del database.
    -   `"jsonb"`: Un oggetto JSON binario.
    -   `"enum"`: Un insieme di valori possibili. Si definisce con un array di stringhe, che viene tipizzato come uno _string literal type_, o anche con un enum Typescript. In entrambi i casi la tipizzazione è garantita.
-   `length: number`: La lunghezza massima della colonna, per i tipi `varchar` e `text`.
-   `nullable: boolean`: Se la colonna può avere valori nulli.
-   `default: any`: Il valore di default della colonna.
-   `unique: boolean`: Se i valori della colonna devono essere unici.
-   `primary: boolean`: Se la colonna è parte della chiave primaria.
-   `generated: boolean`: Se il valore della colonna è generato automaticamente.
-   `comment: string`: Un commento sulla colonna.

#### Migrations

Infine, per modificare lo schema del database, una volta che le entità sono definite, si possono creare delle migrazioni, che sono file Typescript che contengono le query SQL necessarie per modificare lo schema del database.

```typescript
import { MigrationInterface, QueryRunner } from "typeorm";

export class PostRefactoringTIMESTAMP implements MigrationInterface {
	async up(queryRunner: QueryRunner): Promise<void> {
		await queryRunner.query(
			`ALTER TABLE "user" RENAME COLUMN "lastname" TO "surname"`
		);
	}
	async down(queryRunner: QueryRunner): Promise<void> {
		await queryRunner.query(
			`ALTER TABLE "user" RENAME COLUMN "surname" TO "lastname"`
		);
	}
}
```

È anche disponibile l'API `QueryRunner`, che permette di astrarre parti di sintassi SQL specifiche per i vari DBMS, ma i parametri delle query non sono tipizzati.

```typescript
import { MigrationInterface, QueryRunner, TableColumn } from "typeorm";

export class PostRefactoringTIMESTAMP implements MigrationInterface {
	async up(queryRunner: QueryRunner): Promise<void> {
		await queryRunner.renameColumn("user", "lastname", "surname");
	}

	async down(queryRunner: QueryRunner): Promise<void> {
		await queryRunner.renameColumn("post", "surname", "lastname");
	}
}
```

La pratica di migrazione di database è tuttavia consigliata per modifiche in fase di produzione, perché aggiornare le entità di TypeORM e sincronizzare il database può portare a perdita di dati.

### Rappresentazione di relazioni

Dopo la definizione delle entità, si possono definire le relazioni tra di esse, seguendo le convenzioni del modello relazionale.

Si possono definire relazioni uno a uno con `@OneToOne`, relazioni uno a molti con `@OneToMany` e `@ManyToOne`, e relazioni molti a molti con `@ManyToMany`. Ogni decoratore per le relazioni, accetta un argomento `typeFunctionOrTarget` che specifica il tipo di entità correlata con una funzione che restituisce il `type`. Opzionalmente accetta un argomento `inverseSide`, che specifica la proprietà della relazione inversa, tramite una funzione che prende come argomento il tipo di entità corrente e restituisce il suo `field` che inverte la relazione. Si passa infine un oggetto `RelationOptions`, che permette di configurare la relazione con:

-   `cascade?: boolean | ("insert" | "update" | "remove" | "soft-remove" | "recover")[]`: specifica le operazioni che devono essere propagate alla relazione. Se `true`, tutte le operazioni di `insert`, `update` e `remove` sono propagate. Se `false`, nessuna operazione è propagata. Se un array di stringhe tra quelle accettabili, solo le operazioni specificate sono propagate. `false` di default.
-   `eager?: boolean`: se il caricamento della relazione deve essere eager, `true` di default.
-   `lazy?: boolean`: se il caricamento della relazione deve essere lazy.
-   `orphanedRowAction?: "nullify" | "delete" | "soft-delete" | "disable"`: specifica l'azione da intraprendere quando un'entità correlata è rimossa. Se `nullify`, la chiave esterna è impostata a `null`. Se `delete`, l'entità correlata è rimossa. Se `soft-delete`, l'entità correlata è marcata come eliminata. Se `disable`, l'entità correlata è marcata come disabilitata. `nullify` di default.

#### Relazioni uno a uno

Nell'esempio che segue, ogni utente ha un solo profilo, e ogni profilo è associato ad un solo utente. È impostato il `cascade` a `true`, in modo che le operazioni di `insert`, `update` e `remove` siano propagate solo nella direzione `User` -> `Profile`. Questo prevede che un profilo venga creato, aggiornato o rimosso solo quando un utente è già presente, e che un utente venga rimosso solo se il profilo è già stato rimosso.

È fatto uso di una colonna di join, `profile_id`, e punta alla tabella `profiles`. Si usa il decoratore `@JoinColumn()`, che accetta un oggetto di tipo `JoinColumnOptions` per specificare le opzioni della colonna di join, tra cui:

-   `name: string`: il nome della colonna di join.
-   `referencedColumnName: string`: il nome della colonna di riferimento.
-   `foreignKeyConstraintName: string`: il nome del vincolo di chiave esterna.

Questi parametri sono opzionali perché TypeORM usa delle convenzioni per inferire i nomi delle tabelle e delle colonne[^naming-strategy].

```typescript
@Entity()
export class User {
	@PrimaryGeneratedColumn()
	id: number;

	@Column()
	username: string;

	@OneToOne(() => Profile, (profile) => profile.user, {
		cascade: true,
	})
	@JoinColumn()
	profile: Profile;
}

@Entity()
export class Profile {
	@PrimaryGeneratedColumn()
	id: number;

	@Column()
	bio: string;

	@OneToOne(() => User, (user) => user.profile)
	user: User;
}
```

```mermaid {height=4.5cm}
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
erDiagram
    user ||--|| profile : has
    user {
        int id pk
		int profile_id fk
        string username
    }
    profile {
        int id pk
        string bio
    }
```

#### Relazioni uno a molti e molti a uno

Nell'esempio che segue, ogni utente può scrivere molti post, e ogni post è scritto da un solo utente. Dunque la tabella `posts` ha una chiave esterna `author_id` che punta alla tabella `users`.

```typescript
@Entity()
export class User {
	@PrimaryGeneratedColumn()
	id: number;

	@Column()
	username: string;

	@OneToMany(() => Post, (post) => post.author)
	posts: Post[];
}

@Entity()
export class Post {
	@PrimaryGeneratedColumn()
	id: number;

	@Column()
	content: string;

	@ManyToOne(() => User, (user) => user.posts)
	@JoinColumn()
	author: User;
}
```

```mermaid {height=4.5cm}
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
erDiagram
    user ||--o{ post : writes
    user {
        int id pk
        varchar username
    }
    post {
        int id pk
		int author_id fk
        varchar content
    }
```

#### Relazioni molti a molti

Nell'esempio che segue ogni post è scritto da un utente. Ogni utente può mettere "mi piace" a molti post, e ogni post può ricevere il "mi piace" da molti utenti. Viene generata una tabella di join `user_liked_posts`[^naming-strategy] ha due chiavi esterne, `user_id` e `post_id`, che puntano rispettivamente alle tabelle `users` e `posts`. La coppia di chiavi `user_id` e `post_id` è unica, quindi forma una chiave primaria composta per la tabella `user_liked_posts`.

In più ogni utente può avere molti amici, che sono altri utenti, quindi viene generata una tabella di join `user_friends` con due chiavi esterne, `user1_id` e `user2_id`, che puntano entrambe alla tabella `users`. La coppia di chiavi `user1_id` e `user2_id` è unica, quindi forma una chiave primaria composta per la tabella `user_friends`.

Ogni utente può seguire altri utenti, e può essere seguito da altri utenti. Quindi viene generata la tabella di join, `user_following`, con due chiavi esterne, `follower_id` e `following_id`, che puntano entrambe alla tabella `users`. La coppia di chiavi `follower_id` e `following_id` è unica, quindi forma una chiave primaria composta per la tabella `user_following`. Da questa tabella si può ottenere con efficienza sia l'elenco degli utenti seguiti da un utente, sia l'elenco degli utenti che seguono un utente.

È fatto uso di `@JoinTable()` per specificare il nome della tabella di join e le colonne che la compongono. È passato un oggetto di tipo `JoinTableOptions`, che permette di configurare la tabella di join con:

-   `name: string`: il nome della tabella di join.
-   `joinColumn: JoinColumnOptions`: le opzioni per la colonna di join.
-   `inverseJoinColumn: JoinColumnOptions`: le opzioni per la colonna di join inversa, con gli stessi campi di `joinColumn`.
-   `database: string`: il nome del database in cui creare la tabella di join.
-   `synchronize: boolean`: se sincronizzare la tabella di join con il database, `true` di default.

```typescript
@Entity()
export class User {
	@PrimaryGeneratedColumn()
	id: number;

	@Column()
	username: string;

	@OneToMany(() => Post, (post) => post.author)
	posts: Post[];

	@ManyToMany(() => Post, (post) => post.likedBy)
	likedPosts: Post[];

	@ManyToMany(() => User, (user) => user.friends)
	@JoinTable({
		name: "user_friends",
		joinColumn: {
			name: "user1_id",
			referencedColumnName: "id",
		},
		inverseJoinColumn: {
			name: "user2_id",
			referencedColumnName: "id",
		},
	})
	friends: User[];

	@ManyToMany(() => User, (user) => user.followers)
	@JoinTable({
		name: "user_following",
		joinColumn: {
			name: "follower_id",
			referencedColumnName: "id",
		},
		inverseJoinColumn: {
			name: "following_id",
			referencedColumnName: "id",
		},
	})
	following: User[];

	@ManyToMany(() => User, (user) => user.following)
	followers: User[];
}

@Entity()
export class Post {
	@PrimaryGeneratedColumn()
	id: number;

	@Column()
	content: string;

	@ManyToOne(() => User, (user) => user.posts)
	@JoinColumn()
	author: User;

	@ManyToMany(() => User, (user) => user.likedPosts)
	@JoinTable()
	likedBy: User[];
}
```

```mermaid {height=7cm}
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
erDiagram
    user {
      int id PK
      varchar username
    }
    post {
      int id PK
	  int author_id FK
      varchar content
    }
    user_liked_posts {
      int user_id FK
      int post_id FK
    }
    user_friends {
      int user1_id FK
      int user2_id FK
    }
    user_following {
      int follower_id FK
      int following_id FK
    }

    user ||--o{ user_liked_posts : "likes"
    post ||--o{ user_liked_posts : "likedBy"

	post ||--o{ user : "writes"

    user ||--o{ user_friends : "friends"
    user ||--o{ user_friends : "friends"

    user ||--o{ user_following : "following"
    user ||--o{ user_following : "followers"
```

#### Eager e lazy loading

Il caricamento delle relazioni può essere configurato come _eager_ o _lazy_.

Con un caricamento eager le entità correlate vengono caricate insieme all'entità principale, in un'unica query SQL. Questo può essere utile quando si prevede che le entità correlate verranno sempre usate insieme all'entità principale, ma può portare ad inefficienze se queste sono molte o pesanti.

```typescript
@Entity()
export class User {
	@ManyToMany(() => Post, (post) => post.likedBy, { eager: true })
	@JoinTable()
	likedPosts: Post[];
}

@Entity()
export class Post {
	@ManyToMany(() => User, (user) => user.likedPosts, { eager: true })
	likedBy: User[];
}
```

Al contrario, con un caricamento lazy le entità correlate vengono caricate solo quando vengono effettivamente usate. Le entità correlate sono memorizzate come `Promise`, che se risolte restituiscono l'entità correlata. Durante la risoluzione della `Promise` viene eseguita una query SQL per recuperare l'entità correlata.

```typescript
@Entity()
export class User {
	@ManyToMany(() => Post, (post) => post.likedBy, { lazy: true })
	@JoinTable()
	likedPosts: Promise<Post[]>;
}

@Entity()
export class Post {
	@ManyToMany(() => User, (user) => user.likedPosts, { lazy: true })
	likedBy: Promise<User[]>;
}
```

Internamente TypeORM usa delle `Proxy` Javascript per intercettare gli accessi alle proprietà lazy, in modo concettualmente analogo a:

```typescript
user.likedPosts = new Proxy(Promise.resolve([]), {
	get(target, prop) {
		if (!target.__loaded) {
			target.__loaded = true;
			target.__data = databaseQuery(
				"SELECT * FROM post WHERE userId = ?",
				user.id
			);
		}
		return Reflect.get(target.__data, prop);
	},
});
```

#### Strategie di naming automatico

Per le definizioni sopra riportate, i nomi delle tabelle e delle colonne possono essere inferiti da TypeORM, seguendo delle convenzioni di naming automatico. Queste convenzioni possono essere sovrascritte con delle opzioni specifiche, passate ai decoratori delle entità e delle colonne, ma di default sono:

-   Il nome delle tabella è il nome della classe, in minuscolo e con gli spazi sostituiti da `_`.
-   Il nome delle colonne è il nome della proprietà, in minuscolo e con gli spazi sostituiti da `_`.
-   Il nome di tabelle di join è il nome delle entità coinvolte, in ordine `primario_secondario`, in minuscolo e con gli spazi sostituiti da `_`.
-   Il nome delle chiavi esterne è il nome della tabella di riferimento, in minuscolo e con gli spazi sostituiti da `_`, seguito dal nome del suo campo chiave.

Si può assegnare un'oggetto di classe che implementa `NamingStrategyInterface` al campo `namingStrategy` di `DataSource`, come ad esempio:

```typescript
import { NamingStrategyInterface, DefaultNamingStrategy } from "typeorm";
import { snakeCase } from "typeorm/util/StringUtils";

export class CustomNamingStrategy
	extends DefaultNamingStrategy
	implements NamingStrategyInterface
{
	tableName(
		targetName: string,
		userSpecifiedName: string | undefined
	): string {
		return userSpecifiedName || snakeCase(targetName);
	}

	columnName(
		propertyName: string,
		customName: string,
		embeddedPrefixes: string[]
	): string {
		return customName || snakeCase(propertyName);
	}
}
```

#### Listeners e subscribers

È fornita un'API per definire _listeners_ e _subscribers_ per le entità, che permettono di eseguire del codice in risposta a eventi specifici, come il caricamento di un'entità dal database.

###### Listeners

Si può definire un listener che ascolta un'evento su un'entità specifica, usando i decoratori `@BeforeLoad`, `@AfterLoad`, `@BeforeInsert`, `@AfterInsert`, `@BeforeUpdate`, `@AfterUpdate`, `@BeforeRemove`, `@AfterRemove`. Ad esempio:

```typescript
@Entity()
export class Post {
	@AfterLoad() {
		console.log("Post con contenuto: ", this.content, " caricato");
	}

	@Column()
	content: string;
}
```

Tuttavia non si possono eseguire query a database senza garanzia di risoluzione di corse critiche. Per ovviare a questo problema si possono usare i subscribers.

###### Subscribers

Un subscriber ha la stessa funzione di un listener, ma è definito come una classe che implementa l'interfaccia `EntitySubscriberInterface<Entity>`. Si possono definire metodi per gestire gli eventi di un'entità specifica, e si può fare query a database in modo asincrono. Ad esempio:

```typescript
@EventSubscriber()
export class PostSubscriber implements EntitySubscriberInterface<Post> {
	listenTo() {
		return Post;
	}

	afterLoad(event: LoadEvent<Post>) {
		console.log("Post con contenuto: ", event.entity.content, " caricato");
		// query a database ...
	}
}
```

### Query

TypeORM fornisce diverse API per eseguire query CRUD , oltre a supportare transazioni ACID. Typescript garantisce la type safety fino a momento di compilazione: è possibile scrivere metodi ed interfacce che usano le classi delle entità per garantire che gli inserimenti da parte dell'utente siano corretti a tempo di esecuzione. TypeORM fornisce un sistema di _sanitization_ dei dati, ma la responsabilità di garantire la correttezza dei dati, quando ad esempio si tratta di validare un indirizzo email, rimane a carico dello sviluppatore.

Ad ogni entità allegata al DataSource è associato un _repository_, che permette di eseguire query. Il risultato di queste è incapsulato in una `Promise`, che può essere risolta con `await` per ottenere il risultato effettivo. Ogni transazione garantisce che tutte le operazioni al suo interno vengano eseguite con successo o nessuna di esse venga applicata, evitando stati inconsistenti del database. L'isolamento da corse di lettura e scrittura è garantito dalle transazioni, anche risolvendo parallelamente le promise con `Promise.all()`.

Sono supportati due pattern principali: Active Record per eseguire query CRUD direttamente sulle entità, e Query Builder per costruire query SQL in modo programmatico. È inoltre disponibile un API per eseguire query SQL direttamente.

#### Active record

Il pattern Active Record, per la prima volta introdotto da Ruby on Rails, permette di eseguire operazioni CRUD in modo coerente al paradigma ad oggetti. In TypeORM ogni classe `Entity` che rappresenta un'entità del database che estende `BaseEntity` ed è associata staticamente ad un oggetto `DataSource`, ha a disposizione i seguenti:

###### Metodi statici:

-   `getRepository(): Repository<Entity>`: restituisce il repository dell'entità.
-   `find(conditions?: FindManyOptions<Entity>): Promise<Entity[]>`: trova tutte le entità che soddisfano le condizioni specificate.
-   `findOne(conditions?: FindOneOptions<Entity>): Promise<Entity>`: trova tutte le entità che soddisfano le condizioni specificate.
-   `count(conditions?: FindOptionsWhere<Entity>): Promise<number>`: conta il numero di entità che soddisfano le condizioni specificate.
-   `sum(field: string, conditions?: FindOptionsWhere<Entity>): Promise<number>`: calcola la somma dei valori di un campo specificato delle entità che soddisfano le condizioni specificate.
-   `createQueryBuilder(alias?: string): SelectQueryBuilder<Entity>`: restituisce un `SelectQueryBuilder` per costruire query SQL in modo programmatico.

###### Metodi di istanza:

-   `save(): Promise<Entity>`: salva l'entità nel database. Se l'entità ha un campo `id` già valorizzato, viene eseguito un `UPDATE`, altrimenti viene eseguito un `INSERT`.
-   `remove(): Promise<Entity>`: rimuove l'entità dal database. Viene eseguito un `DELETE`.
-   `reload(): Promise<Entity>`: ricarica l'entità dal database. Viene eseguito un `SELECT` in base alla primary key dell'entità.

Un `FindOneOptions<Entity>` è un oggetto che mappa i nomi delle colonne alle condizioni di ricerca, ed è tipizzato tramite il generic `Entity`: Il compilatore Typescript controlla che le colonne sulle quali si effettua la ricerca siano effettivamente presenti nell'entità. Le opzioni che rende disponibili sono:

-   `select: FindOptionsSelect<Entity>`: specifica i campi da selezionare. È un oggetto che mappa i campi di un oggetto di tipo `Entity` a `true` o `false`, per selezionare o meno il campo. Se non è specificato, vengono selezionati tutti i campi. Inoltre, non tutti i campi devono essere presenti: `Entity` viene passato attraverso un _partial_ Typescript[^partial-typescript].
-   `where: FindOptionsWhere<Entity>[]`: specifica le condizioni di ricerca. È un oggetto o un array di oggetti che mappano i campi di un oggetto di tipo `Entity` a delle operazioni di ricerca, e possono anche essere annidati per specificare condizioni complesse, con operatori logici e di confronto. Di default le operazioni sono in OR. Ogni campo di tipo `T` di `Entity` è essere mappato a un oggetto di tipo `T | FindOperator<T>` che specifica l'operatore di confronto.
-   `relations: FindOptionsRelations<Entity>`: specifica le relazioni da caricare in j oin insieme all'entità principale. È un oggetto che ha campi parziali di `Entity` che sono stati decorati con `@ManyToOne`, `@OneToOne`, `@OneToMany` o `@ManyToMany`.
-   `order: FindOptionsOrder<Entity>`: specifica l'ordine con cui le colonne vengono restituite, con degli string literals: `"asc"`, `"desc"`. È analogo a `ORDER BY` in SQL.

[^partial-typescript]: Un oggetto di tipo `Partial<T>` è un oggetto che ha le stesse proprietà di `T`, ma con valori opzionali. Nelle definizioni di TypeORM i campi opzionali sono ottenuti con `[P in keyof Entity]?:`, un _mapped type_ al quale viene applicato l'operatore `?`.

La classe `FindManyOptions<Entity>` estende `FindOneOptions<Entity>` e aggiunge le seguenti opzioni:

-   `take: number`: specifica il numero massimo di entità da restituire. È analogo a `LIMIT` in SQL.
-   `skip: number`: specifica l'offset delle entità da restituire. È analogo a `OFFSET` in SQL. In combinazione con `take` permette di paginare i risultati.

Un `FindOperator<T>` è un oggetto che mappa un operatore di confronto a un valore di tipo `T`, e permette di specificare condizioni logiche:

-   `And<T>`: Specifica che tutte le condizioni devono essere soddisfatte.
-   `Or<T>`: Specifica che almeno una delle condizioni deve essere soddisfatta.
-   `Not<T>`: Specifica che la condizione deve essere negata.

e di confronto:

-   `Equal<T>`: specifica che il campo deve essere uguale al valore specificato.
-   `LessThan<T>`: specifica che il campo deve essere minore del valore specificato.
-   `LessThanOrEqual<T>`: specifica che il campo deve essere minore o uguale al valore specificato.
-   `MoreThan<T>`: specifica che il campo deve essere maggiore del valore specificato.
-   `MoreThanOrEqual<T>`: specifica che il campo deve essere maggiore o uguale al valore specificato.
-   `In<T>`: specifica che il campo deve essere uno dei valori specificati.
-   `Like<T>`: specifica che una stringa deve corrispondere ad un pattern specificato. Il pattern può contenere i caratteri jolly `%` e `_`.

Il workflow per operazioni CRUD in Active record segue il diagramma:

```mermaid {height=6cm}
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
graph LR;
	definizione[Definizione di Entità]-->creazione[Creazione di un'oggetto Entity]
	creazione-->relazioni{Aggiunta di relazioni}
	relazioni-->salvataggio[Salvataggio]
	definizione-->find[Find]
	find-->modifica{Modifica dei campi}
	modifica-->relazioni
	modifica-->salvataggio
	find-->relazioni
	find-->delete{Delete}
	find-->consumazione[Consumazione dell'oggetto]
	delete-->salvataggio
```

Un esempio sulle entità definite nel paragrafo [Relazioni molti a molti](#relazioni-molti-a-molti), è il seguente:

```typescript
// Aggiungi un nuovo utente
const newUser = new User();
newUser.username = "bob";
await newUser.save();

// Trova tutti gli utenti
const allUsers = await User.find();

// Trova l'utente con username "alice"
const alice = await User.findOne({ where: { username: "alice" } });

// Trova un post caricando gli utenti a cui piace ed aggiungi Alice
const postWithLikes = await Post.findOne({
	where: { id: 1 },
	relations: { likedBy: true },
});
postWithLikes.likedBy.push(alice);
await postWithLikes.save();

// Carica gli utenti che hanno messo "mi piace" ai post di Alice o di Bob
const authors = await User.find({
	where: [{ username: In("alice", "bob") }],
	relations: { posts: { likedBy: true } },
});

const usersWhoLikedAuthorsPosts: User[] = authors.flatMap((author) =>
	author.posts.flatMap((post) => post.likedBy)
);
```

#### Query builder

Per efficientare una query complessa, che fa join su più tabelle, si può usare l'API Query Builder, che fa uso del pattern implementativo _Builder_ per costruire una query SQL vincolandone la grammatica ai metodi disponibili.

Si parte dall'oggetto DataSource e si ottiene una repository relativa all'entità, con `getRepository(Entity)`, da questa si accede a `createQueryBuilder(), che restituisce un'istanza di `QueryBuilder<Entity>`, i cui metodi principali sono:

-   `execute(): Promise<any>`: esegue la query e restituisce il risultato.
-   `select(): SelectQueryBuilder<Entity>`: costruisce una query di selezione.
-   `insert(): InsertQueryBuilder<Entity>`: costruisce una query di inserimento.
-   `update(): UpdateQueryBuilder<Entity>`: costruisce una query di aggiornamento.
-   `delete(): DeleteQueryBuilder<Entity>`: costruisce una query di eliminazione.
-   `relation(entity: Entity, property: string): RelationQueryBuilder<Entity>`: costruisce una query per manipolare relazioni.

Ognuno di questi builder estende `QueryBuilder<Entity>` ed ha a disposizione dei metodi che ricalcano la sintassi SQL.

```mermaid {height=5.2cm}
%%{init: {'theme': 'neutral', 'mirrorActors': false} }%%
classDiagram
    class QueryBuilder~Entity~ {
        +getSql() string
        +execute() Promise~any~
		+select() SelectQueryBuilder~Entity~
		+insert() InsertQueryBuilder~Entity~
		+update() UpdateQueryBuilder~Entity~
		+delete() DeleteQueryBuilder~Entity~
		+relation(entity: Entity, property: string) RelationQueryBuilder~Entity~
    }

    class SelectQueryBuilder~Entity~ {
        +from(entity: Entity, alias: string) this
        +where(condition: string, parameters?: any) this
        +andWhere(condition: string, parameters?: any) this
        +orWhere(condition: string, parameters?: any) this
        +orderBy(sort: string, order?: "ASC"|"DESC") this
        +groupBy(group: string) this
        +having(having: string) this
        +limit(limit: number) this
        +offset(offset: number) this
        +innerJoin(property: string, alias: string) this
        +leftJoin(property: string, alias: string) this
        +leftJoinAndSelect(property: string, alias: string) this
        +getOne() Promise~Entity~
        +getMany() Promise~Entity[]~
    }

    class InsertQueryBuilder~Entity~ {
        +into(entity: Entity) this
        +values(values: any) this
        +execute() Promise~InsertResult~
    }

    class UpdateQueryBuilder~Entity~ {
        +update(entity: Entity) this
        +set(values: any) this
        +where(condition: string, parameters?: any) this
        +execute() Promise~UpdateResult~
    }

    class DeleteQueryBuilder~Entity~ {
        +delete() this
        +from(entity: Entity) this
        +where(condition: string, parameters?: any) this
        +execute() Promise~DeleteResult~
    }

    class RelationQueryBuilder~Entity~ {
        +of(entity: Entity) this
        +add(items: Entity[]) Promise~void~
        +remove(items: Entity[]) Promise~void~
    }

    QueryBuilder <|-- SelectQueryBuilder
    QueryBuilder <|-- InsertQueryBuilder
    QueryBuilder <|-- UpdateQueryBuilder
    QueryBuilder <|-- DeleteQueryBuilder
    QueryBuilder <|-- RelationQueryBuilder
```

Per query complesse, Query Builder si basa su _alias_ per le tabelle coinvolte, cioè stringhe che identificano le tabelle in modo univoco all'interno della query. Gli alias sono passati come argomento ai metodi di join e di selezione, e vengono usati per specificare le colonne e le condizioni di ricerca. Questo meccanismo permette di costruire query SQL con più livelli di join, ma è prono ad errori di battitura, potenzialmente difficili da individuare durante un debug. L'utilizzo di costanti per gli alias, definite all'inizio del file, può aiutare a ridurre il rischio di errori.

Lo stesso esempio del paragrafo [Active record](#active-record), dove le entità estendono `BaseEntity` per rendere disponibile il metodo `createQueryBuilder()`, può essere riscritto con Query Builder come segue:

```typescript
const USER = "user";
const POST = "post";
// Aggiungi un nuovo utente
User.createQueryBuilder()
	.insert()
	.into(User)
	.values({ username: "bob" })
	.execute();

// Trova tutti gli utenti
const allUsers = await User.createQueryBuilder().getMany();

// Trova l'utente con username "alice"
const alice = await User.createQueryBuilder(USER)
	.select()
	.where(USER + ".username = :username", { username: "alice" })
	.getOne();

// Trova un post caricando gli utenti a cui piace ed aggiunge Alice
const postWithLikes = await Post.createQueryBuilder(POST)
	.leftJoinAndSelect(POST + ".likedBy", "likedBy")
	.where(POST + ".id = :id", { id: 1 })
	.getOne();

await Post.createQueryBuilder()
	.relation(Post, "likedBy")
	.of(postWithLikes)
	.add(alice);

// Carica gli utenti che hanno messo "mi piace" ai post di Alice o di Bob
const usersWhoLikedAuthorsPosts = await User.createQueryBuilder("user")
	.innerJoin("user.likedPosts", "likedPost")
	.innerJoin("likedPost.author", "author")
	.where("author.username IN (:...usernames)", {
		usernames: ["alice", "bob"],
	})
	.distinct(true)
	.getMany();
```

Le differenze principali con Active Record sono:

-   Query Builder è più verboso, ma permette di costruire query complesse in modo più flessibile, che sono più efficienti e vicine al modello relazionale.
-   L'aggiunta di entità a relazioni molti a molti in Active Record avviene in memoria, e non persiste fino a quando non si chiama `save()` sull'entità principale. Query Builder manipola direttamente la relazione nel database.
-   In Query Builder si possono applicare metodi di aggregazione, come `distinct()`, invece che scorrere in memoria un array di risultati intermedi, che contiene anche elementi da scartare.

#### Query SQL raw

Infine TypeORM rende disponibile un'API per eseguire query SQL interpolate direttamente in stringhe con il metodo `query(query: string, parameters?: any[])` di `EntityManager`. L'unica astrazione fornita in questo caso è la sanificazione dei parametri, che previene attacchi di SQL injection. Lo stesso esempio riportato sopra può essere riscritto con query SQL come segue:

```typescript
// Aggiungi un nuovo utente
await dataSource.query(`
  INSERT INTO "user" ("username")
  VALUES ('bob');
`);

// Trova tutti gli utenti
const allUsers = await dataSource.query(`
  SELECT * FROM "user";
`);

// Trova l'utente con username "alice"
const [alice] = await dataSource.query(`
  SELECT * FROM "user"
  WHERE "username" = 'alice'
  LIMIT 1;
`);

// Trova un post caricando gli utenti a cui piace
const [postWithLikes] = await dataSource.query(`
  SELECT p.*, u.*
  FROM "post" p
  LEFT JOIN "post_likes" pl ON p.id = pl.post_id
  LEFT JOIN "user" u ON pl.user_id = u.id
  WHERE p.id = 1;
`);

// Aggiungi Alice ai like del post
await dataSource.query(
	`
  INSERT INTO "post_likes" ("post_id", "user_id")
  VALUES (?, ?);`,
	[postWithLikes.id, alice.id]
);

// Carica gli utenti che hanno messo "mi piace" ai post di Alice o di Bob
const usersWhoLikedAuthorsPosts = await dataSource.query(`
  SELECT DISTINCT u.*
  FROM "user" u
  INNER JOIN "post_likes" pl ON u.id = pl.user_id
  INNER JOIN "post" p ON pl.post_id = p.id
  INNER JOIN "user" author ON p.author_id = author.id
  WHERE author.username IN ('alice', 'bob');
`);
```

Query come queste massimizzano le prestazioni che si possono ottenere con un database relazionale, al costo di una maggiore probabilità di errori di battitura. L'utilizzo di costanti per le tabelle e le colonne, definite all'inizio del file, può aiutare a ridurre questo rischio.
