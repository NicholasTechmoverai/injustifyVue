import { io } from 'socket.io-client';

const socket = io('http://127.0.0.1:5000/inj', {
    transports: ['websocket'],  // Ensures WebSocket connection
});

socket.on('connect', () => {
    console.log('Connected to WebSocket server');
});

socket.on('disconnect', () => {
    console.log('Disconnected from WebSocket server');
});

socket.on('message', (data) => {
    console.log('Received:', data);
});


export default socket;
