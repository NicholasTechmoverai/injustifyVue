import { defineStore } from 'pinia';
import { useUserStore } from "@/store/index.js";
import { computed } from "vue";
import { BASE_URL,extractYouTubeID } from "@/utils/index.js";


export const adv_UserStore = defineStore('adv_user', {
  state: () => {
    const userStore = useUserStore();
    return {
      email: 'injustify@gmail.com',
      name: 'injustify',
      userId: computed(() => userStore.downloadFileCredential?.userId),
      isAboutToDownload: computed(() => userStore.downloadFileCredential?.isAboutToDownload),
      activeItag: computed(() => userStore.downloadFileCredential?.itag),
      activeService: 'yt',
      songId: computed(() => userStore.downloadFileCredential?.song_url),
      activeFilename: computed(() => userStore.downloadFileCredential?.filename),
      activeFilesize: computed(() => userStore.downloadFileCredential?.size_mb),
      activeFormat: computed(() => userStore.downloadFileCredential?.format || 'mp4'), // Get format dynamically
      thumbnailUrl: computed(() => userStore.downloadFileCredential?.thumbnailUrl),
      start_bytes: computed(() => userStore.downloadFileCredential?.start_byte),
      downloadProgress: 0,
      userStore,
      currentDownloadCount:0,
      onGoingDownloads: {},

    };
  },

  actions: {
    async download_yt_stream() {
      if (!this.activeItag) {
        console.log("Please select a stream to download.");
        return;
      }
      this.userStore.set_isAboutToDownload(true);

      try {

        const response = await fetch(`${BASE_URL}/api/download/yt`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            itag: this.activeItag,
            service: this.activeService,
            songId: extractYouTubeID(this.songId),
            song_url: this.songId,
            filename: this.activeFilename,
            start_byte: this.start_bytes,
            thumbnailUrl: this.thumbnailUrl,
            userId: this.userId,
            file_size: this.activeFilesize,
          })
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        this.userStore.set_isAboutToDownload(false);

        this.downloadsCount('+')
        const contentLength = this.activeFilesize * 1024 * 1024; // Convert MB to bytes
        let downloadedSize = this.start_bytes;
        this.downloadProgress = ((downloadedSize / contentLength) * 100).toFixed(2);
        console.log(`Download Progress: ${this.downloadProgress}%,  total: ${downloadedSize} bytes downloaded ${contentLength}`);

        // Read response as a stream
        const reader = response.body.getReader();
        const chunks = [];
        let progressInterval = setInterval(() => {
          this.downloadProgress = ((downloadedSize / contentLength) * 100).toFixed(2);
          console.log(`Download Progress: ${this.downloadProgress}%,  total: ${downloadedSize} bytes downloaded ${contentLength}`);
        }, 1000);

        let done = false;
        while (!done) {
          const { done: readerDone, value } = await reader.read();
          if (readerDone) break; // Proper exit condition
        
          chunks.push(value);
          downloadedSize += value.length;
        }
        

        clearInterval(progressInterval);

        // Merge chunks and create file blob
        const blob = new Blob(chunks, { type: "video/mp4" });

        const contentDisposition = response.headers.get('Content-Disposition');
        const dwl_Id = response.headers.get('X-Download-URL');
        const dwn_info = {
          download_id: dwl_Id,
          download_url: contentDisposition?.split(';')[1].trim().split('=')[1],
          filename: this.activeFilename,
          filesize: contentLength,
          downloadedSize: downloadedSize,
          progress: this.downloadProgress,
          thumbnail: this.thumbnailUrl,
          timestamp: new Date().toISOString()
        }
        this.set_onGoingDownloads(dwl_Id,dwn_info)

        // Get format from backend response or default to mp4
        const fileFormat = this.activeFormat ? `.${this.activeFormat}` : ".mp4";
        const fullFilename = this.activeFilename + fileFormat; // Append correct format


        this.saveToFile(blob, fullFilename);
        this.downloadsCount('-')
        this.userStore.set_streamloading(false);

      } catch (error) {
        console.error("Download failed:", error);
      } finally {
        this.userStore.set_isAboutToDownload(false);
      }
    },

    saveToFile(blob, filename) {
      const downloadLink = document.createElement("a");
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = filename;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      URL.revokeObjectURL(downloadLink.href);
      console.log("Download completed:", filename);
    },
    downloadsCount(val) {
      if (val === '+') {
        this.currentDownloadCount++;
      } else if (val === '-') {
        this.currentDownloadCount--;
      }
    },
    set_onGoingDownloads(id, dwn) {
      if (!this.onGoingDownloads[id]) {
        this.onGoingDownloads[id] = dwn; // Add new download
      } else {
        Object.assign(this.onGoingDownloads[id], dwn); // Update existing download
      }
    }
    
    
  }
});
