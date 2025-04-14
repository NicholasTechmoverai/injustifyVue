<template>
  <div id="youSectionC" class="card common-scrollbar">
    <div id="sectioncmoststreamedSongs">
    
      <div id="moststreamedSongsHeader" class="header">
        <span>Playlists</span>
        <button class="options-btn" @click="toggleDropdown">
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
              @blur="toggleEdit(playlist.id, playlist.name)"
            />
            <span class="star" @click="toggleStarred($event)"> ★</span>
            <p class="songCount">{{ playlist.song_count }}</p>
            <p class="created_at">{{ formatDate(playlist.created_at) }}</p>
            <router-link :to="`/profile/${playlist.created_by}`">
              <img class="playlistRefPic" :src="playlist.picture" alt="" srcset="" />
            </router-link>
            <div class="playlist-description">{{ playlist.description }}</div>

            <div class="playlist-options">
              <ion-icon
                name="ellipsis-vertical-circle-outline"
                class="menu-icon"
              ></ion-icon>

              <!-- Hidden by default, shown on hover -->
              <div class="playlist_moreinfo" :class="{ 'darktheme-2': isDarkMode }">
                <button @click.stop="toggleEdit(playlist.id, playlist.name)">
                  <ion-icon name="pencil-sharp"></ion-icon>
                  {{ activeEditableId === playlist.id ? "Save" : "Edit" }}
                </button>
                <button @click="deletePlaylist(playlist.id)" class="delete-btn">
                  <ion-icon name="trash-outline"></ion-icon> Delete
                </button>
                <button><ion-icon name="share-social-outline"></ion-icon> Share</button>
              </div>
            </div>
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
import { BASE_URL, formatDate } from "@/utils";
import { useUserStore } from "@/store/index.js";
import injustifyIcon from "../assets/injustify.png";

export default {
  name: "PlaylistPage",
  props: {
    userId: String,
  },

  data() {
    const userStore = useUserStore();

    return {
      playlists: [],
      userIda: this.userId || null,
      loading: false,
      isDarkMode: computed(() => userStore.isdarkmode),
      activeEditableId: null,
      dropdownOpen: false,
      addPlaylist: false,
      formatDate,
      injustifyIcon,
    };
  },
  async mounted() {
    const userStore = useUserStore();
    this.userIda = this.userId || userStore.userId;
    if (this.userIda) {
      await this.fetchPlaylists();
    }
  },
  methods: {
    fetchPlaylists() {
      if (this.loading) return;
      this.loading = true;
      axios
        .get(`${BASE_URL}/api/songs/pls/${this.userIda}?_t=${new Date().getTime()}`)
        .then((response) => {
          console.log("playlist 💯💯::", response.data.playlists);
          const randomPlylist = {
            id: "3031",
            name: "Random Playlist",
            song_count: 20,
            created_at: new Date(),
            created_by: 1,
            picture: this.injustifyIcon,
            description: "",
          };
          this.playlists = [];

          this.playlists = Array.isArray(response.data.playlists)
            ? response.data.playlists
            : [];
          this.playlists.unshift(randomPlylist);
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
        this.renamePlaylist(playlistId, playlistName);
        this.activeEditableId = null;
      } else {
        this.activeEditableId = playlistId;
      }
    },
    toggleDropdown(event) {
      event.stopPropagation();
      this.dropdownOpen = !this.dropdownOpen;
    },
    toggleStarred(event) {
      event.stopPropagation();
      const target = event.target; // Get the clicked element

      if (!target.classList.contains("starred")) {
        target.classList.add("starred");
      } else {
        target.classList.remove("starred");
      }
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
      if (pl_id && newName) {
        axios
          .post(`${BASE_URL}/api/songs/rnm_pls`, {
            playlistId: pl_id,
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
    deletePlaylist(pl_id) {
      if (pl_id) {
        axios
          .post(`${BASE_URL}/api/songs/del_pls`, {
            playlistId: pl_id,
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
.star {
  font-size: 20px;
  color: #444;
  cursor: pointer;
  transition: color 0.3s ease-in-out;
}

.star.starred {
  color: #fdbc00;
  transition: color 0.3s ease-in-out;
}
.playlistRefPic {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
}
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: #ababacf1;
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
  padding: 10px 0;
  font-size: 20px;
  font-weight: bold;
  border-bottom: 1px solid #ddd;
  position: relative;
}

.options-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #666;
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
  display: flex;
  flex-direction: row;
  position: relative;
}
.created_at {
  position: absolute;
  bottom: 0;
  right: 2px;
  white-space: nowrap;
  font-size: 10px;
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
.darktheme-2 input {
  background-color: transparent;
  color: #bdbdbd;
}

.playlist-item {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Soft shadow */
  padding: 15px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  cursor: pointer;
}

.playlist-item:hover {
  transform: scale(1.02); /* Subtle zoom effect */
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  z-index: 20;
}

/* Playlist Title Input */
.playlist-title {
  font-size: 18px;
  font-weight: 600;
  color: #585858;
  border: none;
  background: transparent;
  width: 100% !important;
  outline: none;
}

.playlist-title-edit {
  border-bottom: 2px solid #007bff; /* Highlighted input for editing */
}

/* Playlist Info */
.songCount,
.created_at {
  color: #666;
}
.songCount {
  margin-right: auto;
  font-size: 10px;
  position: absolute;
  left: 5%;
  bottom: 0;
}
.playlist-description {
  font-size: 14px;
  color: #444;
  opacity: 0.85;
  flex: 1;
}

/* Profile Picture */
.playlistRefPic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ddd;
  transition: transform 0.2s ease-in-out;
}

.playlistRefPic:hover {
  transform: scale(1.1);
  border-color: #007bff;
}

/* Playlist Options (Three-Dot Menu) */
.playlist-options {
  position: relative;
}

.menu-icon {
  font-size: 24px;
  color: #666;
  cursor: pointer;
  transition: transform 0.2s ease-in-out, color 0.2s;
}

.menu-icon:hover {
  transform: scale(1.2);
  color: #007bff;
}

/* Dropdown Menu */
.playlist_moreinfo {
  position: absolute;
  top: 80%;
  right: 0;
  background: #dcdcde;
  border-radius: 10px;
  box-shadow: 0 0px 4px rgba(0, 0, 0, 0.15);
  padding: 10px;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s ease-in-out, transform 0.2s ease-in-out;
  min-width: 120px;
  z-index: 10;
}

.playlist-options:hover .playlist_moreinfo {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

/* Buttons inside dropdown */
.playlist_moreinfo button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  padding: 8px;
  width: 100%;
  font-size: 14px;
  cursor: pointer;
  color: inherit;
  text-align: left;
  transition: background 0.2s ease-in-out;
}

.playlist_moreinfo button:hover {
  background: rgba(0, 123, 255, 0.1);
  color: #007bff;
}

.delete-btn {
  color: red;
}

.delete-btn:hover {
  background: rgba(255, 0, 0, 0.1);
}
</style>
