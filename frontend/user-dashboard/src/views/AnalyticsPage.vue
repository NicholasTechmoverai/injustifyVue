<template>
  <div class="notifications-container MainContainer" :class="{ collapsed: iscollapsedBig }">
  <img id="imgg" :src="bckg" alt="" srcset="">
    <div id="Holdcont">
      <h2>📊 Analytics</h2>
      <p class="coming-soon">Coming Soon!</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import socket from "@/services/websocket"; // WebSocket service
import { useUserStore } from "@/store/index.js";
import bckg  from "../assets/original-76bdf3ff530aaf2597691cc659dccd1e.webp"

const messages = ref([]);
const userStore = useUserStore();
const iscollapsedBig = computed(() => userStore.iscollapsedBig);

onMounted(() => {
  socket.on("message", (data) => {
    messages.value.push(data);
  });
});

onUnmounted(() => {
  socket.off("message");
  socket.off("new_notification"); 
});
</script>

<style scoped>
.notifications-container {
  padding: 40px;
  transition: all 0.3s ease-in-out;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden !important;
  justify-content: center;
}

.notifications-container.collapsed {
  margin-left: 80px;
  width: calc(100% - 80px);
}

#imgg{
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: blur(7px) brightness(60%);
  position: absolute;
  user-select: none;
  z-index: 20;
}

h2 {
  color: #cecece;
  font-size: 26px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
  text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
}

/* Container for Centered Text */
#Holdcont {
  display: flex;
  flex-direction: column;
  gap:20px;
  align-items: center;
  justify-content: center;
  width: fit-content;
  height: auto;
  padding:10px 50px;
  background: rgba(6, 16, 26, 0.61);
  border-radius: 10px;
  z-index: 100;
}

/* Animated "Coming Soon" Text */
.coming-soon {
  text-align: center;
  font-size: 32px;
  font-weight: bold;
  color: #f6f6f6;
  text-shadow: 2px 2px 10px rgba(255, 255, 255, 0.5);
  animation: pulse 2s infinite alternate ease-in-out;
}

/* Animation Effect */
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1.1);
    opacity: 1;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .notifications-container {
    margin-left: 0;
    width: 100%;
    padding: 20px;
  }

  .coming-soon {
    font-size: 24px;
  }
}
</style>
