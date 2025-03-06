<template>
  <div id="youSectionC" class="card common-scrollbar">
    <div id="sectioncmoststreamedSongs">
      <div
        id="moststreamedSongsHeader"
        :class="{ 'darktheme-2': isDarkMode }"
        class="header"
      >
        <span>Playlists</span>
        <span>Best</span>
        <button class="options-button" @click="toggleDropdown">
          <ion-icon name="options-outline"></ion-icon>
        </button>
        <div
          v-if="dropdownOpen"
          class="dropdown-menu"
          ref="dropdownRef"
          :class="{ 'darktheme-2': isDarkMode }"
        >
          <ul>
            <li @click="searchPlaylist">🔍 Search</li>
            <li @click="addNewPlaylist">
              <ion-icon name="add-circle-outline"></ion-icon> add
            </li>
          </ul>
        </div>
      </div>

      <div id="moststreamedSongsBody">
        <div v-if="loading" class="loading-text">Loading...</div>
        <div v-else-if="playlists && playlists.length === 0" class="empty-text">
          No playlists found
        </div>
        <div v-else>
          <div
            v-for="playlist in playlists"
            :key="playlist.id"
            class="playlist-item"
            :class="{ 'darktheme-2': isDarkMode }"
            :playlist_id="playlist.id"
            @click="setAsActivePlaylist(playlist.id)"
          >
            <input
              class="playlist-title"
              v-model="playlist.name"
              :class="{ 'playlist-title-edit': activeEditableId === playlist.id }"
              :readonly="activeEditableId !== playlist.id"
            />
            {{ playlist.song_count }}
            {{ formatDate(playlist.created_at)}}
            <img class="playlistRefPic" :src="playlist.picture " alt="" srcset="">
            <div class="playlist-description">{{ playlist.description }}</div>
            <button @click.stop="toggleEdit(playlist.id, playlist.name)">
              {{ activeEditableId === playlist.id ? "Save" : "Edit" }}
            </button>
          </div>
        </div>
        <div
          v-if="addPlaylist"
          class="playlist-item"
          :class="{ 'darktheme-2': isDarkMode }"
        >
          <input
            class="playlist-title-edit"
            v-model="newPlaylistName"
            placeholder="New playlist"
          />
          <button @click="SaveNewPlaylist">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { computed } from "vue";
import { BASE_URL,formatDate } from "@/utils";
import { useUserStore } from "@/store/index.js";

export default {
  name: "PlaylistPage",

  data() {
    const userStore = useUserStore();

    return {
      playlists: [],
      userId: null,
      loading: false,
      isDarkMode: computed(() => userStore.isdarkmode),
      activeEditableId: null,
      dropdownOpen: false,
      addPlaylist: false,
      formatDate,
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
          this.playlists = Array.isArray(response.data.playlists)
            ? response.data.playlists
            : [];
        })
        .catch((error) => {
          console.error("API Error:", error);
          this.playlists = []; // ✅ Handle API failure
        })
        .finally(() => {
          this.loading = false;
        });
    },
    setAsActivePlaylist(playlistId) {
      const userStore = useUserStore();
      userStore.setActivePlaylist(playlistId);
    },
    toggleEdit(playlistId, playlistName) {
      if (this.activeEditableId === playlistId) {
        console.log("Saving:>>", playlistName);
        this.renamePlaylist(playlistId, playlistName)
        this.activeEditableId = null;
      } else {
        this.activeEditableId = playlistId;
      }
    },
    toggleDropdown(event) {
      event.stopPropagation();
      this.dropdownOpen = !this.dropdownOpen;
    },
    addNewPlaylist() {
      this.addPlaylist = true;
      this.newPlaylistName = "";
    },
    SaveNewPlaylist() {
      if (this.newPlaylistName) {
        const userStore = useUserStore();
        axios
          .post(`${BASE_URL}/api/songs/add_pls`, {
            userId: userStore.userId,
            name: this.newPlaylistName,
          })
          .then((response) => {
            console.log("playlist::", response.data.info);
            this.fetchPlaylists();
            this.addPlaylist = false;
          })
          .catch((error) => {
            console.error("API Error:", error);
            alert("Failed to create playlist");
          });
      } else {
        alert("Playlist name is required");
      }
    },
    renamePlaylist(pl_id, newName) {
      if (pl_id && newName ) {
        axios
          .post(`${BASE_URL}/api/songs/rnm_pls`, {
            playlistId:pl_id,
            newName: newName,
          })
          .then((response) => {
            console.log("playlist::", response.data.info);
            this.fetchPlaylists();
            this.addPlaylist = false;
          })
          .catch((error) => {
            console.error("API Error:", error);
            alert("Failed to create playlist");
          });
      } else {
        alert("Playlist name is required");
      }
    },
  },
};
</script>

<style scoped>
.playlistRefPic{
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
}
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: #dcdcde;
  color: rgb(47, 44, 44);
  border-radius: 8px;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.3);
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
  transition: background 0.2s;
}

.dropdown-menu li:hover {
  background: #625b5b94;
}
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
  position: relative;
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

.loading-text,
.empty-text {
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
  border: none;
  outline: none;
  cursor: pointer;
  background-color: transparent;
}
.playlist-title input {
  background-color: transparent;
}
.playlist-title-edit {
  border-bottom: 1px solid green !important;
  outline: 1px solid transparent !important;
  background-color: transparent;
  color: inherit;
  cursor: text !important;
}

.playlist-description {
  font-size: 14px;
  margin-top: 5px;
}
.darktheme-2 {
  background: #2c2c2c !important;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
  color: #e7e7e7 !important;
}
</style>
