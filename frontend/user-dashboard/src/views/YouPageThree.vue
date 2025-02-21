<template>
  <div id="youSectionC" class="card common-scrollbar">
    <div id="sectioncmoststreamedSongs">
      <div id="moststreamedSongsHeader" class="card">
        <span v-if="!playlist_name" class="no-playlist">No playlist!!</span>
        <span v-else>
          <span class="playing-text">Playing...</span><br>
          <span class="playlist-name">{{ playlist_name }}</span>
        </span>

        <!-- Options Button -->
        <button class="options-button" @click="toggleDropdown">
          <ion-icon name="options-outline"></ion-icon>
        </button>

        <!-- Dropdown Menu -->
        <div v-if="dropdownOpen" class="dropdown-menu" ref="dropdownRef">
          <ul>
            <li @click="searchPlaylist">🔍 Search</li>
            <li @click="sharePlaylist">📤 Share</li>
            <li @click="editPlaylist">✏️ Edit</li>
            <li @click="deletePlaylist">🗑️ Delete</li>
          </ul>
        </div>
      </div>

      <div id="moststreamedSongsBody">
        <div v-for="(song, index) in songs" :key="index" class="song-item" :song_id="song.id">
          <img :src="song.thumbnail" alt="Song thumbnail">
          <div class="songTitle">{{ song.title }}</div>
          <div class="songTrendinfo">{{ song.rank }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { BASE_URL } from "@/utils";
import { useUserStore } from "@/store/index.js";
import { computed, watch, ref, onMounted, onUnmounted } from "vue";

export default {
  name: "ActivePlaylist",
  props: {
    playlist_id: String,
  },
  setup(props) {
    const userStore = useUserStore();
    const songs = ref([]);
    const playlist_name = ref("");
    const loading = ref(false);
    const dropdownOpen = ref(false);
    const dropdownRef = ref(null); // ✅ Ref for dropdown

    const playlist_id = computed(() => props.playlist_id || userStore.activePlaylistId);

    const fetchVideos = async () => {
      if (!playlist_id.value) {
        console.warn("Playlist ID is missing.");
        songs.value = [];
        playlist_name.value = "";
        return;
      }

      loading.value = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/songs/pl/${playlist_id.value}`);
        console.log("Playlist Songs:", response.data.songs?.songs || []);

        songs.value = response.data.songs?.songs || [];
        playlist_name.value = response.data.songs?.playlist_name || "Unknown Playlist";
      } catch (error) {
        console.error("API Error:", error);
        songs.value = [];
      } finally {
        loading.value = false;
      }
    };

    watch(playlist_id, fetchVideos, { immediate: true });

    const sharePlaylist = async () => {
      try {
        await navigator.clipboard.writeText(`${window.location.origin}/you/upls/ls/${playlist_id.value}`);
        alert("Link copied to clipboard! 🎉");
      } catch (err) {
        console.error("Failed to copy:", err);
      }
      dropdownOpen.value = false;
    };

    // ✅ Toggle dropdown
    const toggleDropdown = (event) => {
      event.stopPropagation(); // Prevent event bubbling
      dropdownOpen.value = !dropdownOpen.value;
    };

    // ✅ Close dropdown when clicking outside
    const closeDropdownOutside = (event) => {
      if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
        dropdownOpen.value = false;
      }
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
      dropdownRef, // ✅ Bind to template
      toggleDropdown,
      sharePlaylist
    };
  },
};
</script>


<style scoped>
/* Header Styling */
#moststreamedSongsHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #1e1e1e;
  color: white;
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
  color: lightgray;
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


  
<style scoped>
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
    background: linear-gradient(to right,  
        gray 20%,  
        rgba(128,128,128,0.8) 40%,  
        rgba(128,128,128,0.5) 60%,  
        rgba(128,128,128,0.2) 80%,  
        rgba(128,128,128,0) 100%
    );
    margin: 5px 0;
    padding: 5px 10px;
    border-radius: 5px;
    width: 100%;
    min-height: 40px;
    box-sizing: border-box;
}

#youSectionC #moststreamedSongsBody > .song-item:hover {
    background: linear-gradient(to right,  
        rgba(128,128,128,0) 0%,  
        rgba(128,128,128,0.2) 20%,  
        rgba(128,128,128,0.5) 40%,  
        rgba(128,128,128,0.8) 60%,  
        gray 80%
    );
}

#youSectionC .song-item img {
    width: 100px;
    height: auto;
    object-fit: cover;
    border-radius: 5px;
}

#youSectionC .songTitle {
    font-weight: bold;
    color: #fff;
}

#youSectionC .songTrendinfo {
    color: #aaa;
    font-size: 0.9em;
}

</style>
