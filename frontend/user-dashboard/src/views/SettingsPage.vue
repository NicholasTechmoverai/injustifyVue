<template>
  <section
    id="settings"
    class="main_tabs MainContainer"
    :class="{ collabsedBig: iscollapsedBig }"
  >
    <div id="settings-header" :class="{ darkmode4: isDarkMode }">
      <h2>Settings</h2>
      <div id="settings-scroll-select">
        <div id="optSettings">
          <button id="optButton">///</button>
          <div id="scrollsSettings">
            <router-link to="/settings/profile">Profile</router-link>
            <router-link to="/settings/notifications">Notifications</router-link>
            <router-link to="/settings/preferences">Preferences</router-link>
            <router-link to="/settings/security">Security</router-link>
            <div class="dropdown">
              <button class="dropdown-toggle">More</button>
              <div class="dropdown-content">
                <router-link class="inline" to="/help">
                  <ion-icon name="help-circle-outline"></ion-icon>                  Help
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


              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="settings-body" :class="{ darkmode4: isDarkMode }">
      <router-view></router-view>
      <!-- Render the child route component here -->
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";
import { useUserStore } from "@/store/index.js";

const userStore = useUserStore();
const isDarkMode = computed(() => userStore.isdarkmode);
const iscollapsedBig = computed(() => userStore.iscollapsedBig);
</script>

<style scoped>
/* Header Styling */
#settings-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--card-background, #ffffff);
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  width: 650px;
  box-sizing: border-box;
}

#settings-header h2 {
  font-weight: 600;
}

/* Tabs for Navigation */
#scrollsSettings,
#settings-scroll-select {
  display: flex;
  align-items: center;
  gap: 12px;
}

#settings-scroll-select a {
  padding: 10px 16px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  color: var(--text-color, #444);
  background: var(--tab-background, #eeeeee);
  transition: 0.3s ease;
}

#settings-scroll-select a:hover {
  background: var(--hover-color, #d1d1d1);
}

#settings-scroll-select a.router-link-active {
  background: var(--active-color, #007bff);
  color: #ffffff;
}

/* Dropdown Styling */
.dropdown {
  position: relative;
}

.dropdown-toggle {
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  background: var(--tab-background, #eeeeee);
  cursor: pointer;
  font-size: 16px;
  transition: 0.3s;
  width: 100%;
}

.dropdown-toggle:hover {
  background: var(--hover-color, #d1d1d1);
}

.dropdown-content {
  display: none;
  position: absolute;
  right: 0;
  top: 40px;
  background: var(--card-background, #ffffff);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  min-width: 150px;
  z-index: 10;
}

.dropdown-content a {
  display: block;
  padding: 12px;
  text-decoration: none;
  color: var(--text-color, #444);
  transition: 0.3s;
}

.dropdown-content a:hover {
  background: var(--hover-color, #d1d1d1);
}

/* Show Dropdown on Hover */
.dropdown:hover .dropdown-content {
  display: block;
}

/* Settings Body */
#settings-body {
  margin-top: 20px;
  padding: 20px;
  border-radius: 12px;
  background: var(--card-background, #ffffff);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  box-sizing: border-box;
  width: fit-content;
  width: 650px;
}
.darkmode4 {
  background-color: #373737 !important;
  color: white !important;
}
#optButton {
  display: none;
}
/* Responsive Styles */
@media (max-width: 780px) {
  #scrollsSettings {
    display: none;
    flex-direction: column;
    gap: 2px !important;
    border: 1px solid;
    border-radius: 0px 0px 5px 5px;
  }
  #scrollsSettings > * {
    width: 100% !important;
    color: #007bff;
    box-sizing: border-box;
  }
  #settings-scroll-select {
    flex-direction: column;
    gap: 8px;
    position: relative;
    background-color: green;
  }
  #optButton {
    display: flex;
  }
  #optSettings {
    display: flex;
    width: fit-content;
  }
  #optSettings:hover #scrollsSettings {
    min-width: 100px;
    display: flex;
    position: absolute;
    top: 100%;
    right: 0;
  }
  #settings-body {
    width: 97% !important;
  }
  #settings-header {
    width: 97% !important;
  }
}
</style>
