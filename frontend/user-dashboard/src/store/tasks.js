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
      status:'',

    };
  },

  actions: {
    async download_yt_stream(songId, itag, filename) {
      if (!itag) {
        console.log("Please select a stream to download.");
        return;
      }
    
      const downloadId = songId || `download_${Date.now()}`;
      this.userStore.set_isAboutToDownload(true);
    
      try {
        const response = await fetch(`${BASE_URL}/api/download/yt`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            itag, 
            song_url: extractYouTubeID(songId), 
            filename,
            userId: this.userId,
            start_byte: this.start_bytes,
            size_mb: this.activeFilesize,
            format: this.activeFormat,
            thumbnailUrl: this.thumbnailUrl,
          })
        });
    
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    
        this.downloadsCount('+');
    
        const reader = response.body.getReader();
        const chunks = [];
        let downloadedSize = 0;
        const contentLength = this.activeFilesize * 1024 * 1024;
    
        // ✅ Ensure the downloadId exists before setting properties
        if (!this.onGoingDownloads[downloadId]) {
          this.onGoingDownloads[downloadId] = {};
        }
    
        this.onGoingDownloads[downloadId] = { filename, progress: 0, status: "downloading" };
    
        let done = false;
        while (!done) {
          const { done: readerDone, value } = await reader.read();
          if (readerDone) break;
    
          chunks.push(value);
          downloadedSize += value.length;
    
          this.onGoingDownloads[downloadId].progress = ((downloadedSize / contentLength) * 100).toFixed(2);
        }
    
        const blob = new Blob(chunks, { type: "video/mp4" });
        this.saveToFile(blob, filename);
    
        // ✅ Update status safely
        if (this.onGoingDownloads[downloadId]) {
          this.onGoingDownloads[downloadId].status = "completed";
        }
    
        this.downloadsCount('-');
    
      } catch (error) {
        console.error("Download failed:", error);
        
        if (this.onGoingDownloads[downloadId]) {
          this.onGoingDownloads[downloadId].status = "failed";
        }
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
