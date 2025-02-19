<template>
  <div class="preferences-container">
    <h3>Preferences</h3>
    
    <!-- Theme Preference -->
    <div class="preference-item">
      <h4>Theme</h4>
      <label class="toggle ThemeToggle">
        <span><i class="fa-solid fa-sun"></i> Light</span>
        <input type="checkbox" v-model="isDarkMode">
        <span class="slider mode-toggle"></span>
        <span><i class="fa-solid fa-moon"></i> Dark</span>
      </label>
    </div>
    
    <!-- Name Preference -->
    <div class="preference-item">
      <h4>Name Preference</h4>
      <p>Select one of your names below as the default username:</p>
      <div class="name-options">
        <span @click="setName('Nicholas')">Nicholas</span>
        <span @click="setName('Kariuki')">Kariuki</span>
      </div>
      <div class="name-edit">
        <input v-model="selectedName" type="text"/>
        <button @click="saveName">Save</button>
      </div>
    </div>
    
    <!-- Font and Language Preferences -->
    <div class="preference-item">
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
    <div class="preference-item">
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
    <div class="preference-item">
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
    <div class="preference-item">
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
export default {
  props: {
    currentView: String
  },
  data() {
    return {
      isDarkMode: false,
      selectedName: 'Nicholas',
      selectedFont: 'Arial',
      selectedLanguage: 'English',
      enableEqualizer: false,
      enableCrossfade: false,
      playbackQuality: 'medium',
      enableDataSaver: false,
      downloadQuality: '256',
      resumeOnStartup: true,
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
.preferences-container {
  padding: 20px;
  background: #f4f4f4;
  border-radius: 8px;
  max-width: 600px;
  margin: auto;
}
.preference-item {
  background: white;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 5px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}
.name-options span {
  cursor: pointer;
  margin-right: 10px;
  font-weight: bold;
}
.name-edit input {
  width: 70%;
  padding: 5px;
  margin-right: 10px;
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
