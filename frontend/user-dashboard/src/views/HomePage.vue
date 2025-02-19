<template> 
  <div class="MainContainer">
    <div id="homepage-header">
      <div>
      <h3>Videos</h3>
      <p>{{ message }}</p>
    </div>
    <div v-if="loading" class="spinner-container">
      <div class="loader">
        <p>Loading...</p>
      </div> 
    </div>

    <div>
      <h2>Video Filter</h2>
      <input type="text" placeholder="Filter Search" v-model="query" />
      <button @click="reset">Clear</button>
    </div>

    </div>
    <div >
      <div v-if="videos.length" id="videosContainer">
        <div v-for="video in videos" :key="video.song_id" class="video-card">
          <div @click="playVideo(video)">
            <img :src="video.thumbnail" alt="Video Thumbnail" />
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
      <p v-else>No videos found</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { timeAgo } from '@/utils/index';


export default {
  name: "HomePage",
  props: ["useremail"],
  
  data() {
    return {
      message: "",
      query: "",
      videos: [], 
      loading: false, 
    };
  },
  
  watch: {
    query() {
      this.fetchVideos(); 
    },
  },
  
  mounted() {
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

    this.fetchVideos(); 
  },

  methods: {
    reset() {
      this.query = "";
    },

    fetchVideos() {
      this.loading = true; 

      axios
    .get(`http://127.0.0.1:5000/api/songs/${this.useremail}?search=${this.query}`)
    .then((response) => {
      console.log(response.data); // Add this line to log the response
      this.videos = response.data.songs || [];
    })
    .catch((error) => {
      console.error("API Error:", error);
    })
    .finally(() => {
      this.loading = false;
    });

    },

    playVideo(video) {
      console.log("Playing video:", video.url);
      // Play the video using iframe for YouTube or a local player for local videos
      if (video.sourceType === 'youtube') {
        window.open(video.preservedSrc, '_blank');
      } else {
        let videoPlayer = new Audio(video.preservedSrc); // Or use a video player element for better control
        videoPlayer.play();
      }
    },

    likeVideo(video) {
      console.log('Like video:', video.song_id);
      // Handle like/unlike functionality here
      video.liked = !video.liked;
      // Optionally, you could make an API call to update the like status
    },

    handleChat(video) {
      console.log('Chat about video:', video.song_id);
      // Trigger chat UI for the given video
      this.$emit('open-chat', video.song_id);
    },

    timeAgo,

    convertSeconds(seconds) {
    if (seconds < 0) {
      return 0.0;
    }
  
    const hours = Math.floor(seconds / 3600); // Calculate the number of hours
    const minutes = Math.floor((seconds % 3600) / 60); // Calculate remaining minutes
    const remainingSeconds = seconds % 60; // Calculate remaining seconds
  
    // Format the result as HH:MM:SS or MM:SS
    if (hours > 0) {
      return `${hours}h ${minutes}m ${Math.ceil(remainingSeconds)}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${Math.ceil(remainingSeconds)}s`;
    } else {
      return `${ Math.ceil(remainingSeconds)}s`;
    }
  },
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
