<template>
  <div id="youSectionC">
    <div id="sectioncmoststreamedSongs">
      <div
        id="moststreamedSongsHeader"
        class="card"
        :class="{ 'darktheme-2': isDarkMode }"
      >
        <span v-if="!playlist_name" class="no-playlist">No playlist!!</span>
        <span v-else>
          <span class="playing-text">Playing...</span><br />
          <span class="playlist-name">{{ playlist_name }}</span>
        </span>

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
            <li @click="sharePlaylist">📤 Share</li>
            <li @click="editPlaylist">✏️ Edit</li>
            <li @click="deletePlaylist">🗑️ Delete</li>
          </ul>
        </div>
      </div>

      <div id="moststreamedSongsBody">
        <div
          v-for="(song, index) in songs"
          :key="index"
          class="song-item"
          :song_id="song.song_id"
          @click="playthis(song.song_id)"
        >
          <router-link :to="`/you/stream/${song.song_id}`">
            <img :src="song.thumbnail" alt="Song thumbnail"
          /></router-link>
          <div id="songInfo">
            <div class="songTitle">{{ song.title }}</div>
            <div class="songArtist">{{ song.artist }}</div>
            <div class="songTrendinfo">{{ song.rank }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "@/store/index.js";
import { computed, ref, onMounted, onUnmounted } from "vue";

export default {
  name: "ActivePlaylist",
  props: {
    playlist_id: String,
  },
  setup(props, { emit }) {
    const userStore = useUserStore();
    const songs = computed(() => {
      if (props.songs?.length) {
        return props.songs.map((song) => ({ ...song, isPlaying: false }));
      } else if (userStore.songs?.length) {
        return userStore.songs.flat().map((song) => ({ ...song, isPlaying: false }));
      }
      return [];
    });
    const playlist_name = computed(() => userStore.playlistName);
    const loading = ref(false);
    const dropdownOpen = ref(false);
    const dropdownRef = ref(null); // ✅ Ref for dropdown
    const playlist_id = computed(() => props.playlist_id || userStore.activePlaylistId);

    const isDarkMode = computed(() => userStore.isdarkmode);

    const sharePlaylist = async () => {
      try {
        await navigator.clipboard.writeText(
          `${window.location.origin}/you/upls/ls/${playlist_id.value}`
        );
        alert("Link copied to clipboard! 🎉");
      } catch (err) {
        console.error("Failed to copy:", err);
      }
      dropdownOpen.value = false;
    };

    const toggleDropdown = (event) => {
      event.stopPropagation(); // Prevent event bubbling
      dropdownOpen.value = !dropdownOpen.value;
    };

    const closeDropdownOutside = (event) => {
      if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
        dropdownOpen.value = false;
      }
    };

    const playthis = (song_id) => {
      console.log("Playing song:", song_id);
      emit("play-song", song_id);
    };

    onMounted(() => {
      document.addEventListener("click", closeDropdownOutside);
    });

    onUnmounted(() => {
      document.removeEventListener("click", closeDropdownOutside);
    });

    return {
      songs,
      loading,
      playlist_name,
      dropdownOpen,
      dropdownRef,
      toggleDropdown,
      sharePlaylist,
      playthis,
      isDarkMode,
    };
  },
};
</script>

<style scoped>
.darktheme-2 {
  background: #2c2c2c !important;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
  color: #e7e7e7 !important;
}
/* Header Styling */
#moststreamedSongsHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #dcdcde;
  color: rgb(24, 21, 21);
  padding: 10px 15px;
  border-radius: 8px;
  position: relative;
}

.no-playlist {
  font-size: 12px;
  color: red;
  font-weight: bold;
}

.playing-text {
  font-size: 10px;
  font-style: italic;
  color: rgb(160, 155, 155);
}

.playlist-name {
  font-size: 14px;
  font-weight: bold;
}

/* Options Button */
.options-button {
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 18px;
  position: relative;
}

.options-button:hover {
  color: #ffcc00;
}

/* Dropdown menu */
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
  height: 85vh;
  overflow-y: auto;
  position: relative;
}

#youSectionC #sectioncmoststreamedSongs {
  flex-direction: column;
  gap: 10px;
  padding: 3px 5px;
}

#youSectionC #moststreamedSongsHeader {
  font-weight: bold;
  position: sticky;
  top: 0;
}

#youSectionC #moststreamedSongsBody {
  gap: 15px;
}

#youSectionC #moststreamedSongsBody > .song-item {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 15px;
  background: linear-gradient(
    to right,
    gray 20%,
    rgba(128, 128, 128, 0.8) 40%,
    rgba(128, 128, 128, 0.5) 60%,
    rgba(128, 128, 128, 0.2) 80%,
    rgba(128, 128, 128, 0) 100%
  );
  margin: 5px 0;
  padding: 5px 10px;
  border-radius: 5px;
  width: 100%;
  min-height: 40px;
  box-sizing: border-box;
}

#youSectionC #moststreamedSongsBody > .song-item:hover {
  background: linear-gradient(
    to right,
    rgba(128, 128, 128, 0) 0%,
    rgba(128, 128, 128, 0.2) 20%,
    rgba(128, 128, 128, 0.5) 40%,
    rgba(128, 128, 128, 0.8) 60%,
    gray 80%
  );
}

#youSectionC .song-item img {
  width: 100px;
  height: 100%;
  object-fit: cover;
  border-radius: 5px;
}
#youSectionC #songInfo {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
#youSectionC .songTitle {
  color: #ebdede !important;
}
#youSectionC .songArtist {
  color: rgb(162, 154, 154) !important;
  text-shadow: 0px 0px 3px black;
}

#youSectionC .songTrendinfo {
  color: #847f7f !important;
  font-size: 0.9em;
}
</style>
