<template>
  <div id="youSectionA">
    <!-- Scrollable Categories -->
    <div id="sectionAscroll">
      <div id="allScrolls">
        <div class="secAscroll" @click="handleScroll('yls', $event)">
          <router-link :to="`/you/yls/${userId}`">You liked songs</router-link>
        </div>
        <div class="secAscroll" @click="handleScroll('pl', $event)">
          <router-link :to="`/you/pl/${userId}`">Your playlists</router-link>
        </div>
        <div class="secAscroll" @click="handleScroll('str', $event)">
          <router-link :to="`/you/str/${userId}`">Stream rate</router-link>
        </div>
        <div class="secAscroll" @click="handleScroll('utr', $event)">
          <router-link :to="`/you/utr/${userId}`">Your top songs</router-link>
        </div>
        <div class="secAscroll" @click="handleScroll('tr', $event)">
          <router-link to="/you/tr">Trending</router-link> 
          <!-- This one does not need userId, assuming that's intentional -->
        </div>
      </div>
    </div>

    <!-- Dynamic Content Section -->
    <router-view></router-view>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/store/index.js";
import { computed } from "vue";

const userStore = useUserStore();
const userId = computed(() => userStore.userId);
//const userEmail = computed(() => userStore.email);

// Track the selected category
const selectedCategory = ref(null);

const handleScroll = (category, event) => {
  selectedCategory.value = category;

  // Ensure the correct div scrolls into view
  event.currentTarget.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
};
</script>

  
  <style scoped>

  
  #allScrolls::-webkit-scrollbar {
    display: none;
  }
  
  #youSectionA {
    display: flex;
    flex-direction: column;
    gap: 15px;
    max-width: 350px;
  }
  
  #sectionYourTopPlaylistsongs {
    min-height: 250px;
    height: auto;
    overflow-y: auto;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.7);
  }
  #youSectionA{
    display: flex;
    flex-direction: column;
    gap: 15px;
}

#youSectionA > div {
    border-radius: 3px;
    padding: 5px;
    box-sizing: border-box;
}


#youSectionA #sectionAplaylists{
    min-height: 150px !important;
    height: 150px;
    overflow-y: auto;
    position: relative;
    display: flex;
    flex-direction: column;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.703);
}

#youSectionA #sectionAplaylists #sectionAplaylistBody > div {
    cursor: pointer;
    align-items: center;
    display: flex;
    gap: 15px;
    width: 100%;
    margin: 3px 0;
    padding: 3px 5px;
    border-radius: 5px;
    box-sizing: border-box;
}

#youSectionA #sectionAplaylists #sectionAplaylistBody > div:hover{
    background: linear-gradient(to right,  
    rgba(128, 128, 128, 0.057) 20%,  
    rgba(128, 128, 128, 0.325) 40%,
    rgba(128,128,128,0.6) 60%,  
    rgba(128,128,128,0.3) 80%,  
    rgba(128,128,128,0) 100%);
}

#youSectionA #selected_type_view{
    min-height: 250px !important;
    height: 250px;
    overflow-y: auto;
    position: relative;
    display: flex;
    flex-direction: column;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.703);

}

#youSectionA .songs  {
    cursor: pointer;
    align-items: center;
    display: flex;
    gap: 15px;
    width: 100%;
    margin: 3px 0;
    padding: 3px 5px;
    border-radius: 5px;
    box-sizing: border-box;
    height: 50px;
}

#youSectionA .songs:hover{
    background: linear-gradient(to right,  
    gray 20%,  
    rgba(128,128,128,0.9) 40%,  
    rgba(128,128,128,0.6) 60%,  
    rgba(128,128,128,0.3) 80%,  
    rgba(128,128,128,0) 100%);
}


#youSectionA .songs img{
    height: 100% !important;
    object-fit: cover;
}

#youSectionA .songs{
    background: linear-gradient(to left,  
    gray 20%,  
    rgba(128,128,128,0.9) 40%,  
    rgba(128,128,128,0.6) 60%,  
    rgba(128,128,128,0.3) 80%,  
    rgba(128,128,128,0) 100%);
}
#sectionAscroll{
    position:sticky;
    top: 0;
    z-index: 99
}
#allScrolls{
    display: flex;
    flex-direction: row;
    gap: 5px;
    overflow-y: auto;
    z-index: 99;
    font-weight: bold;
    color: rgb(214, 207, 207);

}

#allScrolls .secAscroll{
    white-space: nowrap;
    padding: 5px;
    border-radius: 5px;
    transition: all 0.5s ease;
    cursor: pointer;
    user-select: none;
    background-color: gray;
    text-decoration: none;
    border-bottom: 0px;

}

#allScrolls .secAscroll:hover{
    background-color: rgb(161, 160, 160);
}

#allScrolls .secAscroll a{
  text-decoration: none;
  color:inherit
}

a.router-link-active{
  font-weight: bold;
  text-shadow: 0px 1px 3px rgb(0, 0, 0);
  text-decoration: underline !important;
  color: rgb(75, 75, 190) !important;
}
  </style>
  