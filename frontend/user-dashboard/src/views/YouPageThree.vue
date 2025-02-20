<template>
    <div id="youSectionC" class="card common-scrollbar">
      <div id="sectioncmoststreamedSongs">
        <div id="moststreamedSongsHeader" class="card"><span>playing</span><span>Best</span> <button><ion-icon name="options-outline"></ion-icon></button></div>
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

  export default {
    data() {
      return {
        songs: [
          { id: 1, thumbnail: '../static/thumbnails/@coldplay - Yellow (Lyrics)_njt (1).jpg', title: 'songA', rank: '#1' },
          { id: 2, thumbnail: '../static/thumbnails/@coldplay - Yellow (Lyrics)_njt (1).jpg', title: 'songA', rank: '#1' },
          { id: 3, thumbnail: '../static/thumbnails/@coldplay - Yellow (Lyrics)_njt (1).jpg', title: 'songA', rank: '#1' },
          { id: 4, thumbnail: '../static/thumbnails/@coldplay - Yellow (Lyrics)_njt (1).jpg', title: 'songA', rank: '#1' },
          { id: 5, thumbnail: '../static/thumbnails/@coldplay - Yellow (Lyrics)_njt (1).jpg', title: 'songA', rank: '#1' },
          { id: 6, thumbnail: '../static/thumbnails/@coldplay - Yellow (Lyrics)_njt (1).jpg', title: 'songA', rank: '#1' },
          { id: 7, thumbnail: '../static/thumbnails/@coldplay - Yellow (Lyrics)_njt (1).jpg', title: 'songA', rank: '#1' },
        ]
      };
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
  };
  </script>
  
<style scoped>
#youSectionC {
    height: 85vh;
    overflow-y: auto;
    position: relative;
}

#youSectionC #sectioncmoststreamedSongs {
    flex-direction: column;
    gap: 10px;
    padding: 3px 5px;
}

#youSectionC #moststreamedSongsHeader {
    font-weight: bold;
    position: sticky;
    top: 0;
}

#youSectionC #moststreamedSongsBody {
    gap: 15px;
}

#youSectionC #moststreamedSongsBody > .song-item {
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 15px;
    background: linear-gradient(to right,  
        gray 20%,  
        rgba(128,128,128,0.8) 40%,  
        rgba(128,128,128,0.5) 60%,  
        rgba(128,128,128,0.2) 80%,  
        rgba(128,128,128,0) 100%
    );
    margin: 5px 0;
    padding: 5px 10px;
    border-radius: 5px;
    width: 100%;
    min-height: 40px;
    box-sizing: border-box;
}

#youSectionC #moststreamedSongsBody > .song-item:hover {
    background: linear-gradient(to right,  
        rgba(128,128,128,0) 0%,  
        rgba(128,128,128,0.2) 20%,  
        rgba(128,128,128,0.5) 40%,  
        rgba(128,128,128,0.8) 60%,  
        gray 80%
    );
}

#youSectionC .song-item img {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 5px;
}

#youSectionC .songTitle {
    font-weight: bold;
    color: #fff;
}

#youSectionC .songTrendinfo {
    color: #aaa;
    font-size: 0.9em;
}

</style>