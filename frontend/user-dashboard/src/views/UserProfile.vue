<template>
  <div v-if="loading" id="loading">
    <ion-icon name="reload-outline"></ion-icon>
  </div>
  <div class="MainContainer" :class="{ collabsedBig: iscollapsedBig }">
    <div id="profileUserInfo" :class="{ 'darktheme-5': isDarkMode }">
      <div id="profile-pic">
        <div class="profile-pic-ON">
          <img
            :src="user.picture || defaultProfilePic"
            alt="Profile Picture"
            class="circular-profile_pic"
            @click="triggerFileInput"
          />
        </div>
        <div class="profile-edit" v-if="user.email === this.useremail">
          <button
            type="button"
            id="saveprofileChanges"
            @click="saveProfileChanges"
            :class="{ 'darktheme-3': isDarkMode }"
          >
            <i class="fas fa-pencil-alt"></i> Save
          </button>
        </div>
      </div>

      <div class="profile-info">
        <h3>{{ user.name }}</h3>
        <p v-if="user.created_at">User since: {{ formattedDate }}</p>

        <div id="userEmail" class="card" :class="{ 'darktheme-4': isDarkMode }">
          <div id="veryEmail">{{ user.email }}</div>
          <div v-if="user.verified_email === 1" id="verifiedState">
            <i class="fas fa-check-circle"></i>
            <span>Verified</span>
          </div>
        </div>

        <div id="top-songs-Adhered" :class="{ 'darktheme-4': isDarkMode }">
          <div id="top-songs-adheredHeader">
            <h3>Top Songs Adhered</h3>
          </div>
          <div class="top-songs-list">
            <div class="artist-socialist">
              <div class="artist-info">
                <img src="" />
                <p>Adele</p>
                <div class="WheatherVerified">
                  <i class="fas fa-check-circle"></i>
                </div>
              </div>
              <div class="thesong">
                <h4>Easy On Me</h4>
                <div class="moreOn-song">
                  <div class="songPviews">1.5B views</div>
                  <div class="songpYear">6 months ago</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Hidden File Input -->
      <input
        type="file"
        ref="fileInput"
        accept="image/*"
        @change="handleFileChange"
        style="display: none"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, computed, onMounted, watch, toRefs } from "vue";
import { useUserStore } from "@/store/index.js";
import { BASE_URL } from "@/utils/index.js";
export default {
  name: "UserProfile",
  props: {
    useremail: String, // User email passed as
  },
  setup(props) {
    const { useremail } = toRefs(props); // Make props reactive
    const user = ref({});
    const newProfilePicture = ref(null);
    const defaultProfilePic = "/path/to/default.jpg";
    const fileInput = ref(null);
    const loading = ref(false);
    const playlistId = ref(null); // Store playlist ID
    const userStore = useUserStore();

    // Theme handling
    const themeClass = computed(() => {
      return document.cookie.includes("theme=dark") ? "dark-mode" : "";
    });

    // Format date safely
    const formattedDate = computed(() => {
      if (!user.value.created_at) return "Unknown";
      return user.value.created_at.split(" ").slice(1, 4).join(" ");
    });

    // Fetch user profile
    const fetchUserProfile = async () => {
      loading.value = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/profile/${useremail.value}`);
        user.value = response.data.user_info?response.data.user_info:response.data;
        playlistId.value = response.data.playlistId; // Assuming the response contains a playlistId
      } catch (error) {
        console.error("Error fetching profile:", error);
      } finally {
        loading.value = false;
      }
    };

    // Watch for useremail changes and refetch profile
    watch(useremail, (newEmail, oldEmail) => {
      if (newEmail !== oldEmail) {
        fetchUserProfile();
      }
    });

    // Trigger file input when profile picture is clicked
    const triggerFileInput = () => {
      if (user.value.email === useremail.value) {
        fileInput.value.click();
      }
    };

    // Handle profile picture change
    const handleFileChange = (event) => {
      if (user.value.email === useremail.value) {
        const file = event.target.files[0];
        if (file) {
          user.value.picture = URL.createObjectURL(file);
          newProfilePicture.value = file;
        }
      }
    };

    // Save profile changes
    const saveProfileChanges = async () => {
      if (!newProfilePicture.value) return;

      const formData = new FormData();
      formData.append("profile_picture", newProfilePicture.value);
      formData.append("user_id", user.value.id); // Fix: Use `user.value.id` instead of `props.userId`

      try {
        await axios.post(`${BASE_URL}/api/update-profile`, formData);
        console.log("Profile updated successfully!");
      } catch (error) {
        console.error("Error updating profile:", error);
      }
    };

    // Fetch profile on mount
    onMounted(fetchUserProfile);

    return {
      user,
      loading,
      formattedDate,
      themeClass,
      defaultProfilePic,
      fileInput,
      triggerFileInput,
      handleFileChange,
      saveProfileChanges,
      playlistId,
      iscollapsedBig: computed(() => userStore.iscollapsedBig),
      isDarkMode: computed(() => userStore.isdarkmode),
    };
  },
};
</script>

<style scoped>
h3 {
  color: #2c3e50;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
}

p {
  font-size: 14px;
  color: #7f8c8d;
  margin: 5px 0;
}

#profileUserInfo {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  width: 100%;
  box-sizing: border-box;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}
.circular-profile_pic {
  position: relative;
  width: 150px;
  height: 150px;
  margin-bottom: 15px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #3498db;
}

.cicircular-profile_pic img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-edit {
  position: absolute;
  top: 85%;
  right: 10px;
  background: #3498db;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.profile-edit:hover {
  background: #2980b9;
}

.profile-info {
  text-align: center;
  margin-top: 10px;
}

#userEmail {
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

#verifiedState {
  color: green;
  margin-left: 10px;
  font-weight: bold;
}

#top-songs-Adhered {
  width: 100%;
  margin-top: 20px;
  padding: 15px;
  background: white;
  border-radius: 10px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.top-songs-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.artist-socialist {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.artist-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.artist-info img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.WheatherVerified {
  color: #3498db;
  font-size: 14px;
  margin-left: 5px;
}

.moreOn-song {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #7f8c8d;
}

#loading {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  color: #3498db;
}

/*daark theme*/
.darktheme-1 {
  background: #1e1e1e !important;
  color: #f0f0f0 !important;
}

/* Dark Theme 2 - Header */
.darktheme-2 {
  background: #2c2c2c !important;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
  color: #e7e7e7 !important;
}

/* Dark Theme 3 - Buttons */
.darktheme-3 {
  background: #3a3a3a !important;
  color: #ffffff !important;
  border: 1px solid #555 !important;
}

.darktheme-3:hover {
  background: #505050 !important;
}

/* Dark Theme 4 - Inputs */
.darktheme-4 {
  background: #2a2a2a !important;
  color: #e0e0e0 !important;
  border: 1px solid #444 !important;
}
.darktheme-4 h3 {
  color: #e0e0e0 !important;
}
.darktheme-5 h3,
.darktheme-4 h3 {
  color: #cfc7c7 !important;
}
/* Dark Theme 5 - Video Sections */
.darktheme-5 {
  background: #373737 !important;
  color: #d4d4d4 !important;
}

@media (max-width: 768px) {
  #profileUserInfo {
    padding: 15px;
  }
  .artist-socialist {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
