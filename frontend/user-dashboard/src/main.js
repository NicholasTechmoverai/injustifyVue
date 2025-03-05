import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/styles.css';
import WebSocketService from './services/websocket.js'; // Import WebSocket service
import { createPinia } from 'pinia';
import './registerServiceWorker';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faHouse, faClock, faCloudDownloadAlt, faBell, faHeart, faCog, faSignInAlt, faMusic, faMoon, faSun, faExclamationCircle } from '@fortawesome/free-solid-svg-icons';

library.add(faHouse, faClock, faCloudDownloadAlt, faBell, faHeart, faCog, faSignInAlt, faMusic, faMoon, faSun, faExclamationCircle);

const app = createApp(App);
app.component('font-awesome-icon', FontAwesomeIcon);
app.use(router);
app.use(createPinia());
app.config.globalProperties.$socket = WebSocketService; // ✅ Attach WebSocket globally
app.mount('#app');

// ✅ Start WebSocket connection
WebSocketService.connect();
