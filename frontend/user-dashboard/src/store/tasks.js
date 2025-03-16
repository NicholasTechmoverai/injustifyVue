import { defineStore } from 'pinia';
import { useUserStore } from "@/store/index.js";
import { computed } from "vue";
import { BASE_URL,extractYouTubeID } from "@/utils/index.js";
import { FFmpeg } from '@ffmpeg/ffmpeg';

console.log("FFmpeg",FFmpeg); // Check if this logs the function



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
      ffmpeg: null,
      isFFmpegLoaded: false,
    };
  },


  actions: {

    async download_yt_stream(songId, itag, filename,extension,resolution) {
      if (!itag) {
        console.log("Please select a stream to download.",resolution);
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

        //const audio_blob = await this.audio_decider(songId, itag, extension, resolution);
    
        const stream = new ReadableStream({
          start: (controller) => { 
            const push = () => { 
              reader.read().then(({ done, value }) => {
                if (done) {
                  console.log("\nDownload completed!");
                  this.onGoingDownloads[download_id].status = "completed";
                  controller.close();
                  return;
                }
    
                downloadedSize += value.length;
                const progress = downloadedSize / contentLength;
                const percent = (progress * 100).toFixed(2);
    
                this.onGoingDownloads[download_id] = { filename, progress, status: "downloading" };
    
                console.clear();
                console.log(`Downloading: ${filename}`);    
                console.log("progress::",percent)

                controller.enqueue(value);
                push();
              });
            };
            push();
          }
        });

        const main_blob = await new Response(stream).blob();
  
        this.saveToFile(main_blob, b_filename,b_extension);
    
      } catch (error) {
        console.error("Download failed:", error);
        if (this.onGoingDownloads[download_id]) {
          this.onGoingDownloads[download_id].status = "failed";
        }
      } finally {
        this.userStore.set_isAboutToDownload(false);
      }
    },
 

    // Save File to Local System
    saveToFile(blob, filename, ext) {
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `${filename}.${ext}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(link.href);
      console.log("File saved successfully:", filename);
      this.downloadsCount('-');
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
      console.log("async audio_decider", songId, itag, extension,resolution)
/*      if (itag === '18' || resolution === 'audio only' || extension === 'm4a') {
        console.log(`Skipping audio download for itag: ${itag}, resolution: ${resolution}, extension: ${extension}`);
        return;
      }
    
      const audioItagMap = {
        'mp4': '140',
        'webm': '251',
      };
    
      const audioItag = audioItagMap[extension];
      if (audioItag) {
        console.log(`Downloading audio stream with itag: ${audioItag}`);
        return await this.download_yt_stream_audio(songId, audioItag);
      } else {
        console.log(`No audio download required for extension: ${extension}`);
      } */
    },
    
    async download_yt_stream_audio(songId, itag) {
      if (!itag) {
        console.log("Please select a stream to download.");
        return;
      }
    
      //let download_id;
      console.log("GETTING AUDIO!!!")
    
      try {
        const response = await fetch(`${BASE_URL}/api/download/yt`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            itag, 
            song_url: songId, 
            songId: extractYouTubeID(songId),
            filename:"audio",
            start_byte: 0,
            ext:'mp4'      
          })
        });
    
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const reader = response.body.getReader();
        let downloadedSize = 0;


        //const header_info = response.headers;
        //const contentType = header_info.get("Content-Type");

    
        const stream = new ReadableStream({
          start: (controller) => { 
            const push = () => { 
              reader.read().then(({ done, value }) => {
                if (done) {
                  console.log("\nDownload completed!");
                  controller.close();
                  return;
                }
    
                downloadedSize += value.length;    
 
                console.log(`LOADING AUDIO... ${downloadedSize} `);
    
                controller.enqueue(value);
                push();
              });
            };
            push();
          }
        });
    
        const audio_blob = await new Response(stream).blob();	
        return audio_blob		
      } catch (error) {
        console.error("Download failed:", error);
        
      } finally {console.log("audio download completed")
      }
    },
    

    
    
  }
});
