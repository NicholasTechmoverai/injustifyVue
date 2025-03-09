<template>
  <div class="preferences-container">
    <h3>Preferences</h3>
    
    <!-- Theme Preference -->
    <div class="preference-item" :class="{'darkmode3':isDarkMode}">
      <h4>Theme</h4>
      <label class="toggle ThemeToggle">
        <span><i class="fa-solid fa-sun"></i> Light</span>
        <input type="checkbox" v-model="isDarkMode">
        <span class="slider mode-toggle"></span>
        <span><i class="fa-solid fa-moon"></i> Dark</span>
      </label>
    </div>
    
    <!-- Font and Language Preferences -->
    <div class="preference-item" :class="{'darkmode3':isDarkMode}">
      <h4>Font & Language</h4>
      <label>Font: 
        <select v-model="selectedFont">
          <option value="Arial">Arial</option>
          <option value="Verdana">Verdana</option>
          <option value="Helvetica">Helvetica</option>
        </select>
      </label>
      <label>Language: 
        <select v-model="selectedLanguage">
          <option value="English">English</option>
          <option value="Spanish">Spanish</option>
          <option value="French">French</option>
        </select>
      </label>
    </div>
    
    <!-- Audio Preferences -->
    <div class="preference-item" :class="{'darkmode3':isDarkMode}">
      <h4>Audio Preferences</h4>
      <label><input type="checkbox" v-model="enableEqualizer"> Enable Equalizer</label>
      <label><input type="checkbox" v-model="enableCrossfade"> Enable Crossfade</label>
      <label>Playback Quality:
        <select v-model="playbackQuality">
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </label>
    </div>
    
    <!-- Streaming Preferences -->
    <div class="preference-item" :class="{'darkmode3':isDarkMode}">
      <h4>Streaming Preferences</h4>
      <label><input type="checkbox" v-model="enableDataSaver"> Enable Data Saver Mode</label>
      <label>Download Quality:
        <select v-model="downloadQuality">
          <option value="128">128 kbps</option>
          <option value="256">256 kbps</option>
          <option value="320">320 kbps</option>
        </select>
      </label>
    </div>
    
    <!-- Startup Mode -->
    <div class="preference-item" :class="{'darkmode3':isDarkMode}">
      <h4>On Startup</h4>
      <p>Continue playing the last song before logout?</p>
      <label class="toggle">
        <input type="checkbox" v-model="resumeOnStartup">
        <span class="slider"></span>
      </label>
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import { useUserStore } from "@/store/index.js";
export default {
  props: {
    currentView: String
  },
  data() {
    const userStore = useUserStore();
    return {
      selectedFont: 'Arial',
      selectedLanguage: 'English',
      enableEqualizer: false,
      enableCrossfade: false,
      playbackQuality: 'medium',
      enableDataSaver: false,
      downloadQuality: '256',
      resumeOnStartup: true,
      isDarkMode:computed(() => userStore.isdarkmode),

    };
  },
  methods: {
    setName(name) {
      this.selectedName = name;
    },
    saveName() {
      alert(`Default username saved: ${this.selectedName}`);
    }
  }
};
</script>

<style scoped>
.darkmode3{
  background: #777575 !important;
  color: #ffffff;
}

button {
  padding: 5px 10px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}
</style>
