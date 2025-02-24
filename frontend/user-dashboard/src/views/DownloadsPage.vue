<template>
  <div v-if="loading" id="loading">
    <ion-icon name="reload-outline"></ion-icon>
  </div>
  <div class="MainContainer" :class="{ collabsedBig: iscollapsedBig }">
    <div id="downloads-Main-container">
      downloads
      <div v-if="downloads.length" id="downloads-container">
        <div
          v-for="(download, index) in downloads"
          :key="download.download_id"
          class="downloading-file card"
          :class="{ 'darktheme-5': isDarkMode }"
        >
          <!-- File Info -->
          <div class="ghg">
            <div class="dowloadFileInfo">
              <h3>{{ download.filename }}</h3>
              <div class="downloadfileMeta">
                <p>
                  Total Size: <span>{{ download.filesize }}</span> MB
                </p>
                <p>
                  Downloaded: <span>{{ download.filesize }}</span> MB
                </p>
                <p>
                  Remaining: <span>{{ remainingSize(download) }}</span> MB
                </p>
                <p>
                  ETA: <span>{{ eta(download) }}</span>
                </p>
                <div class="downloadFileProgressBar">
                  <div
                    class="progress-bar"
                    :style="{ width: progress(download) + '%' }"
                  ></div>
                  <span class="progress-percentage">{{ progress(download) }}%</span>
                </div>
              </div>
            </div>

            <!-- File Picture -->
            <div class="downloadFilePic">
              <div class="downloadFileResolution">4K</div>
              <img :src="download.thumbnail" />
            </div>
          </div>

          <!-- Progress and Controls -->
          <div class="progressAndcancel">
            <p>
              <span>{{ timeAgo(download.timestamp) }}</span>
            </p>
            <div class="speed-info">
              <p>
                Speed: <span>{{ speed(download) }} MB/s</span>
              </p>
            </div>

            <button
              type="button"
              class="pauseDownload"
              @click="togglePauseResume(download)"
            >
              <ion-icon
                :name="download.paused ? 'play-circle-outline' : 'pause-circle-outline'"
              ></ion-icon>
            </button>

            <button type="button" class="retryDownload" @click="retryDownload(download)">
              <ion-icon name="refresh-circle-outline"></ion-icon>
            </button>

            <button type="button" class="cancelDownload" @click="cancelDownload(index)">
              <ion-icon name="trash-outline"></ion-icon>
            </button>
          </div>
        </div>
      </div>
      <p v-else class="No-resultFound-message">
        <img src="../assets/no-search-result.png" alt="No search Found" />
        No downloads found.
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { computed } from "vue";
import { timeAgo } from "@/utils/index";
import { useUserStore } from "@/store/index.js";

export default {
  name: "UserDownloads",
  props: ["useremail"],

  setup() {
    const userStore = useUserStore();

    return {
      iscollapsedBig: computed(() => userStore.iscollapsedBig),
      isDarkMode: computed(() => userStore.isdarkmode),
    };
  },

  data() {
    return {
      downloads: [],
      loading: false,
    };
  },
  mounted() {
    this.fetchDownloads();
  },
  methods: {
    async fetchDownloads() {
      this.loading = true;
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/api/downloads/${this.useremail}`
        );
        this.downloads = response.data.downloads;
        this.loading = false;
      } catch (error) {
        console.error("Error fetching downloads:", error);
      }
    },

    progress(download) {
      return Math.round((download.totalSize / download.contentLength) * 100);
    },

    remainingSize(download) {
      if (download.contentLength && download.totalSize) {
        return ((download.contentLength - download.totalSize) / 1024 / 1024).toFixed(2);
      } else {
        return 0;
      }
    },

    speed(download) {
      const elapsedTime = download.totalSize / 1024 / 1024; // Seconds
      return (download.totalSize / elapsedTime / 1024 / 1024).toFixed(2); // MB/s
    },

    eta(download) {
      const remainingSize = download.contentLength - download.totalSize;
      const etaSeconds =
        remainingSize / (download.totalSize / (download.totalSize / 1024 / 1024));

      if (etaSeconds >= 60) {
        return `${Math.floor(etaSeconds / 60)} min ${Math.floor(etaSeconds % 60)} sec`;
      } else {
        return `${Math.floor(etaSeconds)} sec`;
      }
    },

    togglePauseResume(download) {
      download.paused = !download.paused;
      console.log(
        download.paused ? "Paused download" : "Resumed download",
        download.filename
      );
    },

    retryDownload(download) {
      console.log("Retrying download:", download.filename);
      this.fetchDownloads();
    },

    cancelDownload(index) {
      console.log("Canceling download:", this.downloads[index].filename);
      this.downloads.splice(index, 1);
    },
    timeAgo,
  },
};
</script>

<style scoped>
/* General container styling */
.ghg {
  display: flex;
  flex-direction: row;
  width: 100%;
}

/* Main Downloads Container */
#downloads-Main-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

/* Downloads List Container */
#downloads-container {
  display: flex;
  flex-direction: column-reverse;
  position: relative;
  width: 100%;
  min-height: 120px;
  transition: transform 0.5s ease-in-out, opacity 0.3s ease;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  padding: 0px !important;
}

#downloading-container p,
span {
  font-size: 14px;
  color: #333;
}

/* Individual Download Box */
.downloading-file {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  width: 95%;
  max-width: 600px;
  min-height: 120px;
  flex-direction: column;
  height: fit-content;
  gap: 10px;
  margin-top: 10px;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease-in-out;
  box-sizing: border-box;
}

.downloading-file:hover {
  transform: scale(1.02);
}

.dowloadFileInfo {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: 5px;
  width: 100%;
  box-sizing: border-box;
  color: #222;
}

.dowloadFileInfo h3 {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 5px;
}

.dowloadFileInfo p {
  font-size: 14px;
  color: #555;
}

/* File Thumbnail */
.downloadFilePic {
  min-width: 80px;
  width: 40%;
  max-width: 200px;
  height: 100%;
  position: relative;
  background-color: rgba(121, 109, 109, 0.141);
  border-radius: 10px;
}

.downloadFilePic img {
  max-height: 100%;
  width: 100%;
  min-height: 140px;
  height: auto;
  object-fit: cover;
}

/* File Resolution Tag */
.downloadFilePic .downloadFileResolution {
  position: absolute;
  top: 5px;
  left: 5px;
  color: white;
  padding: 5px 10px;
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  transition: all 0.3s ease-in-out;
}

.downloadFilePic .downloadFileResolution:hover {
  background-color: rgba(0, 0, 0, 0.9);
}

/* Progress Bar */
.downloading-file .downloadFileProgressBar {
  width: 100%;
  height: 6px;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
  position: relative;
  overflow: hidden;
}

.downloading-file .downloadFileProgressBar .progress-bar {
  height: 100%;
  background: linear-gradient(to right, #4caf50, #00e676);
  border-radius: 3px;
  position: absolute;
  transition: width 0.5s ease-in-out;
  width: 70%;
}

.downloading-file .downloadFileProgressBar .progress-percentage {
  position: absolute;
  top: -20px;
  right: 5px;
  color: #222;
  font-size: 12px;
  font-weight: bold;
}

/* Control Buttons */
.progressAndcancel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  width: 100%;
  gap: 8px;
  border-top: 1px solid #ddd;
  box-sizing: border-box;
  padding-top: 8px;
}
.downloadfileMeta p,
.progressAndcancel p {
  margin: 0;
  padding: 0;
} /* Pause, Retry, Delete Buttons */
.pauseDownload,
.retryDownload,
.cancelDownload {
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  border: none;
  outline: none;
  font-size: 16px;
  box-sizing: border-box;
  transition: all 0.3s ease-in-out;
}

.pauseDownload {
  background: #f1c40f;
  color: #fff;
}

.pauseDownload:hover {
  background: #d4ac0d;
}

.retryDownload {
  background: #3498db;
  color: #fff;
}

.retryDownload:hover {
  background: #2980b9;
}

.cancelDownload {
  background: #e74c3c;
  color: #fff;
}

.cancelDownload:hover {
  background: #c0392b;
}

/* Notification Badge */
#popUp-Noty-count,
#downloads-count {
  position: absolute;
  top: 5px;
  right: 5px;
  font-size: 12px;
  color: #fff;
  background-color: red;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.5s ease-in-out;
}

/* No Result Message */
.No-resultFound-message {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  font-size: 18px;
  font-weight: bold;
  flex-direction: column;
  color: #666;
  text-align: center;
}

.No-resultFound-message img {
  mix-blend-mode: multiply;
  max-height: 50vh;
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

.darktheme-5 {
  background: #252525 !important;
  color: #d4d4d4 !important;
}
.darktheme-5 .dowloadFileInfo p {
  color: #999;
}
.darktheme-5 span,
.darktheme-5 .darktheme-5 {
  color: #646161;
}
.darktheme-5 .dowloadFileInfo {
  color: rgb(191, 179, 179);
}
@media screen and (max-width: 500px) {
  .ghg {
    flex-direction: column-reverse; /* Stack items vertically */
    align-items: center;
    text-align: center;
    gap: 15px;
  }

  .downloadFilePic {
    width: 100%; /* Full width for better visibility */
    max-width: 300px; /* Prevent oversized images */
  }

  .downloadFilePic img {
    min-height: 120px; /* Ensure image is visible */
    object-fit: contain; /* Prevents cropping */
  }

  .dowloadFileInfo {
    width: 100%;
    padding: 5px;
  }

  .dowloadFileInfo h3 {
    font-size: 16px; /* Adjusted for readability */
  }

  .dowloadFileInfo p {
    font-size: 14px; /* Improve readability */
  }
}
</style>
