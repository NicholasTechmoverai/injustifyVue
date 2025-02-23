<template>
  <div class="MainContainer">
      <h1 class="injustifyLogoR">
        <ion-icon name="musical-note-outline"></ion-icon>Injustify
        <ion-icon name="musical-note-outline"></ion-icon>
      </h1>
      <div class="children">
        <ChildOne />
        <ChildTwo :clickedSongId="playSongID" @toggle-viewPlayersMode="toggleViewPlayersMode" />
        <ChildThree  @play-song="sendId_of_clickedSong" v-if="viewPlayersMode"  />
      </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import ChildOne from "./YouPageONe.vue";
import ChildTwo from "./YouPageTwo.vue";
import ChildThree from "./YouPageThree.vue";

const playSongID = ref(null);
const viewPlayersMode = ref(true);

const toggleViewPlayersMode = () => {
  console.log("Toggled theme in app.vue");
  viewPlayersMode.value = !viewPlayersMode.value;
};

const sendId_of_clickedSong = (id) => {
  console.log("Song ID:", id);
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
  .injustifyLogoR{
    position: relative;
  }
  
  
  </style>
  