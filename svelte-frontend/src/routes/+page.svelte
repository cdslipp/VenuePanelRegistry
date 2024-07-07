<script>
	import { onMount } from 'svelte';
	let message = '';

	onMount(async () => {
		const res = await fetch('http://127.0.0.1:4999/api/hello');
		const data = await res.json();
		message = data.message;
	});
</script>

<h1>Welcome to SvelteKit</h1>

{#if message}
	<p>{message}</p>
{:else}
	<p>Loading...</p>
{/if}
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
