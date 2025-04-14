<template>
  <div v-if="loading" class="loading-overlay">
    <div class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i>
    </div>
  </div>

  <div
    class="MainContainer"
    :class="{ collabsedBig: iscollapsedBig, 'dark-mode': isDarkMode }"
  >
    <div class="profile-card" :class="{ 'dark-card': isDarkMode }">
      <!-- Profile Header -->
      <div class="profile-header">
        <div class="profile-picture" @click="triggerFileInput">
          <img
            :src="user.picture || defaultProfilePic"
            alt="Profile Picture"
            class="profile-image"
          />
          <div v-if="user.email === this.useremail" class="edit-overlay">
            <i class="fas fa-camera"></i>
          </div>
        </div>

        <div class="profile-actions" v-if="user.email === this.useremail">
          <button
            class="save-button"
            @click="saveProfileChanges"
            :class="{ 'dark-button': isDarkMode }"
            :disabled="!newProfilePicture"
          >
            <i class="fas fa-save"></i> Save Changes
          </button>
        </div>
      </div>

      <!-- Profile Info -->
      <div class="profile-info">
        <h2 class="profile-name">{{ user.name }}</h2>
        <p class="member-since" v-if="user.created_at">
          <i class="fas fa-calendar-alt"></i> Member since
          {{ formatDate(user.created_at) }}
        </p>

        <div class="email-card" :class="{ 'dark-email-card': isDarkMode }">
          <div class="email-address">
            <i class="fas fa-envelope"></i> {{ user.email }}
          </div>
          <div v-if="user.verified_email === 1" class="verified-badge">
            <i class="fas fa-check-circle"></i>
            <span>Verified</span>
          </div>
        </div>
      </div>

      <!-- Top Songs Section -->
      <div class="top-songs-section" :class="{ 'dark-section': isDarkMode }">
        <h3 class="section-title"><i class="fas fa-music"></i> Top Songs Adhered</h3>

        <div class="song-list">
          <div class="song-card" v-for="(song, index) in sampleSongs" :key="index">
            <div class="song-number">{{ index + 1 }}</div>
            <div class="song-info">
              <div class="artist-info">
                <img :src="song.artistImage" class="artist-image" />
                <div class="artist-name">{{ song.artist }}</div>
                <div class="verified-icon" v-if="song.verified">
                  <i class="fas fa-check-circle"></i>
                </div>
              </div>
              <div class="song-details">
                <h4 class="song-title">{{ song.title }}</h4>
                <div class="song-meta">
                  <span class="song-views">
                    <i class="fas fa-eye"></i> {{ song.views }}
                  </span>
                  <span class="song-date">
                    <i class="fas fa-clock"></i> {{ song.date }}
                  </span>
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
import { BASE_URL, formatDate } from "@/utils/index.js";

export default {
  name: "UserProfile",
  props: {
    useremail: String,
  },
  setup(props) {
    const { useremail } = toRefs(props);
    const user = ref({});
    const newProfilePicture = ref(null);
    const defaultProfilePic = "/default-profile-blue.png";
    const fileInput = ref(null);
    const loading = ref(false);
    const playlistId = ref(null);
    const userStore = useUserStore();

    // Sample data for top songs
    const sampleSongs = ref([
      {
        artist: "Adele",
        artistImage: "https://i.scdn.co/image/ab6761610000e5ebc9690bc711d04b3d4fd4b87c",
        title: "Easy On Me",
        views: "1.5B views",
        date: "6 months ago",
        verified: true,
      },
      {
        artist: "The Weeknd",
        artistImage: "https://i.scdn.co/image/ab6761610000e5eb092dc8cf4408e6d8eaeef2fe",
        title: "Blinding Lights",
        views: "3.2B views",
        date: "2 years ago",
        verified: true,
      },
      {
        artist: "Dua Lipa",
        artistImage: "https://i.scdn.co/image/ab6761610000e5ebc8d3d98a1bccbe71393dbfbf",
        title: "Don't Start Now",
        views: "2.1B views",
        date: "1 year ago",
        verified: true,
      },
    ]);

    const fetchUserProfile = async () => {
      loading.value = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/profile/${useremail.value}`);
        user.value = response.data.user_info ? response.data.user_info : response.data;
        playlistId.value = response.data.playlistId;
      } catch (error) {
        console.error("Error fetching profile:", error);
        userStore.set_snackbarMessage("Failed to load profile", "error", 5000);
      } finally {
        loading.value = false;
      }
    };

    watch(useremail, fetchUserProfile);

    const triggerFileInput = () => {
      if (user.value.email === useremail.value) {
        fileInput.value.click();
      }
    };

    const handleFileChange = (event) => {
      if (user.value.email === useremail.value) {
        const file = event.target.files[0];
        if (file && file.type.match("image.*")) {
          const reader = new FileReader();
          reader.onload = (e) => {
            user.value.picture = e.target.result;
          };
          reader.readAsDataURL(file);
          newProfilePicture.value = file;
        } else {
          userStore.set_snackbarMessage(
            "Please select a valid image file",
            "error",
            5000
          );
        }
      }
    };

    const saveProfileChanges = async () => {
      if (!newProfilePicture.value) return;

      const formData = new FormData();
      formData.append("profilePic", newProfilePicture.value);
      formData.append("userId", user.value.id);

      try {
        loading.value = true;
        const response = await axios.post(
          `${BASE_URL}/api/profile/updateProfile`,
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );

        if (response.data.success) {
          userStore.setUser(response.data.user ?? user.value);
          userStore.set_snackbarMessage("Profile updated successfully!", "success", 5000);
          newProfilePicture.value = null;
        } else {
          throw new Error(response.data.message || "Update failed");
        }
      } catch (error) {
        console.error("Error updating profile:", error);
        userStore.set_snackbarMessage(
          error.message || "Failed to update profile",
          "error",
          5000
        );
      } finally {
        loading.value = false;
      }
    };

    onMounted(fetchUserProfile);

    return {
      user,
      loading,
      defaultProfilePic,
      fileInput,
      sampleSongs,
      triggerFileInput,
      handleFileChange,
      saveProfileChanges,
      playlistId,
      formatDate,
      newProfilePicture,
      iscollapsedBig: computed(() => userStore.iscollapsedBig),
      isDarkMode: computed(() => userStore.isdarkmode),
    };
  },
};
</script>

<style scoped>
/* Base Styles */
.profile-container {
  transition: all 0.3s ease;
  padding: 20px;
  width: 100%;
  margin: 0 auto;
}


.profile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 120, 255, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.dark-card {
  background: #202124;
  color: #e6e6e6;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  color: #0078ff;
  font-size: 3rem;
}

/* Profile Header */
.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 20px 20px;
  background: linear-gradient(135deg, #0078ff 0%, #00c6ff 100%);
  color: white;
  position: relative;
}

.dark-card .profile-header {
  background: linear-gradient(135deg, #005bb5 0%, #0082e6 100%);
}

.profile-picture {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 4px solid white;
  overflow: hidden;
  cursor: pointer;
  position: relative;
  transition: transform 0.3s ease;
}

.profile-picture:hover {
  transform: scale(1.05);
}

.profile-picture:hover .edit-overlay {
  opacity: 1;
}

.edit-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  color: white;
  font-size: 1.5rem;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-actions {
  margin-top: 20px;
}

.save-button {
  background: white;
  color: #0078ff;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.save-button:hover {
  background: #f0f8ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 120, 255, 0.2);
}

.save-button:disabled {
  background: #cccccc;
  color: #666666;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.dark-button {
  background: #0078ff;
  color: white;
}

.dark-button:hover {
  background: #0066cc;
}

/* Profile Info */
.profile-info {
  padding: 20px;
  text-align: center;
}

.profile-name {
  font-size: 1.8rem;
  margin-bottom: 5px;
  color: #333;
}

.dark-card .profile-name {
  color: #fff;
}

.member-since {
  color: #666;
  margin-bottom: 20px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.dark-card .member-since {
  color: #aaa;
}

.email-card {
  background: #f5f9ff;
  border-radius: 10px;
  padding: 15px;
  margin: 20px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #e0e0e0;
}

.dark-email-card {
  background: #2F2F2F;
  border-color: #373737;
}

.email-address {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: #333;
}

.dark-card .email-address {
  color: #e6e6e6;
}

.verified-badge {
  background: #00c853;
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 5px;
}

/* Top Songs Section */
.top-songs-section {
  margin-top: 20px;
  padding: 20px;
  border-top: 1px solid #eee;
}

.dark-section {
  border-top-color: #2F2F2F;
}

.section-title {
  color: #0078ff;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.dark-card .section-title {
  color: #00c6ff;
}

.song-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.song-card {
  display: flex;
  align-items: center;
  background: #f8faff;
  border-radius: 10px;
  padding: 12px;
  transition: all 0.3s ease;
}

.dark-card .song-card {
  background: #16213e;
}

.song-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 120, 255, 0.1);
}

.song-number {
  font-size: 1.2rem;
  font-weight: bold;
  color: #0078ff;
  min-width: 30px;
}

.song-info {
  display: flex;
  flex: 1;
  align-items: center;
  gap: 15px;
}

.artist-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.artist-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.artist-name {
  font-weight: 500;
}

.verified-icon {
  color: #00c853;
  font-size: 0.9rem;
}

.song-details {
  flex: 1;
  text-align: left;
}

.song-title {
  margin: 0;
  font-size: 1rem;
  color: #333;
}

.dark-card .song-title {
  color: #e6e6e6;
}

.song-meta {
  display: flex;
  gap: 15px;
  margin-top: 5px;
  font-size: 0.8rem;
  color: #666;
}

.dark-card .song-meta {
  color: #aaa;
}

.song-views, .song-date {
  display: flex;
  align-items: center;
  gap: 3px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .profile-card {
   width: 100%;
  }
  .profile-header {
    padding: 20px 0px;
    border-radius: 0px;
  }

  .profile-picture {
    width: 120px;
    height: 120px;
  }

  .profile-name {
    font-size: 1.5rem;
  }

  .song-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
}
</style>
