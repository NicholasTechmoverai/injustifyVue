<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <UserNavBar
      :userEmail="userEmail"
      :userId="userId"
      :user-name="userName"
      :is-verified="isVerified"
      :profile-pic="profilePic"
      :isDarkMode="isDarkMode"
      @open-signup="showSignupModal = true"
      @toggle-theme="toggleTheme"
      v-show="vShowNavbar"
    />

    <keep-alive include="HomePage,SearchResults,PlaylistPage">
      <router-view />
    </keep-alive>

    <SignupModal
      :isOpen="showSignupModal"
      :isDarkMode="isDarkMode"
      @close="showSignupModal = false"
    />
    <SnackBar />
  </div>
</template>

<script>
import { computed, ref,onMounted } from "vue";
import { useUserStore } from "@/store/index.js";
import UserNavBar from "@/components/UserNavBar.vue";
import SignupModal from "@/components/LoginSignup.vue";
import SnackBar from "@/components/SnackBar";
import axios from "axios"
import {BASE_URL } from "@/utils/index.js";

export default {
  components: {
    UserNavBar,
    SignupModal,
    SnackBar,
  },
  setup() {
    const userStore = useUserStore();

    const cookieName = "user_info";
    const cookie = document.cookie
      .split("; ")
      .find((c) => c.trim().startsWith(`${cookieName}=`));

    if (cookie) {
      const value = decodeURIComponent(cookie.split("=")[1]);
      const cookieData = JSON.parse(value);

      if (Date.now() < cookieData.expiresAt) {
        userStore.setUser(cookieData);
      } else {
        document.cookie = `user_info=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC`;
      }
    }

    const params = new URLSearchParams(window.location.search);
    const user = params.get("user");
    if (user) {
      try {
        const decodedUser = decodeURIComponent(decodeURIComponent(user));
        const userObj = JSON.parse(decodedUser).user_info;
        userStore.setUser(userObj);
      } catch (error) {
        console.error("Error parsing user data:", error);
      }
    }

    const userEmail = computed(() => userStore.email);
    const userId = computed(() => userStore.userId);
    const userName = computed(() => userStore.name);
    const profilePic = computed(() => userStore.profilePic);
    const isVerified = computed(() => userStore.verifiedEmail);
    const vShowNavbar = computed(() => userStore.vShowNavbar);

    const showSignupModal = ref(
      !userEmail.value || userEmail.value === "injustify@gamil.com"
    ); //login Modal opens if no user email

    const isDarkMode = computed(() => userStore.isdarkmode);

    // Read from cookie
    const tcookie = document.cookie.split("; ").find((c) => c.startsWith("isDarkmode="));

    if (tcookie) {
      const value = tcookie.split("=")[1];
      const parsed = value === "true";
      userStore.setTheme(parsed);
    }

    const toggleTheme = () => {
      const newVal = !userStore.isdarkmode;
      userStore.setTheme(newVal);
      document.cookie = `isDarkmode=${newVal}; path=/; max-age=31536000`; // store in cookie
    };

    const track = ()=>{
      let dev_info = null; // Use 'let' so we can change it
      let dvc = !userEmail.value ? null :userEmail.value; // cleaner

      fetch('https://ipwho.is/')
        .then(res => res.json())
        .then(data => {
          dev_info = data;

          // Now send AFTER you have dev_info!
          axios
            .post(`${BASE_URL}/api/fadfafref`, {
              dvc: dvc,
              dev_info: dev_info
            })
            .then((response) => {
              this.message = response.data.message;
            })
            .catch((error) => console.error("API Error:", error));
        })
        .catch(error => console.error("IP Fetch Error:", error));
    }
    onMounted(() => {
      setTimeout(() => {
        track();
      }, 300); // wait 300ms just in case (optional)
    });

    return {
      userEmail,
      userId,
      userName,
      profilePic,
      isVerified,
      isDarkMode,
      showSignupModal,
      vShowNavbar,
      toggleTheme,
    };
  },
};
</script>
