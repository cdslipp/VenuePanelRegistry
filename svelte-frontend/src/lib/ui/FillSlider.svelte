<script>
	import { onMount } from 'svelte';

	export let label;
	export let percentage;
	let containerHeight = 0;
	let contentHeight = 0;
	let initialFillBottom = 0;
	let scrollY = 0;

	onMount(() => {
		initialFillBottom = calculateInitialFillBottom();
	});

	function onScroll(event) {
		const scrolled = event.currentTarget.scrollTop;
		const scrollableHeight = (contentHeight - containerHeight) * 2;
		const newPercentage = Math.min(100, Math.max(0, (scrolled / scrollableHeight) * 100));
		percentage = newPercentage;
	}

	function calculateInitialFillBottom() {
		return contentHeight - containerHeight;
	}

	function updateFill(newPercentage) {
		const duration = 500;
		const start = Date.now();

		const scrollableHeight = (contentHeight - containerHeight) * 2;
		const targetScrollTop = (newPercentage / 100) * scrollableHeight;
		const currentScrollTop = document.querySelector('.slider-container').scrollTop;
		const distanceToScroll = targetScrollTop - currentScrollTop;

		const animateScroll = () => {
			const timePassed = Date.now() - start;
			const progress = Math.min(timePassed / duration, 1);

			const scrollTop = currentScrollTop + distanceToScroll * progress;
			document.querySelector('.slider-container').scrollTop = scrollTop;

			if (progress < 1) {
				requestAnimationFrame(animateScroll);
			} else {
				percentage.set(newPercentage);
			}
		};

		requestAnimationFrame(animateScroll);
	}
</script>

<svelte:window bind:scrollY />

<div class="slider-wrapper">
	<div class="slider-labels">
		<h3>{label}</h3>
		<span>{percentage.toFixed(0)}%</span>
	</div>
	<div
		class="slider-container"
		on:scroll={onScroll}
		on:click={() => updateFill(percentage === 0 ? 100 : 0)}
		bind:clientHeight={containerHeight}
		role="slider"
	>
		<div class="slider-content" bind:clientHeight={contentHeight}>
			<div
				class="slider-fill"
				style="height: {containerHeight}px; bottom: -{initialFillBottom}px"
			/>
		</div>
	</div>
</div>

<style>
	.slider-wrapper {
		position: relative;
		height: 100%;
		width: 100%;
		border-radius: 1.5rem;
		background-color: var(--SliderColor);
	}
	.slider-container {
		overflow-y: scroll;
		height: 100%;
		width: 100%;
		scroll-behavior: smooth;
		border-radius: 1.5rem;
		padding: 0px;
	}

	.slider-container::-webkit-scrollbar {
		display: none;
	}

	.slider-content {
		overflow: visible;
		position: relative;
		scroll-behavior: smooth;
		height: 150%;
		padding: 0px;
	}

	.slider-fill {
		position: absolute;
		left: 0;
		right: 0;
		padding: 0px;
		background-color: var(--OnColor);
	}

	.slider-labels {
		position: absolute;
		width: 100%;
		height: 100%;
		z-index: 10;
		color: white;
		pointer-events: none;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		align-items: center;
	}

	.slider-labels h3 {
		color: var(--button-text);
		font-family: var(--main-font);
		font-size: 2rem;
		text-align: center;
	}

	.slider-labels span {
		color: var(--button-text);
		font-family: var(--main-font);
		font-weight: 200;
		font-size: 3.2rem;
		padding-bottom: 1rem;
	}
</style>
