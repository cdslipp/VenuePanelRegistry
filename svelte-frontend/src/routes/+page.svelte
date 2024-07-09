<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import Locked from '$lib/Locked.svelte';
	import MainGrid from '$lib/MainGrid.svelte';
	import io from 'socket.io-client';

	let showMode = false;
	let previousShowMode = showMode;
	const socket = io('http://localhost:4999');

	onMount(() => {
		socket.on('connect', () => {
			console.log('Connected to server');
		});

		socket.on('show_mode', (data) => {
			console.log('Show mode data received:', data);
			showMode = data.showMode;
		});

		socket.on('disconnect', () => {
			console.log('Disconnected from server');
		});

		socket.on('connect_error', (error) => {
			console.error('Connection error:', error);
		});

		return () => {
			socket.off('show_mode');
			socket.off('connect');
			socket.off('disconnect');
			socket.off('connect_error');
		};
	});

	function toggleShowMode() {
		socket.emit('toggle_show_mode');
	}

	$: if (showMode !== previousShowMode) {
		startTransition();
		previousShowMode = showMode;
	}

	async function startTransition() {
		if (document.startViewTransition) {
			await new Promise((resolve) => {
				document.startViewTransition(async () => {
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
