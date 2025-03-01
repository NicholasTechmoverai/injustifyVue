import { defineStore } from 'pinia';
import axios from 'axios';
import { BASE_URL } from "@/utils/index.js";

export const useUserStore = defineStore('user', {
  state: () => ({
    email: 'injustify@gmail.com',
    name: 'injustify',
    isAboutToDownload: false,
    activeItag: null,
    activeService: null,
    songId: null,
    activeFilename: null,
    activeFilesize: 0,
    downloadProgress: 0,
  }),

  actions: {
    set_isAboutToDownload(val) {
      this.isAboutToDownload = val;
    },

    async download_yt_stream() {
      if (!this.activeItag) {
        console.log("Please select a stream to download.");
        return;
      }

      this.isAboutToDownload = true;
      this.set_isAboutToDownload(true);

      try {
        // Start the download request
        const response = await axios.get(`${BASE_URL}/api/download_stream`, {
          params: {
            itag: this.activeItag,
            service: this.activeService,
            songId: this.songId,
            filename: this.activeFilename,
            start_byte: 0,
            thumbnailUrl: getYouTubeThumbnails(this.songId),
            userId: this.userId,
            file_size: this.activeFilesize,
          },
          responseType: 'blob', // Use blob instead of stream
        });

        console.log("Download started:", response);

        // Track progress
        const contentLength = this.activeFilesize * 1024 * 1024; // Convert MB to Bytes
        let downloadedSize = 0;

        console.log("contentLength:", contentLength, "bytes downloaded" , downloadedSize);

        const reader = new FileReader();
        reader.onloadend = () => {
          this.saveToFile(response.data, this.activeFilename);
        };
        reader.readAsArrayBuffer(response.data);
      } catch (error) {
        console.error("Download failed:", error);
      } finally {
        this.isAboutToDownload = false;
        this.set_isAboutToDownload(false);
      }
    },

    saveToFile(blob, filename) {
      const downloadLink = document.createElement('a');
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = filename;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      URL.revokeObjectURL(downloadLink.href);
      console.log("Download completed!");
    }
  }
});
