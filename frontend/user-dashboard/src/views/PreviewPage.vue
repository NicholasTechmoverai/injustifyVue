<script>
import { useUserStore } from "@/store/index.js";
import { computed } from "vue";
import { nextTick } from "vue";
import { BASE_URL } from "@/utils/index.js";
import axios from "axios";

export default {
  name: "UniversalMusicPlayer",
  data() {
    const userStore = useUserStore();

    return {
      iscollapsedBig: computed(() => userStore.iscollapsedBig),
      isDarkMode: computed(() => userStore.isdarkmode),
      isPlaying: false,
      currentTime: 0,
      duration: 0,
      volume: 0.7,
      audioUrl: "",
      youtubeUrl: "",
      spotifyUrl: "",
      activeSource: "file",
      availableSources: [
        { id: "file", label: "File" },
        { id: "url", label: "URL" },
        { id: "youtube", label: "YouTube" },
        { id: "spotify", label: "Spotify" },
      ],
      currentTrack: {
        title: "",
        artist: "",
        source: "",
        src: "",
      },
      embeddedContent: "",
      showEmbed: false,
      isMobile: false,
      visualizerEnabled: true,
      audioContext: null,
      analyser: null,
      dataArray: null,
      animationId: null,
      seekable: true,
    };
  },
  computed: {
    url() {
      return this.$route.query.url || "";
    },

    isYouTube() {
      return this.currentTrack.source === "YouTube";
    },

    isSpotify() {
      return this.currentTrack.source === "Spotify";
    },

    youtubeEmbedUrl() {
      if (!this.youtubeUrl) return "";
      let videoId = this.extractYouTubeId(this.youtubeUrl);
      return `https://www.youtube.com/embed/${videoId}?enablejsapi=1&autoplay=${
        this.isPlaying ? 1 : 0
      }`;
    },
    spotifyEmbedUrl() {
      if (!this.spotifyUrl) return "";
      let spotifyId = this.extractSpotifyId(this.spotifyUrl);
      if (spotifyId.type === "track") {
        return `https://open.spotify.com/embed/track/${spotifyId.id}`;
      } else if (spotifyId.type === "playlist") {
        return `https://open.spotify.com/embed/playlist/${spotifyId.id}`;
      }
      return "";
    },
  },
  methods: {
    categoriseURL(newUrl) {
      const url = newUrl.toLowerCase();
      const audio = this.$refs.audioPlayer;

      if (url.includes("youtube") || url.includes("yutube")) {
        this.youtubeUrl = newUrl;
        this.youtubeEmbedUrl;
        this.loadYouTube();
        this.activeSource = "youtube";
        if (this.isPlaying) {
          audio.pause();
        }
      } else if (url.includes("spotify")) {
        this.spotifyUrl = newUrl;
        this.spotifyEmbedUrl;
        this.loadSpotify();
        this.activeSource = "spotify";
        if (this.isPlaying) {
          audio.pause();
        }
      } else {
        this.showEmbed = false;
        this.seekable = true;
        this.audioUrl = newUrl;
        this.loadAudio(`http://192.168.100.2:5000/api/stream/${this.audioUrl}.mp4`);
        this.activeSource = "url";
        this.fetchVideoForPropUrl(newUrl)
      }
    },
    async fetchVideoForPropUrl(id) {
      this.loading = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/songs/song/info/${id}`);

        if (response.data && response.data.songs) {
          console.log("API Response:", response.data.songs);
          // this.currentTrack.src = `http://192.168.100.2:5000/api/stream/${response.data.songs.url}`;
          this.currentTrack.title = response.data.songs[0].title || "Unknown Title";
          this.currentTrack.artist = response.data.songs[0].artist || "Unknown Artist";
          // this.currentTrack.source = "URL";
          // this.showEmbed = true;
          // this.seekable = false;
          // this.isPlaying = true; // Autoplay for API content
        } else {
          console.error("No video URL found in API response");
        }
      } catch (error) {
        console.error("API Error:", error);
      } finally {
        this.loading = false;
      }
    },

    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
      window.addEventListener("resize", () => {
        this.isMobile = window.innerWidth <= 768;
      });
    },
    extractYouTubeId(url) {
      // Extract ID from various YouTube URL formats
      const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
      const match = url.match(regExp);
      return match && match[2].length === 11 ? match[2] : url;
    },
    extractSpotifyId(url) {
      // Extract ID from Spotify URL
      const trackRegex = /spotify:track:([a-zA-Z0-9]+)/;
      const playlistRegex = /spotify:playlist:([a-zA-Z0-9]+)/;
      const urlTrackRegex = /open\.spotify\.com\/track\/([a-zA-Z0-9]+)/;
      const urlPlaylistRegex = /open\.spotify\.com\/playlist\/([a-zA-Z0-9]+)/;

      let match;
      if ((match = url.match(trackRegex)) || (match = url.match(urlTrackRegex))) {
        return { type: "track", id: match[1] };
      } else if (
        (match = url.match(playlistRegex)) ||
        (match = url.match(urlPlaylistRegex))
      ) {
        return { type: "playlist", id: match[1] };
      }
      return { type: "unknown", id: url };
    },
    playPause() {
      if (!this.currentTrack.src && !this.showEmbed) {
        alert("Please select a media source first");
        return;
      }

      if (this.showEmbed) {
        // For embeds, we can't control playback directly, just toggle the flag
        this.isPlaying = !this.isPlaying;
        return;
      }

      const audio = this.$refs.audioPlayer;
      if (this.isPlaying) {
        audio.pause();
      } else {
        audio.play().catch((error) => {
          console.error("Playback failed:", error);
          alert("Playback failed. Please check the audio source.");
        });
      }
      this.isPlaying = !this.isPlaying;
    },
    stop() {
      if (this.showEmbed) {
        this.showEmbed = false;
        this.embeddedContent = "";
        this.currentTrack = {
          title: "",
          artist: "",
          source: "",
          src: "",
        };
      } else {
        const audio = this.$refs.audioPlayer;
        audio.pause();
        audio.currentTime = 0;
      }
      this.isPlaying = false;
      this.currentTime = 0;
    },
    updateTime() {
      this.currentTime = this.$refs.audioPlayer.currentTime;
    },
    updateDuration() {
      this.duration = this.$refs.audioPlayer.duration;
      this.setupAudioVisualizer();
    },
    seek() {
      if (!this.showEmbed) {
        this.$refs.audioPlayer.currentTime = this.currentTime;
      }
    },
    setVolume() {
      if (!this.showEmbed) {
        this.$refs.audioPlayer.volume = this.volume;
      }
    },
    formatTime(seconds) {
      if (isNaN(seconds)) return "0:00";
      const minutes = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${minutes}:${secs < 10 ? "0" : ""}${secs}`;
    },
    onTrackEnd() {
      this.isPlaying = false;
      this.currentTime = 0;
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      this.currentTrack = {
        title: file.name.replace(/\.[^/.]+$/, ""), // Remove file extension
        artist: "Local file",
        source: "File",
        src: URL.createObjectURL(file),
      };

      this.loadAudio(this.currentTrack.src);
      this.showEmbed = false;
      this.seekable = true;
    },
    loadFromUrl() {
      if (!this.audioUrl) return;

      // Basic check for direct audio files
      if (this.audioUrl.match(/\.(mp3|wav|ogg|m4a|aac|flac)$/i)) {
        this.currentTrack = {
          title: this.audioUrl.split("/").pop() || "Online Audio",
          artist: "Online source",
          source: "URL",
          src: this.audioUrl,
        };
        this.loadAudio(this.audioUrl);
        this.showEmbed = false;
        this.seekable = true;
      } else {
        // Treat as generic embed
        this.embeddedContent = '<iframe src="' + this.audioUrl + '" frameborder="0" allowfullscreen></iframe>';
        this.currentTrack = {
          title: "Embedded Content",
          artist: "",
          source: "URL",
          src: `http://192.168.100.2:5000/api/stream/${this.audioUrl}.mp4`,
        };
        this.showEmbed = true;
        this.seekable = false;
      }
    },
    loadYouTube() {
      if (!this.youtubeUrl) return;

      const videoId = this.extractYouTubeId(this.youtubeUrl);
      if (!videoId) {
        alert("Invalid YouTube URL");
        return;
      }

      this.currentTrack = {
        title: "YouTube Video",
        artist: "",
        source: "YouTube",
        src: this.youtubeUrl,
      };
      this.showEmbed = true;
      this.seekable = false;
      this.isPlaying = true; // Autoplay for YouTube
    },
    loadSpotify() {
      if (!this.spotifyUrl) return;

      const spotifyId = this.extractSpotifyId(this.spotifyUrl);
      if (!spotifyId.id) {
        alert("Invalid Spotify URL");
        return;
      }

      this.currentTrack = {
        title: spotifyId.type === "track" ? "Spotify Track" : "Spotify Playlist",
        artist: "",
        source: "Spotify",
        src: this.spotifyUrl,
      };
      this.showEmbed = true;
      this.seekable = false;
      this.isPlaying = true; // Autoplay for Spotify
    },
    loadAudio(src) {
      const audio = this.$refs.audioPlayer;
      if (!audio) {
        setTimeout(() => {}, 3000);
      }
      audio.src = src;
      audio.load();
      this.isPlaying = false;
      this.currentTime = 0;

      // Try to play automatically (may be blocked by browser policies)
      audio
        .play()
        .then(() => {
          this.isPlaying = true;
        })
        .catch((error) => {
          console.log("Autoplay was prevented:", error);
          // User interaction will be required to play
        });
    },
    setupAudioVisualizer() {
      if (!this.visualizerEnabled) return;

      const audio = this.$refs.audioPlayer;
      const canvas = this.$refs.visualizerCanvas;
      const canvasCtx = canvas.getContext("2d");

      // Set canvas size
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;

      // Create audio context if it doesn't exist
      if (!this.audioContext) {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        this.analyser = this.audioContext.createAnalyser();
        this.analyser.fftSize = 256;

        const source = this.audioContext.createMediaElementSource(audio);
        source.connect(this.analyser);
        this.analyser.connect(this.audioContext.destination);

        this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);
      }

      // Cancel any previous animation frame
      if (this.animationId) {
        cancelAnimationFrame(this.animationId);
      }

      // Draw visualizer
      const draw = () => {
        this.animationId = requestAnimationFrame(draw);

        this.analyser.getByteFrequencyData(this.dataArray);

        canvasCtx.fillStyle = "rgb(0, 0, 0)";
        canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

        const barWidth = (canvas.width / this.analyser.frequencyBinCount) * 2.5;
        let x = 0;

        for (let i = 0; i < this.analyser.frequencyBinCount; i++) {
          const barHeight = (this.dataArray[i] / 255) * canvas.height;

          canvasCtx.fillStyle = `rgb(${barHeight * 2}, 100, 200)`;
          canvasCtx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);

          x += barWidth + 1;
        }
      };

      draw();
    },
  },

watch: {
  url: {
    immediate: true,
    handler(newVal) {
      console.log("URL changed to:", newVal);
      // Defer categoriseURL to ensure $refs is available
      nextTick(() => this.categoriseURL(newVal));
    },
  },
},

  mounted() {
    this.checkMobile();
    this.setVolume(); // Set initial volume
  },
  beforeUnmount() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    if (this.audioContext) {
      this.audioContext.close();
    }
  },
};
</script>


<template>
  <div
    class="music-player"
    :class="{ 'mobile-view': isMobile, 'dark-theme': isDarkMode }"
  >
    <div class="player-header">
      <h2>{{ currentTrack.title || "Universal Music Player" }}</h2>
      <p v-if="currentTrack.artist">{{ currentTrack.artist }}</p>
      <p v-if="currentTrack.source" class="source-badge">{{ currentTrack.source }}</p>
    </div>

    <div class="player-content">
      <!-- Audio element (hidden) for direct audio files -->
      <audio
      crossorigin="anonymous"
        ref="audioPlayer"
        @timeupdate="updateTime"
        @loadedmetadata="updateDuration"
        @ended="onTrackEnd"
        v-show="!showEmbed"
        :volume="volume"
      ></audio>

      <!-- Embedded content display -->
      <div v-if="showEmbed" class="embedded-content">
        <div v-if="isYouTube" class="video-container">
          <iframe
            :src="youtubeEmbedUrl"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
            ref="youtubePlayer"
          ></iframe>
        </div>
        <div v-else-if="isSpotify" class="spotify-container">
          <iframe
            :src="spotifyEmbedUrl"
            frameborder="0"
            allowtransparency="true"
            allow="encrypted-media"
            ref="spotifyPlayer"
          ></iframe>
        </div>
        <div v-else class="generic-embed" v-html="embeddedContent"></div>
      </div>

      <!-- Visualizer for audio files -->
      <div v-if="!showEmbed && visualizerEnabled" class="visualizer">
        <canvas ref="visualizerCanvas"></canvas>
      </div>
    </div>

    <div class="player-controls">
      <div class="control-buttons">
        <button @click="stop" class="control-btn stop-btn" title="download">
          <ion-icon name="download"></ion-icon>
        </button>
        <button @click="playPause" class="control-btn play-pause">
          <span v-if="!isPlaying"><ion-icon name="play"></ion-icon></span>
          <span v-else><ion-icon name="pause"></ion-icon></span>
        </button>
        <button @click="stop" class="control-btn stop-btn" title="Stop">
          <ion-icon name="stop"></ion-icon>
        </button>
      </div>

      <div
        class="progress-container"
        v-if="activeSource !== 'youtube' && activeSource !== 'spotify'"
      >
        <input
          type="range"
          min="0"
          :max="duration"
          v-model="currentTime"
          @input="seek"
          class="progress-bar"
          :disabled="!seekable"
        />
        <div class="time-display">
          {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
        </div>
      </div>
    </div>

    <div class="player-sources" :class="{ 'dark-theme-2': isDarkMode }">
      <div class="source-tabs">
        <button
          v-for="source in availableSources"
          :key="source.id"
          @click="activeSource = source.id"
          :class="{ active: activeSource === source.id }"
          class="source-tab"
        >
          {{ source.label }}
        </button>
      </div>

      <div class="source-inputs">
        <!-- File upload -->
        <div v-if="activeSource === 'file'" class="file-selector">
          <input
            type="file"
            accept="audio/*"
            @change="handleFileUpload"
            id="audio-upload"
            class="file-input"
          />
          <label for="audio-upload" class="file-label">
            <span class="icon"><ion-icon name="folder"></ion-icon></span> Select Audio
            File
          </label>
        </div>

        <!-- URL input -->
        <div v-if="activeSource === 'url'" class="url-input">
          <input
            type="text"
            v-model="audioUrl"
            placeholder="Enter audio URL (MP3, WAV,MP4,MP4a etc.)"
            class="url-field"
            @keyup.enter="loadFromUrl"
            :class="{ 'dark-theme-3': isDarkMode }"
          />
          <button @click="loadFromUrl" class="url-btn">Load</button>
        </div>

        <!-- YouTube input -->
        <div v-if="activeSource === 'youtube'" class="url-input">
          <input
            type="text"
            v-model="youtubeUrl"
            placeholder="Enter YouTube URL or video ID"
            class="url-field"
            @keyup.enter="loadYouTube"
            :class="{ 'dark-theme-3': isDarkMode }"
          />
          <button @click="loadYouTube" class="url-btn youtube-btn">Load</button>
        </div>

        <!-- Spotify input -->
        <div v-if="activeSource === 'spotify'" class="url-input">
          <input
            type="text"
            v-model="spotifyUrl"
            placeholder="Enter Spotify track/playlist URL"
            class="url-field"
            @keyup.enter="loadSpotify"
            :class="{ 'dark-theme-3': isDarkMode }"
          />
          <button @click="loadSpotify" class="url-btn spotify-btn">Load</button>
        </div>
      </div>
    </div>

    <div class="player-options" :class="{ 'dark-theme-2': isDarkMode }">
      <div class="volume-control">
        <span class="icon">🔊</span>
        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          v-model="volume"
          @input="setVolume"
          class="volume-slider"
        />
      </div>

      <div class="visualizer-toggle">
        <label> <input type="checkbox" v-model="visualizerEnabled" /> Visualizer </label>
      </div>
    </div>
  </div>
</template>



<style>
:root {
  /* Light mode colors */
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --bg-tertiary: #e0e0e0;
  --text-primary: #333333;
  --text-secondary: #555555;
  --accent-primary: #4a6bff;
  --accent-secondary: #3a5bef;
  --border-color: #dddddd;
  --shadow-color: rgba(0, 0, 0, 0.1);
  --visualizer-bg: #f0f0f5;
  --visualizer-bar: hsla(240, 80%, 60%, 0.8);

  /* Dark mode colors */
  --bg-primary-dark: #1a1a2e;
  --bg-secondary-dark: #16213e;
  --bg-tertiary-dark: #0f3460;
  --text-primary-dark: #f0f0f0;
  --text-secondary-dark: #cccccc;
  --accent-primary-dark: #6a8cff;
  --accent-secondary-dark: #5a7cff;
  --border-color-dark: #333344;
  --shadow-color-dark: rgba(0, 0, 0, 0.3);
  --visualizer-bg-dark: #202030;
  --visualizer-bar-dark: hsla(240, 80%, 70%, 0.8);
}

[data-theme="dark"] {
  --bg-primary: var(--bg-primary-dark);
  --bg-secondary: var(--bg-secondary-dark);
  --bg-tertiary: var(--bg-tertiary-dark);
  --text-primary: var(--text-primary-dark);
  --text-secondary: var(--text-secondary-dark);
  --accent-primary: var(--accent-primary-dark);
  --accent-secondary: var(--accent-secondary-dark);
  --border-color: var(--border-color-dark);
  --shadow-color: var(--shadow-color-dark);
  --visualizer-bg: var(--visualizer-bg-dark);
  --visualizer-bar: var(--visualizer-bar-dark);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  transition: background-color 0.3s, color 0.3s, border-color 0.3s;
}

.music-player {
  font-family: "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", sans-serif;
  max-width: 400px;
  margin: 0 auto;
  padding: 1rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  border-radius: 12px;
  box-shadow: 0px 0px 4px black;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mobile-view {
  width: 100vw !important;
  border-radius: 12px 12px 0 0;
  max-height: 70%;
  overflow-y: auto;
}

.player-header {
  position: relative;
  text-align: center;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-color);
}

.player-header h2 {
  font-size: 1.2rem;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.player-header p {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.source-badge {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  background-color: var(--accent-primary);
  color: white;
  border-radius: 12px;
  font-size: 0.7rem;
  margin-top: 0.25rem;
}

.theme-toggle {
  position: absolute;
  top: 0;
  right: 0;
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: var(--text-primary);
}

.player-content {
  position: relative;
  min-height: 150px;
  background-color: var(--bg-secondary);
  border-radius: 8px;
  overflow: hidden;
}

.embedded-content {
  width: 100%;
  height: 100%;
  min-height: 150px;
  background-color: gray;
}

.video-container,
.spotify-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
}

.video-container iframe,
.spotify-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

.generic-embed {
  width: 100%;
  height: 100%;
  min-height: 150px;
}

.visualizer {
  width: 100%;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.visualizer canvas {
  width: 100%;
  height: 100%;
}

.player-controls {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.control-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.control-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background-color: var(--accent-primary);
  color: white;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s, background-color 0.2s;
}

.control-btn:hover {
  background-color: var(--accent-secondary);
  transform: scale(1.05);
}

.play-pause {
  width: 50px;
  height: 50px;
  font-size: 1.2rem;
}

.progress-container {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.progress-bar {
  width: 100%;
  height: 6px;
  -webkit-appearance: none;
  appearance: none;
  background-color: var(--bg-tertiary);
  border-radius: 3px;
  outline: none;
  cursor: pointer;
}

.progress-bar::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: var(--accent-primary);
  cursor: pointer;
}

.progress-bar:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.progress-bar:disabled::-webkit-slider-thumb {
  background-color: var(--text-secondary);
}

.time-display {
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-align: center;
}

.player-sources {
  background-color: var(--bg-secondary);
  border-radius: 8px;
  padding: 0.75rem;
}

.source-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 0.75rem;
}

.source-tab {
  flex: 1;
  padding: 0.5rem;
  border: none;
  background: none;
  color: var(--text-secondary);
  font-weight: 500;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.source-tab.active {
  color: var(--accent-primary);
  border-bottom-color: var(--accent-primary);
}

.source-inputs {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.file-selector {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.file-input {
  display: none;
}

.file-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background-color: var(--accent-primary);
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.file-label:hover {
  background-color: var(--accent-secondary);
}

.current-file {
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.url-input {
  display: flex;
  gap: 0.5rem;
}

.url-field {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.url-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  background-color: var(--accent-primary);
  color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.url-btn:hover {
  background-color: var(--accent-secondary);
}

.youtube-btn {
  background-color: #ff0000;
}

.youtube-btn:hover {
  background-color: #cc0000;
}

.spotify-btn {
  background-color: #1db954;
}

.spotify-btn:hover {
  background-color: #1aa34a;
}

.player-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background-color: var(--bg-secondary);
  border-radius: 8px;
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.volume-slider {
  flex: 1;
  height: 6px;
  -webkit-appearance: none;
  appearance: none;
  background-color: var(--bg-tertiary);
  border-radius: 3px;
  outline: none;
  cursor: pointer;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background-color: var(--accent-primary);
  cursor: pointer;
}

.volume-value {
  font-size: 0.8rem;
  color: var(--text-secondary);
  min-width: 40px;
  text-align: right;
}

.option-buttons {
  display: flex;
  gap: 0.5rem;
}

.option-btn {
  padding: 0.3rem 0.6rem;
  font-size: 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
}

.option-btn.active {
  background-color: var(--accent-primary);
  color: white;
  border-color: var(--accent-primary);
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .music-player {
    padding: 0.75rem;
  }

  .player-header h2 {
    font-size: 1.1rem;
  }

  .control-buttons {
    gap: 0.75rem;
  }

  .control-btn {
    width: 36px;
    height: 36px;
  }

  .play-pause {
    width: 44px;
    height: 44px;
  }
}
.dark-theme {
  background-color: var(--bg-dark-2);
  color: var(--text-dark);
}
.dark-theme-2 {
  background-color: var(--bg-dark-3);
}
.dark-theme-3 {
  background-color: var(--bg-dark-5);
  color: var(--bg-light-5);
  border: 1px solid gray;
}
</style>
