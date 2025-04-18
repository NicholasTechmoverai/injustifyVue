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
      userId: computed(() => userStore?.userId),
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
    async calculateETA(fileSizeInMB, downloadSpeedMbps) {
      if (downloadSpeedMbps <= 0) return "Calculating..."; // Avoid division by zero
  
      const etaSeconds = (fileSizeInMB * 8) / downloadSpeedMbps; // Convert MB to Megabits
      const minutes = Math.floor(etaSeconds / 60);
      const seconds = Math.round(etaSeconds % 60);
  
      return minutes > 0 ? `${minutes} min ${seconds} sec` : `${seconds} sec`;
  },

  async calculateSpeedPerSec(fetchedSize, elapseTime) {
    if (fetchedSize <= 0 || elapseTime <= 0) return 0; // Avoid division by zero

    // Convert fetched bytes to Megabits per second (Mbps)
    const speedMbps = (fetchedSize / (1024 * 1024)) * 8 / elapseTime; 

    console.log(`Fetched: ${fetchedSize} bytes | Time: ${elapseTime}s | Speed: ${speedMbps.toFixed(2)} Mbps`);
    
    return speedMbps; // Return numeric value
},

async download_yt_stream(
   songId,
   itag, 
   filename,
   extension, 
   start_byte = 0,
   size_mb=0,
   format = null,
   thumbnail=null,
   resolution) {



    if (!this.userId) {
        console.log("Kindly login to make a Download!!.");
        this.userStore.set_snackbarMessage(
          "Kindly login to make a Download!!",
          "info",
          10000
        );
        return;
    }
    if (!itag) {
        console.log("Please select a stream to download.", resolution);
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
                userId:this.userId ,
                start_byte:start_byte,
                size_mb:size_mb,
                format: format,
                thumbnailUrl: thumbnail,
                ext: extension
            })
        });

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        this.downloadsCount('+');

        const startTime = performance.now();
        const header_info = response.headers;
        const contentDisposition = header_info.get("Content-Disposition");

        const b_filename = contentDisposition 
            ? contentDisposition.split("filename=")[1]?.replace(/"/g, "") 
            : filename || "downloaded_file"; 

        const b_extension = header_info.get("format") || extension;
        download_id = header_info.get("X-Download-URL") || songId;
        const timestamp = Date.now();

        if (!this.onGoingDownloads) {
          this.onGoingDownloads = {};
      }
      
      const contentLength = this.activeFilesize * 1024 * 1024; // Convert MB to bytes
      let downloadedSize = 0;
      let lastUpdateTime = startTime;
      let lastDownloadedSize = 0;
      let speedSamples = [];
      const MAX_SAMPLES = 5; // Number of samples for moving average
  
      const reader = response.body.getReader();

        const stream = new ReadableStream({
            start: (controller) => { 
                const push = () => { 
                    reader.read().then(async ({ done, value }) => {
                        if (done) {
                            console.log("\nDownload completed!");
                            this.onGoingDownloads[download_id].status = "completed";
                            this.onGoingDownloads[download_id].progress = 100;
                            this.onGoingDownloads[download_id].downloadSpeedMbps = "0 Mb/s";
                            this.onGoingDownloads[download_id].eta = "00:00";
                            controller.close();
                            return;
                        }

                        const currentTime = performance.now();
                        const chunkSize = value.length;
                        downloadedSize += chunkSize;
            
                        // Calculate instant speed
                        const timeDiff = (currentTime - lastUpdateTime) / 1000; // in seconds
                        const sizeDiff = downloadedSize - lastDownloadedSize;
                        
                        if (timeDiff > 0) {
                          const instantSpeed = (sizeDiff / timeDiff) / (1024 * 1024); // in MB/s
                          
                          // Add to speed samples for moving average
                          speedSamples.push(instantSpeed);
                          if (speedSamples.length > MAX_SAMPLES) {
                            speedSamples.shift();
                          }
                          
                          // Calculate average speed
                          const avgSpeed = speedSamples.reduce((sum, speed) => sum + speed, 0) / speedSamples.length;
                          
                          // Calculate progress
                          const progress = Math.min((downloadedSize / contentLength) * 100, 100);
                          
                          // Calculate ETA
                          const remainingBytes = contentLength - downloadedSize;
                          const remainingSeconds = remainingBytes / (avgSpeed * 1024 * 1024);
                          const eta = this.formatETA(remainingSeconds);
                          
                          // Format speed
                          let formattedSpeed;
                          if (avgSpeed > 1) {
                            formattedSpeed = `${avgSpeed.toFixed(2)} MB/s`;
                          } else if (avgSpeed > 0.001) {
                            formattedSpeed = `${(avgSpeed * 1024).toFixed(2)} KB/s`;
                          } else {
                            formattedSpeed = `${(avgSpeed * 1024 * 1024).toFixed(0)} B/s`;
                          }
            
                          // Update download info
                          if (!this.onGoingDownloads[download_id]) {
                            this.onGoingDownloads[download_id] = {};
                          }
            
                          this.onGoingDownloads[download_id] = {
                            timestamp,
                            filename,
                            progress,
                            status: "downloading",
                            eta,
                            downloadSpeedMbps: formattedSpeed,
                            thumbnail: thumbnail,
                            filesize: contentLength,
                            downloadedSize: downloadedSize,
                          };
            
                          // Log progress (optional)
                          console.clear();
                          console.log(`Downloading: ${filename}`);
                          console.log(`Progress: ${progress.toFixed(2)}%`);
                          console.log(`Speed: ${formattedSpeed}`);
                          console.log(`ETA: ${eta}`);
            
                          lastUpdateTime = currentTime;
                          lastDownloadedSize = downloadedSize;
                        }
            
                        controller.enqueue(value);
                        push();
                    });
                };
                push();
            }
        });

        const main_blob = await new Response(stream).blob();
        this.saveToFile(main_blob, b_filename, b_extension);
        this.sortDownloadsByTimestamp();
    } catch (error) {
        console.error("Download failed:", error);
        if (this.onGoingDownloads[download_id]) {
            this.onGoingDownloads[download_id].status = "failed";
        }
    } finally {
        this.userStore.set_isAboutToDownload(false);
    }
},

async download_injustify_stream(
  songId,
    itag,
    filename,
      ext,
      size_mb=0,
      format = null,
      url,
      thumbnail=null,
) {
  console.log("Downloading...", filename, "::::::::", this.activeFilename);
  if (!songId || !filename) {
    console.log("Please enter valid song ID and filename.");
    return;
  }


  const user_id = this.userId;
  if (!user_id) {
    console.log("Kindly login to make a Download!!.");
    this.userStore.set_snackbarMessage(
      "Kindly login to make a Download!!",
      "info",
      10000
    );
    return;
  }

  console.log(size_mb,format,url)
  let download_id;
  this.userStore.set_isAboutToDownload(true);

  try {
    const response = await fetch(`${BASE_URL}/api/download/injustify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        songId: `${songId.split('.').slice(0, -1).join('.')}`,
        song_url: songId,
        filename: this.activeFilename,
        userId: user_id,
        itag,
        start_byte: this.start_bytes,
        size_mb: this.activeFilesize,
        format: this.activeFormat,
        thumbnailUrl: `th_${songId.split('.').slice(0, -1).join('.')}.jpg`,
      })
    });

    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    this.downloadsCount('+');

    const startTime = performance.now();
    const header_info = response.headers;
    const contentDisposition = header_info.get("Content-Disposition");

    const b_filename = contentDisposition
      ? contentDisposition.split("filename=")[1]?.replace(/"/g, "")
      : filename || "downloaded_file";

    const b_extension = header_info.get("format") || ext;
    download_id = header_info.get("X-Download-URL") || songId;
    const timestamp = Date.now();

    // Initialize downloads tracking
    if (!this.onGoingDownloads) {
      this.onGoingDownloads = {};
    }

    // Calculate total size in bytes
    const contentLength = this.activeFilesize * 1024 * 1024; // Convert MB to bytes
    let downloadedSize = 0;
    let lastUpdateTime = startTime;
    let lastDownloadedSize = 0;
    let speedSamples = [];
    const MAX_SAMPLES = 5; // Number of samples for moving average

    const reader = response.body.getReader();

    const stream = new ReadableStream({
      start: (controller) => {
        const push = () => {
          reader.read().then(async ({ done, value }) => {
            if (done) {
              console.log("\nDownload completed!");
              if (this.onGoingDownloads[download_id]) {
                this.onGoingDownloads[download_id].status = "completed";
                this.onGoingDownloads[download_id].progress = 100;
                this.onGoingDownloads[download_id].downloadSpeedMbps = "0 Mb/s";
                this.onGoingDownloads[download_id].eta = "00:00";
              }
              controller.close();
              return;
            }

            const currentTime = performance.now();
            const chunkSize = value.length;
            downloadedSize += chunkSize;

            // Calculate instant speed
            const timeDiff = (currentTime - lastUpdateTime) / 1000; // in seconds
            const sizeDiff = downloadedSize - lastDownloadedSize;
            
            if (timeDiff > 0) {
              const instantSpeed = (sizeDiff / timeDiff) / (1024 * 1024); // in MB/s
              
              // Add to speed samples for moving average
              speedSamples.push(instantSpeed);
              if (speedSamples.length > MAX_SAMPLES) {
                speedSamples.shift();
              }
              
              // Calculate average speed
              const avgSpeed = speedSamples.reduce((sum, speed) => sum + speed, 0) / speedSamples.length;
              
              // Calculate progress
              const progress = Math.min((downloadedSize / contentLength) * 100, 100);
              
              // Calculate ETA
              const remainingBytes = contentLength - downloadedSize;
              const remainingSeconds = remainingBytes / (avgSpeed * 1024 * 1024);
              const eta = this.formatETA(remainingSeconds);
              
              // Format speed
              let formattedSpeed;
              if (avgSpeed > 1) {
                formattedSpeed = `${avgSpeed.toFixed(2)} MB/s`;
              } else if (avgSpeed > 0.001) {
                formattedSpeed = `${(avgSpeed * 1024).toFixed(2)} KB/s`;
              } else {
                formattedSpeed = `${(avgSpeed * 1024 * 1024).toFixed(0)} B/s`;
              }

              // Update download info
              if (!this.onGoingDownloads[download_id]) {
                this.onGoingDownloads[download_id] = {};
              }

              this.onGoingDownloads[download_id] = {
                timestamp,
                filename,
                progress,
                status: "downloading",
                eta,
                downloadSpeedMbps: formattedSpeed,
                thumbnail: thumbnail,
                filesize: contentLength,
                downloadedSize: downloadedSize,
              };

              // Log progress (optional)
              console.clear();
              console.log(`Downloading: ${filename}`);
              console.log(`Progress: ${progress.toFixed(2)}%`);
              console.log(`Speed: ${formattedSpeed}`);
              console.log(`ETA: ${eta}`);

              lastUpdateTime = currentTime;
              lastDownloadedSize = downloadedSize;
            }

            controller.enqueue(value);
            push();
          }).catch(error => {
            console.error("Error reading stream:", error);
            if (this.onGoingDownloads[download_id]) {
              this.onGoingDownloads[download_id].status = "failed";
            }
            controller.error(error);
          });
        };
        push();
      }
    });

    const main_blob = await new Response(stream).blob();
    this.saveToFile(main_blob, b_filename, b_extension);

    // Sort downloads by timestamp
    this.sortDownloadsByTimestamp();

  } catch (error) {
    console.error("Download failed:", error);
    if (download_id && this.onGoingDownloads[download_id]) {
      this.onGoingDownloads[download_id].status = "failed";
    }
  } finally {
    this.userStore.set_isAboutToDownload(false);
  }
},

// Helper method to format ETA
formatETA(seconds) {
  if (seconds <= 0) return "00:00";
  
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  
  return [
    hours.toString().padStart(2, '0'),
    minutes.toString().padStart(2, '0'),
    secs.toString().padStart(2, '0')
  ].join(':');
},

// Helper method to sort downloads by timestamp
sortDownloadsByTimestamp() {
  if (!this.onGoingDownloads) return;
  // Convert the object to an array, sort it, and then put it back as an object if needed.
  const sortedDownloads = Object.entries(this.onGoingDownloads) // Convert the object to an array of key-value pairs
      .sort((a, b) => new Date(b[1].timestamp) - new Date(a[1].timestamp))  // Sort by timestamp in descending order
      .reduce((acc, [key, value]) => {
          acc[key] = value;  // Rebuild the object with sorted entries
          return acc;
      }, {});

  this.onGoingDownloads = sortedDownloads;
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
