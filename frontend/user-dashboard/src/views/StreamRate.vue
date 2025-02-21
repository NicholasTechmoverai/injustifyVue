<template>
  <div id="youSectionC" class="card common-scrollbar">
    <div id="sectioncmoststreamedSongs">
      <div id="moststreamedSongsHeader" class="card header">
        <span>Stream Rate</span>
        <span>Best</span>

        <!-- Options Button -->
        <button class="options-button" @click="toggleDropdown">
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
      <div id="moststreamedSongsBody" v-if="loading">
        <p>Loading stream rate data...</p>
      </div>

      <!-- Stream Rate Data -->
      <div id="moststreamedSongsBody" v-else>
        <div 
          v-for="(user, index) in users" 
          :key="index" 
          class="user-item"
          :class="{ 'currentUser': user.userId === userId }"
        >
          <router-link :to="`/profile/${user.userId}`">
            <img :src="user.profile_image_url" alt="User Profile" class="profile-img">
          </router-link>
          <div class="user-info">
            <div class="user-name">{{ user.username }}</div>
            <div class="user-rank">Rank: #{{ user.global_rank }}</div>
            <div class="engagement-score">
                Score: {{ Number(user.engagement_score).toFixed(2) }}
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
import { watch, ref, onMounted, onUnmounted } from "vue";

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

    watch(() => userStore.userId, async (newUserId) => {
      if (newUserId) {
        userId.value = newUserId;
        await fetchStreamRate();
      }
    });

    return {
      users,
      loading,
      dropdownOpen,
      toggleDropdown,
      sharePlaylist,
    };
  },
};
</script>


<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #aaaaae;
  padding: 10px 15px;
  border-radius: 8px;
  margin: 4px 0;
  position: relative;
}

.options-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #ffffff;
  font-size: 20px;
}
#moststreamedHeader {
 
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #dadada;
  padding: 10px 15px;
  border-radius: 8px;

}
.profile-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
}

.user-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-rank, .engagement-score {
  font-size: 14px;
  color: gray;
}

.currentUser {
  background-color: #2bb0ce66;
}
/* Dropdown menu */
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
</style>
