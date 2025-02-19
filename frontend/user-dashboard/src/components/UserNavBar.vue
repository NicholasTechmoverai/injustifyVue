<template id="lfsidebar">
  <aside :class="{ collapsed: !isSidebarOpen }" class="sidecontent">
    <!-- User Info -->
    <div class="userinfo">

      <router-link :to="`/profile/${userEmail}`">
        <div class="UnverifiedEmailWarn" v-if="isVerified === 0">
        <ion-icon name="alert-outline"></ion-icon>
       </div>
       <img :src="profilePic || require('@/assets/unknown-filef.png')" alt="Profile" class="circular-profile_pic" />
      </router-link>

      <div v-if="isSidebarOpen" class="info">
        <h3><router-link :to="`/profile/${userEmail}`">{{ userName }}</router-link></h3>
        <p>{{ userEmail }}</p>
      </div>
    </div>

    <!-- Navigation Links -->
    <nav>
      <ul>
        <li>
          <router-link class="inline" :to="`/${userEmail}`">
            <ion-icon name="home-outline"></ion-icon>
            <div v-if="isSidebarOpen">Dashboard</div>
          </router-link>
        </li>
        <li>
          <router-link class="inline" :to="`/history/${userEmail}`">
            <ion-icon name="time-outline"></ion-icon>
            <div v-if="isSidebarOpen">History</div>
          </router-link>
        </li>
        <li>
          <router-link class="inline" :to="`/downloads/${userEmail}`">
            <ion-icon name="cloud-download-outline"></ion-icon>
            <div v-if="isSidebarOpen">Downloads</div>
          </router-link>
        </li>
        <li>
          <router-link class="inline" :to="`/notifications/${userEmail}`">
            <ion-icon name="notifications-outline"></ion-icon>
            <div v-if="isSidebarOpen">Notifications</div>
          </router-link>
        </li>
        <li>
          <router-link class="inline" :to="`/settings/profile`">
            <ion-icon name="settings-outline"></ion-icon>
            <div v-if="isSidebarOpen">Settings</div>
          </router-link>
        </li>
        <li>
          <router-link class="inline" to="/search">
            <ion-icon name="search-outline"></ion-icon>
            <div v-if="isSidebarOpen">Search</div>
          </router-link>
        </li>
        <li>
          <router-link class="inline" to="/about">
            <ion-icon name="information-circle-outline"></ion-icon>
            <div v-if="isSidebarOpen">About</div>
          </router-link>
        </li>
        <li>
            <a class="inline" href="#" @click.prevent="$emit('open-signup')">
              <ion-icon name="log-in-outline"></ion-icon>
              <div v-if="isSidebarOpen">Signup/Login</div>
            </a>
        
        </li>
      </ul>
    </nav>


    <!-- Sidebar Toggle Button -->
    <button id="sideBartoggle" @click="toggleSidebar">
      <span v-if="isSidebarOpen">❮</span>
      <span v-else>❯</span>
    </button>
    <div class="globalToogle">
      <label class="toggle ThemeToggle">
        <span class="hidden" id="darkthemething"><i class="fa-solid fa-moon"></i> </span>
        <input v-if="isSidebarOpen" @change="toggleThemes" :checked="isDarkMode" type="checkbox" id="themeToggle" >
        <span v-if="isSidebarOpen" class="slider  mode-toggle"></span>
        <span class="hidden" id="lighthemething"><i class="fa-solid fa-sun"></i> </span>
      </label>
    </div>
  </aside>
</template>

<script>
export default {
  props: {
    userEmail: String,
    userName: String,
    profilePic: String,
    isVerified: Boolean,
    isDarkMode: Boolean,
  },
  data() {
    return {
      isSidebarOpen: true,
      deviceWidth: window.innerWidth, // Get the current width on initial load
    };
  },
  mounted() {
    // Run the defaultSidebarHandler when the component is mounted
    this.defaultSidebarHandler();
    
    // Add resize event listener to adjust sidebar on window resize
    window.addEventListener("resize", this.handleResize);
  },
  beforeUnmount() {
    // Clean up the event listener when the component is destroyed
    window.removeEventListener("resize", this.handleResize);
  },
  methods: {
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
    },
    toggleThemes() {
      console.log("Toggled theme in navbar.vue");
      this.$emit('toggle-theme');
    },
    defaultSidebarHandler() {
      // Check if device width is less than 862px and adjust sidebar visibility
      if (this.deviceWidth < 862) {
        this.isSidebarOpen = false;
      } else {
        this.isSidebarOpen = true;
      }
    },
    handleResize() {
      // Update deviceWidth and call defaultSidebarHandler on resize
      this.deviceWidth = window.innerWidth;
      this.defaultSidebarHandler();
    },
  },
};
</script>

<style scoped>
/* Sidebar Styling */
:root {
  --main-color: linear-gradient(45deg, rgb(25, 23, 53) 40%, rgb(95, 239, 255));
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

.sidecontent {
  position: fixed;
  left: 0;
  top: 0;
  width: 250px;
  height: 100%;
  background:linear-gradient(45deg, rgb(25, 23, 53) 40%, rgb(95, 239, 255));
  padding: 10px;
  color: rgb(119, 116, 116);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease-in-out;
  z-index: 100;
  justify-content: space-between;
}

/* Collapsed Sidebar */
.sidecontent.collapsed {
  width: 60px;
}

/* Sidebar Toggle */
#sideBartoggle {
  position: absolute;
  top: 20px;
  left: 100%;
  transform: translateX(-50%);
  border: none;
  background-color: red;
  color: white;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.3s ease-in-out;
}

/* Sidebar Links */
nav{
  overflow-y: auto;
}
nav,li,ul{
  margin: 0;
  padding: 0;
  text-align: center;
}
nav ul {
  list-style: none;
  padding: 0;
}


/* Styling for the inline div */
.inline {
  transition: all 0.3s;
  color: white;
  text-decoration: none;
  display: flex;
  flex-direction: row;
  margin:5px 0px ;
  height: 30px;
  background-color: rgba(21, 21, 21, 0.156);
  text-align: center;
  align-items: center;
  padding: 5px ;
  border-radius: 5px;
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  -ms-border-radius: 5px;
  -o-border-radius: 5px;
  cursor: pointer;
  color: white;
  position: relative;
  overflow: hidden;
  transition:  all 0.5s ease;
}
a{
  color: inherit;
  text-decoration: inherit;
}

/* Hover Effect */
.inline:hover {
  background: var(--hover-color1);
}

/* Ion Icons Styling */
.inline ion-icon {
  font-size: 20px;
}

/* User Info */
.userinfo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 10px;
  position: relative;
  
}
.UnverifiedEmailWarn{
position: relative;
width: 100%;
background: #303030;
}
.UnverifiedEmailWarn ion-icon {
  font-size: 2.4em !important;
  font-weight: bolder;
  color: red;
  position: absolute;
  right: -22px;
  top: 0;
  z-index: 101;


}
.userinfo p,h3{
  margin: 0;
  color: white;
  transition: all 0.3s ease-in-out;
  display: -webkit-box; /* Use a flex-like box for line clamping */
    -webkit-box-orient: vertical; /* Specify vertical stacking of lines */
    -webkit-line-clamp: 1; /* Allow only two lines */
    overflow: hidden; /* Hide overflowed text */
    text-overflow: ellipsis; /* Add ellipsis (...) for overflowing text */
    word-wrap: normal; /* Prevent forced breaks */
    width: 200px;
  
}

.circular-profile_pic {
  min-width: 50px;
  min-height: 50px;
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 50%;
  background-color: gray;
  cursor: pointer;
  position: relative;
}

/* Hide Text When Sidebar Collapses */
.sidecontent.collapsed .info {
  display: none;
}

ion-icon {
  font-weight: bolder;
  margin: 0px 10px;
}
.globalToogle{
  max-width: 150px;background-color: #30303047;
  padding: 0px 5px;
  border-radius: 5px;
  margin: 0 auto;
  display: flex;
}

.globalToogle span{
  margin: 0 5px;
}
</style>
