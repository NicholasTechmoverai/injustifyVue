<template>
  <div class="MainContainer" :class="{ collabsedBig: iscollapsedBig }">
    <!-- Logo Section -->
    <h1 class="injustifyLogoR">
      <ion-icon name="musical-note-outline"></ion-icon>
      Injustify
      <ion-icon name="musical-note-outline"></ion-icon>
    </h1>

    <!-- Router Views -->
    <div class="children">
      <router-view name="childOne"></router-view>
      <router-view name="childTwo"></router-view>
      <router-view name="childThree"></router-view>
    </div>

    <!-- Child Components -->
    <div class="children">
      <ChildOne :isDarkMode="isDarkMode" />
      <ChildTwo
        :isDarkMode="isDarkMode"
        :clickedSongId="playSongID"
        @toggle-viewPlayersMode="toggleViewPlayersMode"
      />
      <ChildThree v-if="viewPlayersMode" @play-song="handlePlaySong" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useUserStore } from "@/store/index.js";
import ChildOne from "./YouPageONe.vue";
import ChildTwo from "./YouPageTwo.vue";
import ChildThree from "./YouPageThree.vue";

// Reactive State
const playSongID = ref(null);
const viewPlayersMode = ref(true);
const userStore = useUserStore();

// Computed Properties
const iscollapsedBig = computed(() => userStore.iscollapsedBig);
const isDarkMode = computed(() => userStore.isdarkmode);

// Event Handlers
const toggleViewPlayersMode = () => {
  console.log("Toggled view players mode in App.vue");
  viewPlayersMode.value = !viewPlayersMode.value;
};

const handlePlaySong = (id) => {
  console.log("Song ID received:", id);
  playSongID.value = id;
};
</script>

<style scoped>
.children {
  display: flex;
  justify-content: space-around;
  gap: 10px;
  transition: all 0.3s ease-in-out;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

.children > * {
  flex: 1;
  border-radius: 8px;
  transition: all 0.3s ease-in-out;
  box-sizing: border-box;
  box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.2);
  padding: 3px;
}
.injustifyLogoR {
  position: relative;
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
