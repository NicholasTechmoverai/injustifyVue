<template>
  <div id="youSectionB" :class="{ fullViewMode: fullViewMode }">
    <button id="FullviewCards" @click="toggleViewMode">
      <ion-icon name="map"></ion-icon>
    </button>

    <!-- Hidden Audio Player -->
    <audio
      ref="audioPlayer"
      :src="currentSongUrl"
      @ended="onSongEnd"
      @timeupdate="updateProgress"
    ></audio>

    <div
      id="playingCardContainer"
      :class="{ 'darktheme-2': isDarkMode }"
      :style="extend_card ? { height: '350px', position: 'absolute', bottom: '0' } : {}"
    >
      <div v-if="loading">loading...</div>
      <div
        v-for="(song, index) in availableSongs"
        :key="song.song_id"
        @click="scrollToview($event)"
        class="playingCard card"
        :class="{
          viewPlayer: viewPlayersMode,
          activePlayingCard: song.isPlaying,
          PlayerModeActivePlayingCard: viewPlayersMode && song.isPlaying,
          'darktheme-card': isDarkMode,
        }"
      >
        <div class="playingSongDateinfo">{{ song.song_id }}</div>

        <div class="PlayingAnimation" v-if="showAnimate">
          <transition name="fade" mode="out-in" v-if="song.isPlaying">
            <img
              id="animation_gif"
              v-if="PlayingAnimation_file"
              :src="PlayingAnimation_file"
              :key="PlayingAnimation_file"
            />
          </transition>
        </div>
        <div class="playingSongArtwork">
          {{}}
          <img :src="song.thumbnail" alt="Artist Image" />
          <div>
            <div class="playingSongArtist">{{ song.artist }}</div>
            <div class="playingSongTitle">{{ song.title }}</div>
          </div>
        </div>

        <div v-if="song.isPlaying">
          <!-- Progress Bar & Timer -->
          <div class="progress-container" @click="seek">
            <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
          </div>
          <div class="time-info">
            {{ formattedCurrentTime }} / {{ formattedDuration }}
          </div>
        </div>
        <div class="somethingIntesting">
          <div class="somethingIntestingTitle">Artist</div>
          <div v-if="song.isPlaying" class="out_of_index">
            {{ currentIndex + 1 }}/{{ availableSongs.length }}
          </div>
          <div class="cardPlayerControl">
            <i v-if="song.isPlaying" class="fa fa-random" @click="toggleShuffle"></i>
            <i
              v-if="song.isPlaying"
              class="fa fa-step-backward"
              @click="playPrevious"
            ></i>
            <i
              :class="song.isPlaying ? 'fa fa-pause' : 'fa fa-play'"
              @click="togglePlay(index)"
            ></i>
            <i v-if="song.isPlaying" class="fa fa-step-forward" @click="playNext"></i>
            <i v-if="song.isPlaying" class="fa fa-repeat" @click="toggleLoop"></i>
          </div>
          <div class="playingCardTimer">{{ song.stype }}</div>
          <div class="volumeToogle" v-if="song.isPlaying">
            <ion-icon name="volume-high-outline"></ion-icon>
            <input
              class="Volume-High-Outline"
              type="range"
              min="0"
              max="1"
              step="0.1"
              v-model="volume"
              @input="updateVolume"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, watch, nextTick, onUnmounted, onMounted } from "vue";
import { useUserStore } from "@/store/index.js";
import { BASE_URL } from "@/utils";
import axios from "axios";
import socket from "@/services/websocket";

export default {
  props: {
    playlist_id: String,
    songs: Array,
    songUrl: String,
    clickedSongId: String,
  },
  setup(props, { emit }) {
    const userStore = useUserStore();
    const fullViewMode = ref(false);
    const viewPlayersMode = ref(false);
    const currentSongUrl = ref("");
    const audioPlayer = ref(null);
    const currentIndex = ref(0);
    const isPlaying = ref(false);
    const loading = ref(false);
    const isShuffle = ref(false);
    const isLoop = ref(false);
    const volume = ref(1);
    const progressPercentage = ref(0);
    const currentTime = ref(0);
    const duration = ref(0);
    let viewUpdateInterval = null;
    const formattedCurrentTime = computed(() => formatTime(currentTime.value));
    const formattedDuration = computed(() => formatTime(duration.value));
    const playlist_id = computed(() => props.playlist_id || userStore.activePlaylistId);
    const availableSongs = ref([]);
    const playlist_name = ref("");
    const PlayingAnimation_file = ref("");
    const userId = computed(() => userStore.userId);
    const isDarkMode = computed(() => userStore.isdarkmode);
    let intervalId = null;
    const showAnimate = ref(true); //wheather show the animate cards
    const extend_card = ref(false); //wheather extend the size of the animate cards(for mobile phones)
    const requestCards = ref(true); //wheather request animatios for playing cards

    // Watch for song URL changes
    watch(
      () => props.songUrl,
      async (newSongUrl) => {
        if (newSongUrl) {
          await fetchVideoForPropUrl(newSongUrl);
        }
      },
      { immediate: true }
    );

    // Set the current song URL when the list changes
    watch(availableSongs, () => {
      if (availableSongs.value.length > 0) {
        currentIndex.value = Math.min(
          currentIndex.value,
          availableSongs.value.length - 1
        );
        currentSongUrl.value = getSongUrl(currentIndex.value);
      }
    });

    // Toggle player view mode
    const toggleViewMode = () => {
      viewPlayersMode.value = !viewPlayersMode.value;
      emit("toggle-viewPlayersMode");
      if (window.innerWidth < 680) {
        extend_card.value = !extend_card.value;
      }
    };

    // Generate the song URL
    const getSongUrl = (index) =>
      `${BASE_URL}/api/stream/${availableSongs.value[index]?.url}`;

    const fetchVideos = async () => {
      if (!playlist_id.value) {
        console.warn("Playlist ID is missing.");
        availableSongs.value = [];
        playlist_name.value = "";
        return;
      }

      loading.value = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/songs/pl/${playlist_id.value}`);
        //console.log("Playlist Songs:", response.data.songs?.songs || []);

        availableSongs.value = response.data.songs?.songs || [];
        playlist_name.value = response.data.songs?.playlist_name || "Unknown Playlist";

        //store the songs in userstore
        userStore.setPlaylistSongs(availableSongs.value, playlist_name.value);
      } catch (error) {
        console.error("API Error:", error);
        availableSongs.value = [];
      } finally {
        loading.value = false;
      }
    };

    watch(playlist_id, fetchVideos, { immediate: true });

    // Play or pause a song
    const togglePlay = async (index) => {
      const song = availableSongs.value[index];
      if (!song) return;

      const player = audioPlayer.value;
      if (!player) return;

      if (index !== currentIndex.value) {
        // Switching to a new song
        availableSongs.value.forEach((s, i) => (s.isPlaying = i === index));
        currentIndex.value = index;
        currentSongUrl.value = getSongUrl(index);
        isPlaying.value = true;
        await nextTick();
        player.load();
        requestNextImage();
      } else {
        // Toggle play/pause for the current song
        isPlaying.value = !isPlaying.value;
        requestCards.value = !requestCards.value;
        if (requestCards.value) {
          requestNextImage();
          startInterval();
        } else {
          PlayingAnimation_file.value = new URL(
            "../assets/injustify.png",
            import.meta.url
          ).href;
          clearInterval(intervalId); // Stop interval when paused
        }
      }

      if (isPlaying.value) {
        player
          .play()
          .then(() => startSendingProgress(player))
          .catch((err) => console.error("Playback error:", err));
      } else {
        player.pause();
        clearInterval(viewUpdateInterval);
      }
    };

    // Handle song ending
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
      let nextIndex = (currentIndex.value + 1) % availableSongs.value.length;
      togglePlay(nextIndex);
    };

    // Play previous song
    const playPrevious = () => {
      let prevIndex =
        (currentIndex.value - 1 + availableSongs.value.length) %
        availableSongs.value.length;
      togglePlay(prevIndex);
    };

    // Change song index based on ID
    const changeIndexBySongID = (songId) => {
      const newIndex = availableSongs.value.findIndex((s) => s.song_id === songId);
      if (newIndex !== -1) togglePlay(newIndex);
    };

    // Auto-scroll to selected song
    const scrollToview = (event) => {
      event.currentTarget.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "center",
      });
    };

    const toggleShuffle = () => (isShuffle.value = !isShuffle.value);
    const toggleLoop = () => (isLoop.value = !isLoop.value);

    const updateProgress = () => {
      if (audioPlayer.value) {
        currentTime.value = audioPlayer.value.currentTime;
        duration.value = audioPlayer.value.duration;
        progressPercentage.value = (currentTime.value / duration.value) * 100;
      }
    };

    const seek = (event) => {
      if (!audioPlayer.value || !duration.value) return;
      const progressBar = event.currentTarget;
      const clickPosition = event.offsetX / progressBar.clientWidth;
      audioPlayer.value.currentTime = clickPosition * duration.value;
    };

    const updateVolume = () => {
      if (audioPlayer.value) audioPlayer.value.volume = volume.value;
    };

    const formatTime = (seconds) => {
      const minutes = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${minutes}:${secs < 10 ? "0" : ""}${secs}`;
    };

    // Watch for clicked song ID change
    watch(
      () => props.clickedSongId,
      (newSongId) => {
        if (newSongId) changeIndexBySongID(newSongId);
      }
    );

    // Fetch song details from API
    const fetchVideoForPropUrl = async (id) => {
      loading.value = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/songs/song/info/${id}`);
        const songs = Array.isArray(response.data.songs)
          ? response.data.songs
          : [response.data.songs];
        userStore.setPlaylistSongs(songs);
      } catch (error) {
        console.error("API Error:", error);
      } finally {
        loading.value = false;
      }
    };

    // Send playback progress updates
    const startSendingProgress = (player) => {
      if (viewUpdateInterval) clearInterval(viewUpdateInterval);
      viewUpdateInterval = setInterval(() => {
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

    const handle_showAnimate = () => {
      if (window.innerWidth < 680) {
        if (extend_card.value) {
          showAnimate.value = true;
        } else if (!extend_card.value) {
          showAnimate.value = false;
        }
      } else {
        showAnimate.value = true;
        extend_card.value = true;
      }
    };

    socket.on("animatesd_player", (data) => {
      if (data && data.image) {
        PlayingAnimation_file.value = data.image;
      } else {
        console.error("Received data does not contain an image:", data);
      }
    });
    const requestNextImage = () => {
      socket.emit("request_image");
    };
    const startInterval = () => {
      clearInterval(intervalId); // Clear any existing interval
      intervalId = setInterval(requestNextImage, 3000);
    };

    onMounted(() => {
      if (requestCards.value) {
        startInterval();
      }
    });

    onUnmounted(() => {
      clearInterval(intervalId); // Clean up interval on component unmount
    });
    return {
      availableSongs,
      fullViewMode,
      viewPlayersMode,
      currentSongUrl,
      currentIndex,
      audioPlayer,
      toggleViewMode,
      togglePlay,
      onSongEnd,
      playNext,
      playPrevious,
      scrollToview,
      isDarkMode,
      progressPercentage,
      formattedCurrentTime,
      formattedDuration,
      toggleShuffle,
      toggleLoop,
      seek,
      updateProgress,
      volume,
      updateVolume,
      PlayingAnimation_file,
      requestNextImage,
      intervalId,
      loading,
      showAnimate,
      extend_card,
      handle_showAnimate,
      requestCards,
    };
  },
};
</script>

<style scoped>
.out_of_index {
  font-size: 12px;
  padding: 0px 5px;
  color: rgb(172, 168, 168);
}
.progress-container {
  width: 100%;
  height: 5px;
  background: #44444453;
  border-radius: 5px;
  position: relative;
  cursor: pointer;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(to right, #036db9d5, #1bca01b4);
  width: 0%;
  border-radius: 5px;
  transition: width 0.3s ease-in-out;
}
.time-info {
  font-size: 10px;
  margin-bottom: 10px;
}
.volumeToogle {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
}
.volumeToogle:hover .Volume-High-Outline {
  display: flex;
}

.Volume-High-Outline {
  display: none;
  transform: rotate(-90deg);
  position: absolute;
  top: -50%;
  left: -20%;
  width: 50px;
  height: 5px;
  cursor: pointer;
}
.PlayingAnimation {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80%;
  height: 60%;
  overflow: hidden;
  animation: spin 2s linear infinite;
  margin: 0 auto;
  border-radius: 10px;
}

.PlayingAnimation img {
  width: 100%;
  height: auto;
  max-width: 100%;
  border-radius: 10px;
  transition: all 0.5s ease;
}

.progress-container:hover .progress-bar {
  background: linear-gradient(to right, #ff9800, #ffeb3b);
}

/*song card*/
#youSectionB {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  position: relative;
}

.PlayerModeActivePlayingCard {
  box-shadow: inset 0px 0px 75px rgb(50, 94, 70) !important;
  border: 3px solid forestgreen !important;
  margin-top: -15px !important;
  margin-right: 70px !important;
  z-index: 90 !important;
}

.activePlayingCard {
  animation: backgroundAnim 5s infinite alternate ease-in-out;
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
#youSectionB #playingCardContainer::-webkit-scrollbar {
  display: none;
}
.viewPlayer:nth-child(n + 2) {
  margin-left: -100px; /* Overlapping effect */
}
.viewPlayer {
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
  scroll-snap-align: center;
}
.playingCard:hover {
  box-shadow: 0px 0px 95px rgb(0, 0, 0) !important;
  margin-right: 50px !important;
}
.playingCard:hover .arc-border {
  transform: rotate(360deg);
}

.playingCard .playingSongDateinfo {
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
.playingCard .playingSongLylics > p {
  font-size: 1em !important;
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

.playingCard .somethingIntesting {
  margin-top: 20px;
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 2px 0;
}

.playingCard .somethingIntestingTitle {
  border: 2px solid gray;
  padding: 3px 15px;
  border-radius: 10px;
  width: fit-content;
}
.playingCard .cardPlayerControl {
  margin: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}
.playingCard .cardPlayerControl > i {
  cursor: pointer;
  transition: all 0.9s ease;
}
.playingCard .cardPlayerControl > i:hover {
  cursor: pointer;
  color: aqua;
}

.playingCard .cardPlayerControl .fa-pause {
  font-size: 20px;
  color: forestgreen;
}

.playingCard .playingCardTimer {
  font-size: 14px;
  font-weight: bold;
}

#FullviewCards {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 98;
}

.darktheme-2 {
  background: #2c2c2c;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
  color: #e7e7e7 !important;
}
.darktheme-card {
  background: #2c2c2c;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
  color: #e7e7e7 !important;
}
/* Vue Transition 
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1.5s ease-in-out, transform 1.5s ease-in-out;
}

.fade-enter-from {
  opacity: 0;
  transform: scale(0.7) translateY(20px); 
}

.fade-enter-to {
  opacity: 1;
  transform: scale(1.05) translateY(-5px); 
}

.fade-leave-from {
  opacity: 1;
  transform: scale(1); 
}

.fade-leave-to {
  opacity: 0;
  transform: scale(1.1) translateY(10px);
}
*/
/* Simple Fade Transition */
/* Ultra-Smooth Fade Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1.2s ease-in-out;
}

.fade-enter-from {
  opacity: 0.5;
}

.fade-enter-to {
  opacity: 1;
}

.fade-leave-from {
  opacity: 1;
}

.fade-leave-to {
  opacity: 0;
}

@media (max-width: 668px) {
  #youSectionB #playingCardContainer {
    height: 200px;
    width: 100%;
    padding: 10px;
  }
  .playingCard .somethingIntesting {
    margin-top: 0px;
  }
}
</style>
