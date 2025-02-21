<template>
  <div id="youSectionC" class="card common-scrollbar">
    <div id="sectioncmoststreamedSongs">
      <div id="moststreamedSongsHeader" class="card header">
        <span>Playlists</span>
        <span>Best</span>
        <button class="options-btn"><ion-icon name="options-outline"></ion-icon></button>
      </div>

      <div id="moststreamedSongsBody">
        <div v-if="loading" class="loading-text">Loading...</div>
        <div v-else-if="playlists && playlists.length === 0" class="empty-text">No playlists found</div>
        <div v-else>
          <div 
            v-for="(playlist) in playlists" 
            :key="playlist.id" 
            class="playlist-item"
            :playlist_id="playlist.id"
            @click="setAsActivePlaylist(playlist.id)"
          >
            <div class="playlist-title">{{ playlist.name }}</div>
            <div class="playlist-description">{{ playlist.description }}</div>
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
  name:"PlaylistPage",

  data() {
    return {
      playlists: [],  // ✅ Always initialized as an array
      userId: null,
      loading: false,  
    };
  },
  async mounted() {
    const userStore = useUserStore();
    this.userId = userStore.userId;
    if (this.userId) {
      await this.fetchPlaylists();
    }
  },
  methods: {
    fetchPlaylists() {
      this.loading = true;
      axios
        .get(`${BASE_URL}/api/songs/pls/${this.userId}`)
        .then((response) => {
          console.log("playlist::", response.data.playlists);
          this.playlists = Array.isArray(response.data.playlists) ? response.data.playlists : [];
        })
        .catch((error) => {
          console.error("API Error:", error);
          this.playlists = [];  // ✅ Handle API failure
        })
        .finally(() => {
          this.loading = false;
        });
    },
    setAsActivePlaylist(playlistId) {
      const userStore = useUserStore();
      userStore.setActivePlaylist(playlistId);
    }
  },
};
</script>

<style scoped>
/* ✅ Added styles for a cleaner UI */
#youSectionC {
  background: inherit;
  padding: 20px;
  border-radius: 10px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #dadada;
  padding: 10px 15px;
  border-radius: 8px;
}

.options-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
}

#moststreamedSongsBody {
  margin-top: 10px;
}

.loading-text, .empty-text {
  text-align: center;
  margin-top: 20px;
}

.playlist-item {
  background: #dcdcde;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: background 0.3s;
}

.playlist-item:hover {
  background: #3a3a3c7b;
}

.playlist-title {
  font-size: 16px;
  font-weight: bold;
}

.playlist-description {
  font-size: 14px;
  margin-top: 5px;
}
</style>
