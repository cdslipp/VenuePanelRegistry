<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import io from 'socket.io-client';

	import Locked from '$lib/Locked.svelte';
	import MainGrid from '$lib/MainGrid.svelte';

	let showMode = false;
	const socket = io('http://127.0.0.1:4999');

	onMount(() => {
		socket.on('connect', () => {
			console.log('Connected to server');
		});

		socket.on('show_mode', (data) => {
			showMode = data.showMode;
		});

		return () => {
			socket.off('show_mode');
			socket.off('connect');
		};
	});

	function toggleShowMode() {
		socket.emit('toggle_show_mode');
	}

	let previousShowMode = showMode;

	$: if (showMode !== previousShowMode) {
		startTransition();
		previousShowMode = showMode;
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
</script>

<button on:click={toggleShowMode}>
	{showMode ? 'Turn Show Mode Off' : 'Turn Show Mode On'}
</button>

{#if showMode}
	<Locked />
{:else}
	<MainGrid />
{/if}
