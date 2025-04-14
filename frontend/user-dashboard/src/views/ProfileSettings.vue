

<script>
import { ref, computed } from "vue";
import { useUserStore } from "@/store/index.js";

export default {
  name: "ProfileSettings",
  setup() {
    const userStore = useUserStore();
    // User settings (moved outside computed)
    const user = ref({
      favoriteGenre: "Pop",
      playbackQuality: "high",
      profilePublic: true,
      allowFriendRequests: true,
    });
    const selectedName = ref("Nicholas");

    const fileInput = ref(null);

    const triggerFileInput = () => fileInput.value.click();

    const handleFileChange = (event) => {
      const file = event.target.files[0];
      if (file) {
        userStore.updateProfilePic(URL.createObjectURL(file));
      }
    };
    const setName = (name) => {
      selectedName.value = name;
    };
    const saveName = () => alert("Name updated!");

    const saveProfile = () => alert("Profile updated!");

    const toggleTheme = () => {
      userStore.setTheme(!userStore.isdarkmode);
    };

    const linkSocialAccount = () => alert("Feature coming soon!");

    return {
      userpicture: computed(() => userStore.profilePic),
      username: computed(() => userStore.name),
      user,
      isDarkMode: computed(() => userStore.isdarkmode),
      fileInput,
      triggerFileInput,
      handleFileChange,
      saveProfile,
      toggleTheme,
      linkSocialAccount,
      setName,
      saveName,
      selectedName,
    };
  },
};
</script>

<template>
  <div class="profile-settings" :class="{ 'dark-mode': isDarkMode }">
    <div class="settings-header">
      <h1 class="settings-title">Profile Settings</h1>
      <div class="theme-toggle">
        <label class="toggle-switch">
          <input type="checkbox" v-model="isDarkMode" @change="toggleTheme" />
          <span class="slider round"></span>
          <span class="toggle-label">{{ isDarkMode ? 'Dark' : 'Light' }} Mode</span>
        </label>
      </div>
    </div>

    <div class="settings-container">
      <!-- Profile Picture & Name Section -->
      <div class="settings-card">
        <div class="card-header">
          <h3 class="card-title">Profile Information</h3>
          <div class="card-actions">
            <button class="save-btn" @click="saveProfile">
              <i class="fas fa-save"></i> Save Changes
            </button>
          </div>
        </div>
        
        <div class="profile-pic-section">
          <div class="avatar-upload" @click="triggerFileInput">
            <div class="avatar-edit">
              <i class="fas fa-camera"></i>
            </div>
            <img :src="userpicture" alt="Profile Picture" class="avatar-preview" />
          </div>
          <input
            type="file"
            ref="fileInput"
            accept="image/*"
            @change="handleFileChange"
            hidden
          />
          
          <div class="profile-name-input">
            <label>Display Name</label>
            <div class="input-with-icon">
              <i class="fas fa-user"></i>
              <input 
                type="text" 
                v-model="username" 
                placeholder="Enter your name" 
                class="modern-input"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Name Preference Section -->
      <div class="settings-card">
        <h3 class="card-title">Name Preferences</h3>
        <p class="card-subtitle">Select your preferred name format</p>
        
        <div class="name-options-grid">
          <div 
            v-for="(namePart, index) in username.split(' ').filter(Boolean)" 
            :key="index"
            class="name-option"
            :class="{ 'selected': selectedName === namePart }"
            @click="setName(namePart)"
          >
            {{ namePart }}
          </div>
        </div>
        
        <div class="custom-name-input">
          <label>Custom Name</label>
          <div class="input-with-action">
            <input 
              v-model="selectedName" 
              type="text" 
              class="modern-input"
              placeholder="Enter custom name"
            />
            <button class="icon-btn" @click="saveName">
              <i class="fas fa-check"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Music Preferences Section -->
      <div class="settings-card">
        <h3 class="card-title">Music Preferences</h3>
        
        <div class="preference-row">
          <div class="preference-control">
            <label>Favorite Genre</label>
            <div class="select-wrapper">
              <i class="fas fa-music"></i>
              <select v-model="user.favoriteGenre" class="modern-select">
                <option value="Pop">Pop</option>
                <option value="Rock">Rock</option>
                <option value="Jazz">Jazz</option>
                <option value="Hip-Hop">Hip-Hop</option>
                <option value="Electronic">Electronic</option>
                <option value="Classical">Classical</option>
              </select>
            </div>
          </div>
          
          <div class="preference-control">
            <label>Playback Quality</label>
            <div class="select-wrapper">
              <i class="fas fa-headphones"></i>
              <select v-model="user.playbackQuality" class="modern-select">
                <option value="low">Low (128kbps)</option>
                <option value="medium">Medium (256kbps)</option>
                <option value="high">High (320kbps)</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Privacy Settings Section -->
      <div class="settings-card">
        <h3 class="card-title">Privacy Settings</h3>
        
        <div class="privacy-options">
          <label class="privacy-toggle">
            <input type="checkbox" v-model="user.profilePublic" />
            <span class="toggle-slider"></span>
            <span class="toggle-text">Make Profile Public</span>
          </label>
          
          <label class="privacy-toggle">
            <input type="checkbox" v-model="user.allowFriendRequests" />
            <span class="toggle-slider"></span>
            <span class="toggle-text">Allow Friend Requests</span>
          </label>
          
          <label class="privacy-toggle">
            <input type="checkbox" v-model="user.showActivityStatus" />
            <span class="toggle-slider"></span>
            <span class="toggle-text">Show Activity Status</span>
          </label>
        </div>
      </div>

      <!-- Social Connections Section -->
      <div class="settings-card">
        <h3 class="card-title">Social Connections</h3>
        <p class="card-subtitle">Connect your accounts for better experience</p>
        
        <div class="social-buttons">
          <button class="social-btn spotify" @click="linkSocialAccount('spotify')">
            <i class="fab fa-spotify"></i> Connect Spotify
          </button>
          <button class="social-btn facebook" @click="linkSocialAccount('facebook')">
            <i class="fab fa-facebook-f"></i> Link Facebook
          </button>
          <button class="social-btn twitter" @click="linkSocialAccount('twitter')">
            <i class="fab fa-twitter"></i> Connect Twitter
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Base Styles */
.profile-settings {
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
  font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
  background-color: var(--bg-color);
  color: var(--text-primary);
  min-height: 100vh;
  transition: all 0.3s ease;
}

/* Dark Mode */
.profile-settings.dark-mode {
  --primary-color: #8ab4f8;
  --primary-light: #202124;
  --text-primary: #e8eaed;
  --text-secondary: #9aa0a6;
  --bg-color: #121212;
  --card-bg: #1e1e1e;
  --border-color: #3c4043;
  --hover-color: #2d2d2d;
}

/* Layout */
.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.settings-title {
  font-size: 2rem;
  font-weight: 600;
  color: var(--primary-color);
  margin: 0;
}

.settings-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}

.settings-card {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
  transition: transform 0.2s, box-shadow 0.2s;
}

.settings-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: var(--primary-color);
}

.card-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
  margin-bottom: 1.5rem;
}

/* Profile Picture Section */
.profile-pic-section {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.avatar-upload {
  position: relative;
  width: 100px;
  height: 100px;
  cursor: pointer;
}

.avatar-preview {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--primary-light);
}

.avatar-edit {
  position: absolute;
  right: 0;
  bottom: 0;
  background-color: var(--primary-color);
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s;
}

.avatar-upload:hover .avatar-edit {
  transform: scale(1.1);
}

.profile-name-input {
  flex: 1;
}

/* Input Styles */
.modern-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background-color: var(--card-bg);
  color: var(--text-primary);
  font-size: 1rem;
  transition: border 0.3s, box-shadow 0.3s;
  box-sizing: border-box;
}

.modern-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
}

.input-with-icon {
  position: relative;
}

.input-with-icon i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.input-with-action {
  display: flex;
  gap: 0.5rem;
}

/* Select Styles */
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

.select-wrapper {
  position: relative;
}

.select-wrapper i {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  pointer-events: none;
}

/* Button Styles */
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

.icon-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.icon-btn:hover {
  background-color: var(--primary-dark);
  transform: scale(1.05);
}

/* Name Options */
.name-options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.name-option {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background-color: var(--primary-light);
  color: var(--primary-color);
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid transparent;
}

.name-option:hover {
  background-color: rgba(66, 133, 244, 0.1);
}

.name-option.selected {
  background-color: var(--primary-color);
  color: white;
  font-weight: 500;
}

/* Preference Rows */
.preference-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.preference-control {
  margin-bottom: 1rem;
}

.preference-control label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

/* Toggle Switches */
.toggle-switch {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.toggle-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.slider {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: var(--primary-color);
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.privacy-toggle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  cursor: pointer;
}

.toggle-text {
  flex: 1;
}

.toggle-slider {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
  background-color: #ccc;
  transition: .4s;
  border-radius: 20px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked ~ .toggle-slider {
  background-color: var(--primary-color);
}

input:checked ~ .toggle-slider:before {
  transform: translateX(20px);
}

/* Social Buttons */
.social-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.social-btn {
  flex: 1;
  min-width: 150px;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.social-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.social-btn.spotify {
  background-color: #1DB954;
  color: white;
}

.social-btn.facebook {
  background-color: #1877F2;
  color: white;
}

.social-btn.twitter {
  background-color: #1DA1F2;
  color: white;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .settings-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .profile-pic-section {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .preference-row {
    grid-template-columns: 1fr;
  }
  .profile-settings{
    padding: 0;
  }
}
</style>