<template>
  <div id="stream-container">
    <div id="streams-container-Header">
      <div>
        streams:
        <p v-if="info.title || info.artist">{{ info.title }} - {{ info.artist }}</p>
        <p v-else>{{ songId }}</p>
        <button id="closeOpenContainerButton" @click="toogleStreamContainer()">
          <ion-icon name="chevron-down-outline"></ion-icon>
        </button>
        <div v-if="isAboutToDownload" class="inline-loader-container">
          <div class="lder"></div>
        </div>
      </div>
      <transition name="fade">
        <div v-if="isLoading" class="loader-container">
          <div class="loader"></div>
        </div>
      </transition>
    </div>
    <transition name="fade">
      <template v-if="isDroppeddown">
        <!-- Streams (Visible Once Fetched) -->
        <div v-if="streams.length" class="streams-container">
          <div
            v-for="(stream, index) in streams"
            :key="index"
            class="stream-item"
            @click="ActivateStream($event, stream)"
          >
            <span class="stream-name">{{ stream.resolution }}</span>
            <p>itag:: {{ stream.itag }}</p>
            <img
              class="stream-audio-icon"
              :src="showfileicon(convertResolution(stream.resolution))"
              loading="lazy"
              :alt="convertResolution(stream.resolution) + ' icon'"
            />
            <p v-if="activeItag === stream.itag">
              <ion-icon name="checkmark-done-outline"></ion-icon>
            </p>
          </div>
          <button
            id="downloadSt"
            :class="{ disabledDownload: !activeItag }"
            @click="handleDownload()"
            :disabled="!activeItag"
          >
            Confirm
          </button>
        </div>

        <!-- No Streams Found -->
        <p v-else class="no-streams">No streams available.</p>
      </template>
    </transition>
  </div>
</template>

<script>
import { BASE_URL, showfileicon, convertResolution } from "@/utils/index.js";
import axios from "axios";
import { computed } from "vue";
import { useUserStore } from "@/store/index.js";
import { getYouTubeThumbnails } from "@/utils/index.js";

export default {
  props: {
    songId: String,
    streamloading: Boolean, // Keep this, but use it as an initial value
  },
  data() {
    const userStore = useUserStore();

    return {
      streams: [],
      info: {},
      isLoading: this.streamloading,
      showfileicon,
      convertResolution,
      activeItag: null,
      activeFilename: null,
      activeFilesize: null,
      activeService: null,
      userId: computed(() => userStore.userId),
      isDroppeddown: false,
      isAboutToDownload: false,
    };
  },
  methods: {
    toogleStreamContainer() {
      this.isDroppeddown = !this.isDroppeddown;
    },
    ActivateStream(event, stream) {
      event.preventDefault();
      event.stopPropagation();
      document.querySelectorAll(".active-stream").forEach((st) => {
        st.classList.remove("active-stream");
      });

      const clickedElement = event.currentTarget;
      clickedElement.classList.add("active-stream");

      this.activeItag = stream.itag;
      this.activeFilename = `${this.info.title}-${this.info.artist}`;
      this.activeFilesize = stream.size_mb;
      const info = {
        song_url:this.songId,
        filename: this.activeFilename,
        itag: this.activeItag,
        size_mb: this.activeFilesize,
        start_byte: 0,
        thumbnailUrl: getYouTubeThumbnails(this.songId),
        userId: this.userId,
      };
      useUserStore.set_DownloadFileCredential(info)
      console.log(this.activeItag, this.activeFilesize);
    },

    categorize_url() {
      this.isDroppeddown = false;
      if (this.songId.includes("youtube" || "youtu")) {
        this.activeService = "youtube";
        this.fetchStreams_youtube();
      } else if (this.songId.includes("spotify")) {
        this.activeService = "spotify";
        this.fetchStreams_spotify();
      } else {
        this.activeService = "injustify";
        this.fetchStreams_injustify();
      }
    },
    fetchStreams_spotify() {
      this.isLoading = true; // Update local state instead of prop
      axios
        .get(`${BASE_URL}/api/download_streams/spotify/${this.songId}`)
        .then((response) => {
          console.log(response.data);
          this.streams = response.data;
        })
        .catch((error) => {
          console.error("Error fetching streams:", error);
        });
    },
    fetchStreams_youtube() {
      this.isLoading = true; // Use local state

      axios
        .post(`${BASE_URL}/api/download_streams/youtube`, { songId: this.songId }) // ✅ Send data in body
        .then((response) => {
          console.log("Fetched Streams:", response.data);
          if (response.data.success) {
            this.streams = response.data.streams;
            this.info = response.data.info;
            this.isDroppeddown = true;
            console.log("info::", this.info);
          } else {
            console.error("Stream fetch failed:", response.data.message);
          }
        })
        .catch((error) => {
          console.error("Error fetching streams:", error);
        })
        .finally(() => {
          this.isLoading = false; // Reset loading state
        });
    },

    fetchStreams_injustify() {
      this.isLoading = true; // Update local state instead of prop
      axios
        .get(`${BASE_URL}/api/download_streams/injustify/${this.songId}`)
        .then((response) => {
          console.log(response.data);
          this.streams = response.data;
          this.isDroppeddown = true;
        })
        .catch((error) => {
          console.error("Error fetching streams:", error);
        })
        .finally(() => {
          this.isLoading = false; // Ensure loading stops after fetch
        });
    },

    handleDownload() {
      if (this.activeService === null) {
        console.log("Service not available for this song.");
        return;
      } else if (this.activeService === "youtube") {
        console.log("Downloading YouTube video streams.");
        this.download_yt_stream();
      }
    },
  },
  mounted() {
    this.categorize_url();
  },
  watch: {
    songId() {
      this.categorize_url();
      this.streams = [];
      this.info = {};
      this.activeItag = null;
    },
  },
};
</script>

<style scoped>
#streams-container-Header {
  display: flex;
  flex-direction: column;
}
#streams-container-Header p {
  margin: 0;
  padding: 0;
}
#closeOpenContainerButton {
  position: absolute;
  right: 0;
  top: 5px;
}
#downloadSt {
  background-color: #0435bc;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  position: absolute;
  bottom: 2px;
  right: 0;
}
.disabledDownload {
  background-color: grey !important;
  cursor: not-allowed !important;
}
.active-stream {
  background-color: rgba(255, 0, 0, 0.5) !important;
  cursor: pointer;
  outline: none;
  transition: background 0.3s ease-in-out;
  color: #0435bc;
}
.stream-audio-icon {
  height: 30px;
}
#stream-container {
  width: 100%;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
  overflow: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: background 0.3s ease-in-out;
}

/* Streams Styling */
.streams-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: rgba(102, 100, 100, 0.541);
  color: black;
  border-radius: 8px;
  height: auto;
  max-height: 75vh;
  overflow-y: auto;
}
.stream-item {
  padding: 8px;
  background: #1d242d;
  color: white;
  border-radius: 5px;
  text-align: center;
  font-weight: bold;
  display: flex;
  flex-direction: row !important;
  align-items: center;
}

/* No Streams Found */
.no-streams {
  color: lightgray;
  font-style: italic;
}
.loader-container {
  width: 100%;
  height: 30px;
}
.loader {
  width: 100%;
  height: 100%;
  font-weight: bold;
  font-family: monospace;
  font-size: 20px;
  background: linear-gradient(
      135deg,
      #0000 calc(50% - 0.5em),
      #000 0 calc(50% + 0.5em),
      #0000 0
    )
    right/300% 100%;
  animation: l22 2s infinite;
}
.loader::before {
  content: "Fetching streams...";
  color: #0000;
  padding: 0 5px;
  background: inherit;
  background-image: linear-gradient(
    135deg,
    #000 calc(50% - 0.5em),
    #fff 0 calc(50% + 0.5em),
    #000 0
  );
  -webkit-background-clip: text;
  background-clip: text;
}

@keyframes l22 {
  100% {
    background-position: left;
  }
}
</style>
