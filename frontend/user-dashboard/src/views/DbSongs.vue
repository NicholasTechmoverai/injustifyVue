<template>
    <div class="MainContainer">
      <div v-if="songs.length">
        <h3>Search Results for: "{{ searchQuery }}"</h3>
        <div v-for="song in songs" :key="song.song_id">
          <div class="song-card" @click="playsong(song.url)">
            <img :src="song.thumbnail" alt="Song Cover" />
            <div>
              <h4>{{ song.title }}</h4>
              <p>{{ song.artist }}</p>
            </div>
          </div>
        </div>
      </div>
      <p v-else>No songs found for "{{ searchQuery }}"</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "HomeSearch",
    data() {
      return {
        songs: [],
        searchQuery: this.$route.query.search || "", // Get search query from URL
      };
    },
  
    mounted() {
      if (!this.searchQuery) {
        console.error("Search query is undefined");
        return;
      }
  
      this.fetchSongs(); // Fetch songs when component is mounted
    },
  
    methods: {
      fetchSongs() {
        axios
          .get(`http://127.0.0.1:5000/api/songs/${this.$route.params.useremail}?search=${this.searchQuery}`)
          .then((response) => {
            this.songs = response.data.songs || [];
          })
          .catch((error) => console.error("API Error:", error));
      },
  
      playsong(url) {
        console.log("Playing song:", url);
        let audio = new Audio(url);
        audio.play();
      },
    },
  };
  </script>
  
  <style scoped>
  .song-card {
    width: 300px;
    height: 200px;
    border-radius: 10px;
    background-color: gray;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    gap: 5px;
    margin: 5px;
  }
  
  .song-card img {
    width: 100%;
    height: 70%;
    object-fit: cover;
  }
  </style>
  