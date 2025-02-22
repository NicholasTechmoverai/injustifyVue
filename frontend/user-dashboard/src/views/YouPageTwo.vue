<template>
  <div id="youSectionB" :class="{ fullViewMode: fullViewMode }">
    <button id="FullviewCards" @click="toggleViewMode">
      <ion-icon name="map"></ion-icon>
    </button>

    <!-- Hidden Audio Player -->
    <audio ref="audioPlayer" :src="currentSongUrl" @ended="onSongEnd"></audio>
  
    <div id="playingCardContainer">
       <div v-if="loading">loading...</div>
      <div 
        v-for="(song, index) in availableSongs" 
        :key="song.song_id" 
        class="playingCard card" 
        :class="{ 'viewPlayer': viewPlayersMode, 'activePlayingCard': song.isPlaying, 'PlayerModeActivePlayingCard': viewPlayersMode && song.isPlaying }"
      >
        <div class="playingSongDateinfo">{{ song.song_id }}</div>
        <div class="playingSongArtwork">
          <img :src="song.thumbnail" alt="Artist Image">
          <div>
            <div class="playingSongArtist">{{ song.artist }}</div>
            <div class="playingSongTitle">{{ song.title }}</div>
          </div>
        </div>
        <div class="somethingIntesting">
          <div class="somethingIntestingTitle">Artist</div>
          <div class="cardPlayerControl">
            <i class="fa fa-step-backward" @click="playPrevious"></i>
            <i 
              :class="song.isPlaying ? 'fa fa-pause' : 'fa fa-play'" 
              @click="togglePlay(index)"
            ></i>
            <i class="fa fa-step-forward" @click="playNext"></i>
          </div>
          <div class="playingCardTimer">{{ song.stype }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, watch, watchEffect, nextTick, onUnmounted } from "vue";
import { useUserStore } from "@/store/index.js";
import { BASE_URL } from "@/utils";
import axios from "axios";
import socket from "@/services/websocket"; // Ensure WebSocket is imported correctly

export default {
  props: {
    songs: Array, // Optional array of songs
    songUrl: String, // Optional single song URL
  },
  setup(props, { emit }) {
    const userStore = useUserStore();
    const fullViewMode = ref(false);
    const viewPlayersMode = ref(false);
    const currentSongUrl = ref("");
    const audioPlayer = ref(null);
    const currentIndex = ref(0);
    const userId = computed(() => userStore.userId);
    let viewUpdateInterval = null;
    const loading = ref(false);

    // Fetch song if only songUrl is provided
    watch(
      () => props.songUrl,
      async (newSongUrl) => {
        if (newSongUrl) {
          await fetchVideoForPropUrl(newSongUrl);
        }
      },
      { immediate: true }
    );

    // Compute available songs from props or store
    const availableSongs = computed(() => {
      if (props.songs?.length) {
        return props.songs.map((song) => ({ ...song, isPlaying: false }));
      } else if (userStore.songs?.length) {
        return userStore.songs.flat().map((song) => ({ ...song, isPlaying: false }));
      }
      return [];
    });

    // Watch for changes in availableSongs and set initial values
    watchEffect(() => {
      if (availableSongs.value.length > 0) {
        if (currentIndex.value >= availableSongs.value.length) {
          currentIndex.value = 0;
        }
        currentSongUrl.value = `${BASE_URL}/api/stream/${availableSongs.value[currentIndex.value].url}`;
      }
    });

    // Toggle view mode
    const toggleViewMode = () => {
      viewPlayersMode.value = !viewPlayersMode.value;
      emit("toggle-viewPlayersMode");
    };

    // Start sending playback progress to server
    const startSendingProgress = (player) => {
      if (viewUpdateInterval) clearInterval(viewUpdateInterval);

      viewUpdateInterval = setInterval(() => {
        if (!socket || !socket.emit) {
          console.error("Socket is undefined or not ready!");
          return;
        }
        if (player && player.currentTime > 0 && player.duration > 0) {
          let progress = (player.currentTime / player.duration) * 100;
          socket.emit("updateViewCount", {
            userId: userId.value,
            songId: availableSongs.value[currentIndex.value]?.song_id,
            progress: progress,
          });
        }
      }, 5000);
    };

    // Play/Pause functionality
    const togglePlay = async (index) => {
      const song = availableSongs.value[index];
      if (!song) return;

      const player = audioPlayer.value;
      if (!player) return;

      if (song.isPlaying) {
        player.pause();
        song.isPlaying = false;
        clearInterval(viewUpdateInterval);
      } else {
        availableSongs.value.forEach((s, i) => (s.isPlaying = i === index));
        currentIndex.value = index;
        currentSongUrl.value = `${BASE_URL}/api/stream/${song.url}`;

        await nextTick(); // Ensure UI updates before playing

        player.load();
        player.play()
          .then(() => startSendingProgress(player))
          .catch((err) => console.error("Playback error:", err));
      }
    };

    // Handle song end event
    const onSongEnd = () => {
      clearInterval(viewUpdateInterval);
      socket.emit("updateViewCount", {
        userId: userId.value,
        songId: availableSongs.value[currentIndex.value]?.song_id,
        progress: 100.0,
      });
      playNext();
    };

    // Play next song
    const playNext = () => {
      clearInterval(viewUpdateInterval);
      if (currentIndex.value < availableSongs.value.length - 1) {
        togglePlay(++currentIndex.value);
      }
    };

    // Play previous song
    const playPrevious = () => {
      clearInterval(viewUpdateInterval);
      if (currentIndex.value > 0) {
        togglePlay(--currentIndex.value);
      }
    };

    // Fetch song from API using song URL
    const fetchVideoForPropUrl = async (id) => {
      loading.value = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/songs/song/info/${id}`);
        console.log("Single Song:", response.data.songs || {});

        const songs = Array.isArray(response.data.songs) ? response.data.songs : [response.data.songs];

        userStore.setPlaylistSongs(songs);
      } catch (error) {
        console.error("API Error:", error);
      } finally {
        loading.value = false;
      }
    };

    // Cleanup intervals on component unmount
    onUnmounted(() => {
      if (viewUpdateInterval) clearInterval(viewUpdateInterval);
    });

    return {
      availableSongs,
      fullViewMode,
      viewPlayersMode,
      currentSongUrl,
      audioPlayer,
      toggleViewMode,
      togglePlay,
      onSongEnd,
      playNext,
      playPrevious,
    };
  },
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

.PlayerModeActivePlayingCard{
  box-shadow:inset 0px 0px 75px rgb(50, 94, 70) !important;
    border: 3px solid forestgreen !important;
    margin-top: -15px !important;
    margin-right: 70px !important;
    z-index: 90 !important;
}


.activePlayingCard{
    box-shadow:inset 0px 0px 5px rgb(1, 201, 91) !important;
    margin-right: 70px !important;
    z-index: 91 !important;

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
    left: 0% !important;
    box-shadow: -15px 0px 55px black !important;
    z-index: 90;
    margin-left: 0;
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
    margin-right: 50px !important;
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
    text-wrap: wrap;
    word-break: break-all;
    overflow: hidden;
    width: 100%;
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