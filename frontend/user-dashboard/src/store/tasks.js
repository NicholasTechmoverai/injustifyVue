import { defineStore } from 'pinia';
import { useUserStore } from "@/store/index.js";
import { computed } from "vue";
import { BASE_URL } from "@/utils/index.js";


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
    };
  },

  actions: {
    async download_yt_stream() {
      if (!this.activeItag) {
        console.log("Please select a stream to download.");
        return;
      }

      try {
        this.userStore.set_isAboutToDownload(true);

        const response = await fetch(`${BASE_URL}/api/download/yt`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            itag: this.activeItag,
            service: this.activeService,
            songId: this.songId,
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

        // Get content length
        const contentLength = this.activeFilesize * 1024 * 1024; // Convert MB to bytes
        let downloadedSize = this.start_bytes;

        // Read response as a stream
        const reader = response.body.getReader();
        const chunks = [];
        let progressInterval = setInterval(() => {
          this.downloadProgress = ((downloadedSize / contentLength) * 100).toFixed(2);
          console.log(`Download Progress: ${this.downloadProgress}%`);
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

        // Get format from backend response or default to mp4
        const fileFormat = this.activeFormat ? `.${this.activeFormat}` : ".mp4";
        const fullFilename = this.activeFilename + fileFormat; // Append correct format

        this.saveToFile(blob, fullFilename);
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
    }
  }
});
