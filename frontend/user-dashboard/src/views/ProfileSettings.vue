<template>
  <div class="profile-settings">
    <h2>Profile Settings</h2>
    
    <!-- Profile Picture & Name -->
    <div class="section">
      <h3>Profile Info</h3>
      <div class="profile-pic">
        <img :src="user.picture || defaultProfilePic" alt="Profile Picture" @click="triggerFileInput"/>
        <input type="file" ref="fileInput" accept="image/*" @change="handleFileChange" hidden />
      </div>
      <div class="profile-name">
        <input type="text" v-model="user.name" placeholder="Enter your name"/>
        <button @click="saveProfile">Save</button>
      </div>
    </div>

    <!-- Theme Preference -->
    <div class="section">
      <h3>Appearance</h3>
      <label class="toggle">
        <input type="checkbox" v-model="darkMode" @change="toggleTheme"/>
        <span class="slider"></span> Dark Mode
      </label>
    </div>

    <!-- Music Preferences -->
    <div class="section">
      <h3>Music Preferences</h3>
      <label>Favorite Genre:</label>
      <select v-model="user.favoriteGenre">
        <option value="Pop">Pop</option>
        <option value="Rock">Rock</option>
        <option value="Jazz">Jazz</option>
        <option value="Hip-Hop">Hip-Hop</option>
      </select>
      <label>Playback Quality:</label>
      <select v-model="user.playbackQuality">
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
    </div>

    <!-- Privacy Settings -->
    <div class="section">
      <h3>Privacy Settings</h3>
      <label>
        <input type="checkbox" v-model="user.profilePublic"/> Make Profile Public
      </label>
      <label>
        <input type="checkbox" v-model="user.allowFriendRequests"/> Allow Friend Requests
      </label>
    </div>

    <!-- Social Connections -->
    <div class="section">
      <h3>Social Connections</h3>
      <button @click="linkSocialAccount">Connect to Spotify</button>
      <button @click="linkSocialAccount">Link Facebook</button>
    </div>
  </div>
</template>

<script>

import { ref } from "vue";

export default {
  
  name: "ProfileSettings",
  setup() {
    const user = ref({
      picture: "",
      name: "",
      favoriteGenre: "Pop",
      playbackQuality: "high",
      profilePublic: true,
      allowFriendRequests: true,
    });
    const darkMode = ref(false);
    const defaultProfilePic = "/default-profile.jpg";
    const fileInput = ref(null);

    const triggerFileInput = () => fileInput.value.click();
    const handleFileChange = (event) => {
      const file = event.target.files[0];
      if (file) user.value.picture = URL.createObjectURL(file);
    };
    const saveProfile = () => alert("Profile updated!");
    const toggleTheme = () => (document.body.classList.toggle("dark-mode"));
    const linkSocialAccount = () => alert("Feature coming soon!");

    return { user, darkMode, fileInput, defaultProfilePic, triggerFileInput, handleFileChange, saveProfile, toggleTheme, linkSocialAccount };
  },
};
</script>

<style scoped>
.profile-settings {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.section {
  margin-bottom: 20px;
}
.profile-pic img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  cursor: pointer;
}
.profile-name input {
  width: 100%;
  padding: 8px;
  margin-top: 10px;
}
button {
  background: #3498db;
  color: #fff;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.toggle {
  display: flex;
  align-items: center;
}
.toggle input {
  margin-right: 10px;
}
</style>
