<template>
  <div class="about-container" :class="{ collabsedBig: isCollapsedBig }">
    <div class="about-content">
      <h1 class="about-title">
        <h1 @click="reloadPage" class="injustifyLogoR">Injustify</h1>
        Verify Your Email
      </h1>
      <p class="about-subtitle">
        To protect your account and personalize your experience, we kindly ask you to
        verify your email.
      </p>

      <div class="about-sections">
        <div class="about-card">
          <ion-icon name="shield-checkmark-outline"></ion-icon>
          <div class="card-content">
            <h3>Why Verify?</h3>
            <p>
              Email verification ensures your account is safe and you receive important
              updates.
            </p>
          </div>
        </div>
        <div class="about-card">
          <ion-icon name="mail-outline"></ion-icon>
          <div class="card-content">
            <h3>Fast & Secure</h3>
            <p>
              Just one click and you're all set to explore all our features safely and
              securely.
            </p>
          </div>
        </div>
      </div>

      <p class="cta-text">{{ msg }}</p>
      <button v-if="!verified" @click="verifyemail" class="cta-button">
        <span v-if="!verificationLoading"
          ><ion-icon name="checkmark-circle"></ion-icon> Verify Email</span
        >
        <span v-if="verificationLoading">verifying...</span>
      </button>

      <router-link to="/" v-if="verified" class="cta-button">
        🎵 Go to Homepage || Explore Music💫
      </router-link>
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

const msg = ref("Click the button below to confirm your email address.");

const verifyemail = () => {
  if (verificationLoading.value || verified.value) return;

  verificationLoading.value = true;

  const params = new URLSearchParams(window.location.search);
  const email = params.get("email");
  const token = params.get("token");

  if (!email || !token) {
    console.error("Missing email or token in query parameters.");
    msg.value = "Missing email or token in query parameters!";
    verificationLoading.value = false;
    return;
  }

  axios
    .post(`${BASE_URL}/account/verify`, {
      email,
      token,
    })
    .then((response) => {
      if (response.data.success) {
        msg.value = response.data.message || "Email verified successfully.";
        verified.value = true;
        userStore.set_snackbarMessage(
          `Account verified successfully! <a href="/">Go to homepage</a>`,
          "success",
          10000
        );

        setTimeout(() => {
          msg.value = "Click the button below to confirm your email address.";
        }, 10000);
      }
    })
    .catch((error) => {
      console.error("Error verifying email", error);
      msg.value = error?.response?.data?.detail || "Verification failed.";
    })
    .finally(() => {
      verificationLoading.value = false;
    });
};

const reloadPage = () => {
  window.location.reload();
};

// Lifecycle hooks
onMounted(() => {
  userStore.setShowNavbar(false);
});

onBeforeUnmount(() => {
  userStore.setShowNavbar(true);
});
</script>

<style scoped>
.about-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #5fefff, #007bff);
  text-align: center;
  min-height: 100vh;
  height: 100%;
  width: 100vw;
  padding: 40px;
  animation: backgroundAnim 40s infinite alternate ease-in-out;
  box-sizing: border-box;
}

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

.about-title {
  font-size: 32px;
  font-weight: bold;
  color: white;
  letter-spacing: 1px;
  margin-bottom: 10px;
}

.about-subtitle {
  font-size: 18px;
  color: white;
  margin-bottom: 20px;
  font-style: italic;
}

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
}

.about-card:hover {
  transform: scale(1.05);
  background: rgba(255, 255, 255, 0.3);
}

ion-icon {
  font-size: 40px;
  color: white;
}

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
  cursor: pointer;
}

.cta-button:hover {
  background: #ff5fa2;
  color: white;
  transform: scale(1.05);
}

.injustifyLogoR {
  margin: 0 !important;
  margin-right: auto !important;
  margin-bottom: 5px !important;
  padding-top: 2px !important;
  text-shadow: 0px 2px 5px black;
  position: relative;
}

@media (max-width: 600px) {
  .about-container {
    padding: 3px;
  }
  .about-content {
    padding: 5px;
  }
}
</style>
