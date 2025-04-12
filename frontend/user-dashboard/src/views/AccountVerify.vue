<template>
  <div class="verify-container" :class="{ collabsedBig: isCollapsedBig }">
    <div class="verify-content">
      <div class="verify-header">
        <h1 class="verify-title">🔐 Account Verification</h1>
        <p class="verify-subtitle">
          One last step to unlock your full music experience
        </p>
      </div>

      <div class="verification-stats">
        <div class="stat-card">
          <div class="stat-icon">
            <ion-icon name="shield-checkmark"></ion-icon>
          </div>
          <div class="stat-content">
            <h3>Security Boost</h3>
            <p>+95% account protection</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <ion-icon name="musical-notes"></ion-icon>
          </div>
          <div class="stat-content">
            <h3>Full Access</h3>
            <p>100+ features unlocked</p>
          </div>
        </div>
      </div>

      <div class="verification-details">
        <div class="detail-item">
          <ion-icon name="checkmark-circle" class="verified-icon"></ion-icon>
          <span>Email: <strong>{{ maskedEmail }}</strong></span>
        </div>
        <div class="detail-item">
          <ion-icon name="time" class="pending-icon"></ion-icon>
          <span>Status: <strong>{{ verificationStatus }}</strong></span>
        </div>
      </div>

      <div class="progress-container" v-if="!verified">
        <div class="progress-bar" :style="{ width: progressWidth }"></div>
        <span class="progress-text">{{ progressText }}</span>
      </div>

      <div class="action-buttons">
        <button 
          v-if="!verified" 
          @click="verifyemail" 
          class="verify-button"
          :class="{ loading: verificationLoading }"
        >
          <template v-if="!verificationLoading">
            <ion-icon name="mail-unread"></ion-icon>
            Confirm Verification
          </template>
          <template v-else>
            <div class="spinner"></div>
            Processing...
          </template>
        </button>

        <router-link 
          v-if="verified" 
          to="/" 
          class="success-button"
        >
          <ion-icon name="rocket"></ion-icon>
          Launch Music Dashboard
        </router-link>
      </div>

      <div class="verification-benefits">
        <h3>You'll gain access to:</h3>
        <ul>
          <li><ion-icon name="infinite"></ion-icon> Unlimited streaming</li>
          <li><ion-icon name="download"></ion-icon> Offline downloads</li>
          <li><ion-icon name="stats-chart"></ion-icon> Personalized analytics</li>
          <li><ion-icon name="heart"></ion-icon> Premium content</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useUserStore } from "@/store/index.js";
import { BASE_URL } from "@/utils/index.js";
import axios from "axios";

const userStore = useUserStore();
const isCollapsedBig = computed(() => userStore.iscollapsedBig);
const verified = ref(false);
const verificationLoading = ref(false);
const verificationProgress = ref(0);

const params = new URLSearchParams(window.location.search);
const email = params.get("email") || '';
const token = params.get("token") || '';

const maskedEmail = computed(() => {
  if (!email) return 'your@email.com';
  const [name, domain] = email.split('@');
  return `${name.substring(0, 2)}****@${domain}`;
});

const verificationStatus = computed(() => {
  return verified.value ? 'Verified' : 'Pending Verification';
});

const progressWidth = computed(() => {
  return `${verificationProgress.value}%`;
});

const progressText = computed(() => {
  if (verificationLoading.value) return 'Securing your account...';
  return verified.value ? 'Complete!' : 'Ready to verify';
});

const msg = ref("Click to verify your email and unlock full access");

const verifyemail = () => {
  if (verificationLoading.value || verified.value) return;

  verificationLoading.value = true;
  verificationProgress.value = 30;

  if (!email || !token) {
    console.error("Missing email or token in query parameters.");
    msg.value = "Missing verification details! Check your email link.";
    verificationLoading.value = false;
    return;
  }

  axios
    .post(`${BASE_URL}/account/verify`, { email, token })
    .then((response) => {
      if (response.data.success) {
        verificationProgress.value = 100;
        verified.value = true;
        msg.value = response.data.message || "Verification successful!";
        userStore.set_snackbarMessage(
          `Account verified! <a href="/">Start exploring</a>`,
          "success",
          10000
        );
      }
    })
    .catch((error) => {
      console.error("Error verifying email", error);
      msg.value = error?.response?.data?.detail || "Verification failed. Please try again.";
      verificationProgress.value = 0;
    })
    .finally(() => {
      verificationLoading.value = false;
    });
};

// Lifecycle hooks
onMounted(() => {
  userStore.setShowNavbar(false);
  // Simulate progress animation
  if (!verified.value) {
    const interval = setInterval(() => {
      if (verificationProgress.value < 25 && !verificationLoading.value) {
        verificationProgress.value += 5;
      } else {
        clearInterval(interval);
      }
    }, 300);
  }
});

onBeforeUnmount(() => {
  userStore.setShowNavbar(true);
});
</script>

<style scoped>
.verify-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  min-height: 100vh;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.verify-content {
  max-width: 600px;
  width: 100%;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.verify-header {
  text-align: center;
  margin-bottom: 30px;
}

.verify-title {
  font-size: 2.2rem;
  color: white;
  margin-bottom: 10px;
  background: linear-gradient(90deg, #00d2ff, #3a7bd5);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.verify-subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 0;
}

.verification-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin: 30px 0;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.15);
}

.stat-icon {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.stat-icon ion-icon {
  font-size: 24px;
  color: #00d2ff;
}

.stat-content h3 {
  font-size: 1.1rem;
  color: white;
  margin-bottom: 5px;
}

.stat-content p {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.verification-details {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  padding: 20px;
  margin: 25px 0;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.9);
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item ion-icon {
  margin-right: 10px;
  font-size: 20px;
}

.verified-icon {
  color: #4caf50;
}

.pending-icon {
  color: #ff9800;
}

.progress-container {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  margin: 30px 0 15px;
  position: relative;
  overflow: hidden;
}

.progress-bar {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: linear-gradient(90deg, #00d2ff, #3a7bd5);
  border-radius: 10px;
  transition: width 0.5s ease;
}

.progress-text {
  display: block;
  text-align: center;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 10px;
}

.action-buttons {
  margin: 30px 0;
}

.verify-button, .success-button {
  width: 100%;
  padding: 16px;
  border-radius: 12px;
  border: none;
  font-size: 1.1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.verify-button {
  background: linear-gradient(90deg, #00d2ff, #3a7bd5);
  color: white;
}

.verify-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 210, 255, 0.4);
}

.verify-button.loading {
  opacity: 0.8;
  pointer-events: none;
}

.success-button {
  background: linear-gradient(90deg, #4caf50, #8bc34a);
  color: white;
}

.success-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.verification-benefits {
  margin-top: 30px;
}

.verification-benefits h3 {
  color: white;
  font-size: 1.2rem;
  margin-bottom: 15px;
}

.verification-benefits ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.verification-benefits li {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  color: rgba(255, 255, 255, 0.9);
}

.verification-benefits li ion-icon {
  margin-right: 10px;
  color: #00d2ff;
  font-size: 20px;
}

@media (max-width: 768px) {
  .verify-content {
    padding: 30px 20px;
  }
  
  .verify-title {
    font-size: 1.8rem;
  }
  
  .verification-stats {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .verify-container {
    padding: 10px;
  }
  
  .verify-content {
    padding: 25px 15px;
  }
  
  .verify-title {
    font-size: 1.6rem;
  }
  
  .verify-button, .success-button {
    padding: 14px;
    font-size: 1rem;
  }
}
</style>