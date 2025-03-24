<template>
  <div class="common-scrollbar">
    <div id="sectioncmoststreamedSongs">
      <div class="header">
        <span>Stream Rate</span>

        <!-- Options Button -->
        <button class="options-btn" @click="toggleDropdown">
          <ion-icon name="options-outline"></ion-icon>
        </button>

        <!-- Dropdown Menu -->
        <div v-if="dropdownOpen" class="dropdown-menu">
          <ul>
            <li @click="searchPlaylist">🔍 Search</li>
            <li @click="sharePlaylist">📤 Share</li>
          </ul>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading">
        <p>Loading stream rate data...</p>
      </div>

      <!-- Stream Rate Data -->
      <div id="moststreamedSongsBody" v-else>
        <div
          v-for="(user, index) in users"
          :key="index"
          class="user-item"
          :class="{ currentUser: user.userId === userId, 'darktheme-2': isDarkMode }"
        >
          <router-link :to="`/profile/${user.userId}`">
            <img :src="user.profile_image_url" alt="User Profile" class="profile-img" />
          </router-link>
          <div class="user-info">
            <div class="user-name">{{ user.username }}</div>
            <div class="user-rank">Rank: #{{ user.global_rank }}</div>
            <div class="engagement-score">
              Notch: {{ Number(user.engagement_score).toFixed(2) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { BASE_URL } from "@/utils";
import { useUserStore } from "@/store/index.js";
import { watch, ref, onMounted, onUnmounted, computed } from "vue";

export default {
  props: {
    userId: { type: String, required: false },
  },
  setup(props) {
    const users = ref([]);
    const loading = ref(false);
    const dropdownOpen = ref(false);
    const userStore = useUserStore();
    const userId = ref(props.userId || userStore.userId);

    const isDarkMode = computed(() => userStore.isdarkmode);

    const fetchStreamRate = async () => {
      loading.value = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/songs/str/${userId.value}`);
        console.log("Stream Rate Data:", response.data.stream_rate);
        users.value = response.data.stream_rate;
      } catch (error) {
        console.error("API Error:", error);
      } finally {
        loading.value = false;
      }
    };

    const toggleDropdown = (event) => {
      event.stopPropagation();
      dropdownOpen.value = !dropdownOpen.value;
    };

    const sharePlaylist = async () => {
      try {
        await navigator.clipboard.writeText(window.location.href);
        alert("Link copied to clipboard! 🎉");
      } catch (err) {
        console.error("Failed to copy:", err);
      }
      dropdownOpen.value = false;
    };

    // Close dropdown when clicking outside
    const closeDropdownOutside = (event) => {
      if (!event.target.closest(".dropdown-container")) {
        dropdownOpen.value = false;
      }
    };

    onMounted(() => {
      if (userId.value) fetchStreamRate();
      document.addEventListener("click", closeDropdownOutside);
    });

    onUnmounted(() => {
      document.removeEventListener("click", closeDropdownOutside);
    });

    watch(
      () => userStore.userId,
      async (newUserId) => {
        if (newUserId) {
          userId.value = newUserId;
          await fetchStreamRate();
        }
      }
    );

    return {
      users,
      loading,
      dropdownOpen,
      toggleDropdown,
      sharePlaylist,
      isDarkMode,
    };
  },
};
</script>

<style scoped>
/* Header Styling */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(10px);
  padding: 10px 0;
  font-size: 20px;
  font-weight: bold;
  position: relative;
  transition: all 0.3s ease-in-out;
  border-bottom: 1px solid #ddd;
  margin-bottom: 5px;
  color: inherit;
}

.options-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #666;
  transition: color 0.3s ease, transform 0.2s ease;
}

.options-btn:hover {
  color: #f0f0f0;
  transform: scale(1.1);
}

#moststreamedHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: inherit;
  backdrop-filter: blur(8px);
  padding: 12px 18px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
}

#moststreamedHeader:hover {
  transform: scale(1.02);
}

.profile-img {
  width: 55px;
  height: 55px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
}

.profile-img:hover {
  transform: scale(1.1);
}

.user-item {
  display: flex;
  align-items: center;
  padding: 10px;
  background: #dcdcde;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: background 0.3s ease-in-out, transform 0.2s ease;
}

.user-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.02);
}
.user-item:hover .profile-img {
  border: 3px solid #2bb0ce;
}

.user-info {
  display: flex;
  flex-direction: column;
  margin-left: 10px;
}

.user-name {
  font-size: 1.1rem;
  font-weight: bold;
  color: #222;
}

.user-rank,
.engagement-score {
  font-size: 14px;
  color: #8f8a8a;
  transition: color 0.3s ease-in-out;
}

.user-item:hover .user-rank,
.user-item:hover .engagement-score {
  color: #908e8e;
}

.currentUser {
  border-left: 4px solid #2bb0ce;
  padding-left: 12px;
  box-shadow: 0 2px 6px rgba(43, 176, 206, 0.5);
  transition: background 0.5s ease;
  animation: backgroundAnim 20s infinite alternate ease-in-out;
}
.currentUser .profile-img {
  border: 3px solid #2bb0ce;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: #2c2c2c;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3);
  width: 120px;
  padding: 5px 0;
  z-index: 10;
}

.dropdown-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown-menu li {
  padding: 10px;
  font-size: 14px;
  cursor: pointer;
  color: white;
  transition: background 0.2s;
}

.dropdown-menu li:hover {
  background: #444;
}

#moststreamedSongsBody {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/*dark theme*/
.darktheme-2 {
  background: #2c2c2c !important;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
  color: #e7e7e7 !important;
}
</style>
