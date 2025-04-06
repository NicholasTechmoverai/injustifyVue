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

    <keep-alive include="HomePage,SearchResults">
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
import { computed, ref } from "vue";
import { useUserStore } from "@/store/index.js";
import UserNavBar from "@/components/UserNavBar.vue";
import SignupModal from "@/components/LoginSignup.vue";
import SnackBar from "@/components/SnackBar";

export default {
  components: {
    UserNavBar,
    SignupModal,
    SnackBar,
  },
  setup() {
    const userStore = useUserStore();

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
    let isDarkMode = ref(false);

    const toggleTheme = () => {
      isDarkMode.value = !isDarkMode.value;
      userStore.setTheme(isDarkMode.value);
    };

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
