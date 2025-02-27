<template>
  <div id="stream-container">
    streams:{{ songId }}
    <transition name="fade">
      <div v-if="isLoading" class="loader-container">
        <div class="loader"></div>
      </div>
    </transition>

    <transition name="fade">
      <template v-if="!isLoading">
        <!-- Streams (Visible Once Fetched) -->
        <div v-if="streams.length" class="streams-container">
          <div v-for="(stream, index) in streams" :key="index" class="stream-item">
            <span class="stream-name">{{ stream.name }}</span>
          </div>
        </div>

        <!-- No Streams Found -->
        <p v-else class="no-streams">No streams available.</p>
      </template>
    </transition>
  </div>
</template>

<script>
import { BASE_URL } from "@/utils/index.js";
import axios from "axios";

export default {
  props: {
    songId: String,
    streamloading: Boolean, // Keep this, but use it as an initial value
  },
  data() {
    return {
      streams: [],
      isLoading: this.streamloading, // Use a local state variable
    };
  },
  methods: {
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
    },
  },
};
</script>

<style scoped>
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
  background: white;
  color: black;
  padding: 15px;
  border-radius: 8px;
  height: auto;
  max-height: 75vh;
  overflow-y: auto;
}
.stream-item {
  padding: 8px;
  background: #0077ff;
  color: white;
  border-radius: 5px;
  text-align: center;
  font-weight: bold;
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
