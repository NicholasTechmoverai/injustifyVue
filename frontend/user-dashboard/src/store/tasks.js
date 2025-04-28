import { defineStore } from 'pinia';
import { useUserStore } from "@/store/index.js";
import { computed } from "vue";
import { BASE_URL,extractYouTubeID } from "@/utils/index.js";
// import { FFmpeg } from '@ffmpeg/ffmpeg';

import socket from "@/services/websocket";
// import { ID3Writer } from 'browser-id3-writer';

// console.log("FFmpeg",FFmpeg); // Check if this logs the function



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

                          // setInterval(() => {
                          //   socket.emit("download_progress", {
                          //     songId: extractYouTubeID(songId),
                          //     user_id: this.userId,
                          //     itag,
                          //     progress,
                          //     status: "IN_PROGRESS",
                          //     filename,
                          //     thumbnail: thumbnail,
                          //     filesize: contentLength,
                          //     downloadedSize: downloadedSize,
                          //     format: format,
                          //   });
                            
                          // }, 3000);
                        }
            
                        controller.enqueue(value);
                        push();
                    });
                };
                push();
            }
        });

        const main_blob = await new Response(stream).blob();
        this.saveToFile(main_blob, b_filename, b_extension,{
          title: 'My Cool Song',
          artist: 'Gee',
          album: 'Awesome Album',
          comment: 'Made with ❤️',
          genre: 'Afrobeat'
        });
        socket.emit("download_progress", {
          songId: extractYouTubeID(songId),
          user_id: this.userId,
          itag,
          status: "SUCCESS",  
          filename,
          thumbnail: thumbnail,
          filesize: contentLength? contentLength : downloadedSize,
          downloadedSize: downloadedSize,
          format: format,
        });
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
    itag='18',
    filename,
      ext='mp4',
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
        filename: this.activeFilename? this.activeFilename : filename,
        userId: user_id,
        itag,
        start_byte: size_mb,
        size_mb: this.activeFilesize? this.activeFilesize : size_mb,
        format: songId.split('.').pop(),
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
    const contentLength = this.size_mb * 1024 * 1024; // Convert MB to bytes
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

    this.saveToFile(main_blob, b_filename, b_extension,{
      title: 'My Cool Song',
      artist: 'Gee',
      album: 'Awesome Album',
      comment: 'Made with ❤️',
      genre: 'Afrobeat'
    });
    socket.emit("download_progress", {
      songId:  `${songId.split('.').slice(0, -1).join('.')}`,
      user_id: this.userId,
      itag,
      status: "SUCCESS",  
      filename: this.activeFilename? this.activeFilename : filename,
      filesize: contentLength? contentLength : downloadedSize,
      downloadedSize: downloadedSize,
      format: songId.split('.').pop(),
      thumbnail: `th_${songId.split('.').slice(0, -1).join('.')}.jpg`,
    });

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



// async fetchCoverImage(url) {
//   try {
//     const response = await fetch(url);
//     if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
//     const blob = await response.blob();
//     const arrayBuffer = await blob.arrayBuffer();
//     const view = new DataView(arrayBuffer);

//     const magic = [
//       view.getUint32(0),
//       view.getUint32(4)
//     ];
//     const isJPEG = magic[0] === 0xFFD8FFE0 || magic[0] === 0xFFD8FFE1;
//     const isPNG = magic[0] === 0x89504E47 && magic[1] === 0x0D0A1A0A;

//     if (isJPEG || isPNG) {
//       return new Uint8Array(arrayBuffer); // Return correct type for APIC
//     } else {
//       throw new Error("Invalid image format");
//     }
//   } catch (error) {
//     console.error('Failed to fetch cover image:', error);
//     return null;
//   }
// },

// async saveToFile(blobOrUrl, filename, ext, img_url = null) {
//   let taggedBlob, url;
//   const tempLink = document.createElement('a');

//   try {
//     // Convert blobOrUrl to ArrayBuffer
//     let arrayBuffer;
//     if (blobOrUrl instanceof Blob) {
//       arrayBuffer = await blobOrUrl.arrayBuffer();
//     } else if (typeof blobOrUrl === 'string') {
//       const response = await fetch(blobOrUrl);
//       if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
//       const blob = await response.blob();
//       arrayBuffer = await blob.arrayBuffer();
//     } else {
//       throw new Error('Invalid input to saveToFile');
//     }

//     // Sanitize filename and extract metadata
//     const sanitizedFilename = filename.replace(/[<>:"/\\|?*]/g, '_');
//     const [artist, ...titleParts] = sanitizedFilename.split('-');
//     const title = titleParts.join('-').trim();

//     // Initialize ID3 writer with the ArrayBuffer
//     const writer = new ID3Writer(arrayBuffer);

//     // Handle cover image
//     if (img_url) {
//       const coverImage = await this.fetchCoverImage(img_url);
//       if (coverImage) {
//         writer.setFrame('APIC', {
//           type: 3,
//           data: coverImage,
//           description: 'Cover Image'
//         });
//       }
//     }

//     // Set ID3 tags
//     writer
//       .setFrame('TIT2', title || sanitizedFilename)
//       .setFrame('TPE1', artist ? [artist.trim()] : ['Unknown Artist'])
//       .setFrame('TALB', 'Injustify Collection')
//       .setFrame('COMM', {
//         description: 'Like No Other...South of Sahara',
//         text: 'injustify.buzz'
//       });

//     // Add tag and get the final blob
//     writer.addTag();
//     taggedBlob = writer.getBlob();

//     if (taggedBlob.size <= 0) {
//       throw new Error('Tagged blob is empty');
//     }

//     // Set up download
//     url = URL.createObjectURL(taggedBlob);
//     tempLink.href = url;
//     tempLink.download = `${sanitizedFilename}.${ext}`;
//     tempLink.style.display = 'none';
//     document.body.appendChild(tempLink);

//     // Trigger download
//     tempLink.click();

//     console.log("✅ File saved successfully:", sanitizedFilename);
//     this.downloadsCount('-');
//     return true;
//   } catch (error) {
//     console.error('❌ Failed to save file:', error);
//     throw error;
//   } finally {
//     // Cleanup resources
//     if (tempLink.parentNode) {
//       document.body.removeChild(tempLink);
//     }
//     if (url) {
//       setTimeout(() => URL.revokeObjectURL(url), 0);
//     }
//   }
// },






// async  saveToFile(blob, filename, ext, metadata = {}) {
//   if (!(blob instanceof Blob)) {
//     throw new Error('Input must be a valid Blob object');
//   }

//   const ffmpeg = new FFmpeg({ log: true });
//   let url = null;
//   const tempLink = document.createElement('a');

//   try {
//     // Load FFmpeg
//     console.log('⏳ Loading FFmpeg...');
//     await ffmpeg.load();
//     console.log('✅ FFmpeg loaded successfully');

//     // Sanitize filename and prepare file names
//     const sanitizedFilename = filename.replace(/[<>:"/\\|?*]/g, '_');
//     const inputFileName = `input.${ext}`;
//     const outputFileName = `output.${ext}`;

//     // Write input file
//     console.log('⏳ Processing audio file...');
//     const arrayBuffer = await blob.arrayBuffer();
//     ffmpeg.FS('writeFile', inputFileName, new Uint8Array(arrayBuffer));

//     // Prepare metadata arguments
//     const metadataArgs = [];
//     const validMetadataFields = ['title', 'artist', 'album', 'comment', 'genre'];
    
//     validMetadataFields.forEach(field => {
//       if (metadata[field]) {
//         metadataArgs.push('-metadata', `${field}=${metadata[field]}`);
//       }
//     });

//     // Add cover art if provided
//     let coverArtArgs = [];
//     if (metadata.coverArt && metadata.coverArt instanceof Blob) {
//       const coverFileName = 'cover.jpg';
//       const coverArrayBuffer = await metadata.coverArt.arrayBuffer();
//       ffmpeg.FS('writeFile', coverFileName, new Uint8Array(coverArrayBuffer));
//       coverArtArgs = [
//         '-i', coverFileName,
//         '-map', '0',
//         '-map', '1',
//         '-c:v', 'mjpeg',
//         '-disposition:v', 'attached_pic'
//       ];
//     }

//     // Execute FFmpeg command
//     const command = [
//       '-i', inputFileName,
//       ...coverArtArgs,
//       ...metadataArgs,
//       '-c:a', 'copy',
//       '-id3v2_version', '3',
//       '-write_id3v1', '1',
//       outputFileName
//     ];

//     console.log('🏃‍♂️ Executing FFmpeg command:', command.join(' '));
//     await ffmpeg.exec(command);

//     // Read output file
//     const outputData = ffmpeg.FS('readFile', outputFileName);
    
//     if (outputData.length === 0) {
//       throw new Error('FFmpeg output is empty');
//     }

//     // Create output blob with correct MIME type
//     const mimeType = this.getMimeType(ext);
//     const outputBlob = new Blob([outputData.buffer], { type: mimeType });

//     // Set up download
//     url = URL.createObjectURL(outputBlob);
//     tempLink.href = url;
//     tempLink.download = `${sanitizedFilename}.${ext}`;
//     tempLink.style.display = 'none';
//     document.body.appendChild(tempLink);

//     // Trigger download
//     console.log('⬇️ Starting download...');
//     tempLink.click();

//     console.log('✅ File saved successfully with metadata!');
//     return {
//       success: true,
//       filename: `${sanitizedFilename}.${ext}`,
//       size: outputBlob.size
//     };

//   } catch (error) {
//     console.error('❌ Error processing file:', error);
//     throw new Error(`Failed to process file: ${error.message}`);
//   } finally {
//     // Cleanup
//     if (tempLink.parentNode) {
//       document.body.removeChild(tempLink);
//     }
//     if (url) {
//       setTimeout(() => URL.revokeObjectURL(url), 100);
//     }
//     try {
//       await ffmpeg.exit();
//     } catch (cleanupError) {
//       console.warn('⚠️ Error during FFmpeg cleanup:', cleanupError);
//     }
//   }
// },

// // Helper function to get MIME type from extension
//  getMimeType(ext) {
//   const mimeTypes = {
//     mp3: 'audio/mpeg',
//     m4a: 'audio/mp4',
//     ogg: 'audio/ogg',
//     wav: 'audio/wav',
//     flac: 'audio/flac'
//   };
//   return mimeTypes[ext.toLowerCase()] || 'application/octet-stream';
// },


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
