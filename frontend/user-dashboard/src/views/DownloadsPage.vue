<template>
  <div v-if="loading" id="loading">
    <ion-icon name="reload-outline"></ion-icon>
  </div>
  <div class="MainContainer" :class="{ collabsedBig: iscollapsedBig }">
    <div id="downloads-Main-container">
      <div id="page_inner-header" :class="{ 'darktheme-2': isDarkMode }">
        <div id="iconPlusQuery">
          <h1 @click="reloadPage" class="injustifyLogoR">Injustify</h1>
          <div>Downloads</div>
        </div>

        <div id="searchcontrols">
          <button><ion-icon name="clipboard"></ion-icon></button>
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
              v-model="search"
              @input="
                () => {
                  offset = 0;
                  hasMore = true;
                  fetchDownloads(true);
                }
              "
              :class="{ 'darktheme-4': isDarkMode }"
            />
            <button
              @click="
                () => {
                  offset = 0;
                  search = null;
                  hasMore = true;
                  fetchDownloads(true);
                }
              "
              :class="{ 'darktheme-3': isDarkMode }"
            >
              <ion-icon name="reload-outline"></ion-icon>
            </button>
            <button
              @click="
                () => {
                  offset = 0;
                  hasMore = true;
                  fetchDownloads(true);
                }
              "
              :class="{ 'darktheme-3': isDarkMode }"
            >
              <ion-icon name="search-outline"></ion-icon>
            </button>
          </div>
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
            <label for="monthYear">Select date:</label>
            <input
              v-model="s_date"
              @change="handleDateChange"
              type="date"
              id="monthYear"
              name="monthYear"
            />
          </div>
        </div>
      </div>
      <div
        v-if="downloads.length || Object.keys(onGoingDownloads).length"
        id="downloads-container"
      >
        <!-- Display Ongoing Downloads -->
        <div
          v-for="(download, id) in onGoingDownloads"
          :key="id"
          class="downloading-file card"
          :class="{ 'darktheme-5': isDarkMode }"
        >
          <div class="ghg">
            <div class="dowloadFileInfo">
              <h3>{{ download.filename }}</h3>
              <div class="downloadfileMeta">
                <p>
                  Total Size:
                  <span>{{ (download.filesize / (1024 * 1024)).toFixed(2) }}</span> MB
                </p>
                <p>
                  Downloaded:
                  <span>{{ (download.downloadedSize / (1024 * 1024)).toFixed(2) }}</span>
                  MB
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
                    :style="{ width: (download.progress * 100).toFixed(2) + '%' }"
                  ></div>
                </div>
              </div>
            </div>

            <div class="downloadFilePic">
              <div class="downloadFileResolution">4K</div>
              <img :src="download.thumbnail" />
            </div>
          </div>

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

            <button
              type="button"
              class="cancelDownload"
              @click="cancelDownload(download.download_id)"
            >
              <ion-icon name="trash-outline"></ion-icon>
            </button>
          </div>
        </div>

        <!-- Display Completed Downloads -->
        <div
          v-for="(download, index) in downloads"
          :key="download.download_id"
          class="downloading-file card"
          :class="{ 'darktheme-5': isDarkMode }"
        >
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

            <div class="downloadFilePic">
              <div class="downloadFileResolution">4K</div>
              <img :src="download.thumbnail" />
            </div>
          </div>

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

            <button type="button" class="cancelDownload" @click="cancelDownload(index,download.song_id)">
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
import { adv_UserStore } from "@/store/tasks.js";
import { BASE_URL } from "@/utils/index.js";
import socket from "@/services/websocket";

export default {
  name: "UserDownloads",
  props: ["useremail"],

  setup() {
    const userStore = useUserStore();
    const advUserStore = adv_UserStore();

    return {
      iscollapsedBig: computed(() => userStore.iscollapsedBig),
      isDarkMode: computed(() => userStore.isdarkmode),
      onGoingDownloads: computed(() => advUserStore.onGoingDownloads),
    };
  },

  data() {
    const userStore = useUserStore();

    return {
      downloads: [],
      loading: false,
      hasMore: true,
      offset: 0,
      limit: 15,
      throttleTimeout: null,
      search: null,
      s_name: null,
      s_artist: null,
      s_date: null,
      showSearch: false,
      showMoreAdvancedFeatures: false,
      searchFrom: { injustify: true, youtube: true, spotify: true },
      filterBy: { artist: true, title: true, date: false },
      userId: computed(() => userStore.userId),

    };
  },
  mounted() {
    this.fetchDownloads(false);

    window.addEventListener("scroll", this.handleScroll);
  },
  beforeUnmount() {
    // Clean up the event listener to prevent memory leaks
    window.removeEventListener("scroll", this.handleScroll);
  },

  methods: {
    handleScroll() {
      const scrollTop = window.scrollY;
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;

      if (scrollTop + windowHeight >= documentHeight - 20) {
        this.offset += this.limit;
        this.fetchDownloads(false);
      }
    },
    handleDateChange(event) {
      this.s_date = event.target.value || null;
      this.offset = 0;
      (this.hasMore = true), this.fetchDownloads(true);
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
    async fetchDownloads(clr = false) {
      if (this.loading || !this.hasMore) return; // Prevent redundant fetches

      this.loading = true;
      try {
        const response = await axios.get(
          `${BASE_URL}/api/profile/downloads/${this.useremail}`,
          {
            params: {
              search: this.search,
              offset: this.offset,
              order_by: this.order_by,
              limit: this.limit,
              name: this.s_name,
              artist: this.s_artist,
              date: this.s_date,
            },
          }
        );
        const newDownloads = response.data.downloads || [];

        if (clr) this.downloads = [];
        if (newDownloads.length > 0) {
          this.downloads.push(...newDownloads);

          // Sort by date in descending order (newest first)
          this.downloads.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        }

        if (newDownloads.length < this.limit) {
          this.hasMore = false;
        }
      } catch (error) {
        console.error("Error fetching downloads:", error);
        this.errorMessage = "Failed to fetch downloads. Please try again later.";
      } finally {
        this.loading = false;
      }
    },

    progress(download) {
      return Math.round((download.filesize / download.filesize) * 100);
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
      this.fetchDownloads(true);
    },

    cancelDownload(index,download_id) {
      console.log("Canceling download:",download_id);
      this.downloads.splice(index, 1);
      socket.emit("deleteDownload", {
        downloadId: download_id,
        userId: this.userId,
      });
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
  flex-direction: column;
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
  width: 0%;
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
  background: #373737 !important;
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

#page_inner-header {
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
    margin: 0 !important;
    margin-right: auto !important;
    margin-bottom: 5px !important;
    padding-top: 0;
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
    top: 50px;
    padding: 10px 5px !important;
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    max-width: 360px;
    width: 100%;
    margin: auto;
    overflow-wrap: break-word;
    transition: background-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
    z-index: 100;
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
    padding: 0px !important;

    div {
      padding: 0 !important;
    }
  }

  #queryShow {
    display: flex;
    flex-direction: row;
    gap: 8px;
    align-items: center;
    padding: 3px 10px;
    border-radius: 8px;
    color: #f1f5f9;
    font-family: "Arial", sans-serif;
    box-sizing: border-box;

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
    ion-icon {
      padding: 3px 5px;
      min-width: 15px;
      min-height: 10px;
      cursor: pointer;
      font-weight: bolder;
      font-size: 20px !important;
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
      padding: 0!important;
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
<style scoped>
#AdvancedFeatures {
  position: absolute;
  right: 0;
  top: 50px;
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
