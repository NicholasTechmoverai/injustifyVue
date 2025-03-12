<template>
  <div class="MainContainer" :class="{ collabsedBig: iscollapsedBig }">
    <div id="homepage-header" :class="{ 'darktheme-2': isDarkMode }">
      <h1 class="injustifyLogoR">Injustify</h1>
      <p>{{ message }}</p>
      <div
        v-if="loading.injustify || loading.youtube || loading.spotify"
        class="spinner-container"
      >
        <h5 class="loader"></h5>
        <p class="loadert">Loading...</p>
      </div>

      <h5>search download</h5>
      {{ query }}
      <div id="searchcontrols">
        <button>tt</button>
        <ion-icon
          @click="toggleSearch"
          :name="showSearch ? 'close-circle-outline' : 'search-circle-outline'"
        ></ion-icon>
        <ion-icon name="options-outline"></ion-icon>
      </div>

      <div id="searchBar" :class="{ 'darktheme-1': isDarkMode }" v-if="showSearch">
        <input
          type="text"
          placeholder="Filter Search"
          v-model="query"
          @input="fetch_suggestions" 

          :class="{ 'darktheme-4': isDarkMode }"
        />
        <button @click="reset" :class="{ 'darktheme-3': isDarkMode }">Clear</button>
        <button @click="searchAll" :class="{ 'darktheme-3': isDarkMode }">Search</button>

        <div v-for="suggestion in search_suggestions" :key="suggestion.name">
          <div>{{ suggestion.name }} {{ suggestion.artist }}</div>
        </div>
      </div>
    </div>

    <!-- Video Sections -->

    <div
      v-for="(videoList, service) in videoSources"
      :key="service"
      id="holder"
      :class="{ 'darktheme-5': isDarkMode }"
    >
      <div class="service" :class="{ 'darktheme-1': isDarkMode }">
        {{ service }} Videos
        <p v-if="loading[service]" class="loadert" :class="{ 'darktheme-2': isDarkMode }">
          Loading...
        </p>
        <img v-if="getLogo(service)" :src="getLogo(service)" alt="Service Logo" />
      </div>

      <div v-if="videoList.length" id="videosContainer">
        <div
          v-for="(video, index) in videoList"
          :key="video.song_id"
          class="video-card"
          :class="{ 'darkthemec-a': isDarkMode }"
        >
          <div @click="playVideo(video)">
            <img :src="getThumbnail(video, service)" alt="Video Thumbnail" />
            <div>
              <h4>{{ getTitle(video, service) }}</h4>
              <p>{{ getArtist(video, service) }}</p>
            </div>
          </div>
          <div class="video-info-holder">
            <div class="video-Meta-info-holder">
              <span><i class="fa-solid fa-eye"></i>{{ video.views }}</span>
              <span>{{ timeAgo(video.date) || "many hours " }}</span>
              <span class="video-duration">{{
                convertSeconds(video.duration) || ""
              }}</span>
            </div>
            <div @click="likeVideo(video)">
              <ion-icon :name="video.liked ? 'heart' : 'heart-outline'"></ion-icon>
            </div>
            <div class="dropdown-container">
              <!-- Skull Icon (Toggle Button) -->
              <div @click="toggleDropdown(index)" class="skull-icon">
                <ion-icon name="skull-sharp"></ion-icon>
              </div>

              <!-- Dropdown Menu -->
              <div v-if="openIndex === index" class="skull-more-options">
                <button @click="handleDownload(video.url)">
                  Injust <ion-icon name="download"></ion-icon>
                </button>
                <button>Djust</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <p v-else class="no-data">
        No {{ service }} videos found
        <img src="../assets/no-videos.webp" alt="" />
      </p>
    </div>
    <!-- Downloads Selector Container -->
    <DownlodSelectorHold
      id="streamsContainer"
      :songId="streamSongID"
      :streamloading="streamloading"
      @selected="handleDownloadSelect"
      v-if="streamloading"
      :class="{ 'darktheme-4': isDarkMode }"
    />
  </div>
</template>

<script>
import DownlodSelectorHold from "./downloadsSelectorContainer.vue";
import socket from "@/services/websocket";
import { computed } from "vue";
import axios from "axios";
import { timeAgo } from "@/utils/index";
import { getYouTubeThumbnails, getSpotifyThumbnail } from "@/utils/index.js";
import { useUserStore } from "@/store/index.js";
import { BASE_URL } from "@/utils/index.js";

export default {
  name: "HomePage",
  components: { DownlodSelectorHold },
  setup() {
    const userStore = useUserStore();

    return {
      iscollapsedBig: computed(() => userStore.iscollapsedBig),
      isDarkMode: computed(() => userStore.isdarkmode),
      useremail: computed(() => userStore.email),
      userId: computed(() => userStore.userId),
      streamloading: computed(() => userStore.streamloading),
    };
  },

  data() {
    const userStore = useUserStore();

    return {
      message: "",
      query: "",
      inj_videos: [],
      yt_videos: [],
      sp_videos: [],
      search_suggestions: [],
      loading: { injustify: false, youtube: false, spotify: false },
      spotifyThumbnails: {}, // Store fetched Spotify thumbnails
      openIndex: null,
      streamSongID: null,
      userStore,
      showSearch: false,
    };
  },

  computed: {
    videoSources() {
      return {
        injustify: this.inj_videos,
        YouTube: this.yt_videos,
        Spotify: this.sp_videos,
      };
    },
  },

  async mounted() {
    if (!this.useremail) {
      console.error("User email is undefined");
      return;
    }

    axios
      .get(`${BASE_URL}/api/${this.useremail}`)
      .then((response) => {
        this.message = response.data.message;
      })
      .catch((error) => console.error("API Error:", error));

    await this.fetchVideos();
    await this.fetchSpotifyThumbnails(); // Preload Spotify thumbnails
  },

  methods: {
    toggleSearch() {
      this.showSearch = !this.showSearch;
    },
    getLogo(service) {
      if (service === "injustify") {
        return new URL("../assets/injustify.png", import.meta.url).href;
      } else if (service === "YouTube") {
        return new URL("../assets/youtube-icon2.jpg", import.meta.url).href;
      } else if (service === "Spotify") {
        return new URL("../assets/spotify-logo.png", import.meta.url).href;
      } else {
        return new URL("../assets/injustify.png", import.meta.url).href;
      }
    },
    toggleDropdown(index) {
      this.openIndex = this.openIndex === index ? null : index;
    },

    handleDownload(video) {
      console.log("Downloading:", video);
      this.streamSongID = video;
      this.userStore.set_streamloading(true);
      this.toggleDropdown();
    },

    reset() {
      this.query = "";
      this.inj_videos = [];
      this.yt_videos = [];
      this.sp_videos = [];
      this.spotifyThumbnails = {};
    },

    async fetch_suggestions() {
  if (this.query.trim() !== '') {
    console.log("Getting suggestions for query:", this.query);
    socket.emit("get_search_suggestions", {
      userId: this.userId,
      query: this.query,
    });
  }
},


    async fetchVideos() {
      this.loading.injustify = true;

      try {
        const response = await axios.get(
          `${BASE_URL}/api/songs/${this.useremail}?search=${this.query}`
        );
        console.log(response.data);
        this.inj_videos = response.data.songs || [];
      } catch (error) {
        console.error("API Error:", error);
      } finally {
        this.loading.injustify = false;
      }
    },

    async fetchSpotifyThumbnails() {
      for (const video of this.sp_videos) {
        if (!this.spotifyThumbnails[video.url]) {
          this.spotifyThumbnails[video.url] = await getSpotifyThumbnail(video.url);
        }
      }
    },

    async searchYouTube(retries = 20, interval = 3000) {
      this.pollServiceResults("youtube", retries, interval);
    },

    async searchSpotify(retries = 20, interval = 3000) {
      this.pollServiceResults("spotify", retries, interval);
    },

    async searchAll() {
      await this.fetchVideos(); // Search local database
      await this.searchYouTube(); // Search YouTube
      await this.searchSpotify(); // Search Spotify
    },

    async pollServiceResults(service, retries = 20, interval = 3000) {
      console.log(`Polling ${service} results for:`, this.query);
      const urls = {
        youtube: `${BASE_URL}/api/songs/pol/yt/${
          this.useremail
        }?search=${encodeURIComponent(this.query)}`,
        spotify: `${BASE_URL}/api/songs/pol/sp/${
          this.useremail
        }?search=${encodeURIComponent(this.query)}`,
      };

      const url = urls[service];
      if (!url) {
        console.error(`Unknown service: ${service}`);
        return;
      }

      this.loading[service] = true;

      const poll = async () => {
        try {
          const response = await axios.get(url);

          if (response.status !== 200) {
            console.error(`${service} server responded with status: ${response.status}`);
            throw new Error(`${service} Error: ${response.statusText}`);
          }

          const data = response.data;

          if (data.success) {
            console.log(`${service} Results:`, data.songs);
            if (service === "youtube") {
              this.yt_videos = data.songs;
            } else {
              this.sp_videos = data.songs;
              await this.fetchSpotifyThumbnails(); // Preload Spotify thumbnails
            }
            this.loading[service] = false;
            return;
          } else {
            console.log(`${service} Results not ready yet...`);
          }
        } catch (error) {
          console.error(`${service} Polling error:`, error);
        }

        retries--;
        if (retries > 0) {
          setTimeout(poll, interval);
        } else {
          console.error(`${service} Polling failed after maximum retries.`);
          this.loading[service] = false;
        }
      };

      poll();
    },

    playVideo(video) {
      console.log("Playing video:", video.url);
      if (video.sourceType === "youtube") {
        window.open(video.preservedSrc, "_blank");
      } else {
        let videoPlayer = new Audio(video.preservedSrc);
        videoPlayer.play();
      }
    },

    likeVideo(video) {
      console.log("Like video:", video.song_id);
      video.liked = !video.liked;
    },

    handleChat(video) {
      console.log("Chat about video:", video.song_id);
      this.$emit("open-chat", video.song_id);
    },

    convertSeconds(seconds) {
      if (seconds < 0) {
        return "0s";
      }

      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const remainingSeconds = seconds % 60;

      if (hours > 0) {
        return `${hours}h ${minutes}m ${Math.ceil(remainingSeconds)}s`;
      } else if (minutes > 0) {
        return `${minutes}m ${Math.ceil(remainingSeconds)}s`;
      } else {
        return `${Math.ceil(remainingSeconds)}s`;
      }
    },

    getThumbnail(video, service) {
      if (service === "YouTube") {
        return getYouTubeThumbnails(video.url);
      } else if (service === "Spotify") {
        return this.spotifyThumbnails[video.url] || video.thumbnail;
      }
      return video.thumbnail;
    },
    getTitle(video, service) {
      if (service === "YouTube") {
        let title = video.title;

        if (title.includes(" - ")) {
          return title.split(" - ")[1].trim();
        } else if (title.includes(" | ")) {
          return title.split(" | ")[0].trim();
        } else if (title.includes(": ")) {
          return title.split(": ")[1].trim();
        } else {
          return title; // Default
        }
      }
      return video.title;
    },

    getArtist(video, service) {
      if (service === "YouTube") {
        let title = video.title;

        if (title.includes(" - ")) {
          return title.split(" - ")[0].trim();
        } else if (title.includes(" | ")) {
          return title.split(" | ")[1].trim();
        } else if (title.includes(": ")) {
          return title.split(": ")[0].trim();
        } else {
          return "Unknown Artist"; // Default
        }
      }
      return video.artist;
    },
    mounted() {
      socket.on("respoce_search_suggestions", (data) => {
        console.log("found suggeestions::",data.search_suggestions)
        this.search_suggestions = data.search_suggestions;
      });
    },
    beforeUnmount() {
      // Remove the listener to prevent memory leaks
      socket.off("respoce_search_suggestions");
    },

    timeAgo,
    getYouTubeThumbnails,
  },
};
</script>

<style scoped>
#streamsContainer {
  border-radius: 10px 10px 0 0;
  position: fixed;
  bottom: 0;
  left: 50%;
  width: 60%;
  transform: translateX(-50%);
  background-color: rgb(222, 217, 217);
  z-index: 100;
  padding: 0 10px;
  box-sizing: border-box;
  box-shadow: 0px 0px 5px black;
}
.dropdown-container {
  position: relative;
  display: inline-block;
}

/* Skull Icon (Toggle Button) */
.skull-icon {
  cursor: pointer;
  font-size: 24px;
  padding: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease-in-out;
}

/* Dropdown Menu */
.skull-more-options {
  position: absolute;
  bottom: 100%;
  right: 0;
  background: rgb(89, 85, 85);
  box-shadow: 0px 0px 8px rgb(0, 0, 0);
  border-radius: 0 15px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  width: 140px;
  border: 1px solid rgb(83, 78, 78);
  color: white;
}

/* Dropdown Buttons */
.skull-more-options button {
  background: none;
  border: none;
  padding: 10px;
  text-align: left;
  cursor: pointer;
  font-size: 14px;
  color: #faf7f7;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.skull-more-options button:hover {
  background: #9c9898;
}
.no-data {
  width: 100%;
  padding: 2rem 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: sticky;
  top: 0;

  img {
    width: 200px;
  }
}
#videosContainer {
  gap: 3px;
  width: 100%;
  margin: 0 auto;
  columns: 5 200px;
  padding: 5px 0;
  box-sizing: border-box;

  .video-card {
    display: inline-block;
    width: 100%;
    break-inside: avoid;
    background: #fff;
    border: solid 2px #ddd;
    border-radius: 8px;
    padding: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease-in-out, box-shadow 0.5s;
    box-sizing: border-box;
    margin: 2px 0;
    color: rgb(66, 62, 62);

    &:hover {
      transform: scale(1.01);
      box-shadow: 0px 0px 5px black;
    }

    > div:first-child {
      cursor: pointer;
      width: 100%;
      text-align: center;
    }

    img {
      width: 100%;
      height: auto;
      border-radius: 8px;
      transition: filter 0.2s ease-in-out;

      &:hover {
        filter: brightness(0.9);
      }
    }

    h4 {
      margin: 8px 0 4px;
      font-size: 1rem;
      font-weight: bold;
      text-align: center;
    }

    p {
      font-size: 0.9rem;
      color: #666;
      text-align: center;
    }

    .video-info-holder {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      padding: 8px;
      border-top: 1px solid #dad1d1;
      margin-top: 8px;
      box-sizing: border-box;

      .video-Meta-info-holder {
        display: flex;
        gap: 10px;
        font-size: 0.85rem;
        color: #555;

        span {
          display: flex;
          align-items: center;
          gap: 5px;
        }
      }

      ion-icon {
        font-size: 1.2rem;
        color: #666;
        cursor: pointer;
        transition: color 0.2s ease-in-out;

        &:hover {
          color: #007bff;
        }
      }

      .video-duration {
        background: rgba(70, 67, 67, 0.8);
        color: #fff;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.8rem;
      }
    }
  }
}
#holder {
  width: 100%;
}
.service {
  width: 90%;
  padding: 5px;
  background-color: white;
  box-shadow: 0 0px 10px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  border-radius: 5px;
  margin: 5px auto;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  font-family: "poppins";
  font-weight: bold;
  box-sizing: border-box;
  img {
    height: 50px;
    width: auto;
    filter: drop-shadow(5px 0px 2px rgba(142, 139, 139, 0.5));
  }
}

#homepage-header {
  width: 100%;
  margin: 0 auto !important;
  padding: 1.5rem;
  padding-top: 0;
  text-align: center;
  background: #eae9e9;
  border-radius: 0 0 10px 10px;
  box-shadow: 0 0px 10px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
  position: sticky;
  top: 0;
  z-index: 99;

  .injustifyLogoR {
    margin-top: 0;
    padding-top: 0;
    text-shadow: 0px 2px 5px black;
  }

  h5 {
    font-size: 1rem;
    font-weight: normal;
    color: inherit;
    margin: auto;
    padding: 0;
    text-align: center;
    font-variant: small-caps;
    text-transform: capitalize;
    font-family: "Arial", sans-serif;
  }

  #searchBar {
    position: absolute !important;
    right: 0;
    top: 50px;
  }

  #searchcontrols {
    position: relative;
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 10px;

    button {
      background: #007bff;
      color: white;
      padding: 3px 10px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background 0.3s ease-in-out;
      &:hover {
        background: #0069d9;
      }
    }
  }
  h3 {
    font-size: 1.2rem;
    font-weight: bold;
    color: inherit;
    margin-bottom: 0.5rem;
    margin: 0;
    padding: 0;
  }

  p {
    font-size: 1rem;
    color: inherit;
    margin-bottom: 1rem;
  }

  .spinner-container {
    position: fixed;
    top: 0;
    right: 1%;
    display: flex;
    justify-content: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    background-color: rgba(255, 255, 255, 0.169) !important;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.815);
    height: fit-content !important;
    padding: 4px !important;
    .loadert {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 120px;
      height: 30px;
      background: #007bff;
      color: white;
      font-weight: bold;
      border-radius: 5px;
      animation: pulse 1.5s infinite alternate;
    }
    .loader {
      transform: scale(0.6);
      padding: 0 !important;
    }

    p,
    h5 {
      margin: 0;
      padding: 0;
    }
    @keyframes pulse {
      0% {
        transform: scale(1);
        opacity: 1;
      }
      100% {
        transform: scale(1.1);
        opacity: 0.8;
      }
    }
  }

  div {
    margin-top: 0px;
    padding: 1rem;
    border-radius: 0px 0px 10px 10px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.05);

    h2 {
      font-size: 1.4rem;
      font-weight: 600;
      color: inherit;
    }

    input {
      width: 80%;
      max-width: 400px;
      padding: 0.6rem;
      font-size: 1rem;
      border: 2px solid #ddd;
      border-radius: 6px;
      outline: none;
      transition: border-color 0.3s ease-in-out;

      &:focus {
        border-color: #007bff;
      }
    }

    button {
      padding: 0.6rem 1rem;
      font-size: 1rem;
      font-weight: bold;
      border: none;
      cursor: pointer;
      border-radius: 6px;
      margin-left: 0.5rem;
      transition: background 0.3s ease-in-out;

      &:first-of-type {
        background: gray;
        color: white;

        &:hover {
          background: darkgray;
        }
      }

      &:last-of-type {
        background: #007bff;
        color: white;

        &:hover {
          background: #007bff;
        }
      }
    }
  }
}
/*daark theme*/
.darktheme-1 {
  background: #1e1e1e !important;
  color: #f0f0f0 !important;
}

/* Dark Theme 2 - Header */
.darktheme-2 {
  background: #2c2c2c !important;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
  color: #e7e7e7 !important;
}

/* Dark Theme 3 - Buttons */
.darktheme-3 {
  background: #3a3a3a !important;
  color: #ffffff !important;
  border: 1px solid #555 !important;
}

.darktheme-3:hover {
  background: #505050 !important;
}

/* Dark Theme 4 - Inputs */
.darktheme-4 {
  background: #2a2a2a !important;
  color: #e0e0e0 !important;
  border: 1px solid #444 !important;
}

/* Dark Theme 5 - Video Sections */
.darktheme-5 {
  background: #252525 !important;
  color: #d4d4d4 !important;
}
.darkthemec-a {
  background-color: #333 !important;
  border: 1px solid #333 !important;
  color: rgb(172, 168, 168) !important;
}
.darkthemec-a .video-info-holder {
  border-top: 1px solid #444 !important;
}
.darkthemec-a .video-duration {
  background: rgba(28, 27, 27, 0.8) !important;
  color: #868484 !important;
}
@media (max-width: 863px) {
  #homepage-header {
    padding: 3px;
    padding-top: 0;
    div > {
      margin-top: 0;
      padding: 0.5rem;
    }
  }
  .injustifyLogoR {
    font-size: 20px;
  }
  #streamsContainer {
    width: 95%;
  }
}
</style>
