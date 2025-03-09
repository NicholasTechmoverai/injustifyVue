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
            song_url: songId, 
            songId: extractYouTubeID(songId),
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
    
        // ✅ Ensure `onGoingDownloads` is initialized
        if (!this.onGoingDownloads) this.onGoingDownloads = {};
        if (!this.onGoingDownloads[downloadId]) {
          this.onGoingDownloads[downloadId] = {};
        }
    
        const reader = response.body.getReader();
        const contentLength = this.activeFilesize * 1024 * 1024; // Convert MB to bytes
        let downloadedSize = 0;
        const progressBarWidth = 40; // Number of characters in progress bar
    
        const stream = new ReadableStream({
          start: (controller) => { // ✅ Fix `this` binding issue
            const push = () => { 
              reader.read().then(({ done, value }) => {
                if (done) {
                  console.log("\nDownload completed!");
                  this.downloadsCount('-');
                  this.onGoingDownloads[downloadId].status = "completed"; // ✅ Mark as completed
                  controller.close();
                  return;
                }
    
                downloadedSize += value.length;
                const progress = downloadedSize / contentLength;
                const filledBar = "█".repeat(Math.floor(progress * progressBarWidth));
                const emptyBar = " ".repeat(progressBarWidth - filledBar.length);
                const percent = (progress * 100).toFixed(2);
    
                this.onGoingDownloads[downloadId] = { filename, progress, status: "downloading" };
    
                console.clear();
                console.log(`Downloading: ${filename}`);
                console.log(`[${filledBar}${emptyBar}] ${percent}% (${(downloadedSize / 1024 / 1024).toFixed(2)}MB / ${contentLength}MB)`);
    
                controller.enqueue(value);
                push();
              });
            };
            push();
          }
        });
    
        const blob = await new Response(stream).blob();
        this.saveToFile(blob, filename);
    
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
