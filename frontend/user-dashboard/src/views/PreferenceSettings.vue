

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
      isDarkMode:computed(() => userStore.isdarkmode),
      fontSize: 16,
      selectedLanguage: 'en',
      availableFonts: [
        { value: 'Arial', label: 'Arial' },
        { value: 'Verdana', label: 'Verdana' },
        { value: 'Helvetica', label: 'Helvetica' },
        { value: 'Georgia', label: 'Georgia' },
        { value: 'Courier New', label: 'Courier New' },
        { value: 'Roboto', label: 'Roboto' },
        { value: 'Open Sans', label: 'Open Sans' }
      ],
      availableLanguages: [
        { code: 'en', name: 'English', native: 'English' },
        { code: 'es', name: 'Spanish', native: 'Español' },
        { code: 'fr', name: 'French', native: 'Français' },
        { code: 'de', name: 'German', native: 'Deutsch' },
        { code: 'ja', name: 'Japanese', native: '日本語' }
      ],
      // Audio
      enableEqualizer: false,
      enableCrossfade: true,
      crossfadeDuration: 3,
      playbackQuality: 'high',
      playbackQualities: [
        { value: 'low', name: 'Low', desc: '128 kbps', icon: 'fas fa-battery-quarter' },
        { value: 'medium', name: 'Medium', desc: '256 kbps', icon: 'fas fa-battery-half' },
        { value: 'high', name: 'High', desc: '320 kbps', icon: 'fas fa-battery-full' },
        { value: 'lossless', name: 'Lossless', desc: 'FLAC/ALAC', icon: 'fas fa-bolt' }
      ],
      // Streaming
      enableDataSaver: false,
      downloadOnWifiOnly: true,
      downloadQuality: '320',
      cacheSize: 500,
      downloadQualities: [
        { value: '128', name: 'Standard', desc: '128 kbps' },
        { value: '256', name: 'High', desc: '256 kbps' },
        { value: '320', name: 'Premium', desc: '320 kbps' }
      ],
      // Startup
      resumeOnStartup: true,
      startMinimized: false,
      autoUpdateCheck: true,
      defaultView: 'library',
      defaultViews: [
        { value: 'library', name: 'Library', icon: 'fas fa-book' },
        { value: 'discover', name: 'Discover', icon: 'fas fa-compass' },
        { value: 'recent', name: 'Recent', icon: 'fas fa-history' },
        { value: 'playlists', name: 'Playlists', icon: 'fas fa-list' }
      ]
    }
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

<template>
  <div class="preferences-container" :class="{'dark-mode': isDarkMode}">
    <div class="preferences-header">
      <h2 class="preferences-title">
        <i class="fas fa-sliders-h"></i> Preferences
      </h2>
      <div class="preferences-actions">
        <button class="reset-btn" @click="resetToDefaults">
          <i class="fas fa-undo"></i> Reset Defaults
        </button>
        <button class="save-btn" @click="savePreferences">
          <i class="fas fa-save"></i> Save Changes
        </button>
      </div>
    </div>

    <div class="preferences-grid">
      <!-- Font & Language Section -->
      <div class="preference-card">
        <div class="card-header">
          <i class="fas fa-font"></i>
          <h3>Display & Language</h3>
        </div>
        
        <div class="preference-control">
          <label>App Font</label>
          <div class="select-wrapper">
            <select v-model="selectedFont" class="modern-select">
              <option v-for="font in availableFonts" :value="font.value" :key="font.value" :style="{ fontFamily: font.value }">
                {{ font.label }}
              </option>
            </select>
            <i class="fas fa-chevron-down"></i>
          </div>
          <div class="font-preview" :style="{ fontFamily: selectedFont }">
            Preview: The quick brown fox jumps over the lazy dog
          </div>
        </div>
        
        <div class="preference-control">
          <label>Interface Language</label>
          <div class="select-wrapper">
            <select v-model="selectedLanguage" class="modern-select">
              <option v-for="lang in availableLanguages" :value="lang.code" :key="lang.code">
                {{ lang.name }} ({{ lang.native }})
              </option>
            </select>
            <i class="fas fa-chevron-down"></i>
          </div>
        </div>
        
        <div class="preference-control">
          <label>Font Size</label>
          <div class="range-control">
            <i class="fas fa-text-height"></i>
            <input 
              type="range" 
              v-model="fontSize" 
              min="12" 
              max="24" 
              step="1"
              @input="updateFontSizePreview"
            >
            <span class="range-value">{{ fontSize }}px</span>
          </div>
        </div>
      </div>

      <!-- Audio Preferences Section -->
      <div class="preference-card">
        <div class="card-header">
          <i class="fas fa-music"></i>
          <h3>Audio Settings</h3>
        </div>
        
        <div class="toggle-group">
          <label class="toggle-item">
            <input type="checkbox" v-model="enableEqualizer" class="toggle-input">
            <span class="toggle-slider"></span>
            <span class="toggle-label">Enable Equalizer</span>
            <i class="fas fa-info-circle" title="Customize audio frequencies for optimal listening"></i>
          </label>
          
          <label class="toggle-item">
            <input type="checkbox" v-model="enableCrossfade" class="toggle-input">
            <span class="toggle-slider"></span>
            <span class="toggle-label">Enable Crossfade</span>
            <span class="subtext">({{ crossfadeDuration }} seconds)</span>
            <i class="fas fa-info-circle" title="Smooth transition between tracks"></i>
          </label>
          
          <div v-if="enableCrossfade" class="range-control">
            <i class="fas fa-exchange-alt"></i>
            <input 
              type="range" 
              v-model="crossfadeDuration" 
              min="1" 
              max="10" 
              step="1"
            >
            <span class="range-value">{{ crossfadeDuration }}s</span>
          </div>
        </div>
        
        <div class="preference-control">
          <label>Playback Quality</label>
          <div class="quality-options">
            <label 
              v-for="quality in playbackQualities" 
              :key="quality.value"
              :class="{ 'active': playbackQuality === quality.value }"
            >
              <input 
                type="radio" 
                v-model="playbackQuality" 
                :value="quality.value"
              >
              <div class="quality-card">
                <div class="quality-icon">
                  <i :class="quality.icon"></i>
                </div>
                <div class="quality-details">
                  <span class="quality-name">{{ quality.name }}</span>
                  <span class="quality-desc">{{ quality.desc }}</span>
                </div>
              </div>
            </label>
          </div>
        </div>
      </div>

      <!-- Streaming & Download Section -->
      <div class="preference-card">
        <div class="card-header">
          <i class="fas fa-wifi"></i>
          <h3>Streaming & Download</h3>
        </div>
        
        <div class="toggle-group">
          <label class="toggle-item">
            <input type="checkbox" v-model="enableDataSaver" class="toggle-input">
            <span class="toggle-slider"></span>
            <span class="toggle-label">Data Saver Mode</span>
            <i class="fas fa-info-circle" title="Reduce data usage when on mobile networks"></i>
          </label>
          
          <label class="toggle-item">
            <input type="checkbox" v-model="downloadOnWifiOnly" class="toggle-input">
            <span class="toggle-slider"></span>
            <span class="toggle-label">Download on Wi-Fi Only</span>
          </label>
        </div>
        
        <div class="preference-control">
          <label>Download Quality</label>
          <div class="quality-options compact">
            <label 
              v-for="quality in downloadQualities" 
              :key="quality.value"
              :class="{ 'active': downloadQuality === quality.value }"
            >
              <input 
                type="radio" 
                v-model="downloadQuality" 
                :value="quality.value"
              >
              <div class="quality-card">
                <span class="quality-name">{{ quality.name }}</span>
                <span class="quality-desc">{{ quality.desc }}</span>
              </div>
            </label>
          </div>
        </div>
        
        <div class="preference-control">
          <label>Cache Size</label>
          <div class="range-control">
            <i class="fas fa-database"></i>
            <input 
              type="range" 
              v-model="cacheSize" 
              min="100" 
              max="1000" 
              step="50"
            >
            <span class="range-value">{{ cacheSize }}MB</span>
          </div>
          <button class="clear-cache-btn" @click="clearCache">
            <i class="fas fa-trash-alt"></i> Clear Cache
          </button>
        </div>
      </div>

      <!-- Startup & Behavior Section -->
      <div class="preference-card">
        <div class="card-header">
          <i class="fas fa-power-off"></i>
          <h3>Startup & Behavior</h3>
        </div>
        
        <div class="toggle-group">
          <label class="toggle-item">
            <input type="checkbox" v-model="resumeOnStartup" class="toggle-input">
            <span class="toggle-slider"></span>
            <span class="toggle-label">Resume Playback</span>
            <span class="subtext">Continue where you left off</span>
          </label>
          
          <label class="toggle-item">
            <input type="checkbox" v-model="startMinimized" class="toggle-input">
            <span class="toggle-slider"></span>
            <span class="toggle-label">Start Minimized</span>
          </label>
          
          <label class="toggle-item">
            <input type="checkbox" v-model="autoUpdateCheck" class="toggle-input">
            <span class="toggle-slider"></span>
            <span class="toggle-label">Check for Updates</span>
            <span class="subtext">Automatically check for new versions</span>
          </label>
        </div>
        
        <div class="preference-control">
          <label>Default View</label>
          <div class="view-options">
            <label 
              v-for="view in defaultViews" 
              :key="view.value"
              :class="{ 'active': defaultView === view.value }"
            >
              <input 
                type="radio" 
                v-model="defaultView" 
                :value="view.value"
              >
              <div class="view-card">
                <i :class="view.icon"></i>
                <span>{{ view.name }}</span>
              </div>
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
/* Base Styles */
.preferences-container {
  --primary-color: #4285f4;
  --primary-light: #e8f0fe;
  --primary-dark: #3367d6;
  --text-primary: #202124;
  --text-secondary: #5f6368;
  --bg-color: #ffffff;
  --card-bg: #ffffff;
  --border-color: #dadce0;
  --hover-color: #f1f3f4;
  --success-color: #34a853;
  --error-color: #ea4335;
  --warning-color: #fbbc05;
  --toggle-off: #cccccc;
  font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
  background-color: var(--bg-color);
  color: var(--text-primary);
  transition: all 0.3s ease;
}

/* Dark Mode */
.preferences-container.dark-mode {
  --primary-color: #8ab4f8;
  --primary-light: #202124;
  --text-primary: #e8eaed;
  --text-secondary: #9aa0a6;
  --bg-color: #121212;
  --card-bg: #1e1e1e;
  --border-color: #3c4043;
  --hover-color: #2d2d2d;
  --toggle-off: #555555;
}

/* Layout */
.preferences-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.preferences-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--primary-color);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.preferences-actions {
  display: flex;
  gap: 0.75rem;
}

.preferences-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.preference-card {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
  transition: transform 0.2s, box-shadow 0.2s;
}

.preference-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  color: var(--primary-color);
}

.card-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

/* Buttons */
.save-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.save-btn:hover {
  background-color: var(--primary-dark);
  transform: translateY(-1px);
}

.reset-btn {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.reset-btn:hover {
  background-color: var(--hover-color);
  color: var(--text-primary);
}

.clear-cache-btn {
  background-color: transparent;
  color: var(--error-color);
  border: 1px solid var(--error-color);
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.clear-cache-btn:hover {
  background-color: rgba(234, 67, 53, 0.1);
}

/* Form Controls */
.preference-control {
  margin-bottom: 1.5rem;
}

.preference-control label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.select-wrapper {
  position: relative;
}

.modern-select {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background-color: var(--card-bg);
  color: var(--text-primary);
  font-size: 1rem;
  appearance: none;
  transition: border 0.3s, box-shadow 0.3s;
}

.modern-select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
}

.select-wrapper i {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  pointer-events: none;
}

.font-preview {
  margin-top: 0.5rem;
  padding: 0.75rem;
  background-color: var(--primary-light);
  color: var(--primary-color);
  border-radius: 6px;
  font-size: 1rem;
}

/* Toggle Switches */
.toggle-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.toggle-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  position: relative;
}

.toggle-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: relative;
  display: inline-block;
  width: 42px;
  height: 22px;
  background-color: var(--toggle-off);
  transition: .4s;
  border-radius: 22px;
  flex-shrink: 0;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

.toggle-input:checked + .toggle-slider {
  background-color: var(--primary-color);
}

.toggle-input:checked + .toggle-slider:before {
  transform: translateX(20px);
}

.toggle-label {
  flex: 1;
  font-size: 0.9375rem;
}

.subtext {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  margin-left: auto;
}

.toggle-item i.fa-info-circle {
  color: var(--text-secondary);
  opacity: 0.7;
}

/* Range Controls */
.range-control {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.range-control i {
  color: var(--text-secondary);
  width: 20px;
  text-align: center;
}

input[type="range"] {
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: var(--border-color);
  appearance: none;
  outline: none;
}

input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--primary-color);
  cursor: pointer;
  transition: all 0.2s;
}

input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}

.range-value {
  min-width: 50px;
  text-align: right;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

/* Quality Options */
.quality-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
}

.quality-options.compact {
  grid-template-columns: 1fr 1fr;
}

.quality-options label {
  position: relative;
  cursor: pointer;
}

.quality-options input[type="radio"] {
  position: absolute;
  opacity: 0;
}

.quality-card {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  height: 100%;
}

.quality-options input[type="radio"]:checked + .quality-card {
  border-color: var(--primary-color);
  background-color: var(--primary-light);
  color: var(--primary-color);
}

.quality-options input[type="radio"]:hover + .quality-card {
  border-color: var(--primary-color);
}

.quality-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.quality-options input[type="radio"]:checked + .quality-card .quality-icon {
  color: var(--primary-color);
}

.quality-name {
  font-weight: 500;
  display: block;
}

.quality-desc {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  display: block;
}

.quality-options input[type="radio"]:checked + .quality-card .quality-desc {
  color: var(--primary-color);
}

/* View Options */
.view-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 0.75rem;
}

.view-options label {
  position: relative;
  cursor: pointer;
}

.view-options input[type="radio"] {
  position: absolute;
  opacity: 0;
}

.view-card {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.view-options input[type="radio"]:checked + .view-card {
  border-color: var(--primary-color);
  background-color: var(--primary-light);
  color: var(--primary-color);
}

.view-options input[type="radio"]:hover + .view-card {
  border-color: var(--primary-color);
}

.view-card i {
  font-size: 1.25rem;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .preferences-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .preferences-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 480px) {
  .preferences-grid {
    grid-template-columns: 1fr;
  }
  
  .quality-options {
    grid-template-columns: 1fr;
  }
}
</style>