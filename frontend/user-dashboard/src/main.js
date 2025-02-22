import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/styles.css';
import WebSocketService from './services/websocket.js'; // WebSocket
import { createPinia } from 'pinia'; // Import Pinia
import './registerServiceWorker'
//import './assets/tailwind.css'




const app = createApp(App);

//setupuserdetails(); // Uncomment this line to enable user authentication


app.use(router); // Register the router
app.use(createPinia()); // Register Pinia store
app.mount('#app'); // Mount the app

WebSocketService.connect(); // Initialize WebSocket service
