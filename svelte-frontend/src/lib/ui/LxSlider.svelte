<script>
	import { onMount } from 'svelte';
	import io from 'socket.io-client';

	export let lightSetName;
	export let label;

	const socket = io('http://127.0.0.1:4999');
	let percentage = 0;

	onMount(() => {
		socket.on('connect', () => {
			console.log('Connected to server');
		});

		socket.on('light_levels', (data) => {
			if (data[lightSetName] !== undefined) {
				percentage = data[lightSetName];
			}
		});

		return () => {
			socket.off('light_levels');
			socket.off('connect');
		};
	});

	function cycleLightLevel() {
		const levels = [25, 50, 75, 100, 75, 50, 25, 0];
		let currentIndex = levels.indexOf(percentage);
		if (currentIndex === -1 || currentIndex === levels.length - 1) {
			currentIndex = 0;
		} else {
			currentIndex += 1;
		}
		const newLevel = levels[currentIndex];
		updateLightLevel(newLevel);
	}

	async function updateLightLevel(level) {
		try {
			const response = await fetch(
				`http://127.0.0.1:4999/api/set_light_level/${lightSetName}/${level}`,
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					}
				}
			);

			if (response.ok) {
				console.log(`Light level set to ${level}`);
				console.log(await response.json());
			} else {
				const result = await response.json();
				throw new Error(result.error || 'An error occurred while setting the light level');
			}
		} catch (error) {
			console.error('Error setting light level:', error);
		}
	}
</script>

<div id="{lightSetName}-slider" class="slider-wrapper">
	<button on:click={cycleLightLevel}>
		<h3>{label}</h3>
		<span>{percentage}%</span>
	</button>
</div>

<style>
	.slider-wrapper {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100%;
		background-color: var(--SliderColor);
		border-radius: 1.5rem;
	}

	button {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
		background: transparent;
		border: none;
		color: white;
		font-size: 2rem;
		cursor: pointer;
	}

	button:focus {
		outline: none;
	}

	h3 {
		margin: 0;
	}

	span {
		font-size: 3rem;
	}
</style>
