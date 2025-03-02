# Soluzioni di design

soluzioni implementative ... tirocinio... 


## Architettura del cloud e integrazione continua

### Infrastruttura dei servizi cloud

> ![Setup](./res/aws-1-setup.png){width=90%}

> ![Infrastructure](./res/aws-2-infrastructure.png){width=90%}

> ![Service](./res/aws-3-infrastructure.png){width=90%}


### Integrazione continua e deployment

> ![Impostazione dei secrets di github](./res/aggiunta-secrets.png){width=70%}


## Analisi di performance e sicurezza

> ![Creazione stack](./res/actions-creazione-stack.png){width=70%}

> ![Aggiornamento stack](./res/actions-aggiornamento.png){width=70%}



In questo capitolo si illustrano alcune soluzioni di design per la realizzazione di applicazioni web con Nuxt in combinazione con TypeORM.


```html
<script setup lang="ts">
import { User } from "~/entities/User";

definePageMeta({
	prerender: true,
})

// query diretta nel lato ssr
const { data: users } = await useAsyncData('users', async () => {
	// questa chiamata a useAsyncData non è risolvibile a build time
	console.log("Server side only");
	try {
		let users = await User.find(); // undefined
		// le funzioni di active record per typeorm sono tree-shaked e non vengono incluse nel bundle
		return users
	} catch (error) {
		console.error(error);
	}
	return [];
}, {
	// Impedisce la ri-esecuzione lato client
	server: true,
});
</script>

<template>
	<div>
		<li v-for="user in users">
			{{ user.fullName() }}
		</li>
	</div>
</template>
```

## Applicazione che usa Nuxt e typeORM

### Strumenti dell'editor di testo
#### Language server


[^serverless]: [Serverless architectures](https://martinfowler.com/articles/serverless.html) - Articolo di Mike Roberts sul blog di Martin Fowler che descrive 

