<template>
  <div id="youSectionC" class="card common-scrollbar">
    <div id="sectioncmoststreamedSongs">
      <div id="moststreamedSongsHeader" class="card header">
        <span>Your Top Songs This Month</span>
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

      <div id="moststreamedSongsBody">
        <div v-if="loading" class="loading-text">Loading...</div>
        <div v-else-if="songs.length === 0" class="empty-text">No songs found</div> 
        
        <div v-else>
          <div 
            v-for="(song, index) in songs" 
            :key="index" 
            class="song-item"
            :song_id="song.id"
          >
            <img :src="song.thumbnail" alt="Song thumbnail" class="song-thumbnail">
            <div class="song-details">
              <div class="songTitle">{{ song.title }}</div>
              <div class="songTrendinfo">Rank: {{ song.rank }}</div>
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

export default {
  props: {
    userId: {
      type: String,
      required: false, 
    },
  },
  data() {
    return {
      songs: [], 
      loading: false,
      dropdownOpen: false,
      actualUserId: this.userId || useUserStore().userId, 
    };
  },
  async mounted() {
    if (this.actualUserId) {
      await this.fetchSongs();
    }

    document.addEventListener("click", this.closeDropdownOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.closeDropdownOutside);
  },
  methods: {
    async fetchSongs() {
      if (!this.actualUserId) return; 

      this.loading = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/songs/utr/${this.actualUserId}`);
        console.log("playlist::", response.data.songs);

        this.songs = Array.isArray(response.data.songs) ? response.data.songs : [];
      } catch (error) {
        console.error("API Error:", error);
        this.songs = []; // ✅ Prevent null errors
      } finally {
        this.loading = false;
      }
    },
    toggleDropdown(event) {
      event.stopPropagation();
      this.dropdownOpen = !this.dropdownOpen;
    },
    async sharePlaylist() {
      try {
        await navigator.clipboard.writeText(window.location.href);
        alert("Link copied to clipboard! 🎉");
      } catch (err) {
        console.error("Failed to copy:", err);
      }
      this.dropdownOpen = false;
    },
    closeDropdownOutside(event) {
      if (!event.target.closest(".dropdown-container")) {
        this.dropdownOpen = false;
      }
    },
  },
};
</script>


<style scoped>
/* 🔥 Overall Container Styling */
#youSectionC {
  padding: 20px;
  border-radius: 10px;
  color: #ffffff;
}

/* 🔥 Header Styling */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgb(180, 178, 178);
  padding: 10px 15px;
  border-radius: 8px;
  position: relative;
}

.options-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #ffffff;
  font-size: 20px;
}

/* 🔥 Song List Styling */
#moststreamedSongsBody {
  margin-top: 10px;
}

/* 🔥 Loading & Empty States */
.loading-text, .empty-text {
  text-align: center;
  color: #bbb;
  margin-top: 20px;
}

.song-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: background 0.3s ease-in-out;
  background-color: gray;
}


.song-item:hover {
  background: #3a3a3c;
}

.song-thumbnail {
  width: 200px;
  min-height: 50px;
  background-size: cover; 
  height: auto;
  border-radius: 8px;
  margin-right: 15px;
}

.song-details {
  display: flex;
  flex-direction: column;
}

.songTitle {
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
}

.songTrendinfo {
  font-size: 14px;
  color: #bbb;
  margin-top: 5px;
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
