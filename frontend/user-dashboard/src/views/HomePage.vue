<template>
  <div class="MainContainer" :class="{ collabsedBig: iscollapsedBig }">
    <div id="homepage-header" :class="{ 'darktheme-2': isDarkMode }">
      <div id="iconPlusQuery">
        <h1 @click="reloadPage" class="injustifyLogoR">Injustify</h1>

        <div id="queryShow">
          <div class="s_result" @click="setActiveTab('injustify', 100)">
            <img :src="injustifyIcon" alt="Justify Icon" />
            <span>{{ inj_videos.length }}</span>
          </div>
          <div class="s_result" @click="setActiveTab('YouTube', 100)">
            <img :src="youtubeIcon" alt="Justify Icon" />
            <span>{{ yt_videos.length }}</span>
          </div>
          <div class="s_result" @click="setActiveTab('Spotify', 100)">
            <img :src="spotifyIcon" alt="Justify Icon" />
            <span>{{ sp_videos.length }}</span>
          </div>
          <label for="filterSearch" id="queryHold" v-if="query" @click="toggleSearch">
            [ <span>{{ query }}</span> ]
          </label>
        </div>
      </div>
      <div
        v-if="loading.injustify || loading.youtube || loading.spotify"
        class="spinner-container"
      >
        <h5 class="loader"></h5>
        <p class="loadert">Loading...</p>
      </div>

      <div id="searchcontrols">
        <p id="voice_recording" v-if="isVoiceSearch">recording...</p>

        <ion-icon @click="searchByVoice" name="mic-outline"></ion-icon>

        <!-- <button><ion-icon name="clipboard"></ion-icon></button> -->
        <ion-icon
          @click="toggleSearch"
          :name="showSearch ? 'close-circle-outline' : 'search-circle-outline'"
        ></ion-icon>
        <ion-icon @click="toggleAdvancedFeatures" name="options-outline"></ion-icon>
      </div>

      <div id="searchBar" :class="{ 'darktheme-1': isDarkMode }" v-if="showSearch">
        <div class="input-container">
          <input
            id="filterSearch"
            type="text"
            placeholder="Filter Search"
            v-model="query"
            @input="fetch_suggestions"
            @keydown.enter="searchAll"
            :class="{ 'darktheme-4': isDarkMode }"
          />
          <button @click="resetSearch" :class="{ 'darktheme-3': isDarkMode }">
            <ion-icon name="reload-outline"></ion-icon>
          </button>
          <button @click="searchAll" :class="{ 'darktheme-3': isDarkMode }">
            <ion-icon name="search-outline"></ion-icon>
          </button>
          <ion-icon
            @click="toggleSearch"
            :name="showSearch ? 'close-circle-outline' : 'search-circle-outline'"
          ></ion-icon>
        </div>
        <div v-if="search_suggestions.length" id="suggestionContainer">
          <div
            v-for="suggestion in search_suggestions"
            :key="suggestion.name"
            id="suggestion"
            @click="FillSuggestion(`${suggestion.name} ${suggestion.artist}`)"
          >
            {{ suggestion.name }} - <span class="artist">{{ suggestion.artist }}</span>
          </div>
        </div>
        <p v-else>No suggestions</p>
      </div>

      <div
        id="AdvancedFeatures"
        :class="{ 'darktheme-1': isDarkMode }"
        v-if="showMoreAdvancedFeatures"
      >
        <div id="ft12">
          <div class="section">
            <h6>Search from:</h6>
            <div class="checkbox-group">
              <label>
                <input
                  type="checkbox"
                  :checked="searchFrom.injustify"
                  @change="toggleCheckbox('searchFrom', 'injustify')"
                />
                Injustify
              </label>

              <label>
                <input
                  type="checkbox"
                  :checked="searchFrom.youtube"
                  @change="toggleCheckbox('searchFrom', 'youtube')"
                />
                YouTube
              </label>

              <label>
                <input
                  type="checkbox"
                  :checked="searchFrom.spotify"
                  @change="toggleCheckbox('searchFrom', 'spotify')"
                />
                Spotify
              </label>
            </div>
          </div>

          <div class="section">
            <h6>Filter by:</h6>
            <div class="checkbox-group">
              <label>
                <input
                  type="checkbox"
                  :checked="filterBy.artist"
                  @change="toggleCheckbox('filterBy', 'artist')"
                />
                Artist
              </label>

              <label>
                <input
                  type="checkbox"
                  :checked="filterBy.title"
                  @change="toggleCheckbox('filterBy', 'title')"
                />
                Title
              </label>

              <label>
                <input
                  type="checkbox"
                  :checked="filterBy.date"
                  @change="toggleCheckbox('filterBy', 'date')"
                />
                Date
              </label>
            </div>
          </div>
        </div>
        <div v-if="filterBy.date">
          <label for="monthYear">Select Month and Year:</label>
          <input type="month" id="monthYear" name="monthYear" />
        </div>
        <div class="section" :class="{ 'darktheme-4': isDarkMode }">
          <h6>
            Advanced
            <button @click="toggleDwnPlaylists">
              <ion-icon name="layers"></ion-icon>
            </button>
          </h6>
          <div class="advanced-features">
            <div class="input-container" :class="{ 'darktheme-2': isDarkMode }">
              <label for="searchUrl">Paste YouTube videoURL to download</label>
              <input
                v-model="dwn_url"
                type="text"
                id="searchUrl"
                placeholder="Enter URL here..."
              />
              <button @click="handleDownload(normalizeYouTubeUrl(dwn_url)), null">
                Download
              </button>
            </div>
            <div class="input-container" :class="{ 'darktheme-2': isDarkMode }">
              <label for="searchUrl">Paste YouTube Playlist URL to download</label>
              <input
                v-model="yt_PLAYLIST_url"
                type="text"
                id="searchUrl"
                placeholder="Enter URL here..."
              />
              <button
                @click="getPlaylistSongs(normalizeYouTubePlaylistUrl(yt_PLAYLIST_url))"
              >
                Load
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        :class="{ 'darktheme-4': isDarkMode }"
        class="playlist-popup common-scroolbar"
        ref="popup"
        v-if="playlist_loading || showdwnPlaylists"
      >
        <p @mousedown="startDrag" v-if="playlist_loading" id="playlist_loader">
          Loading playlist...
        </p>

        <div v-if="showdwnPlaylists" id="playlistSongsContainer" class="common-scroolbar">
          <h3 @mousedown="startDrag">
            <span> Playlist Songs {{ yt_playlistSongs.length + 1 }}</span>
            <button @click="toggleDwnPlaylists" class="close-playlist">
              <ion-icon name="close-outline"></ion-icon>
            </button>
          </h3>
          <div class="playlist-songs common-scroolbar">
            <label
              v-for="(song, index) in yt_playlistSongs"
              :key="index || song.url"
              class="playlist-song"
              :class="{ 'darktheme-3': isDarkMode }"
            >
              <input
                type="checkbox"
                name="playlistSongs"
                :value="song"
                :disabled="isDisabled(song)"
                v-model="selectedPlaylistSongs"
                @change="handleSelection"
                :checked="index < 15"
              />

              <img :src="getThumbnail(song, 'YouTube')" alt="Thumbnail" />
              <div class="song-info">
                <h4>{{ getTitle(song, "YouTube") }}</h4>
                <p>{{ getArtist(song, "YouTube") }}</p>
              </div>
            </label>
          </div>
          <div id="playlistDownloadFooter">
            <button @click="handlePlalistDownloadSelect">
              Download {{ selectedPlaylistSongs.length }}/{{ yt_playlistSongs.length }}
            </button>
          </div>
        </div>
        <p v-if="!yt_playlistSongs.length && !playlist_loading">No playlist songs</p>
      </div>
    </div>

    <!-- Video Sections -->

    <div
      v-if="videoSources[activeTab]"
      :key="activeTab"
      :ref="activeTab"
      id="holder"
      :class="{ 'darktheme-5': isDarkMode }"
    >
      <div class="service" :class="{ 'darktheme-1': isDarkMode }">
        {{ activeTab }} Videos
        <p v-if="loading[service]" class="loadert" :class="{ 'darktheme-2': isDarkMode }">
          Loading...
        </p>
        <img v-if="getLogo(activeTab)" :src="getLogo(activeTab)" alt="Service Logo" />
      </div>

      <div v-if="videoSources[activeTab].length" id="videosContainer">
        <div
          v-for="(video, index) in videoSources[activeTab]"
          :key="video.song_id"
          class="video-card"
          :class="{ 'darkthemec-a': isDarkMode }"
        >
          <div @click="playVideo(video)">
            <router-link
              :to="{
                path: '/p',
                query: { url: video.song_id ? video.song_id : video.url },
              }"
            >
              <img :src="getThumbnail(video, activeTab)" alt="Video Thumbnail" />
            </router-link>
            <div>
              <h4>{{ getTitle(video, activeTab) }}</h4>
              <p>{{ getArtist(video, activeTab) }}</p>
            </div>
          </div>
          <div class="video-info-holder">
            <div class="video-Meta-info-holder">
              <span
                ><ion-icon name="cloud-download-outline"></ion-icon
                >{{ video.views }}</span
              >
              <span class="timeAgo">{{ getDate(video, activeTab) }}</span>
              <span class="video-duration">{{ getDuration(video, activeTab) }}</span>
            </div>
            <div @click="likeUnlikeSong(video)">
              <ion-icon :name="video.liked ? 'heart' : 'heart-outline'"></ion-icon>
            </div>
            <div class="dropdown-container">
              <!-- MORE OPTIONS Icon (Toggle Button) -->
              <div @click="toggleDropdown(index)" class="skull-icon">
                <ion-icon name="swap-vertical-outline"></ion-icon>
              </div>

              <!-- Dropdown Menu -->
              <div v-if="openIndex === index" class="skull-more-options">
                <button @click="handle_dwn_Download(video)">
                  <ion-icon name="download"></ion-icon> Injust
                </button>

                <button
                  @click="
                    handleDownload(
                      video.url,
                      `${getTitle(video, activeTab)} ${getArtist(video, activeTab)}`
                    )
                  "
                >
                  <ion-icon name="receipt-outline"></ion-icon> Load Streams
                </button>

                <!-- Playlist Selector -->
                <div class="playlist-dropdown" v-show="userId">
                  <button class="playlist-toggle">
                    <div
                      class="asdaca"
                      @click="add_to_playlist(selectedPlaylist.id, video.song_id)"
                    >
                      <ion-icon name="bag-add-outline"></ion-icon> Add to Playlist
                      <span
                        :title="selectedPlaylist?.name || 'No Playlist Selected'"
                        class="activeplaylist_name"
                        >({{ selectedPlaylist.name || "None" }})</span
                      >
                    </div>
                    <ion-icon
                      @click="togglePlaylists"
                      :name="showPlaylists ? 'caret-up-outline' : 'caret-down-outline'"
                      class="caret-icon"
                    ></ion-icon>
                  </button>

                  <!-- Playlists List -->
                  <div v-show="showPlaylists" class="playlist-list">
                    <div
                      v-for="playlist in playlists"
                      :key="playlist.id"
                      class="playlist-item"
                      :class="{ 'darktheme-2': isDarkMode }"
                      @click="setAsActivePlaylist(playlist)"
                    >
                      <span class="playlist-name">{{ playlist.name }}</span>
                    </div>
                  </div>
                </div>
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
    <router-view id="previewContainer"></router-view>

    <DownlodSelectorHold
      id="streamsContainer"
      :songId="streamSongID"
      :stmName="stmName"
      :streamloading="streamloading"
      @selected="handleDownloadSelect"
      v-if="streamloading && streamSongID"
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
import { adv_UserStore } from "@/store/tasks.js";
import { BASE_URL, formatDate, extractYouTubeID } from "@/utils/index.js";
import injustifyIcon from "../assets/injustify.png";
import youtubeIcon from "../assets/youtube-icon2.jpg";
import spotifyIcon from "../assets/spotify-logo.png";

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
    const advUserStore = adv_UserStore();
    return {
      injustifyIcon,
      youtubeIcon,
      spotifyIcon,
      message: "",
      query: "",
      offset: 0,
      limit: 24,
      playlists: [],
      inj_videos: [],
      yt_videos: [],
      sp_videos: [],
      search_suggestions: [],
      loading: { injustify: false, youtube: false, spotify: false },
      spotifyThumbnails: {},
      openIndex: null,
      streamSongID: null,
      stmName: null,
      dwn_url: null,
      userStore,
      showSearch: false,
      showMoreAdvancedFeatures: false,
      selectedPlatforms: [],
      selectedFilters: [],
      youtubeUrl: "",
      yt_PLAYLIST_url: "",
      searchFrom: { injustify: true, youtube: true, spotify: true },
      filterBy: { artist: true, title: true, date: false },
      advUserStore,
      activeTab: "injustify",
      showPlaylists: false,
      isVoiceSearch: false,
      formatDate,
      extractYouTubeID,
      selectedPlaylist: [],
      yt_playlistSongs: [],
      playlist_loading: false,
      maxSelection: 25,
      selectedPlaylistSongs: [],
      showdwnPlaylists: false,
      isDragging: false,
      dragOffset: { x: 0, y: 0 },
      yt_videos_details: {},
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
    window.addEventListener("scroll", await this.handleScroll);

    socket.on("respoce_search_suggestions", (data) => {
      this.search_suggestions = data.search_suggestions;
    });

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

    await this.fetchVideos(true);
    await this.fetchSpotifyThumbnails(); // Preload Spotify thumbnails
  },
  // watch: {
  //   yt_playlistSongs(newSongs) {
  //     if (newSongs.length) {
  //       this.selectedPlaylistSongs = newSongs.slice(0, 15);
  //     }
  //   },
  // },

  methods: {
    startDrag(e) {
      // Optional: Only drag if clicking near the top or add specific drag handle
      if (e.target.closest(".playlist-popup")) {
        this.isDragging = true;
        this.dragOffset.x = e.clientX - this.$refs.popup.offsetLeft;
        this.dragOffset.y = e.clientY - this.$refs.popup.offsetTop;

        document.addEventListener("mousemove", this.onDrag);
        document.addEventListener("mouseup", this.stopDrag);
      }
    },
    onDrag(e) {
      if (this.isDragging) {
        this.$refs.popup.style.left = `${e.clientX - this.dragOffset.x}px`;
        this.$refs.popup.style.top = `${e.clientY - this.dragOffset.y}px`;
        this.$refs.popup.style.position = "absolute"; // Ensure it's draggable
        this.$refs.popup.style.margin = "0"; // Avoid offset issues
      }
    },
    stopDrag() {
      this.isDragging = false;
      document.removeEventListener("mousemove", this.onDrag);
      document.removeEventListener("mouseup", this.stopDrag);
    },
    handleSelection(e) {
      if (this.selectedPlaylistSongs.length > this.maxSelection) {
        e.target.checked = false;
        this.selectedSongs.pop(); // remove last
        this.userStore.set_snackbarMessage(
          `You can only select up to ${this.maxSelection} songs.`,
          "warn",
          10000
        );
      }
    },
    isDisabled(song) {
      return (
        this.selectedPlaylistSongs.length >= this.maxSelection &&
        !this.selectedPlaylistSongs.includes(song)
      );
    },
    searchByVoice() {
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

      if (!SpeechRecognition) {
        console.error("Speech Recognition API is not supported in this browser.");
        return false;
      }

      if (this.isVoiceSearch) {
        console.log("Voice search is already active.");
        return false;
      }

      const recognition = new SpeechRecognition();
      recognition.lang = "en-US";
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        // console.log("🎤 Voice recognition started");
        this.isVoiceSearch = true;
      };

      recognition.onend = () => {
        // console.log("🛑 Voice recognition ended");
        this.isVoiceSearch = false;
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        // console.log("🗣️ Recognized:", transcript);
        this.query = transcript;
        this.searchAll();
      };

      recognition.onerror = (event) => {
        console.error("❌ Voice recognition error:", event.error);
        this.isVoiceSearch = false;
      };

      recognition.start();
      return true;
    },
    async add_to_playlist(playlistId, songId) {
      this.loading = true;

      if (!playlistId || !songId) {
        this.userStore.set_snackbarMessage(
          "Playlist or Song ID is missing!",
          "error",
          10000
        );
        return;
      }

      axios
        .post(
          `${BASE_URL}/api/songs/pls_update`,
          { playlistId, songId, action: "add" },
          { headers: { "Content-Type": "application/json" } }
        )
        .then((response) => {
          if (response.data) {
            this.userStore.set_snackbarMessage(response.data.message, "success", 10000);
          }
        })
        .catch((error) => {
          console.error("API Error:", error);
          this.userStore.set_snackbarMessage(
            "Failed to add song to playlist.",
            "error",
            10000
          );
        })
        .finally(() => {
          this.loading = false;
        });
    },

    togglePlaylists() {
      this.fetchPlaylists();
      this.showPlaylists = !this.showPlaylists;
    },
    setAsActivePlaylist(playlist) {
      this.selectedPlaylist = playlist;
      this.showPlaylists = false;
    },

    async handleScroll() {
      const scrollTop = window.scrollY;
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;

      if (scrollTop + windowHeight >= documentHeight - 20) {
        this.offset += this.limit;
        await this.fetchVideos(false);
      }
    },
    async likeUnlikeSong(video) {
      if (!this.userId && video.song_id) {
        this.userStore.set_snackbarMessage("You need to login!!, ", "error", 10000);
        return;
      }
      video.liked = !video.liked;
      socket.emit("likeUnlikeSong", { songId: video.song_id, userId: this.userId });
    },
    toggleCheckbox(group, key) {
      this[group][key] = !this[group][key];
    },
    toggleSearch() {
      this.showSearch = !this.showSearch;
      this.showMoreAdvancedFeatures = false;
    },
    toggleAdvancedFeatures() {
      this.showMoreAdvancedFeatures = !this.showMoreAdvancedFeatures;
      this.showSearch = false;
    },
    getLogo(service) {
      if (service === "injustify") {
        return injustifyIcon;
      } else if (service === "YouTube") {
        return youtubeIcon;
      } else if (service === "Spotify") {
        return spotifyIcon;
      } else {
        return injustifyIcon;
      }
    },
    toggleDropdown(index) {
      this.openIndex = this.openIndex === index ? null : index;
    },

    handleDownload(video, stmName) {
      console.log("Downloading:", video);
      this.streamSongID = video;
      this.stmName = stmName;
      this.userStore.set_streamloading(true);
      this.toggleDropdown();
      this.dwn_url = null;
      this.showMoreAdvancedFeatures = false;
    },
    handle_dwn_Download(video) {
      console.log("Downloading:", video, "from", video.Stype);
      if (video.Stype == null) {
        this.userStore.set_snackbarMessage(
          `Error downloading from  ${video.stype},try downloading from a different source!`,
          "error",
          10000
        );
        console.log("Service not selected.");
        return;
      }
      const sname = video.artist ? `${video.artist}-${video.title}` : `${video.title}`;
      if (video.Stype === "injustify") {
        this.advUserStore.download_injustify_stream(
          video.url,
          video.itag,
          sname,
          video.ext,
          0,
          null,
          video.url.split(".").pop(),
          video.thumbnail
        );
      } else if (video.Stype === "youtube") {
        this.advUserStore.download_yt_stream(
          video.url,
          "140",
          sname,
          "m4a",
          0,
          0,
          null,
          getYouTubeThumbnails(video.url),
          "audio only"
        );
      }
      this.streamSongID = video;
      this.stmName = sname;
      this.toggleDropdown();
      this.dwn_url = null;
    },

    resetSearch() {
      this.query = "";
      //this.inj_videos = [];
      this.yt_videos = [];
      this.sp_videos = [];
      this.search_suggestions = [];
      this.spotifyThumbnails = {};
    },

    async fetch_suggestions() {
      if (this.query.trim() !== "") {
        console.log("Getting suggestions for query:", this.query);
        socket.emit("get_search_suggestions", {
          userId: this.userId,
          query: this.query,
        });
      }
    },

    async fetchVideos(clr = false) {
      if (this.loading.injustify && this.activeTab === "injustify") return;
      this.loading = { ...this.loading, injustify: true };

      try {
        const searchQuery =
          this.query && this.query.toLowerCase() !== "null" ? this.query : null;
        const response = await axios.get(`${BASE_URL}/api/songs/${this.userId}`, {
          params: {
            search: searchQuery,
            offset: this.offset,
            order_by: this.order_by,
            limit: this.limit,
          },
        });

        console.log(response.data);
        if (clr) {
          this.inj_videos = [];
          this.offset = 0;
        }
        const newsongs = response.data.songs || [];
        if (newsongs.length > 0) {
          this.inj_videos.push(...newsongs);
        } else {
          this.setActiveTab("YouTube", 100);
        }
      } catch (error) {
        console.error("API Error:", error);
        this.userStore.set_snackbarMessage("API Error!!, ", error, "error", 10000);
      } finally {
        this.loading = { ...this.loading, injustify: false };
        this.offset = this.inj_videos.length;
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
      this.showSearch = false;
      this.offset = 0;
      await this.fetchVideos(true); // Search injustify database
      await this.searchYouTube(); // Search YouTube
      await this.searchSpotify(); // Search Spotify
    },
    // formatYtDate(uploadDate) {
    //   try {
    //     if (!uploadDate || uploadDate.length !== 8) return "Unknown";

    //     const year = parseInt(uploadDate.substring(0, 4), 10);
    //     const month = parseInt(uploadDate.substring(4, 6), 10) - 1; // 0-indexed
    //     const day = parseInt(uploadDate.substring(6, 8), 10);

    //     const date = new Date(year, month, day);
    //     if (isNaN(date.getTime())) return "Unknown";
    //     console.log(
    //       "Formatted date:",
    //       date.toISOString().replace("T", " ").substring(0, 19)
    //     );

    //     return date.toISOString().replace("T", " ").substring(0, 19);
    //   } catch (error) {
    //     return "Unknown";
    //   }
    // },
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
            //this.userStore.set_snackbarMessage(`${service} Polling error, refresh page and retry!`,'error',10000);
            throw new Error(`${service} Error: ${response.statusText}`);
          }

          const data = response.data;

          if (data.success) {
            console.log(`${service} Results:`, data.songs);
            if (service === "youtube") {
              this.yt_videos = data.songs;
              this.getYoutubeSongsDetails(); // Fetch YouTube song details
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
          //this.userStore.set_snackbarMessage(`${service} Polling error, refresh page and retry!`,'error',10000);
        }

        retries--;
        if (retries > 0) {
          setTimeout(poll, interval);
        } else {
          console.error(`${service} Polling failed after maximum retries.`);
          this.userStore.set_snackbarMessage(
            `${service} search failed after maximum retries, refresh page and retry!`,
            "error",
            10000
          );
          this.loading[service] = false;
        }
      };

      poll();
    },

    async getYoutubeSongsDetails() {
      this.loading.youtube = true;
      this.yt_videos_details = {};

      try {
        const response = await axios.post(`${BASE_URL}/api/yt/details`, {
          userId: this.userId,
          video_urls: this.yt_videos.map((video) => video.url),
        });

        this.yt_videos_details = response.data.song_details || {};
        console.log("YouTube Songs Details:", this.yt_videos_details);
      } catch (error) {
        console.error("API Error:", error);
        this.userStore.set_snackbarMessage(
          "API Error!!",
          error.message || "Unknown error",
          "error",
          10000
        );
      } finally {
        this.loading.youtube = false;
      }
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
    getDate(video, service) {
      if (service === "YouTube") {
        return (
          this.timeAgo(
            this.yt_videos_details[this.extractYouTubeID(video.url)]?.publishedAt
          ) || "Unknown"
        );
      } else if (service === "Spotify") {
        return video.date ? this.formatDate(video.date) : "?";
      }
      return timeAgo(video.date);
    },
    FillSuggestion(query_suggest) {
      this.query = query_suggest;
      this.searchAll();
      this.showSearch = false;
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
    getDuration(video, service) {
      if (service === "YouTube") {
        return (
          this.convertSeconds(
            this.yt_videos_details[this.extractYouTubeID(video.url)]?.duration
          ) || "Unknown"
        );
      } else if (service === "Spotify") {
        return video.duration ? this.formatDate(video.duration) : "?";
      }
      return this.convertSeconds(video.duration);
    },
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
          this.playlists = [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    setActiveTab(tg, offset = 100) {
      this.activeTab = tg;

      const target = this.$refs[tg]?.[0]; // Access the first element if in v-f

      if (target) {
        // Get the element's position relative to the viewport
        const rect = target.getBoundingClientRect();

        // Calculate the absolute position and add the offset
        const scrollTop = window.pageYOffset + rect.top - offset;

        window.scrollTo({
          top: scrollTop,
          behavior: "smooth",
        });
      } else {
        console.warn(`No element found for: ${tg}`);
      }
    },
    normalizeYouTubePlaylistUrl(input) {
      return input;
    },
    getPlaylistSongs(playlistUrl) {
      this.showMoreAdvancedFeatures = false;
      this.playlist_loading = true;

      axios
        .post(`${BASE_URL}/api/playlist/youtube`, {
          playlistUrl: playlistUrl,
          userId: this.userId,
        })
        .then((response) => {
          console.log("Playlist Songs:", response.data.songs);
          this.yt_playlistSongs = response.data.songs || [];
          this.showdwnPlaylists = true;
          this.selectedPlaylistSongs = this.yt_playlistSongs.slice(0, 15);
        })
        .catch((error) => {
          console.error("API Error:", error);
          this.yt_playlistSongs = [];
        })
        .finally(() => {
          this.playlist_loading = false;
        });
    },

    normalizeYouTubeUrl(input) {
      if (!input) return;
      const regex = /(?:youtu\.be\/|youtube\.com\/(?:embed\/|watch\?v=|v\/|shorts\/)?|src="(?:https:\/\/www\.youtube\.com\/embed\/))([\w-]{11})/;

      const match = input.match(regex);

      if (match && match[1]) {
        return `https://www.youtube.com/watch?v=${match[1]}`;
      }

      return null;
    },
    async handlePlalistDownloadSelect() {
      const batchSize = 4; // Max concurrent downloads
      const selected = [...this.selectedPlaylistSongs]; // make a local copy

      if (selected.length === 0) {
        this.userStore.set_snackbarMessage(
          "No songs selected for download",
          "error",
          10000
        );
        return;
      }

      this.userStore.set_snackbarMessage(
        `Downloading ${selected.length} songs...`,
        "success",
        10000
      );
      this.showdwnPlaylists = false;

      for (let i = 0; i < selected.length; i += batchSize) {
        const batch = selected.slice(i, i + batchSize);

        // Start up to 4 parallel downloads
        await Promise.all(
          batch.map((song) =>
            this.advUserStore.download_yt_stream(
              song.url,
              "140",
              `${this.getTitle(song, "YouTube")} ${this.getArtist(song, "YouTube")}`,
              "m4a",
              0,
              0,
              null,
              getYouTubeThumbnails(song.url),
              "audio only"
            )
          )
        );

        // Optional delay between batches
        await new Promise((res) => setTimeout(res, 300));
      }

      // ✅ Only clear after all batches
      this.selectedPlaylistSongs = [];

      this.userStore.set_snackbarMessage(
        `Downloaded ${selected.length} songs successfully`,
        "success",
        10000
      );
    },

    toggleDwnPlaylists() {
      this.showdwnPlaylists = !this.showdwnPlaylists;

      // If opening the playlist again, cancel any pending clear
      if (this.showdwnPlaylists && this.playlistClearTimeout) {
        clearTimeout(this.playlistClearTimeout);
        this.playlistClearTimeout = null;
      }

      // If closing, start timeout to clear songs
      if (!this.showdwnPlaylists) {
        this.playlistClearTimeout = setTimeout(() => {
          this.selectedPlaylistSongs = [];
          this.yt_playlistSongs = [];
          this.playlistClearTimeout = null;
        }, 10000);
      }
    },
    reloadPage() {
      window.location.reload();
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
#voice_recording {
  color: #9333ea !important; /* purple-600 */
  font-size: 10px !important;
  position: absolute;
  bottom: 0;
}
.activevoicesearch {
  background-color: #9333ea; /* purple-600 */
  color: white;
  border-radius: 0.5rem;
}
#previewContainer {
  position: fixed;
  bottom: 0;
  left: 50%;
  width: 60%;
  height: fit-content;
  transform: translateX(-50%);
  z-index: 100;
}
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
  columns: 5 230px;
  padding: 5px 0;
  box-sizing: border-box;
  overflow-x: hidden;
  scroll-behavior: smooth;

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
      .timeAgo {
        font-size: 11px;
        color: #666;
      }
    }
  }
}
#holder {
  width: 100%;
  min-height: 100vh;
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
  padding: 0.5rem;
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
    margin: 0 !important;
    margin-right: auto !important;
    margin-bottom: 5px !important;
    padding-top: 2px !important;
    text-shadow: 0px 2px 5px black;
    position: relative;
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
    top: 80px;
    padding: 10px 5px !important;
    background-color: #fff;
    border-radius: 0px 0px 12px 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    width: 360px;
    margin: auto;
    overflow-wrap: break-word;
    transition: background-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
    z-index: 102 !important;
    box-sizing: border-box;

    &.darktheme-1 {
      background-color: #1e1e1e;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
      border: 1px solid #333;
    }

    input {
      width: 75%;
      padding: 10px 15px;
      border: 1px solid #ccc;
      border-radius: 8px;
      margin-bottom: 12px;
      font-size: 14px;
      transition: border-color 0.3s ease, box-shadow 0.3s ease;
      box-sizing: border-box;

      &:focus {
        border-color: #5a9;
        box-shadow: 0 0 8px rgba(90, 170, 100, 0.5);
        outline: none;
      }

      &.darktheme-4 {
        background-color: #2b2b2b;
        border-color: #555;
        color: #e0e0e0;
      }
    }

    button {
      border: 1px solid transparent;
      border-radius: 8px;
      background-color: #5a9;
      color: #fff;
      height: 100% !important;
      cursor: pointer;
      margin-left: 0.2rem !important;
      padding: 2px 5px !important;
      font-weight: 500;
      transition: background-color 0.3s ease, transform 0.2s;

      &:hover {
        background-color: #48976b;
        transform: translateY(-2px);
      }

      &:active {
        transform: scale(0.98);
      }

      &.darktheme-3 {
        background-color: #444;
        border-color: #555;
        color: #fff;
      }

      &.darktheme-3:hover {
        background-color: #555;
      }
    }
    .input-container {
      flex-direction: row !important;
      padding: 3px !important;

      button {
        font-weight: normal;
      }
    }
    #suggestionContainer {
      margin-top: 2px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      max-height: 200px;
      overflow-y: auto;
      padding-right: 4px;
      border-radius: 8px;
      box-sizing: border-box;
      overflow-x: hidden;

      &.darktheme-1 {
        border-color: #444;
      }
    }

    #suggestion {
      padding: 8px 12px;
      background-color: #81818171;
      border-radius: 3px;
      cursor: pointer;
      transition: background-color 0.3s ease, transform 0.2s;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
      box-sizing: border-box;

      &:hover {
        background-color: #7f7f7f;
        transform: translateX(5px);
      }

      .artist {
        font-size: 12px;
        color: #918d8d;
        font-style: italic;
      }
    }

    .darktheme-1 #suggestion {
      background-color: #2b2b2b;
      color: #ccc;
      border: 1px solid #444;
    }

    .darktheme-1 #suggestion:hover {
      background-color: #444;
    }

    #suggestionContainer::-webkit-scrollbar {
      width: 6px;
    }

    #suggestionContainer::-webkit-scrollbar-thumb {
      background-color: #ccc;
      border-radius: 8px;
    }

    .darktheme-1 #suggestionContainer::-webkit-scrollbar-thumb {
      background-color: #555;
    }
  }

  #iconPlusQuery {
    display: flex;
    flex-direction: column;
    padding: 5px !important;
    box-shadow: none !important;
    height: 100%;
    justify-content: space-between;
    div {
      padding: 0 !important;
    }
  }

  #queryShow {
    display: flex;
    flex-direction: row;
    gap: 10px;
    align-items: center;
    padding: 3px 10px;
    border-radius: 8px;
    color: #f1f5f9;
    font-family: "Arial", sans-serif;
    box-sizing: border-box;
    margin-top: 8px;

    #queryHold {
      width: 120px;
      height: fit-content;
      overflow: hidden;
      position: relative;
      border: 1px solid #475569;
      border-radius: 6px;
      padding: 0;
      box-shadow: inset 0 0px 4px rgba(0, 0, 0, 0.3);

      span {
        width: 100px;
        display: inline-block;
        white-space: nowrap;
        animation: scrollText 6s linear infinite;
        color: #535354;
        font-size: 12px;
      }

      div > img {
        width: 18px !important; /* Adjusted size */
        height: 18px !important; /* Adjusted size */
        object-fit: contain;
        border-radius: 4px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease;
      }
    }

    p {
      margin: 0;
    }

    div {
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
      cursor: pointer;
      transition: background-color 0.3s ease, transform 0.3s ease;
      box-sizing: border-box;
    }

    div:hover {
      background-color: #334155;
      transform: translateY(-2px);
    }

    .s_result {
      color: gray;
      font-style: italic;
      font-size: 13px;
      display: flex;
      align-items: center;
      flex-direction: row;
      gap: 2px;
    }

    /* Animation for scrolling text */
    @keyframes scrollText {
      0% {
        transform: translateX(100%);
      }
      100% {
        transform: translateX(-100%);
      }
    }
  }

  /* Styling for images */
  #queryShow > div img {
    width: 24px;
    height: 24px;
    object-fit: contain;
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
    transition: transform 0.3s ease;
  }

  #searchcontrols {
    position: relative;
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 10px;

    button {
      background: #007bff;
      color: rgb(226, 221, 221);
      padding: 3px 10px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background 0.3s ease-in-out;
      box-sizing: border-box;
      &:hover {
        background: #0069d9;
      }
    }
    ion-icon {
      padding: 3px 5px;
      min-width: 15px;
      min-height: 10px;
      cursor: pointer;
      font-weight: bolder;
      font-size: 20px !important;
      box-sizing: border-box;

      &:hover {
        color: #0069d9;
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
    top: 100px;
    right: 1%;
    display: flex;
    justify-content: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    background-color: rgba(255, 255, 255, 0.169) !important;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.815);
    height: fit-content !important;
    padding: 4px !important;
    z-index: 100;
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
          background: rgb(0, 204, 222) !important;
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
@media (max-width: 568px) {
  #searchBar {
    width: 100% !important;
  }
}
</style>
<style scoped>
#AdvancedFeatures {
  position: absolute;
  right: 0;
  top: 80px;
  padding: 10px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 3px 14px rgba(0, 0, 0, 0.1) !important;
  max-width: 250px;
  width: fit-content;
  max-height: 400px;
  overflow-y: auto;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  z-index: 100;
  box-sizing: border-box;

  div {
    margin: 0;
    padding: 0;
  }
  h6 {
    margin: 3px;
    color: gray;
    text-shadow: 0px 2px 4px black;
  }
}

#ft12 {
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: space-between;
}

.darktheme-1 {
  background-color: #1e1e1e;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  border: 1px solid #333;
}

.section {
  margin-bottom: 16px;
  border-radius: 0px !important;
  padding: 5px 15px !important;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
  padding: 3px !important;
  border-radius: 0px !important;
}

.asdaca {
  cursor: pointer;
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-right: auto;
  gap: 5px;
}

.checkbox-group label {
  font-size: 14px;
  cursor: pointer;
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-right: auto;
}

.input-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 5px !important;
  width: 100%;
  min-width: 200px;
  max-width: 300px;
}

.advanced-features {
  display: flex;
  flex-direction: row;
  gap: 8px;
  width: 100%;
  overflow: auto;
}

#AdvancedFeatures input[type="text"] {
  width: 100% !important;
  padding: 2px 8px !important;
  border: 1px solid #ccc;
  border-radius: 8px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  box-sizing: border-box;
}

input:focus {
  border-color: #5a9;
  box-shadow: 0 0 8px rgba(90, 170, 100, 0.5);
  outline: none;
}

button {
  padding: 8px !important;
  border: none;
  border-radius: 8px;
  background-color: #5a9;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s;
  box-sizing: border-box;
}
button:hover {
  background-color: #48976b;
  transform: translateY(-2px);
}

button:active {
  transform: scale(0.98);
}
</style>
<style scoped>
.skull-more-options {
  position: absolute;
  background: var(--menu-bg, #222);
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  padding: 10px;
  min-width: 200px;
  z-index: 10;
}
/* Dropdown Buttons */
.skull-more-options button {
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  color: #faf7f7;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  font-size: 12px; /* Small font */
  padding: 6px;
  cursor: pointer;
  width: 100%;
  transition: background 0.2s ease-in-out;
}

.skull-more-options button:hover {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
}

/* Playlist Dropdown */
.playlist-dropdown {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
}

.playlist-toggle {
  display: flex;
  justify-content: space-between;
  width: 100%;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 6px;
  border-radius: 5px;
}

.caret-icon {
  color: var(--accent-color, #f39c12);
  transition: transform 0.2s ease-in-out;
}

/* Playlist List */
.playlist-list {
  display: flex;
  flex-wrap: nowrap; /* Inline display */
  overflow-x: auto;
  max-height: 100px; /* Limit height */
  background: var(--dark-bg, #333);
  border-radius: 5px;
  padding: 5px;
  margin-top: 5px;
}

.playlist-item {
  font-size: 10px; /* Small text */
  white-space: nowrap;
  padding: 5px 10px;
  margin: 2px;
  border-radius: 5px;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.2);
  transition: background 0.2s;
}

.playlist-item:hover {
  background: var(--hover-bg, rgba(255, 255, 255, 0.3));
}

.darktheme-2 {
  background: #444;
}
.activeplaylist_name {
  font-size: 12x;
  color: #595555;
  display: -webkit-box; /* Use a flex-like box for line clamping */
  -webkit-box-orient: vertical; /* Specify vertical stacking of lines */
  -webkit-line-clamp: 1; /* Allow only two lines */
  overflow: hidden; /* Hide overflowed text */
  text-overflow: ellipsis; /* Add ellipsis (...) for overflowing text */
  word-wrap: normal; /* Prevent forced breaks */
  width: 50px;
}
</style>
<style scoped>
.playlist-popup {
  position: absolute !important;
  right: 0 !important;
  top: 20px;
  max-width: 400px;
  width: 99%;
  height: fit-content;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  padding: 5px;
  font-size: 0.85rem;
  z-index: 102;
}
#playlistSongsContainer {
  width: 100%;
  position: relative;
}
.playlist-popup input {
  width: 20px !important;
}
.darktheme-4 {
  background-color: #1e1e2f;
  color: #eee;
}

h3 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  position: sticky;
  top: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: row;
  user-select: none;
  cursor: move;
}
h3 button {
  background: none !important;
  border: none !important;
  color: #f00 !important;
  cursor: pointer !important;
  font-size: 1.2rem !important;
  transition: color 0.3s ease-in-out;
}

.playlist-songs {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 70vh;
  overflow-y: auto;
}

.playlist-song {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem;
  border-bottom: 1px solid #ccc;
}

.darktheme-3 {
  background-color: #2c2c3e;
}

.song-info h4,
.song-info p {
  margin: 0;
  line-height: 1.2;
  padding: 0;
}

img {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 5px;
}
#playlistDownloadFooter {
  position: sticky;
  bottom: 0;
}
#playlist_loader {
  font-size: 13px;
  margin: 0;
  padding: 5px !important;
  color: #aba1a1 !important;
  user-select: none;
  cursor: move;
}
@media (max-width: 863px) {
  .playlist-popup {
    position: fixed;
    top: 100% !important;
    width: 100% !important;
  }
}
</style>
