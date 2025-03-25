<template>
  <div class="MainContainer" :class="{ collabsedBig: iscollapsedBig }">
    <!-- Logo Section -->
    <h1 class="injustifyLogoR">
      <ion-icon name="musical-note-outline"></ion-icon>
      Injustify
      <ion-icon name="musical-note-outline"></ion-icon>
    </h1>

    <div class="children">
      <ChildTwo
        class="common-scroolbar"
        v-if="currentChild === 'stream' || !currentChild"
        :isDarkMode="isDarkMode"
        :clickedSongId="playSongID"
        @toggle-viewPlayersMode="toggleViewPlayersMode"
      />

      <ChildOne
        class="common-scroolbar"
        v-if="currentChild === 'xy' || !currentChild"
        :isDarkMode="isDarkMode"
      />

      <ChildThree
        class="common-scroolbar"
        v-if="(currentChild === 'yz' || !currentChild) && viewPlayersMode"
        @play-song="handlePlaySong"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useRoute } from "vue-router";
import { useUserStore } from "@/store/index.js";
import ChildOne from "./YouPageONe.vue";
import ChildTwo from "./YouPageTwo.vue";
import ChildThree from "./YouPageThree.vue";

// Reactive State
const route = useRoute();
const playSongID = ref("3031");
const viewPlayersMode = ref(true);
const userStore = useUserStore();

// Computed Properties
const iscollapsedBig = computed(() => userStore.iscollapsedBig);
const isDarkMode = computed(() => userStore.isdarkmode);

const currentChild = ref(route.params.child ? String(route.params.child) : null);

console.log("Current Child:", currentChild.value);

// Watch for route changes and update `currentChild`
watch(
  () => route.params.child,
  (newChild) => {
    currentChild.value = newChild ? String(newChild) : null;
    console.log("Updated Child:", currentChild.value);
  }
);

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
  font-size: 20px;
  margin: 0 !important;
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
