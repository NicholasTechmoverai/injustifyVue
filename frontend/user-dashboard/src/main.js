


import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/styles.css';
import WebSocketService from './services/websocket.js'; // WebSocket
import { createPinia } from 'pinia'; // Import Pinia
import './registerServiceWorker'
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faHouse, faClock, faCloudDownloadAlt, faBell, faHeart, faCog, faSignInAlt, faMusic, faMoon, faSun, faExclamationCircle } from '@fortawesome/free-solid-svg-icons';
library.add(faHouse, faClock, faCloudDownloadAlt, faBell, faHeart, faCog, faSignInAlt, faMusic, faMoon, faSun, faExclamationCircle);
//import './assets/tailwind.css'




const app = createApp(App);
app.component('font-awesome-icon', FontAwesomeIcon); // Register component globally

//setupuserdetails(); // Uncomment this line to enable user authentication


app.use(router); // Register the router
app.use(createPinia()); // Register Pinia store
app.mount('#app'); // Mount the app

WebSocketService.connect(); // Initialize WebSocket service
