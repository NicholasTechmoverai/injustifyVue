<template>
  <div>
    <h3>Notifications for {{ useremail }}</h3>
    <ul>
      <li v-for="notif in notifications" :key="notif.id">
        {{ notif.message }} - {{ notif.date }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';
import WebSocketService from '../websocket.js';

export default {
  name: "UserNotifications",
  props: ['useremail'],
  data() {
    return { notifications: [] };
  },
  mounted() {
    // Fetch initial notifications from the backend
    axios.get(`http://127.0.0.1:5000/api/notifications/${this.useremail}`)
      .then(response => this.notifications = response.data.notifications)
      .catch(error => console.error(error));

    // Connect WebSocket for real-time updates
    WebSocketService.connect();

    // Listen for incoming notifications
    WebSocketService.socket.onmessage = (event) => {
      const newNotification = JSON.parse(event.data);
      this.notifications.unshift(newNotification); // Add to the top of the list
    };
  }
};
</script>
