import { writable } from 'svelte/store';
import io from 'socket.io-client';

const showMode = writable(false);
const socket = io('http://127.0.0.1:4999');

socket.on('connect', () => {
	console.log('Connected to server');
});

socket.on('show_mode', (data) => {
	showMode.set(data.showMode);
});

export function toggleShowMode() {
	socket.emit('toggle_show_mode');
}

export { showMode };
