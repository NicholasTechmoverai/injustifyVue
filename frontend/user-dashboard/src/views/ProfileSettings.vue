<template>
  <div class="profile-settings" :class="{ darkmode4: isDarkMode }">
    <h2>Profile Settings</h2>

    <!-- Profile Picture & Name -->
    <div class="section">
      <h3>Profile Info</h3>
      <div class="profile-pic">
        <img :src="userpicture" alt="Profile Picture" @click="triggerFileInput" />
        <input
          type="file"
          ref="fileInput"
          accept="image/*"
          @change="handleFileChange"
          hidden
        />
      </div>
      <div class="profile-name">
        <input type="text" v-model="username" placeholder="Enter your name" />
        <button @click="saveProfile">Save</button>
      </div>
    </div>

    <!-- Name Preference -->
    <div class="preference-item" :class="{ darkmode3: isDarkMode }">
      <h4>Name Preference</h4>
      <p>Select one of your names below as the default username:</p>
      <div class="name-options">
        <span @click="setName('Nicholas')">Nicholas</span>
        <span @click="setName('Kariuki')">Kariuki</span>
      </div>
      <div class="name-edit">
        <input v-model="selectedName" type="text" />
        <button @click="saveName">Save</button>
      </div>
    </div>

    <!-- Theme Preference -->
    <div class="section">
      <h3>Appearance</h3>
      <label class="toggle">
        <input type="checkbox" v-model="isDarkMode" @change="toggleTheme" />
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
        <input type="checkbox" v-model="user.profilePublic" /> Make Profile Public
      </label>
      <label>
        <input type="checkbox" v-model="user.allowFriendRequests" /> Allow Friend Requests
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

<style scoped>
.section {
  margin-bottom: 20px;
}
.profile-pic {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: gray;
  overflow: hidden;
}
.profile-pic img {
  width: 100%;
  height: 100%;
  cursor: pointer;
  object-fit: cover;
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
.preference-item {
  background: rgba(255, 255, 255, 0.149);
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
</style>
