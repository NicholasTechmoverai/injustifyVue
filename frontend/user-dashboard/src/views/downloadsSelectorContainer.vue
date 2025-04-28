<template>
  <div id="stream-container" v-if="streamloading && songId">
    <div id="streams-container-Header">
      <div class="header-content">
        <!-- Stream Title -->
        <div class="stream-title">
          <!-- <p class="stream-label">Streams:</p> -->
          <p v-if="info.title || info.artist" class="song-info">
            {{ info.title }} - {{ info.artist }}
          </p>
          <p v-else-if="stmName">{{ stmName }}</p>
          <p v-else class="song-info">{{ songId }}</p>
          <!-- <div id="defultStreamHolder">
            <p id="descpt">default</p>
            <div id="itsContent">
              <div id="theDefultStream"><span>audio</span>(<span>mp4</span>)</div>
              <ion-icon name="close-outline"></ion-icon>
            </div>
          </div> -->
        </div>

        <!-- Control Buttons -->
        <div id="streamControler">
          <!-- Toggle Stream Container -->
          <button id="closeOpenContainerButton" @click="toogleStreamContainer()">
            <ion-icon
              :name="isDroppeddown ? 'chevron-down-outline' : 'chevron-up-outline'"
            ></ion-icon>
          </button>

          <!-- More Options Dropdown -->
          <div class="dropdown-container">
            <button id="moreOnStreams">
              <ion-icon name="list-outline"></ion-icon>
            </button>
            <div class="moreDropdown">
              <!-- Toggle Show All Streams -->
              <button @click="toggleShowAllStreams">
                <ion-icon
                  :name="showAll_streams ? 'list-outline' : 'filter-outline'"
                ></ion-icon>
                {{ showAll_streams ? "Show Selected Streams" : "Show All Streams" }}
              </button>

              <!-- Toggle Additional Info -->
              <button @click="toggleViewMore">
                <ion-icon :name="viewMore ? 'eye-off-outline' : 'eye-outline'"></ion-icon>
                {{ viewMore ? "Hide Info" : "Show Info" }}
              </button>
            </div>
          </div>

          <button @click="closeDownContainer"><ion-icon name="close"></ion-icon></button>
        </div>

        <!-- Download Indicator (Loader Unchanged) -->
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
            v-for="(stream, index) in activeService != 'youtube' || showAll_streams
              ? streams
              : filteredStreams"
            :key="index"
            class="stream-item"
            @click="ActivateStream($event, stream)"
          >
            <img
              class="stream-audio-icon"
              :src="showfileicon(convertResolution(stream.resolution))"
              loading="lazy"
              :alt="convertResolution(stream.resolution) + ' icon'"
            />
            <span class="stream-name">{{ convertResolution(stream.resolution) }}</span>
            <p>{{ stream.size_mb }}MB</p>
            <p>({{ stream.ext }})</p>
            <p v-if="viewMore">audio Codec::{{ stream.audio_codec }}</p>
            <p v-if="viewMore">video Codec::{{ stream.video_codec }}</p>
            <p v-if="viewMore">itag::{{ stream.itag }}</p>
            <p v-if="viewMore">vbr ::{{ stream.vbr }}</p>
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
import { adv_UserStore } from "@/store/tasks.js";

import { getYouTubeThumbnails } from "@/utils/index.js";

export default {
  props: {
    songId: String,
    stmName: String,
    streamloading: Boolean,
    streamSongId: String,
  },
  data() {
    const userStore = useUserStore();
    const advUserStore = adv_UserStore();

    return {
      streams: [],
      info: {},
      isLoading: this.streamloading,
      showAll_streams: false,
      showfileicon,
      convertResolution,
      activeItag: null,
      activeFilename: null,
      activeFilesize: null,
      activeService: null,
      activeResolution: null,
      activeThumbnail: null,
      activeExt: "mp4",
      userId: computed(() => userStore.userId),
      isDroppeddown: false,
      isAboutToDownload: computed(() => userStore.isAboutToDownload),
      userStore,
      advUserStore,
      viewMore: false,
      select: null,
      filter: null,
      filteredStreams: computed(() => {
        return this.streams.filter(
          (stream) => ["18", "140", "152"].includes(stream.itag) || this.showAll_streams
        );
      }),
    };
  },
  methods: {
    closeDownContainer(){
      this.$emit("closeDownContainer");
    },
    toggleShowAllStreams() {
      this.showAll_streams = !this.showAll_streams;
    },
    toggleViewMore() {
      this.viewMore = !this.viewMore;
    },
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
      this.activeFilename = this.stmName || `${this.info.title}-${this.info.artist}`;
      this.activeFilesize = stream.size_mb;
      this.activeExt = stream.ext;
      this.activeResolution = stream.resolution;
      this.activeThumbnail = getYouTubeThumbnails(this.songId);
      const info = {
        song_url: this.songId,
        filename: this.activeFilename,
        itag: this.activeItag,
        size_mb: this.activeFilesize,
        start_byte: 0,
        thumbnailUrl: getYouTubeThumbnails(this.songId),
        userId: this.userId,
        ext: this.activeExt,
      };
      this.userStore.set_DownloadFileCredential(info);
      console.log(this.activeItag, this.activeFilesize);
    },

    categorize_url() {
      this.isDroppeddown = false;
      if (this.songId && (this.songId != null || this.songId != '')) {
        if (this.songId.includes("youtu")) {
          this.activeService = "youtube";
          this.fetchStreams_youtube();
        } else if (this.songId.includes("spotify")) {
          this.activeService = "spotify";
          this.fetchStreams_spotify();
        } else {
          this.activeService = "injustify";
          this.fetchStreams_injustify();
        }
      }
    },
    fetchStreams_spotify() {
      this.isLoading = true;
      axios
        .get(`${BASE_URL}/api/download_streams/spotify/${this.songId}`)
        .then((response) => {
          console.log(response.data);
          this.streams = response.data;
        })
        .catch((error) => {
          console.error("Error fetching streams:", error);
          this.userStore.set_snackbarMessage(
            "Error fetching streams!,Kindly try again!!",
            "error",
            10000
          );
        });
    },
    fetchStreams_youtube() {
      this.isLoading = true; // Use local state

      axios
        .post(`${BASE_URL}/api/download_streams/youtube`, { songId: this.songId })
        .then((response) => {
          console.log("Fetched Streams:", response.data);
          if (response.data.success) {
            this.streams = response.data.streams;
            this.info = response.data.info;
            this.isDroppeddown = true;
          } else {
            console.error("Stream fetch failed:", response.data.message);
            this.userStore.set_snackbarMessage(
              "Error fetching streams!,Kindly try again!!",
              "error",
              10000
            );
          }
        })
        .catch((error) => {
          console.error("Error fetching streams:", error);
          this.userStore.set_snackbarMessage(
            "Error fetching streams!,Kindly try again!!",
            "error",
            10000
          );
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
          this.userStore.set_snackbarMessage(
            "Error fetching streams!,Kindly try again!!",
            "error",
            10000
          );
        })
        .finally(() => {
          this.isLoading = false; // Ensure loading stops after fetch
        });
    },

    handleDownload() {
      if (this.activeService === null) {
        console.log("Service not available for this song.");
        this.userStore.set_snackbarMessage(
          "Service not available for this song.!",
          "error",
          10000
        );

        return;
      } else if (this.activeService === "youtube") {
        this.isDroppeddown = false;
        this.advUserStore.download_yt_stream(
          this.songId,
          this.activeItag,
          this.activeFilename,
          this.activeExt,
          0,
          this.activeFilesize,
          null,
          this.activeThumbnail,
          this.activeResolution
        );
      } else if (this.activeService === "injustify") {
        this.isDroppeddown = false;
        this.advUserStore.download_injustify_stream(
          this.songId,
          this.activeItag,
          this.activeFilename,
          this.activeExt || "mp4"
        );
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
#moreOnStreams {
  position: relative;
}
.moreDropdown {
  position: absolute;
  top: 100%;
  right: 0%;
  display: none;
}
.moreDropdown button {
  white-space: nowrap;
}
#moreOnStreams:hover .moreDropdown {
  display: flex;
}
#streams-container-Header {
  display: flex;
  flex-direction: column;
}
#streams-container-Header p {
  margin: 0;
  padding: 0;
}
#streamControler {
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
  background: linear-gradient(
    to right,
    rgba(144, 145, 145, 0.438),
    rgba(126, 172, 217, 0.9)
  );
  cursor: pointer;
  outline: none;
  transition: background 0.3s ease-in-out, transform 0.2s ease-in-out;
  color: white;
  font-weight: bold;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(65, 68, 77, 0.3);
  transform: scale(1.02);
}

.active-stream:hover {
  background: linear-gradient(
    to right,
    rgba(130, 159, 218, 0.438),
    rgba(175, 179, 184, 0.9)
  );
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
  gap: 7px;
  color: black;
  border-radius: 8px;
  height: auto;
  max-height: 75vh;
  overflow-y: auto;
  padding: 2px;
  box-sizing: border-box;
  width: 100% !important;
}
.stream-item {
  padding: 8px;
  border-radius: 5px;
  box-shadow: 0px 0px 5px black;
  text-align: center;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 3px;
  width: 100% !important;
  overflow-wrap: break-word;
  box-sizing: border-box;
}

.stream-item p {
  margin: 0px;
  padding: 0px;
  color: inherit;
  word-break: break-word;
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
/* Light & Dark Themes */
.light-theme {
  --bg-color: #fff;
  --text-color: #333;
  --header-bg: #f0f0f0;
  --btn-bg: #ddd;
  --border-color: #ccc;
}

.dark-theme {
  --bg-color: #181818;
  --text-color: #f5f5f5;
  --header-bg: #222;
  --btn-bg: #333;
  --border-color: #444;
}

#stream-container {
  background: var(--bg-color);
  color: var(--text-color);
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

#streams-container-Header {
  background: var(--header-bg);
  padding: 10px 15px;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  width: 100%;
  position: relative;
}

.stream-title {
  text-align: left;
}

.stream-label {
  font-weight: bold;
  opacity: 0.8;
}

.song-info {
  font-weight: 500;
}

#streamControler {
  display: flex;
  gap: 10px;
  align-items: center;
}

button {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 5px;
  transition: 0.3s;
  border-radius: 5px;
}

button:hover {
  background: rgba(255, 255, 255, 0.2);
}

ion-icon {
  font-size: 1.4rem;
  color: var(--text-color);
}

.dropdown-container {
  position: relative;
  z-index: 100;
}

.moreDropdown {
  background: rgba(151, 145, 145, 0.928);
  border: 1px solid rgba(128, 128, 128, 0.622);
  border-radius: 5px;
}

.dropdown-container:hover .moreDropdown {
  display: block;
}

.moreDropdown button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-color);
  padding: 5px;
}

.streams-container {
  padding: 10px;
}

.stream-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-bottom: 1px solid var(--border-color);
}

#downloadSt {
  background: #007bff;
  color: #fff;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.3s;
}

#downloadSt:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.no-streams {
  text-align: center;
  font-weight: bold;
}

#defultStreamHolder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0px;
  padding: 5px 9px;
  background-color: #08111bef; /* Soft gray */
  border-radius: 6px;
  border: 1px solid #dddddd81; /* Light border */
  color: #555; /* Muted text color */
  max-width: 100px;
  position: absolute;
  right: 5px;
  top: 100%;
  font-size: 10px !important;
}
#defultStreamHolder > p {
  margin: 0 !important;
  padding: 0;
}

#defultStreamHolder #descpt {
  font-size: 8px;
  color: rgba(113, 110, 110, 0.939);
  margin: 0 !important;
  padding: 0;
}
#defultStreamHolder #itsContent {
  display: flex;
  flex-direction: row;
  gap: 5px;
}

#defultStreamHolder #itsContent ion-icon {
  margin-right: 0;
  color: #777;
  cursor: pointer;
  transition: color 0.3s ease;
  font-size: 12px !important;
  position: absolute;
  top: 2px;
  right: 2px;
}

#defultStreamHolder #itsContent ion-icon:hover {
  color: #0353c2; /* Darker on hover */
}
#theDefultStream {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #666; /* Softer text */
}

#theDefultStream span {
  font-size: 10px;
  color: #444; /* Not too strong */
}

ion-icon {
  font-size: 18px; /* Adjust icon size */
  color: #777; /* Muted icon */
  cursor: pointer;
  transition: color 0.3s ease;
}

ion-icon:hover {
  color: #333; /* Darker on hover */
}
</style>
