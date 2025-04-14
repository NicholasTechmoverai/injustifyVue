<template>
  <div id="youSectionC" class="common-scrollbar">
    <div id="sectioncmoststreamedSongs">
      <div class="header">
        <span>#Trending</span>
        <!-- Options Button -->
        <button class="options-btn" @click="toggleDropdown">
          <ion-icon name="options-outline"></ion-icon>
        </button>

        <!-- Dropdown Menu -->
        <div
          v-if="dropdownOpen"
          class="dropdown-menu"
          :class="{ 'darktheme-2': isDarkMode }"
        >
          <ul>
            <li @click="searchPlaylist">🔍 Search</li>
            <li @click="sharePlaylist">📤 Share</li>
          </ul>
        </div>
      </div>

      <div id="moststreamedSongsBody">
        <div v-if="loading" class="loading-text">Loading...</div>
        <div v-else-if="songs.length === 0" class="empty-text">No songs available</div>
        <div v-else id="ssfads">
          <div
            v-for="(song, index) in songs"
            :key="song.song_id || index"
            :class="{ 'darktheme-2': isDarkMode }"
            class="song-item"
          >
            <router-link :to="`/you/stream/${song.song_id}`">
              <img :src="song.thumbnail" alt="Song thumbnail" class="song-thumbnail" />
            </router-link>
            <div class="song-duration">{{ song.duration || "3:50" }}</div>
            <div class="song-info">
              <div class="song-text">
                <div class="songTitle">{{ song.title }}</div>
                <div class="songArtist">{{ song.artist }}</div>
              </div>

              <div class="song-actions-container">
                <ion-icon
                  class="song-actions-p-button"
                  name="ellipsis-vertical"
                  @click="toggleActions"
                ></ion-icon>
                <div class="song-actions" :class="{ 'darktheme-2': isDarkMode }">
                  <button @click="unlikeSong(song.id)" class="action-btn unlike-btn">
                    <ion-icon name="heart-dislike-outline"></ion-icon>
                  </button>
                  <button @click="downloadSong(song.id)" class="action-btn">
                    <ion-icon name="download-outline"></ion-icon>
                  </button>
                  <button @click="shareSong(song.id)" class="action-btn">
                    <ion-icon name="share-social-outline"></ion-icon>
                  </button>
                </div>
              </div>
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
import { computed } from "vue";

export default {
  name: "UserDownloads",
  data() {
    const userStore = useUserStore();
    return {
      songs: [],
      loading: false,
      isDarkMode: computed(() => userStore.isdarkmode),
    };
  },
  async mounted() {
    await this.fetchTrendingSongs();
  },
  methods: {
    async fetchTrendingSongs() {
      this.loading = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/songs/tr`);
        console.log("playlist::", response.data.songs);

        this.songs = Array.isArray(response.data.songs) ? response.data.songs : [];
      } catch (error) {
        console.error("API Error:", error);
        this.songs = [];
      } finally {
        this.loading = false;
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
}
/* Header Styling */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  font-size: 20px;
  font-weight: bold;
  border-bottom: 1px solid #ddd;
}

.options-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #666;
}

#moststreamedSongsBody {
  margin-top: 15px;
  gap: 2px;
}
#ssfads {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  gap: 2px !important;
}

.loading-text,
.empty-text {
  text-align: center;
  color: #888;
  margin-top: 20px;
}

/* Song Item Styling */
.song-item {
  display: flex;
  align-items: center;
  padding: 5px;
  border-radius: 8px;
  transition: all 0.2s ease-in-out;
  position: relative;
  overflow: visible;
  background: #dcdcde;
}
.song-item:hover {
  background: #f0f0f0;
}

/* Song Thumbnail */
.song-thumbnail {
  width: 100px;
  height: 65px;
  border-radius: 5px;
  object-fit: cover;
  margin-right: 15px;
}

/* Song Information and Actions */
.song-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.song-text {
  display: flex;
  flex-direction: column;
}

.songTitle {
  font-size: 16px;
  color: #222;
  display: -webkit-box; /* Use a flex-like box for line clamping */
  -webkit-box-orient: vertical; /* Specify vertical stacking of lines */
  -webkit-line-clamp: 3; /* Allow only two lines */
  overflow: hidden; /* Hide overflowed text */
  text-overflow: ellipsis; /* Add ellipsis (...) for overflowing text */
  word-wrap: normal; /* Prevent forced breaks */
  width: 100%;
}

.songArtist {
  font-size: 14px;
  color: #555;
  margin-top: 3px;
}

.song-actions-container {
  position: relative;
  display: inline-block;
}

.song-actions-p-button {
  position: absolute;
  right: 3px;
  top: 0;
  font-size: 18px;
  cursor: pointer;
  font-weight: bolder;
  color: grey;
}

.song-actions-p-button:hover {
  transform: scale(1.2);
  color: blue;
}

.song-actions {
  display: none;
  flex-direction: column;
  position: absolute;
  top: 100%;
  right: 0;
  background: #fff;
  padding: 5px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.song-actions-container:hover .song-actions {
  display: flex;
  z-index: 102;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
  transition: transform 0.2s ease-in-out;
}

.action-btn:hover {
  transform: scale(1.2);
}

.unlike-btn {
  color: #e74c3c;
}
.song-duration {
  position: absolute;
  bottom: 0;
  border-radius: 4px;
  padding: 2px 4px;
  background: #f4f4f4;
  color: #333;
  font-size: 10px !important;
  margin-left: 0px;
  margin-bottom: 5px;
}

/*dark theme*/
.darktheme-2 {
  background: #2c2c2c !important;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
  color: #e7e7e7 !important;
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
