<template>
  <div v-if="loading" id="loading">
    <ion-icon name="reload-outline"></ion-icon>
  </div>
  <div class="MainContainer">

  <div id="downloads-Main-container">
    downloads
  <div v-if="downloads.length" id="downloads-container">
    <div v-for="(download, index) in downloads" :key="index" class="downloading-file card">
      <!-- File Info -->
      <div class="ghg">
        <div class="dowloadFileInfo">
          <h3>{{ download.filename }}</h3>
          <div class="downloadfileMeta">
            <p>Total Size: <span>{{ download.filesize }}</span> MB</p>
            <p>Downloaded: <span>{{ download.filesize }}</span> MB</p>
            <p>Remaining: <span>{{ remainingSize(download) }}</span> MB</p>
            <p>ETA: <span>{{ eta(download) }}</span></p>
            <div class="downloadFileProgressBar">
              <div class="progress-bar" :style="{ width: progress(download) + '%' }"></div>
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
        <p><span>{{ timeAgo(download.timestamp) }}</span></p>
        <div class="speed-info">
          <p>Speed: <span>{{ speed(download) }} MB/s</span></p>
        </div>
        
        <button
          type="button"
          class="pauseDownload"
          @click="togglePauseResume(download)"
        >
          <ion-icon :name="download.paused ? 'play-circle-outline' : 'pause-circle-outline'"></ion-icon>
        </button>

        <button
          type="button"
          class="retryDownload"
          @click="retryDownload(download)"
        >
          <ion-icon name="refresh-circle-outline"></ion-icon>
        </button>

        <button type="button" class="cancelDownload" @click="cancelDownload(index)">
          <ion-icon name="trash-outline"></ion-icon>
        </button>
      </div>
    </div>
  </div>
  <p v-else class="No-resultFound-message">
      <img src="../assets/no-search-result.png" alt="No search Found">
      No downloads found.
  </p>
  </div>
  </div>

</template>

<script>
import axios from "axios";
import { timeAgo } from '@/utils/index';

export default {
  name: "UserDownloads",
  props: ["useremail"],
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
        const response = await axios.get(`http://127.0.0.1:5000/api/downloads/${this.useremail}`);
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
      return ((download.contentLength - download.totalSize) / 1024 / 1024).toFixed(2);
    },

    speed(download) {
      const elapsedTime = download.totalSize / 1024 / 1024; // Seconds
      return (download.totalSize / elapsedTime / 1024 / 1024).toFixed(2); // MB/s
    },

    eta(download) {
      const remainingSize = download.contentLength - download.totalSize;
      const etaSeconds = remainingSize / (download.totalSize / (download.totalSize / 1024 / 1024));

      if (etaSeconds >= 60) {
        return `${Math.floor(etaSeconds / 60)} min ${Math.floor(etaSeconds % 60)} sec`;
      } else {
        return `${Math.floor(etaSeconds)} sec`;
      }
    },

    togglePauseResume(download) {
      download.paused = !download.paused;
      console.log(download.paused ? "Paused download" : "Resumed download", download.filename);
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
.ghg{
    display: flex;
    flex-direction: row;
    width: 100%;
}
#downloads-Main-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
  justify-content: center;
}
#downloads-container {
    display: flex;
    flex-direction: column-reverse;
    position: relative;
    width: 100%;
    min-height: 100px; /* Ensures the container has a minimum height */
    transition: all 0.5s ease;
    justify-content: center;
    align-items: center;
    font-size: 12px;
    padding: 5px;
    box-sizing: border-box;
 
}
#downloading-container p,span {
    font-size: 12px;
}
.downloading-file {
    display: flex;
    align-items: center;
    justify-content: space-around;
    position: relative;
    width: 90%;
    max-width: 600px;
    min-height: 100px; /* Ensures it keeps its height */
    padding-right: 0;
    flex-direction: column;
    height: fit-content;
    gap:10px;
    margin-top: 20px;
}

.dowloadFileInfo{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    padding: 3px;
    width: 100%;

}

.downloading-file .end-handle {
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    background-color: gold;
    width: 10px;
    height: 50%;
    display: inline-block; /* Maintains width even if empty */
    border-radius: 3px 0 0 3px;
}
.downloadFilePic{
    min-width: 70px;
    width: 40%;
    max-width: 200px;
    height: 100%;
    position:relative;
}
.downloadFilePic img{
    max-height: 100%;
    width: 100%;
    min-height: 130px;
    height: 100% !important;
    object-fit: cover;
}
.downloadFilePic .downloadFileResolution{
    position: absolute;
    top: 0;
    left: -8%;
    color: inherit;
    padding: 5px;
    text-align: center;
    background-color: rgba(0, 0, 0, 0.818);
    border-radius: 50%;
    color: rgb(165, 165, 165);
    cursor: pointer;
}
.dowloadFileInfo h3,p{
    margin: 0;
    padding: 0;
    font-size: 14px;
    line-height: 1.4;
}

.dowloadFileInfo h3{
    font-weight: bold;
}

.progressAndcancel{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 5px;
    width: 100%;
    gap: 5px;
}
.downloading-file .downloadFileProgressBar{
    width: 100px;
    height: 5px;
    background-color: rgba(0, 0, 0, 0.2);
    border-radius: 3px;
    position: relative;
    margin: 2px 0;
}

.downloading-file .downloadFileProgressBar .progress-bar{
    height: 100%;
    background-color: rgb(0, 153, 0);
    border-radius: 3px;
    position: absolute;
    transition: width 0.5s ease;
    width: 70%;
}
.downloading-file .downloadFileProgressBar .progress-percentage{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    right:-10%;
    color: inherit;
    font-size: 10px;
}
.pauseDownload{
    padding: 5px 10px;
    border-radius: 3px;
    cursor: pointer;
    border: none;
    outline: none;
    box-shadow: none;
    font-size: 20px;
    color:  inherit;
}
.retryDownload{
    padding: 5px 10px;
    border-radius: 3px;
    cursor: pointer;
    border: none;
    outline: none;
    box-shadow: none;
    font-size: 20px;
    color:  inherit;
}
.deleteDownload{
    font-size: 20px!important;
}
.progressAndcancel .cancelDownload{
    color: rgb(147, 7, 7);
    padding: 5px 10px;
    border-radius: 3px;
    cursor: pointer;
    border: none;
    outline: none;
    box-shadow: none;
    min-width: 25px;
}

.progressAndcancel .cancelDownload:hover{
    color: rgb(255, 4, 4);
}

#popUp-Noty-count,
#downloads-count {
    position: absolute;
    top: 1%;
    left: 98%;
    transform: translateX(-100%);
    font-size: 12px;
    color: inherit;
    background-color: rgba(248, 0, 0, 0.818);
    border-radius: 50%;
    width: 20px;
    height: 20px;
    display: none;
    align-items: center;
    justify-content: center;
    transition: all 0.5s ease;
}
.No-resultFound-message{
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 20px;
    font-size: 16px;
    font-weight: bold;
    flex-direction: column;
}
.No-resultFound-message img{
    mix-blend-mode: multiply;
}
</style>
