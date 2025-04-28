<template>
  <aside :class="{ collapsed: !isSidebarOpen }" class="sidecontent">
    <!-- User Info -->
    <div class="userinfo">
      <router-link :to="`/profile/${userEmail}`">
        <div class="UnverifiedEmailWarn" v-if="isVerified === 0">
          <ion-icon name="alert-outline"></ion-icon>
        </div>
        <img
          :src="profilePic || require('@/assets/unknown-filef.png')"
          alt="Profile"
          class="circular-profile_pic"
        />
      </router-link>
      <div v-if="isSidebarOpen" class="info">
        <h3>
          <router-link :to="`/profile/${userEmail}`">{{ userName }}</router-link>
        </h3>
        <p>{{ userEmail }}</p>
      </div>
    </div>

    <!-- Navigation Links -->
    <nav>
      <ul>
        <li>
          <router-link class="inline" :to="`/`">
            <ion-icon name="home-outline"></ion-icon>
            <div v-if="isSidebarOpen">Dashboard</div>
          </router-link>
        </li>
        <li>
          <router-link class="inline" :to="`/analytics/${userEmail}`">
            <ion-icon name="analytics-outline"></ion-icon>
            <div v-if="isSidebarOpen">Analytics</div>
          </router-link>
        </li>
        <li>
          <router-link class="inline" :to="`/downloads/${userEmail}`">
            <div id="outerProgressBar" :style="{ '--progress': averageProgress + '%' }">
              <div id="downloadCount">{{ downloadCount }}</div>
            </div>

            <ion-icon name="cloud-download-outline"></ion-icon>
            <div v-if="isSidebarOpen">Downloads</div>
            <div v-if="isAboutToDownload" class="inline-loader-container">
              <div class="lder"></div>
            </div>
          </router-link>
        </li>
        <li>
          <router-link class="inline" :to="`/notifications/${userEmail}`">
            <ion-icon name="notifications-outline"></ion-icon>
            <div v-if="isSidebarOpen">Notifications</div>
          </router-link>
        </li>
        <li>
          <router-link class="inline" :to="`/you`">
            <ion-icon name="heart-half-outline"></ion-icon>
            <div v-if="isSidebarOpen">You</div>
          </router-link>
        </li>
        <li>
          <router-link class="inline" :to="`/settings`">
            <ion-icon name="settings-outline"></ion-icon>
            <div v-if="isSidebarOpen">Settings</div>
          </router-link>
        </li>

        <li v-if="userId">
          <a class="inline" @click="HandleLogout">
            <ion-icon name="log-out-outline"></ion-icon>
            <div v-if="isSidebarOpen">Logout</div>
          </a>
        </li>

        <li v-else>
          <a class="inline" href="#" @click.prevent="$emit('open-signup')">
            <ion-icon name="log-in-outline"></ion-icon>
            <div v-if="isSidebarOpen">Login</div>
          </a>
        </li>
      </ul>
    </nav>

    <!-- Sidebar Toggle Button -->
    <button id="sideBartoggle" @click="toggleSidebar">
      <span v-if="isSidebarOpen">❮</span>
      <span v-else>❯</span>
    </button>
    <div id="sidebarBottom">
      <div id="moreONnav" v-if="more_injust">
        <router-link class="inline" to="/help">
          <ion-icon name="help-circle-outline"></ion-icon> Help
        </router-link>
        <router-link class="inline" to="/search">
          <ion-icon name="code-slash-outline"></ion-icon>
          devs
        </router-link>

        <router-link class="inline" to="/about">
          <ion-icon name="information-circle-outline"></ion-icon>
          About
        </router-link>

        <router-link class="inline" to="/feedback">
          <ion-icon name="information-circle-outline"></ion-icon>
          feedback
        </router-link>

        <div class="globalToogle">
          <label class="toggle ThemeToggle">
            <span class="hidden" id="darkthemething"
              ><i class="fa-solid fa-moon"></i>
            </span>
            <input
              @change="toggleThemes"
              :checked="isDarkMode"
              type="checkbox"
              id="themeToggle"
            />
            <span class="slider mode-toggle"></span>
            <span class="hidden" id="lighthemething"
              ><i class="fa-solid fa-sun"></i>
            </span>
          </label>
        </div>
      </div>
      <h1 class="injustifyLogoR">
        <ion-icon name="musical-note-outline" v-if="isSidebarOpen"></ion-icon>
        Injustify
        <ion-icon name="musical-note-outline" v-if="isSidebarOpen"></ion-icon>
      </h1>
      <button
        id="moreONnavButton"
        @click="
          () => {
            more_injust = !more_injust;
          }
        "
      >
        <ion-icon
          :name="more_injust ? 'close-circle-outline' : 'ellipsis-horizontal'"
        ></ion-icon>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useUserStore } from "@/store/index.js";
import { adv_UserStore } from "@/store/tasks.js";
//import axios from "axios";

// Define props
defineProps({
  userEmail: String,
  userId: String,
  userName: String,
  profilePic: String,
  isVerified: Boolean,
  isDarkMode: Boolean,
});

const emit = defineEmits(["toggle-theme"]);

const userStore = useUserStore();
const advUserStore = adv_UserStore();

//const logout_loading = ref(false);

const isSidebarOpen = ref(true);
const deviceWidth = ref(window.innerWidth);

const more_injust = ref(false);

const isAboutToDownload = computed(() => userStore.isAboutToDownload);
const downloadCount = computed(() => advUserStore.currentDownloadCount);

const activeDownloads = computed(() => {
  const downloads = advUserStore.onGoingDownloads;
  return Object.fromEntries(
    Object.entries(downloads).filter(
      ([, download]) => download.status !== "completed" && (download.progress || 0) < 1
    )
  );
});

const averageProgress = computed(() => {
  const downloadArray = Object.values(activeDownloads.value);

  console.log("Active Downloads:", downloadArray.length);
  console.log("Download Progress Details:", downloadArray);

  if (downloadArray.length === 0) return 0;

  const totalProgress = downloadArray.reduce(
    (sum, download) => sum + (download.progress || 0),
    0
  );

  const avgProgress = Math.round((totalProgress / downloadArray.length) * 100);
  console.log("Average Progress:", avgProgress, "%");

  return avgProgress;
});

// Methods
const toggleSidebar = () => {
  const deviceWidth = window.innerWidth;

  if (deviceWidth >= 862) {
    userStore.setMainContainerWidthMarginLeft(isSidebarOpen.value);
  }

  isSidebarOpen.value = !isSidebarOpen.value;
};

const toggleThemes = () => {
  console.log("Toggled theme in navbar.vue");
  emit("toggle-theme");
};

const defaultSidebarHandler = () => {
  isSidebarOpen.value = deviceWidth.value >= 862;
};

const handleResize = () => {
  deviceWidth.value = window.innerWidth;
  defaultSidebarHandler();
};

const HandleLogout = async () => {
  userStore.clearUser();
  document.cookie = `user_info={}; expires=; path=/`;

  //logout_loading.value = true;

  // try {
  //       const response = await axios.post("/auth/logout", {
  //         session: "",
  //       });

       
  //       userStore.set_snackbarMessage("Logout successful!", "info", 5000);
  //       if (response) {
  //         logout_loading.value= false;
  //       }
  //     } catch (error) {
  //       userStore.set_snackbarMessage(
  //         "Logout failed!",
  //         "info",
  //         10000
  //       );
  //       console.error("Logout error:", error);
  //     }
  //     finally{
  //       logout_loading.value = false;

  //     }
  
}

// Lifecycle hooks
onMounted(() => {
  defaultSidebarHandler();
  window.addEventListener("resize", handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
});
</script>

<style scoped>
#outerProgressBar {
  position: absolute;
  top: 0;
  right: 0;
  padding: 2px;
  width: 17px;
  height: 17px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: conic-gradient(
    rgb(0, 255, 89) var(--progress, 0%),
    rgba(200, 200, 200, 0.5) 0%
  );
  transition: background 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 100;
}

#downloadCount {
  background-color: red;
  color: white;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  font-size: 10px;
  font-weight: bold;
  display: flex;
  justify-content: center;
  align-items: center;
}

.inline-loader-container {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 3px;
  overflow: hidden;
}
.lder {
  height: 100%;
  width: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.injustifyLogoR {
  position: relative;
  font-size: 1em;
}
.injustifyLogoR h1 {
  margin: 0;
  padding: 0;
}
#sidebarBottom {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
  justify-content: center;
}
:root {
  --main-color: linear-gradient(
    45deg,
    rgb(25, 23, 53) 10%,
    rgb(60, 90, 180) 50%,
    rgb(95, 239, 255) 90%
  );
  --hover-color1: rgb(12, 216, 231);
  --hover-color2: red;
  --other-color-balanced: rgba(132, 124, 124, 0.2);
  --white-background: rgb(233, 231, 229);
  --white-foreground: rgb(219, 216, 216);
  --dark-background: #303030;
  --dark-foreground: #373737;
  --dark-third-background: rgb(63, 62, 62);
  --white-third-background: rgb(240, 233, 233);
}

/* Sidebar Styling */
.sidecontent {
  position: fixed;
  left: 0;
  top: 0;
  width: 250px;
  height: 100%;
  background: linear-gradient(
    45deg,
    rgb(25, 23, 53) 10%,
    rgb(60, 90, 180) 50%,
    rgb(95, 239, 255) 90%
  );
  padding: 15px;
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  z-index: 100;
  justify-content: space-between;
  box-sizing: border-box;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
}

/* Collapsed Sidebar */
.sidecontent.collapsed {
  width: 60px;
  padding: 15px 5px;
}

/* Sidebar Toggle */
#sideBartoggle {
  position: absolute;
  top: 20px;
  right: -12px;
  border: none;
  background-color: red;
  color: white;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
  z-index: 101;
}

#sideBartoggle:hover {
  transform: scale(1.1);
}

/* Sidebar Links */
nav {
  overflow-y: auto;
  margin-top: 20px;
  flex-grow: 1;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

nav::-webkit-scrollbar {
  width: 4px;
}

nav::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

nav ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.inline {
  transition: all 0.3s ease;
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  margin: 3px 0;
  height: 40px;
  background-color: rgba(21, 21, 21, 0.2);
  padding: 0 10px;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border-left: 3px solid transparent;
}
a {
  color: inherit;
  text-decoration: inherit;
}

.inline:hover {
  background: rgba(255, 0, 0, 0.3);
  transform: translateX(3px);
}
.inline ion-icon {
  font-size: 20px;
  min-width: 24px;
  text-align: center;
}
.userinfo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 10px;
  position: relative;
}
.UnverifiedEmailWarn {
  position: relative;
  width: 100%;
  height: 100%;
  background: #303030b1;
}
.UnverifiedEmailWarn ion-icon {
  font-size: 2em;
  font-weight: bolder;
  color: red;
  position: absolute;
  right: 0px;
  top: 0px;
  z-index: 101;
  background: rgba(0, 0, 0, 0.535);
  border-radius: 50%;
  padding: 2px;
}

.userinfo p, .userinfo h3 {
  margin: 0;
  color: rgb(232, 225, 225);
  transition: all 0.3s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}
.userinfo h3 a {
  color: inherit;
  text-decoration: underline;
  color:gray;
}

.userinfo h3 a:hover {
  color: var(--hover-color1);
}


.circular-profile_pic {
  width: 50px;
  height: 50px;
  min-height: 50px;
  min-width: 50px;
  object-fit: cover;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  cursor: pointer;
  border: 2px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.circular-profile_pic:hover {
  border-color: var(--hover-color1);
  transform: scale(1.05);
}

/* Hide Text When Sidebar Collapses */
.sidecontent.collapsed .info {
  display: none;
}

ion-icon {
  font-weight: bolder;
  margin: 0px 10px;
}
.globalToogle {
  max-width: 150px;
  background-color: #30303047;
  padding: 0px 5px;
  border-radius: 5px;
  margin: 0 auto;
  display: flex;
}

.globalToogle span {
  margin: 0 5px;
}

/* Active Link */
.router-link-active {
  font-weight: bold;
  color: white;
  border-left: 3px solid red;
  border-bottom: 3px solid red;
  background: rgba(255, 0, 0, 0.2);
}

.router-link-active ion-icon {
  color: var(--hover-color1);
}

#moreONnavButton {
  font-size: 20px;
  margin-bottom: 5px;
  cursor: pointer;
  border-radius: 5px;
  background-color: transparent;
  border: none;
  color: white;
  padding: 5px;
  width: 100%;
  transition: all 0.3s ease;
}

#moreONnavButton:hover {
  color: var(--hover-color1);
  background-color: rgba(255, 255, 255, 0.1);
}

.collapsed #moreONnav {
  right: -150% !important;
}

#moreONnav {
  position: absolute;
  bottom: 60px;
  background: rgba(25, 23, 53, 0.95);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  width: calc(100% - 30px);
  min-width: 150px;
  max-width: 250px;
  padding: 10px;
  transition: all 0.3s ease;
  z-index: 100;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
  gap: 8px;
}

#moreONnav .inline {
  background: transparent;
  border-left: none;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: start;
}

#moreONnav .inline:hover {
  background: rgba(255, 255, 255, 0.1);
}
#sidebarBottom {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
