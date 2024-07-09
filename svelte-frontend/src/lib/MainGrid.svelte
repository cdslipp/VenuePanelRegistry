<script>
	import { goto } from '$app/navigation';
	import Nav from './Nav.svelte';
	import LxSlider from '$lib/ui/LxSlider.svelte';

	let isLightsOn = false;

	async function toggleWorkLights() {
		try {
			const url = isLightsOn ? '/api/tplight/turn_off' : '/api/tplight/turn_on';
			const response = await fetch(`http://127.0.0.1:4999${url}`, {
				method: 'POST'
			});
			if (response.ok) {
				isLightsOn = !isLightsOn;
			} else {
				const result = await response.json();
				console.error('Error toggling work lights:', result.error);
			}
		} catch (error) {
			console.error('Error toggling work lights:', error);
		}
	}

	function navigateToPin() {
		goto('/pin');
	}
</script>

<Nav />
<section id="main-grid">
	<button id="showModeButton" on:click={navigateToPin}>
		<h2>SHOW MODE</h2>
	</button>
	<button class="nav-button" on:click={toggleWorkLights}>
		<div>
			<h2>{isLightsOn ? 'TURN OFF WORK LIGHTS' : 'TURN ON WORK LIGHTS'}</h2>
		</div>
	</button>
	<a href="/lights" class="nav-button" id="lighting-button">
		<div>
			<h2>LIGHTING</h2>
		</div>
	</a>
	<LxSlider lightSetName="tops" label="HOUSE LIGHTS" />
	<a href="/help" id="help-button" class="nav-button">
		<div>
			<h2>HELP</h2>
		</div>
	</a>
	<a href="/video/projector" id="video-button" class="nav-button">
		<div>
			<h2>VIDEO</h2>
		</div>
	</a>
</section>

<style>
	#main-grid {
		display: grid;
		margin: auto;
		padding: 0.2rem;
		width: 100%;
		min-height: 60vh;
		max-height: 70vh;
		grid-template-rows: repeat(3, 1fr);
		grid-template-columns: repeat(3, 1fr);
		grid-gap: 0.8em;
	}

	#main-grid a {
		text-decoration: none;
	}

	#main-grid a > div {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		border-radius: 1.5rem;
		padding: 0.2rem;
		position: relative;
		height: 100%;
		box-sizing: border-box;
	}

	#showModeButton {
		grid-column: 1 / span 2;
		font-size: 3rem;
		background-color: var(--orange);
		border-radius: var(--border-radius);
	}

	.nav-button {
		border-radius: var(--border-radius);
		text-decoration: none;
	}

	.nav-button h2 {
		color: var(--button-text);
	}

	#lighting-button {
		background-color: var(--blue);
		border-radius: var(--border-radius);
		grid-column: 1 / span 2;
	}

	#help-button {
		background-color: var(--yellow);
	}

	#video-button {
		background-color: var(--blue);
	}

	:global(#house-slider) {
		grid-column: 3;
	}
</style>
