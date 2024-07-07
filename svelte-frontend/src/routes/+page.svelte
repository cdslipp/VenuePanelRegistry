<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { showMode, toggleShowMode } from '$lib/websocket';
	import Locked from '$lib/Locked.svelte';
	import MainGrid from '$lib/MainGrid.svelte';

	let localShowMode = $showMode;

	let previousShowMode = localShowMode;

	$: if (localShowMode !== previousShowMode) {
		startTransition();
		previousShowMode = localShowMode;
	}

	async function startTransition() {
		if (document.startViewTransition) {
			await new Promise((resolve) => {
				document.startViewTransition(async () => {
					// force Svelte to re-render the DOM by invalidating the page store
					page.set($page);
					resolve();
				});
			});
		}
	}

	$: $showMode;
</script>

<button on:click={toggleShowMode}>
	{$showMode ? 'Turn Show Mode Off' : 'Turn Show Mode On'}
</button>

{#if $showMode}
	<Locked />
{:else}
	<MainGrid />
{/if}
