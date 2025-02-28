<template>
  <div id="stream-container">
    streams:{{ songId }}
    {{ info.title }}
    {{ info.author }}
    <transition name="fade">
      <div v-if="isLoading" class="loader-container">
        <div class="loader"></div>
      </div>
    </transition>

    <transition name="fade">
      <template v-if="!isLoading">
        <!-- Streams (Visible Once Fetched) -->
        <div v-if="streams.length" class="streams-container">
          <div
            v-for="(stream, index) in streams"
            :key="index"
            class="stream-item"
            @click="ActivateStream($event, stream.itag)"
          >
            <span class="stream-name">{{ stream.resolution }}</span>
            <p>itag:: {{ stream.itag }}</p>
            <img
              class="stream-audio-icon"
              :src="showfileicon(convertResolution(stream.resolution))"
              loading="lazy"
              :alt="convertResolution(stream.resolution) + ' icon'"
            />
            <p v-if="activeItag === stream.itag "><ion-icon name="checkmark-done-outline"></ion-icon></p>
          </div>
          <button id="downloadSt" :class="{'disabledDownload': !activeItag}" @click="handleDownload" :disabled="!activeItag">Confirm</button>
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

export default {
  props: {
    songId: String,
    streamloading: Boolean, // Keep this, but use it as an initial value
  },
  data() {
    return {
      streams: [],
      info: {},
      isLoading: this.streamloading, // Use a local state variable
      showfileicon,
      convertResolution,
      activeItag: null,
    };
  },
  methods: {
    ActivateStream(event, itag) {
      event.preventDefault();
      event.stopPropagation();
      document.querySelectorAll(".active-stream").forEach(st=>{
        st.classList.remove("active-stream");
       });

      const clickedElement = event.currentTarget; // Get the clicked element
      clickedElement.classList.add("active-stream"); // Add class to it

      this.activeItag = itag;
    },

    categorize_url() {
      if (this.songId.includes("youtube" || "youtu")) {
        this.fetchStreams_youtube();
      } else if (this.songId.includes("spotify")) {
        this.fetchStreams_spotify();
      } else {
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
        })
        .catch((error) => {
          console.error("Error fetching streams:", error);
        })
        .finally(() => {
          this.isLoading = false; // Ensure loading stops after fetch
        });
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

#downloadSt{
  background-color: #0435bc;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  position: absolute;
  bottom: 2px;
  right:0;
}
.disabledDownload{
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
