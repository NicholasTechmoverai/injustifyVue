<template>
  <div class="MainContainer">
    <h3>Notifications for {{ useremail }}</h3>
    <ul>
      <li v-for="notif in notifications" :key="notif.id">
        {{ notif.message }} - {{ notif.date }}
      </li>
    </ul>
    <div>
      <h2>WebSocket Messages:</h2>
      <ul>
        <li v-for="(msg, index) in messages" :key="index">{{ msg }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineProps } from 'vue';
import axios from 'axios';
import socket from '@/services/websocket'; // Use one WebSocket service

const props = defineProps(['useremail']);
const notifications = ref([]);
const messages = ref([]);

// Fetch notifications from backend
const fetchNotifications = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/notifications/${props.useremail}`);
    notifications.value = response.data.notifications;
  } catch (error) {
    console.error("Error fetching notifications:", error);
  }
};

onMounted(() => {
  fetchNotifications(); // Initial API fetch

  // Listen for WebSocket messages
  socket.on('message', (data) => {
    messages.value.push(data);
  });

  // Listen for real-time notifications
  socket.on('new_notification', (notif) => {
    notifications.value.unshift(notif); // Add new notification at top
  });

  socket.emit('join', { user: props.useremail }); // Example event
});

onUnmounted(() => {
  socket.off('message');
  socket.off('new_notification'); // Cleanup listeners
});
</script>
