<template>
  <div class="MainContainer" :class="{ collabsedBig: isCollapsedBig }">
    <div class="help-container" :class="{ 'darktheme-2': isDarkMode }">
      <h1 class="help-title">Need Help? 🤔</h1>
      <p class="help-subtitle">Choose wisely... Your fate depends on it. 😆</p>

      <div class="help-options">
        <button @click="goToPolice" class="help-btn">🚔 Go to Police Station</button>
        <button @click="call911" class="help-btn">📞 Call 911 (No jokes!)</button>
        <button @click="stayWithMom" class="help-btn">
          👩 Stay with Mom (Free food!)
        </button>
        <button @click="giveUp" class="help-btn rude">
          🤡GIVE UP!! (Accept Your Fate)
        </button>
      </div>

      <p v-if="message" class="response-message">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useUserStore } from "@/store/index.js";

const userStore = useUserStore();
const message = ref("");

const isDarkMode = computed(() => userStore.isdarkmode);
const isCollapsedBig = computed(() => userStore.iscollapsedBig);

const goToPolice = () =>
  (message.value = "Smart choice! 🚔 Hope they take you seriously.");
const call911 = () => (message.value = "Hope this ain't a prank... 👀");
const stayWithMom = () => (message.value = "Best decision ever! Free food & no rent. 🏡");
const giveUp = () => (message.value = "😂 Welp... at least you tried. Good luck! 🍀");
</script>

<style scoped>
.MainContainer {
  transition: all 0.3s ease-in-out;
}

.collabsedBig {
  transform: scale(0.95);
  opacity: 0.9;
}

.help-container {
  text-align: center;
  background: #ffffff;
  padding: 40px;
  max-width: 500px;
  margin: 50px auto;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease-in-out;
}

.darktheme-2 {
  background: #2c2c2c;
  color: #e7e7e7;
  box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.2);
}

.help-title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 10px;
}

.help-subtitle {
  font-size: 18px;
  color: #555;
  margin-bottom: 20px;
}

.help-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.help-btn {
  background: #007bff;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s;
}

.help-btn:hover {
  background: #0056b3;
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

.rude {
  background: red;
}

.rude:hover {
  background: darkred;
  transform: rotate(-2deg) scale(1.05);
}

.response-message {
  margin-top: 20px;
  font-size: 18px;
  font-weight: bold;
}
</style>
