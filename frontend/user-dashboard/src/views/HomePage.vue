<template>  
  <div class="MainContainer">
    <div id="homepage-header">
      <h3>Videos</h3>
      <p>{{ message }}</p>

      <div v-if="loading.local || loading.youtube || loading.spotify" class="spinner-container">
        <div class="loader">
          <p>Loading...</p>
        </div> 
      </div>

      <div>
        <h2>Video Filter</h2>
        <input type="text" placeholder="Filter Search" v-model="query" />
        <button @click="reset">Clear</button>
        <button @click="searchAll">Search</button>
      </div>
    </div>

    <!-- Video Sections -->
    <div v-for="(videoList, service) in videoSources" :key="service">
      <h2>{{ service }} Videos</h2>
      <div v-if="videoList.length" id="videosContainer">
        <div v-for="video in videoList" :key="video.song_id" class="video-card">
          <div @click="playVideo(video)">
            <img :src="getThumbnail(video, service)" alt="Video Thumbnail" />
            <div>
              <h4>{{ video.title }}</h4>
              <p>{{ video.artist }}</p>
            </div>
          </div>
          <div class="video-info-holder">
            <div class="video-Meta-info-holder">
              <span><i class="fa-solid fa-eye"></i>{{ video.views }}</span> 
              <span>{{ timeAgo(video.date) || 'many hours ago' }}</span>
              <span class="video-duration">{{ convertSeconds(video.duration) || '' }}</span>
            </div>
            <div @click="likeVideo(video)">
              <ion-icon :name="video.liked ? 'heart' : 'heart-outline'"></ion-icon>
            </div>
            <div @click="handleChat(video)">
              <ion-icon name="chatbubble-ellipses-outline"></ion-icon>
            </div>
          </div>
        </div>
      </div>
      <p v-else>No {{ service }} videos found</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { timeAgo } from '@/utils/index';
import { getYouTubeThumbnails, getSpotifyThumbnail } from "@/utils/index.js";

export default {
  name: "HomePage",
  props: ["useremail"],
  
  data() {
    return {
      message: "",
      query: "",
      videos: [], 
      yt_videos: [], 
      sp_videos: [], 
      loading: { local: false, youtube: false, spotify: false },
      spotifyThumbnails: {}, // Store fetched Spotify thumbnails
    };
  },
  
  computed: {
    videoSources() {
      return {
        "Local": this.videos,
        "YouTube": this.yt_videos,
        "Spotify": this.sp_videos
      };
    }
  },

  watch: {
    query() {
      //this.fetchVideos(); 
    },
  },
  
  async mounted() {
    if (!this.useremail) {
      console.error("User email is undefined");
      return;
    }

    axios
      .get(`http://127.0.0.1:5000/api/${this.useremail}`)
      .then((response) => {
        this.message = response.data.message;
      })
      .catch((error) => console.error("API Error:", error));

    await this.fetchVideos(); 
    await this.fetchSpotifyThumbnails(); // Preload Spotify thumbnails
  },

  methods: {
    reset() {
      this.query = "";
      this.videos = [];
      this.yt_videos = [];
      this.sp_videos = [];
      this.spotifyThumbnails = {};
    },

    // Fetch Local Server Videos
    async fetchVideos() {
      this.loading.local = true;

      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/songs/${this.useremail}?search=${this.query}`);
        console.log(response.data);
        this.videos = response.data.songs || [];
      } catch (error) {
        console.error("API Error:", error);
      } finally {
        this.loading.local = false;
      }
    },

    async fetchSpotifyThumbnails() {
      for (const video of this.sp_videos) {
        if (!this.spotifyThumbnails[video.url]) {
          this.spotifyThumbnails[video.url] = await getSpotifyThumbnail(video.url);
        }
      }
    },

    async searchYouTube(retries = 20, interval = 3000) {
      this.pollServiceResults("youtube", retries, interval);
    },

    async searchSpotify(retries = 20, interval = 3000) {
      this.pollServiceResults("spotify", retries, interval);
    },

    async searchAll() {
      await this.fetchVideos();       // Search local database
      await this.searchYouTube();     // Search YouTube
      await this.searchSpotify();     // Search Spotify
    },

    async pollServiceResults(service, retries = 20, interval = 3000) {
      console.log(`Polling ${service} results for:`, this.query);
      const urls = {
        youtube: `http://127.0.0.1:5000/api/songs/pol/yt/${this.useremail}?search=${encodeURIComponent(this.query)}`,
        spotify: `http://127.0.0.1:5000/api/songs/pol/sp/${this.useremail}?search=${encodeURIComponent(this.query)}`
      };

      const url = urls[service];
      if (!url) {
        console.error(`Unknown service: ${service}`);
        return;
      }

      this.loading[service] = true;

      const poll = async () => {
        try {
          const response = await axios.get(url);

          if (response.status !== 200) {
            console.error(`${service} server responded with status: ${response.status}`);
            throw new Error(`${service} Error: ${response.statusText}`);
          }

          const data = response.data;

          if (data.success) {
            console.log(`${service} Results:`, data.songs);
            if (service === "youtube") {
              this.yt_videos = data.songs;
            } else {
              this.sp_videos = data.songs;
              await this.fetchSpotifyThumbnails(); // Preload Spotify thumbnails
            }
            this.loading[service] = false;
            return;
          } else {
            console.log(`${service} Results not ready yet...`);
          }
        } catch (error) {
          console.error(`${service} Polling error:`, error);
        }

        retries--;
        if (retries > 0) {
          setTimeout(poll, interval);
        } else {
          console.error(`${service} Polling failed after maximum retries.`);
          this.loading[service] = false;
        }
      };

      poll();
    },

    playVideo(video) {
      console.log("Playing video:", video.url);
      if (video.sourceType === 'youtube') {
        window.open(video.preservedSrc, '_blank');
      } else {
        let videoPlayer = new Audio(video.preservedSrc);
        videoPlayer.play();
      }
    },

    likeVideo(video) {
      console.log('Like video:', video.song_id);
      video.liked = !video.liked;
    },

    handleChat(video) {
      console.log('Chat about video:', video.song_id);
      this.$emit('open-chat', video.song_id);
    },

    convertSeconds(seconds) {
      if (seconds < 0) {
        return "0s";
      }
  
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const remainingSeconds = seconds % 60;
  
      if (hours > 0) {
        return `${hours}h ${minutes}m ${Math.ceil(remainingSeconds)}s`;
      } else if (minutes > 0) {
        return `${minutes}m ${Math.ceil(remainingSeconds)}s`;
      } else {
        return `${Math.ceil(remainingSeconds)}s`;
      }
    },

    getThumbnail(video, service) {
      if (service === "YouTube") {
        return getYouTubeThumbnails(video.url);
      } else if (service === "Spotify") {
        return this.spotifyThumbnails[video.url] || video.thumbnail;
      }
      return video.thumbnail;
    },

    timeAgo,
    getYouTubeThumbnails,
  },
};
</script>


<style scoped>

#videosContainer {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); /* Responsive grid */
    gap: 10px;
    width: 100%;
    box-sizing: border-box;
    padding: 10px;
    grid-auto-rows: min-content; /* Ensures height matches content */
}

/* Default Video Card Styling */
.video-card {
  background: #d9d7d7;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
    padding: 10px;
    border-radius: 5px;
    transition: all 0.3s ease-in-out;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: auto; /* Ensures height is based on content */
}

/* Responsive Layout: 3 Columns for Larger Screens */
@media (min-width: 1024px) {
    #videosContainer {
        grid-template-columns: repeat(3, 1fr); /* Exactly 3 columns on large screens */
    }
}

/* Responsive Layout: 2 Columns for Tablets */
@media (max-width: 1023px) {
    #videosContainer {
        grid-template-columns: repeat(2, 1fr); /* 2 columns on medium screens */
    }
}

/* Responsive Layout: 1 Column for Mobile */
@media (max-width: 600px) {
    #videosContainer {
        grid-template-columns: repeat(1, 1fr); /* 1 column on small screens */
    }
}


/* Make sure video elements fit inside the card */
.video-card video {
    width: 100%;
    height: auto;
    border-radius: 5px;
}


.video-card img{
  min-width: 200px;
  min-height: 75px;
  background-color: rgb(78, 77, 77);
  height: auto;
  width: 200px;
  border-radius: 10px;
}
.video-card.dark-mode{
  background-color: var(--dark-foreground);
}


.video-info-holder {
  display: flex;
  justify-content: space-between;
}
.video-Meta-info-holder{
  display: flex;
  align-items: center;
  gap: 5px;

}
#spinner-container{
  position: absolute;
  right: 0;
  background-color: aqua;
}
#homepage-header{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding:0 10px;
  position: sticky;
  top: 0;
  background-color: rgb(216, 210, 210);
  z-index: 99;
  width: 100%;
  box-sizing: border-box;
}
</style>
