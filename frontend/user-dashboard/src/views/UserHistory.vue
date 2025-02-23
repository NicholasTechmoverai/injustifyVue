<script setup>
import { ref, onMounted, onUnmounted, defineProps, computed } from "vue";
import axios from "axios";
import socket from "@/services/websocket"; // WebSocket service
import { useUserStore } from "@/store/index.js";

const props = defineProps(["useremail"]);
const notifications = ref([]);
const messages = ref([]);

const userStore = useUserStore();
const iscollapsedBig = computed(() => userStore.iscollapsedBig);

// Fetch notifications from backend
const fetchNotifications = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:5000/api/notifications/${props.useremail}`
    );
    notifications.value = response.data.notifications;
  } catch (error) {
    console.error("Error fetching notifications:", error);
  }
};

onMounted(() => {
  fetchNotifications(); // Initial API fetch

  // Listen for WebSocket messages
  socket.on("message", (data) => {
    messages.value.push(data);
  });

  // Listen for real-time notifications
  socket.on("new_notification", (notif) => {
    notifications.value.unshift(notif); // Add new notification at top
  });

  socket.emit("join", { user: props.useremail }); // Example event
});

onUnmounted(() => {
  socket.off("message");
  socket.off("new_notification"); // Cleanup listeners
});
</script>

<style scoped>
/* Temporary Styling */
.notifications-container {
  width: calc(100% - 270px);
  margin-left: 270px;
  padding: 20px;
  transition: all 0.3s ease-in-out;
  background-color: #f9f9f9;
  min-height: 100vh;
}

.notifications-container.collapsed {
  margin-left: 80px;
  width: calc(100% - 80px);
}

.notification-card {
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
  transition: transform 0.2s ease;
}

.notification-card:hover {
  transform: scale(1.02);
}

h2 {
  color: #333;
  font-size: 20px;
}
</style>

<template>
  <div class="notifications-container" :class="{ collapsed: iscollapsedBig }">
    <h2>Notifications</h2>
    <div v-for="notif in notifications" :key="notif.id" class="notification-card">
      {{ notif.message }}
    </div>

    <h2>Messages</h2>
    <div v-for="msg in messages" :key="msg.id" class="notification-card">
      {{ msg }}
    </div>
  </div>
</template>
