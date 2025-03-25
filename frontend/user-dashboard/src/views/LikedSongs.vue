<template>
  <div id="youSectionC">
    <div id="sectioncmoststreamedSongs">
      <div
        id="moststreamedSongsHeader"
        class="header"
        :class="{ 'darktheme-3': isDarkMode }"
      >
        <span>Liked Songs</span>
        <button class="options-btn">
          <ion-icon name="options-outline"></ion-icon>
        </button>
      </div>

      <div id="moststreamedSongsBody">
        <div v-if="loading" class="loading-text">Loading...</div>
        <div v-else-if="songs.length === 0" class="empty-text">No songs available</div>
        <div v-else id="ssfads">
          <div
            v-for="(song, index) in songs"
            :key="song.id || index"
            :class="{ 'darktheme-2': isDarkMode }"
            class="song-item"
          >
            <img :src="song.thumbnail" alt="Song thumbnail" class="song-thumbnail" />
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
                  <button @click="likeunlikeS(song)" class="action-btn unlike-btn">
                    <ion-icon :name="song.liked ? 'heart' : 'heart-outline'"></ion-icon>
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

<script setup>
import { ref, watch, onMounted, computed } from "vue";
import axios from "axios";
import { BASE_URL } from "@/utils";
import { likeUnlikeSong } from "@/services/websocket";
import { useUserStore } from "@/store/index.js";

const userStore = useUserStore();

const props = defineProps({
  userId: String,
});

const songs = ref([]);
const loading = ref(false);
const isDarkMode = computed(() => userStore.isdarkmode);

const fetchSongs = async () => {
  if (!props.userId) return;
  loading.value = true;
  try {
    const response = await axios.get(`${BASE_URL}/api/songs/yls/${props.userId}`);
    songs.value = Array.isArray(response.data.songs) ? response.data.songs : [];
  } catch (error) {
    console.error("API Error:", error);
    songs.value = [];
  } finally {
    loading.value = false;
  }
};

const likeunlikeS = async (song) => {
  song.liked = !song.liked;
  await likeUnlikeSong(song.song_id, props.userId);
};

const downloadSong = (songId) => {
  console.log(`Downloading song: ${songId}`);
};

const shareSong = (songId) => {
  console.log(`Sharing song: ${songId}`);
};

watch(() => props.userId, fetchSongs, { immediate: true });
onMounted(fetchSongs);
</script>

<style scoped>
/* Overall Container resets any background */
#youSectionC {
  padding: 20px;
  font-family: sans-serif;
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
  color: inherit !important;
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
  height: 60px;
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
</style>
