<template>
  <div class="dev-container MainContainer" :class="{ collabsedBig: isCollapsedBig }">
    <div class="dev-content">
      <h1 class="dev-title">👨‍💻 Welcome, Developers!</h1>
      <p class="dev-subtitle">Join us in building the future of injustify.</p>

      <!-- Feature Sections -->
      <div class="dev-sections">
        <div class="dev-card" v-for="(section, index) in devSections" :key="index">
          <ion-icon :name="section.icon"></ion-icon>
          <div class="card-content">
            <h3>{{ section.title }}</h3>
            <p>{{ section.description }}</p>
            <a :href="section.link" target="_blank" class="learn-more">Learn More →</a>
          </div>
        </div>
      </div>

      <!-- Call to Action -->
      <p class="cta-text">Ready to contribute? 🚀</p>
      <a
        href="https://github.com/NicholasTechmoverai/injustifyVue.git"
        class="cta-button"
        target="_blank"
      >
        🔗 Join Our GitHub
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useUserStore } from "@/store/index.js";

const userStore = useUserStore();
const isCollapsedBig = computed(() => userStore.iscollapsedBig);

const devSections = ref([
  {
    icon: "code-slash-outline",
    title: "Tech Stack",
    description: "Vue 3, Node.js, Express, MongoDB, Tailwind CSS, and more!",
    link: "https://vuejs.org/",
  },
  {
    icon: "terminal-outline",
    title: "API Documentation",
    description:
      "Explore our RESTful API with authentication, rate limits, and real-time updates.",
    link: "https://yourwebsite.com/api-docs",
  },
  {
    icon: "git-branch-outline",
    title: "Contribute",
    description: "Fork our repo, create a feature branch, and submit a PR!",
    link: "https://github.com/NicholasTechmoverai/techmove.git",
  },
  {
    icon: "chatbubbles-outline",
    title: "Community",
    description: "Join our Discord & forums to collaborate and share ideas.",
    link: "https://discord.gg/yourcommunity",
  },
]);
</script>

<style scoped>

.dev-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100% !important;
  background: linear-gradient(135deg, #252525, #1b1b1b);
  text-align: center;
  padding: 40px;
  animation: backgroundAnim 10s infinite alternate ease-in-out;
  box-sizing: border-box;
}

/* Animated Background */
@keyframes backgroundAnim {
  0% {
    background: linear-gradient(135deg, #252525, #1b1b1b);
  }
  100% {
    background: linear-gradient(135deg, #161616, #101010);
  }
}

/* Content Box */
.dev-content {
  max-width: 700px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease-in-out;
  box-sizing: border-box;

}

.dev-content:hover {
  transform: translateY(-5px);
}

/* Titles */
.dev-title {
  font-size: 32px;
  font-weight: bold;
  color: #5fefff;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.dev-subtitle {
  font-size: 18px;
  color: #aaa;
  margin-bottom: 20px;
  font-style: italic;
}

/* Feature Cards */
.dev-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.dev-card {
  display: flex;
  align-items: center;
  gap: 15px;
  background: rgba(255, 255, 255, 0.15);
  padding: 20px;
  border-radius: 12px;
  transition: 0.3s ease-in-out;
  cursor: pointer;
}

.dev-card:hover {
  transform: scale(1.05);
  background: rgba(255, 255, 255, 0.2);
}

/* Icon Styling */
ion-icon {
  font-size: 40px;
  color: #5fefff;
}

/* Links */
.learn-more {
  color: #5fefff;
  font-weight: bold;
  text-decoration: none;
  transition: 0.3s;
}

.learn-more:hover {
  text-decoration: underline;
}

/* CTA */
.cta-text {
  font-size: 20px;
  margin-top: 30px;
  color: #ddd;
}

.cta-button {
  display: inline-block;
  margin-top: 15px;
  background: #5fefff;
  color: #000;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 18px;
  text-decoration: none;
  font-weight: bold;
  transition: 0.3s ease-in-out;
}

.cta-button:hover {
  background: #007bff;
  color: white;
  transform: scale(1.05);
}


@media (max-width:600px) {
  .dev-container {
    padding:3px;
  }
  .dev-content {
    padding:5px;
  }
  
}
</style>
