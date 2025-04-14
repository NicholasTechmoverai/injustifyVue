<template>
  <div id="youSectionB" :class="{ fullViewMode: fullViewMode }">
    <button id="FullviewCards" @click="toggleViewMode">
      <ion-icon name="map"></ion-icon>
    </button>

    <!-- Hidden Audio Player -->
    <audio
      ref="audioPlayer"
      :src="currentSongUrl"
      @waiting="onWaiting"
      @canplay="onCanPlay"
      @ended="onSongEnd"
      @timeupdate="updateProgress"
      @loadedmetadata="onLoadedMetadata"
      @volumechange="onVolumeChange"
    ></audio>

    <div
      id="playingCardContainer"
      :class="{ 'darktheme-2': isDarkMode }"
      :style="extend_card ? { height: '350px', position: 'absolute', bottom: '0' } : {}"
    >
      <div v-if="loading" class="loading-indicator">
        <div class="spinner"></div>
        <span>Loading...</span>
      </div>
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
          <div v-if="song.isPlaying && !viewPlayersMode" class="arc-border"></div>
          <img :src="song.thumbnail" alt="Artist Image" @error="handleImageError" />
          <div>
            <div class="playingSongArtist">{{ song.artist }}</div>
            <div class="playingSongTitle">{{ song.title }}</div>
          </div>
        </div>

        <div v-if="song.isPlaying">
          <!-- Progress Bar & Timer -->
          <div class="progress-container" @click="seek">
            <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
            <div
              class="progress-buffer"
              :style="{ width: bufferedPercentage + '%' }"
            ></div>
          </div>
          <div class="time-info">
            {{ formattedCurrentTime }} / {{ formattedDuration }}
          </div>
        </div>
        <div class="somethingIntesting">
          <div class="somethingIntestingTitle" v-if="!viewPlayersMode">Artist</div>
          <div v-if="song.isPlaying" class="out_of_index">
            {{ currentIndex + 1 }}/{{ availableSongs.length }}
          </div>
          <div class="cardPlayerControl">
            <i
              v-if="song.isPlaying"
              class="fa fa-random"
              @click="toggleShuffle"
              :class="{ 'active-control': isShuffle }"
              :title="isShuffle ? 'Shuffle: ON' : 'Shuffle: OFF'"
            ></i>
            <router-link
              v-if="song.isPlaying"
              :to="`/you/stream/${getPreviousSongId()}`"
              custom
              v-slot="{ navigate }"
            >
              <i class="fa fa-step-backward" @click="navigate"></i>
            </router-link>
            <i
              :class="
                song.isPlaying ? (isPlaying ? 'fa fa-pause' : 'fa fa-play') : 'fa fa-play'
              "
              @click="togglePlay(index, song.song_id)"
            ></i>
            <router-link
              v-if="song.isPlaying"
              :to="`/you/stream/${getNextSongId()}`"
              custom
              v-slot="{ navigate }"
            >
              <i class="fa fa-step-forward" @click="navigate"></i>
            </router-link>
            <i
              v-if="song.isPlaying"
              class="fa fa-repeat"
              @click="toggleLoop"
              :class="{ 'active-control': isLoop }"
              :title="isLoop ? 'Loop: ON' : 'Loop: OFF'"
            ></i>
          </div>
          <div class="playingCardTimer">{{ song.stype }}</div>
          <div class="volumeToogle" v-if="song.isPlaying">
            <ion-icon :name="volumeIcon" @click="toggleMute"></ion-icon>
            <input
              class="Volume-High-Outline"
              type="range"
              min="0"
              max="1"
              step="0.01"
              v-model="volume"
              @input="updateVolume"
            />
          </div>
          <div class="playback-rate" v-if="song.isPlaying && !viewPlayersMode">
            <select v-model="playbackRate" @change="updatePlaybackRate">
              <option value="0.5">0.5x</option>
              <option value="0.75">0.75x</option>
              <option value="1" selected>1x</option>
              <option value="1.25">1.25x</option>
              <option value="1.5">1.5x</option>
              <option value="2">2x</option>
            </select>
          </div>
        </div>
        <!-- <p v-if="audio_loading">loading...</p> -->
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
import { useRouter } from "vue-router";

export default {
  props: {
    songUrl: String,
    playlist_id: String,
    playthem: String,
  },
  setup(props, { emit }) {
    const userStore = useUserStore();
    const router = useRouter();
    const fullViewMode = ref(false);
    const viewPlayersMode = ref(false);
    const currentSongUrl = ref("");
    const audioPlayer = ref(null);
    const currentIndex = ref(0);
    const isPlaying = ref(false);
    const loading = ref(false);
    const isShuffle = ref(false);
    const isLoop = ref(false);
    const volume = ref(0.7);
    const isMuted = ref(false);
    const progressPercentage = ref(0);
    const bufferedPercentage = ref(0);
    const currentTime = ref(0);
    const duration = ref(0);
    const playbackRate = ref(1);
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
    const showAnimate = ref(true);
    const extend_card = ref(false);
    const requestCards = ref(true);
    const previousVolume = ref(volume.value);
    const audio_loading = ref(false);

    const onWaiting = () => {
      audio_loading.value = true;
    };

    const onCanPlay = () => {
      loading.value = false;
    };

    const volumeIcon = computed(() => {
      if (isMuted.value || volume.value === 0) return "volume-mute-outline";
      if (volume.value < 0.33) return "volume-low-outline";
      if (volume.value < 0.66) return "volume-medium-outline";
      return "volume-high-outline";
    });

    // Get next song ID for router link
    const getNextSongId = () => {
      if (isShuffle.value) {
        const randomIndex = Math.floor(Math.random() * availableSongs.value.length);
        return availableSongs.value[randomIndex]?.song_id;
      }
      const nextIndex = (currentIndex.value + 1) % availableSongs.value.length;
      return availableSongs.value[nextIndex]?.song_id;
    };

    // Get previous song ID for router link
    const getPreviousSongId = () => {
      const prevIndex =
        (currentIndex.value - 1 + availableSongs.value.length) %
        availableSongs.value.length;
      return availableSongs.value[prevIndex]?.song_id;
    };

    const toggleViewMode = () => {
      viewPlayersMode.value = !viewPlayersMode.value;
      emit("toggle-viewPlayersMode");
      if (window.innerWidth < 680) {
        extend_card.value = !extend_card.value;
      }
    };

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
        availableSongs.value = response.data.songs?.songs || [];
        playlist_name.value = response.data.songs?.playlist_name || "Unknown Playlist";
        userStore.setPlaylistSongs(availableSongs.value, playlist_name.value);
      } catch (error) {
        console.error("API Error:", error);
        availableSongs.value = [];
      } finally {
        loading.value = false;
      }
    };

    // const togglePlay = async (index, s_url) => {
    //   const song = availableSongs.value[index];
    //   if (!song) return;

    //   const player = audioPlayer.value;
    //   if (!player) return;

    //   if (index !== currentIndex.value || !isPlaying.value) {
    //     availableSongs.value.forEach((s, i) => (s.isPlaying = i === index));
    //     currentIndex.value = index;
    //     currentSongUrl.value = getSongUrl(index);
    //     router.push(`/you/stream/${s_url}`);
    //     isPlaying.value = true;
    //     await nextTick();
    //     player.load();
    //     requestNextImage();
    //     player
    //       .play()
    //       .then(() => {
    //         startSendingProgress(player);
    //         updateBuffered();
    //       })
    //       .catch((err) => {
    //         console.error("Playback error:", err);
    //       });
    //   } else {
    //     isPlaying.value = !isPlaying.value;
    //     if (isPlaying.value) {
    //       player.play();
    //       startSendingProgress(player);
    //       updateBuffered();
    //     } else {
    //       player.pause();
    //       clearInterval(viewUpdateInterval);
    //     }
    //   }
    // };

    const togglePlay = async (index, s_url) => {
      const song = availableSongs.value[index];
      if (!song) return;

      const player = audioPlayer.value;
      if (!player) return;

      const isNewSong = index !== currentIndex.value;

      if (isNewSong || !isPlaying.value) {
        availableSongs.value.forEach((s, i) => (s.isPlaying = i === index));
        const wasNewSong = index !== currentIndex.value;
        currentIndex.value = index;
        currentSongUrl.value = getSongUrl(index);

        if (wasNewSong) {
          router.push(`/you/stream/${s_url}`);
          await nextTick(); // Wait for DOM update
          player.load(); // Only load when switching songs
        }

        isPlaying.value = true;
        requestNextImage();

        player
          .play()
          .then(() => {
            startSendingProgress(player);
            updateBuffered();
          })
          .catch((err) => {
            console.error("Playback error:", err);
          });
      } else {
        isPlaying.value = !isPlaying.value;

        if (isPlaying.value) {
          player.play();
          startSendingProgress(player);
          updateBuffered();
        } else {
          player.pause();
          clearInterval(viewUpdateInterval);
        }
      }
    };

    const onSongEnd = () => {
      clearInterval(viewUpdateInterval);
      socket.emit("updateViewCount", {
        userId: userId.value,
        songId: availableSongs.value[currentIndex.value]?.song_id,
        progress: 100.0,
      });

      if (isLoop.value) {
        audioPlayer.value.currentTime = 0;
        audioPlayer.value.play();
      } else if (isShuffle.value) {
        router.push(`/you/stream/${getNextSongId()}`);
      } else {
        router.push(`/you/stream/${getNextSongId()}`);
      }
    };

    // const playRandom = () => {
    //   let nextIndex;
    //   do {
    //     nextIndex = Math.floor(Math.random() * availableSongs.value.length);
    //   } while (nextIndex === currentIndex.value && availableSongs.value.length > 1);

    //   router.push(`/you/stream/${availableSongs.value[nextIndex]?.song_id}`);
    // };

    const playNext = () => {
      router.push(`/you/stream/${getNextSongId()}`);
    };

    const playPrevious = () => {
      router.push(`/you/stream/${getPreviousSongId()}`);
    };

    const changeIndexBySongID = (songId) => {
      const newIndex = availableSongs.value.findIndex((s) => s.song_id === songId);
      if (newIndex !== -1) togglePlay(newIndex, songId);
    };

    const scrollToview = (event) => {
      event.currentTarget.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "center",
      });
    };

    const toggleShuffle = () => {
      isShuffle.value = !isShuffle.value;
      // You can add a toast notification here if desired
      console.log(`Shuffle ${isShuffle.value ? "enabled" : "disabled"}`);
    };

    const toggleLoop = () => {
      isLoop.value = !isLoop.value;
      // You can add a toast notification here if desired
      console.log(`Loop ${isLoop.value ? "enabled" : "disabled"}`);
    };

    // ... (keep all other methods the same as previous version)

    const fetchVideoForPropUrl = async (id) => {
      loading.value = true;
      try {
        const response = await axios.get(`${BASE_URL}/api/songs/song/info/${id}`);
        const songs = Array.isArray(response.data.songs)
          ? response.data.songs
          : [response.data.songs];
        const newSongs = songs.filter(
          (song) =>
            !availableSongs.value.some((existing) => existing.song_id === song.song_id)
        );

        // Add only the new, non-duplicate songs
        if (newSongs.length > 0) {
          // availableSongs.value.push(...newSongs);
          availableSongs.value = [...availableSongs.value, ...newSongs];

          userStore.setPlaylistSongs(availableSongs.value);
        }
      } catch (error) {
        console.error("API Error:", error);
      } finally {
        loading.value = false;
      }
    };

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

    // ... (keep all other methods and lifecycle hooks the same)
    // Watch for song URL changes
    watch(
      () => props.songUrl,
      async (newSongUrl) => {
        if (!newSongUrl) return;

        await fetchVideoForPropUrl(newSongUrl);
        changeIndexBySongID(newSongUrl);
      },
      { immediate: true }
    );

    watch(playlist_id, fetchVideos, { immediate: true });

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

    // const playRandom = () => {
    //   let nextIndex;
    //   do {
    //     nextIndex = Math.floor(Math.random() * availableSongs.value.length);
    //   } while (nextIndex === currentIndex.value && availableSongs.value.length > 1);

    //   router.push(`/you/stream/${availableSongs.value[nextIndex]?.song_id}`);
    // };

    const updateProgress = () => {
      if (audioPlayer.value) {
        currentTime.value = audioPlayer.value.currentTime;
        duration.value = audioPlayer.value.duration;
        progressPercentage.value = (currentTime.value / duration.value) * 100;
      }
    };

    const updateBuffered = () => {
      if (audioPlayer.value && audioPlayer.value.buffered.length > 0) {
        const bufferedEnd = audioPlayer.value.buffered.end(
          audioPlayer.value.buffered.length - 1
        );
        const duration = audioPlayer.value.duration;

        if (duration > 0) {
          bufferedPercentage.value = (bufferedEnd / duration) * 100;
        } else {
          bufferedPercentage.value = 0;
        }
      }
    };

    const seek = (event) => {
      if (!audioPlayer.value || !duration.value) return;
      const progressBar = event.currentTarget;
      const clickPosition = event.offsetX / progressBar.clientWidth;
      audioPlayer.value.currentTime = clickPosition * duration.value;
    };

    const updateVolume = () => {
      if (audioPlayer.value) {
        audioPlayer.value.volume = volume.value;
        isMuted.value = volume.value === 0;
        if (volume.value > 0) {
          previousVolume.value = volume.value;
        }
      }
    };

    const toggleMute = () => {
      if (audioPlayer.value) {
        if (isMuted.value) {
          // Unmute and restore to previous volume
          volume.value = previousVolume.value;
          audioPlayer.value.volume = volume.value;
          isMuted.value = false;
        } else {
          // Mute and remember current volume
          previousVolume.value = volume.value;
          volume.value = 0;
          audioPlayer.value.volume = 0;
          isMuted.value = true;
        }
      }
    };

    const updatePlaybackRate = () => {
      if (audioPlayer.value) {
        audioPlayer.value.playbackRate = playbackRate.value;
      }
    };

    const onLoadedMetadata = () => {
      duration.value = audioPlayer.value.duration;
      updateBuffered();
    };

    const onVolumeChange = () => {
      if (audioPlayer.value) {
        volume.value = audioPlayer.value.volume;
        isMuted.value = audioPlayer.value.muted;
      }
    };

    const handleImageError = (event) => {
      // Fallback image if the thumbnail fails to load
      event.target.src = "https://via.placeholder.com/150";
    };

    const formatTime = (seconds) => {
      if (isNaN(seconds)) return "0:00";
      const minutes = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${minutes}:${secs < 10 ? "0" : ""}${secs}`;
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
      // Initialize audio player settings
      if (audioPlayer.value) {
        audioPlayer.value.volume = volume.value;
        audioPlayer.value.playbackRate = playbackRate.value;
      }
    });

    onUnmounted(() => {
      clearInterval(intervalId);
      clearInterval(viewUpdateInterval);
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
      getNextSongId,
      getPreviousSongId,
      scrollToview,
      isDarkMode,
      progressPercentage,
      bufferedPercentage,
      formattedCurrentTime,
      formattedDuration,
      toggleShuffle,
      toggleLoop,
      seek,
      updateProgress,
      volume,
      updateVolume,
      toggleMute,
      volumeIcon,
      playbackRate,
      updatePlaybackRate,
      PlayingAnimation_file,
      requestNextImage,
      intervalId,
      loading,
      showAnimate,
      extend_card,
      handle_showAnimate,
      requestCards,
      handleImageError,
      onLoadedMetadata,
      onVolumeChange,
      isPlaying,
      isShuffle,
      isLoop,
      onCanPlay,
      onWaiting,
      audio_loading,
    };
  },
};
</script>

<style scoped>
/* Add these styles to enhance the active state visibility */
.active-control {
  position: relative;
  color: forestgreen !important;
}

.active-control::after {
  content: "";
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 5px;
  height: 5px;
  background-color: var(--primary-color);
  border-radius: 50%;
}

.cardPlayerControl {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.cardPlayerControl i {
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1.1rem;
}

.cardPlayerControl i:hover {
  transform: scale(1.2);
  color: var(--primary-color);
}

/* Keep all other existing styles from previous version */
</style>
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
@media (max-width: 668px) {
  .injustifyLogoR {
    display: none;
  }

  #youSectionC {
    display: none;
  }
  #youSectionA {
    width: 100%;
    height: 95vh !important;
  }
  #youSectionB {
    display: flex;
    width: 100%;
    height: 200px;
    position: absolute;
    bottom: 0%;
    left: 0 !important;
    margin-left: 0% !important;
    margin-top: auto;
    position: absolute;
  }
}

@media (max-width: 480px) {
  #youSectionA {
    width: 100% !important;
  }

  #youSectionB {
    display: flex !important;
    width: 100% !important;
    height: 200px !important;
    position: fixed;
    left: 0 !important;
    margin-left: 0% !important;
    margin-top: auto;
    position: absolute;
  }
  #youSectionC {
    display: none;
  }
}
</style>
