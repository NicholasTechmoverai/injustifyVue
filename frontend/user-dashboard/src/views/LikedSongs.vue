<template>
  <div id="youSectionC" class="card common-scrollbar">
    <div id="sectioncmoststreamedSongs">
      <div id="moststreamedSongsHeader" class="card header">
        <span>Liked Songs</span>
        <span>Best</span> 
        <button class="options-btn"><ion-icon name="options-outline"></ion-icon></button>
      </div>

      <div id="moststreamedSongsBody">
        <div v-if="loading" class="loading-text">Loading...</div>
        <div v-else-if="songs.length === 0" class="empty-text">No songs available</div>
        
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
              <div class="songTrendinfo">{{ song.rank }}</div>
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
  data() {
    return {
      songs: [], // ✅ Always an array
      loading: false,
      userId: null,
    };
  },
  async mounted() {
    const userStore = useUserStore();
    this.userId = userStore.userId; // ✅ Ensure userId is assigned
    if (this.userId) {
      await this.fetchSongs();
    }
  },
  methods: {
    async fetchSongs() {
      if (!this.userId) return; // ✅ Prevent fetching if userId is missing

      this.loading = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/songs/yls/${this.userId}`);
        console.log("playlist::", response.data.songs);

        // ✅ Ensure songs is always an array
        this.songs = Array.isArray(response.data.songs) ? response.data.songs : [];
      } catch (error) {
        console.error("API Error:", error);
        this.songs = []; // ✅ Prevent null errors
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
  color: #ffffff;
}

/* 🔥 Header Styling */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #c6c6c8;
  padding: 10px 15px;
  border-radius: 8px;
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

/* 🔥 Song Item Styling */
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

/* 🔥 Song Thumbnail */
.song-thumbnail {
  width: 200px;
  min-height: 50px;
  background-size: cover; 
  height: auto;
  border-radius: 8px;
  margin-right: 15px;
}

/* 🔥 Song Details */
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
</style>
