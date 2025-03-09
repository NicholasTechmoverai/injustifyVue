<template>
  <div class="about-container MainContainer" :class="{ collabsedBig: isCollapsedBig }">
    <div class="about-content">
      <h1 class="about-title">🎶 About injustify</h1>
      <p class="about-subtitle">
        Your go-to destination for high-quality, free music downloads. Fast, secure, and
        easy.
      </p>

      <div class="about-sections">
        <div class="about-card" v-for="(feature, index) in features" :key="index">
          <ion-icon :name="feature.icon"></ion-icon>
          <div class="card-content">
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>
      </div>

      <p class="cta-text">Start exploring your favorite tracks today! 🔥</p>
      <router-link to="/" class="cta-button">🎵 Explore Music</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useUserStore } from "@/store/index.js";

const userStore = useUserStore();

const isCollapsedBig = computed(() => userStore.iscollapsedBig);

const features = ref([
  {
    icon: "musical-notes-outline",
    title: "High-Quality Music",
    description: "Enjoy studio-quality audio downloads with no hidden costs.",
  },
  {
    icon: "flash-outline",
    title: "Lightning Fast",
    description: "Our optimized servers ensure the fastest download speeds possible.",
  },
  {
    icon: "shield-checkmark-outline",
    title: "Safe & Secure",
    description: "100% safe downloads with no ads or malicious software.",
  },
]);
</script>

<style scoped>
/* Container */
.about-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #5fefff, #007bff);
  text-align: center;
  height: 100vh;
  padding: 40px;
  animation: backgroundAnim 40s infinite alternate ease-in-out;
  box-sizing: border-box;

}



/* Content Box */
.about-content {
  max-width: 600px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease-in-out;
  box-sizing: border-box;
}

.about-content:hover {
  transform: translateY(-5px);
}

/* Titles */
.about-title {
  font-size: 32px;
  font-weight: bold;
  color: white;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.about-subtitle {
  font-size: 18px;
  color: white;
  margin-bottom: 20px;
  font-style: italic;
}

/* Feature Cards */
.about-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.about-card {
  display: flex;
  align-items: center;
  gap: 15px;
  background: rgba(255, 255, 255, 0.2);
  padding: 20px;
  border-radius: 12px;
  transition: 0.3s ease-in-out;
  cursor: pointer;
}

.about-card:hover {
  transform: scale(1.05);
  background: rgba(255, 255, 255, 0.3);
}

/* Icon Styling */
ion-icon {
  font-size: 40px;
  color: white;
}

/* CTA */
.cta-text {
  font-size: 20px;
  margin-top: 30px;
  color: white;
}

.cta-button {
  display: inline-block;
  margin-top: 15px;
  background: white;
  color: #007bff;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 18px;
  text-decoration: none;
  font-weight: bold;
  transition: 0.3s ease-in-out;
}

.cta-button:hover {
  background: #ff5fa2;
  color: white;
  transform: scale(1.05);
}

@media (max-width:600px) {
  .about-container {
    padding:3px;
  }
  .about-content {
    padding:5px;
  }
  
}
</style>
