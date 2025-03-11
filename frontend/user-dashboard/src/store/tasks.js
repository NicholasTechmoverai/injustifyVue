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
    async download_yt_stream(songId, itag, filename,extension,resolution) {
      if (!itag) {
        console.log("Please select a stream to download.");
        return;
      }
    
      this.userStore.set_isAboutToDownload(true);
      let download_id;
    
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
            ext:extension
          })
        });
    
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        this.downloadsCount('+');

        const header_info = response.headers;
        //const contentType = header_info.get("Content-Type");

        const contentDisposition = header_info.get("Content-Disposition");
        const b_filename = contentDisposition
            ? contentDisposition.split("filename=")[1]?.replace(/"/g, "") 
            : filename; 
        
        const b_extension = header_info.get("format") || extension;
        
        download_id = header_info.get("X-Download-URL") ||songId ;
        
    
        if (!this.onGoingDownloads) this.onGoingDownloads = {};
        if (!this.onGoingDownloads[download_id]) {
          this.onGoingDownloads[download_id] = {};
        }
    
        const reader = response.body.getReader();
        const contentLength = this.activeFilesize * 1024 * 1024; // Convert MB to bytes
        let downloadedSize = 0;
        const progressBarWidth = 40; 

        await audio_decider(itag,extension,resolution)
    
        const stream = new ReadableStream({
          start: (controller) => { 
            const push = () => { 
              reader.read().then(({ done, value }) => {
                if (done) {
                  console.log("\nDownload completed!");
                  this.downloadsCount('-');
                  this.onGoingDownloads[download_id].status = "completed";
                  controller.close();
                  return;
                }
    
                downloadedSize += value.length;
                const progress = downloadedSize / contentLength;
                const filledBar = "█".repeat(Math.floor(progress * progressBarWidth));
                const emptyBar = " ".repeat(progressBarWidth - filledBar.length);
                const percent = (progress * 100).toFixed(2);
    
                this.onGoingDownloads[download_id] = { filename, progress, status: "downloading" };
    
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
        this.saveToFile(blob, b_filename,b_extension);
    
      } catch (error) {
        console.error("Download failed:", error);
        if (this.onGoingDownloads[download_id]) {
          this.onGoingDownloads[download_id].status = "failed";
        }
      } finally {
        this.userStore.set_isAboutToDownload(false);
      }
    },
    
    
    

    saveToFile(blob, filename,extension) {
      const fileExtension = extension.startsWith(".") ? extension.slice(1) : extension;

      const downloadLink = document.createElement("a");
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = `${filename}.${fileExtension}`;
    
      document.body.appendChild(downloadLink);
      downloadLink.click();
    
      URL.revokeObjectURL(downloadLink.href);
      //document.body.removeChild(downloadLink); 
      
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
    },

    async audio_decider(songId, itag, extension, resolution) {
      if (itag === '18' || resolution === 'audio only' || extension === 'm4a') {
        return;
      }
    
      const audioItagMap = {
        'mp4': '140',   // Standard audio for mp4
        'webm': '251',  // Standard audio for webm
      };
    
      const audioItag = audioItagMap[extension];
      if (audioItag) {
        await download_yt_stream_audio(songId, audioItag);
      }
    }
    

    
    
  }
});
