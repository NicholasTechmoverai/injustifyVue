<template>
    <div id="youSectionC" class="card common-scrollbar">
      <div id="sectioncmoststreamedSongs">
        <div id="moststreamedSongsHeader" class="card"><span>your top songs</span><span>Best</span> <button><ion-icon name="options-outline"></ion-icon></button></div>
        <div id="moststreamedSongsBody">
          <div v-for="(song, index) in songs" :key="index" class="song-item" :song_id="song.id">
            <img :src="song.thumbnail" alt="Song thumbnail">
            <div class="songTitle">{{ song.title }}</div>
            <div class="songTrendinfo">{{ song.rank }}</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import { BASE_URL } from "@/utils";

  export default {
    data() {
      return {
        songs: [], 

      };
    },
    mounted() {
        this.fetchVideos(); 

  },
  methods:{
    fetchVideos() {
        this.loading = true; 

        axios
        .get(`${BASE_URL}/api/songs/pl/ple8dd2fc4`)
        .then((response) => {
        console.log("playlist::",response.data.songs); // Add this line to log the response
        this.songs = response.data.songs;
        })
        .catch((error) => {
        console.error("API Error:", error);
        })
        .finally(() => {
        this.loading = false;
        });

        },
  }
  };
  </script>