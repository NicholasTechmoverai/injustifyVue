<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
  
    <UserNavBar :userEmail="userEmail" :user-name="userName" :is-verified="isVerified" :profile-pic="profilePic" :isDarkMode="isDarkMode"  @open-signup="showSignupModal = true" @toggle-theme="toggleTheme" />
    
    <keep-alive include="HomePage,SearchResults">
      <router-view />
    </keep-alive>

    <SignupModal :isOpen="showSignupModal" :isDarkMode="isDarkMode" @close="showSignupModal = false" />
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useUserStore } from "@/store/index.js";
import UserNavBar from "@/components/UserNavBar.vue";
import SignupModal from "@/components/LoginSignup.vue";

export default {
  components: {
    UserNavBar,
    SignupModal,
  },
  setup() {
    const userStore = useUserStore();

    const params = new URLSearchParams(window.location.search);
    const user = params.get('user');
    if(user){
        try {
            const decodedUser = decodeURIComponent(user);  // Decode URL-encoded JSON string
            const userObj = JSON.parse(decodedUser);  // Convert to JavaScript object
            userStore.setUser(userObj);
            console.log("User logged in successfully:", userObj);
        } catch (error) {
            console.error("Error parsing user data:", error);
        }
    }

    
    const userEmail = computed(() => userStore.email);
    const userId = computed(() => userStore.userId);
    const userName = computed(() => userStore.name);
    const profilePic = computed(() => userStore.profilePic);
    const isVerified = computed(() => userStore.verifiedEmail);



    const showSignupModal = ref(!userEmail.value ||userEmail.value==='injustify@gamil.com' ); // Modal opens if no user email
    let isDarkMode = ref(false);
 
    const toggleTheme = () => {
      console.log("Toggled theme in app.vue");
      isDarkMode.value = !isDarkMode.value;
    };

    return { userEmail,userId,userName,profilePic,isVerified,isDarkMode, showSignupModal,toggleTheme };
  },
};
</script>
