<template>
    <div id="youSectionB" :fullViewMode="fullViewMode">
      <button id="FullviewCards" @click="toggleViewMode">
        <ion-icon name="map"></ion-icon>
      </button>
      <div id="playingCardContainer" >
        <div v-for="(song, index) in songs" :key="index" class="playingCard card" :class="{ 'viewPlayer': viewPlayersMode }">
          <div class="playingSongDateinfo">{{ song.date }}</div>
          <div class="playingSongLylics">
            <p>{{ song.lyrics }}</p>
          </div>
          <div class="playingSongArtwork">
            <div class="arc-border"></div>
            <img :src="song.image" alt="Artist Image">
            <div>
              <div class="playingSongArtist">{{ song.artist }}</div>
              <div class="playingSongTitle">{{ song.title }}</div>
            </div>
          </div>
          <div class="somethingIntesting">
            <div class="somethingIntestingTitle">Artist</div>
            <div class="cardPlayerControl">
              <i class="fa fa-step-backward"></i>
              <i :class="song.isPlaying ? 'fa fa-pause' : 'fa fa-play'" @click="togglePlay(index)"></i>
              <i class="fa fa-step-forward"></i>
            </div>
            <div class="playingCardTimer">{{ song.duration }}</div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        fullViewMode: false,
        viewPlayersMode: false,

        songs: [
          {
            date: "1st January 2024",
            lyrics: "New year, new dreams, a fresh start awaits.",
            image: "../static/thumbnails/song1.jpg",
            artist: "John Doe",
            title: "New Beginnings",
            duration: "2:45",
            isPlaying: false,
          },
          {
            date: "14th February 2024",
            lyrics: "Love is in the air, hearts beating in sync.",
            image: "../static/thumbnails/song2.jpg",
            artist: "Emily Heart",
            title: "Valentine's Serenade",
            duration: "3:12",
            isPlaying: false
          },
          {
            date: "4th March 2024",
            lyrics: "Spring blooms, bringing melodies of joy.",
            image: "../static/thumbnails/song3.jpg",
            artist: "Liam Spring",
            title: "Blossom Tunes",
            duration: "4:00",
            isPlaying: true
          },
          {
            date: "1st January 2024",
            lyrics: "New year, new dreams, a fresh start awaits.",
            image: "../static/thumbnails/song1.jpg",
            artist: "John Doe",
            title: "New Beginnings",
            duration: "2:45",
            isPlaying: false,
          },
          {
            date: "14th February 2024",
            lyrics: "Love is in the air, hearts beating in sync.",
            image: "../static/thumbnails/song2.jpg",
            artist: "Emily Heart",
            title: "Valentine's Serenade",
            duration: "3:12",
            isPlaying: false
          },
          {
            date: "4th March 2024",
            lyrics: "Spring blooms, bringing melodies of joy.",
            image: "../static/thumbnails/song3.jpg",
            artist: "Liam Spring",
            title: "Blossom Tunes",
            duration: "4:00",
            isPlaying: true
          },
          {
            date: "1st January 2024",
            lyrics: "New year, new dreams, a fresh start awaits.",
            image: "../static/thumbnails/song1.jpg",
            artist: "John Doe",
            title: "New Beginnings",
            duration: "2:45",
            isPlaying: false,
          },
          {
            date: "14th February 2024",
            lyrics: "Love is in the air, hearts beating in sync.",
            image: "../static/thumbnails/song2.jpg",
            artist: "Emily Heart",
            title: "Valentine's Serenade",
            duration: "3:12",
            isPlaying: false
          },
          {
            date: "4th March 2024",
            lyrics: "Spring blooms, bringing melodies of joy.",
            image: "../static/thumbnails/song3.jpg",
            artist: "Liam Spring",
            title: "Blossom Tunes",
            duration: "4:00",
            isPlaying: true
          }
        ]
      };
    },
    methods: {
      toggleViewMode() {
        this.viewPlayersMode = !this.viewPlayersMode;
        this.$emit('toggle-viewPlayersMode');
      },
      togglePlay(index) {
        this.songs[index].isPlaying = !this.songs[index].isPlaying;
      }
    }
  };
  </script>
  
  <style scoped>
/*song card*/
#youSectionB{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
    position: relative;
}
.activePlayingCard{
    box-shadow:inset 0px 5px 75px rgb(50, 94, 70) !important;
    border: 3px solid forestgreen !important;
    margin-top: -15px !important;
    margin-right: 70px !important;

}


#youSectionB #playingCardContainer {
    margin: auto;
    display: flex;
    flex-direction: row;
    padding: 40px 20px;
    position: relative;
    height: 500px; /* Adjust as needed */
    overflow-x: auto;
    scroll-behavior: smooth;
    scroll-snap-type: x mandatory;
    overflow-y: hidden;
    background-color: transparent;
    width: 100%;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    border-radius: 12px;
    max-width: 900px;
}
#youSectionB #playingCardContainer::-webkit-scrollbar{
    display: none;
}
.viewPlayer:nth-child(n+2) {
    margin-left: -100px; /* Overlapping effect */
}
.viewPlayer{
    position: relative !important;
    left: 35% !important;
    box-shadow: -15px 0px 55px black !important;
}
.playingCard {
    border-radius: 10px;
    height: 100%;
    width: 100%;
    min-width: 250px;
    padding: 20px 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.5s ease-in-out;
    cursor: pointer;
    border: 3px solid transparent;
    position: absolute;
    left: 0%;
    z-index: 90;
    box-sizing: border-box;
}
.playingCard:hover{
    box-shadow: 0px 0px 95px rgb(0, 0, 0) !important;
}
.playingCard:hover .arc-border {
    transform: rotate(360deg);
}

.playingCard .playingSongDateinfo{
    font-size: 14px;
    color: rgb(80, 78, 78);
    font-weight: bold;
}

.playingCard .playingSongLylics {
    color: rgb(145, 145, 145);
    font-weight: bolder;
    background-color: rgba(35, 74, 35, 0.113);
    padding: 5px;
    border-radius: 5px;
    height: 200px;
    overflow: hidden;
    line-height: 1.5; /* Normalized for better spacing */
    word-spacing: 10px; /* Adjusting spacing if needed */
    margin: auto;
    text-align: center;
}
.playingCard .playingSongLylics > p{
    font-size: 1em!important; /* Adjusted for readability */
}


.playingCard .playingSongArtwork {
    position: relative;
    display: flex;
    align-items: center;
    gap: 10px;
    width: fit-content;
    background-color: transparent;
    padding: 10px;
    transition: 0.5s ease;
}

.arc-border {
    margin-left: 5px;
    margin-bottom: 5px;
    position: absolute;
    width: 70px;
    height: 70px;
    bottom: 0px;
    left: 0%;
    border-radius: 5px 5px 50px 50px;
    background: linear-gradient(to right, red, orange, purple, red);
    transition: all 0.5s ease-in-out; 
    clip-path: inset(50% 0px 0px 0px); /* Hides the right half */
    z-index: 90;

}

.playingCard .playingSongArtwork:hover .arc-border {
    transform: rotate(360deg);

}

.playingCard .playingSongArtwork img {
    background-color: rgb(104, 104, 104);
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 50%;
    position: relative;
    display: block;
    z-index: 95;
}

.playingCard .playingSongArtist {
    font-size: 12px;
    color: gray;
    font-weight: bold;
}

.playingCard .playingSongTitle {
    font-size: 16px;
    font-weight: bold;
    color: white;
}

.playingCard .somethingIntesting{
    margin-top: 20px;
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 2px 0;
}

.playingCard .somethingIntestingTitle{
    border: 2px solid gray;
    padding:3px 15px;
    border-radius:  10px;
    width: fit-content;
}
.playingCard .cardPlayerControl{
    margin: auto;
    display: flex;
    align-items: center;
    gap: 10px;
}
.playingCard .cardPlayerControl > i{
    cursor: pointer;
    transition: all 0.9s ease;
}
.playingCard .cardPlayerControl > i:hover {
    cursor: pointer;
    color: aqua;
}

.playingCard .cardPlayerControl .fa-pause{
    font-size: 20px;
    color: forestgreen;
}

.playingCard .playingCardTimer{
    font-size: 14px;
    font-weight: bold;
}



#FullviewCards{
    position: absolute;
    left: 0;
    top: 0;
    z-index: 98;
}

@media (max-width:668px) {
    #youMain{
        flex-direction: column !important;
        width: 100% !important;
    }
    #youSectionC{
        display:none !important;
    }
    #youSectionA{
        width: 100% !important;
    }
    #youSectionB{
        display: flex !important;
        height: 1050px !important;
        transform: scale(0.6);
        position: fixed;
        bottom: 0;
    }
}

@media (max-width:480px) {
    #youMain{
        flex-direction: column !important;
        width: 100% !important;
    }
    #youSectionA{
        width: 100% !important;
    }
    #playingCardContainer{
        width: 100% !important;
        height: 100vh;
        background-color: rgba(255, 0, 0, 0.857);
    }
    #youSectionB{
        display: flex !important;
        width: 160% !important;
        height: 90vh !important;
        position: fixed;
        bottom: 0;
        left: 0 !important;
        margin-left: -30% !important;

    }
    #youSectionC{
        display: none ;
    }
}
</style>