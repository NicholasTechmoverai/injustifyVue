<template>
    <div id="youSectionA">

      <!-- Scrollable Categories -->
      <div id="sectionAscroll">
        <div id="allScrolls">
          <div  class="secAscroll"
            v-for="(section, index) in scrollSections" 
            :key="index" 
      @click="handleScroll(section.name, $event)">
            {{ section.name }}
          </div>
        </div>
      </div>
  
      <!-- Dynamic Content Section -->
      <div id="selected_type_view">
        <h2>{{ selectedCategory }}</h2>
        <div>
          <div v-for="(item, index) in selectedContent" :key="index" class="songs">
            <img v-if="item.thumbnail" :src="item.thumbnail" alt="Thumbnail">
            <div>
              <div>{{ item.title || item.name }}</div>
              <div v-if="item.rank">{{ item.rank }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>


  
  <script setup>
  import { ref } from 'vue';
  

  const scrollSections = ref([
    { name: 'Your Top Songs' },
    { name: 'Your Liked Songs' },
    { name: 'Your Top Artists' },
    { name: 'Your Stream Rate' },
    { name: 'Trending' },
    { name: 'Your Playlists' }
  ]);
  
  const topSongs = ref([
    { title: 'Song A', rank: '#1', thumbnail: 'https://via.placeholder.com/50' },
    { title: 'Song B', rank: '#2', thumbnail: 'https://via.placeholder.com/50' },
    { title: 'Song C', rank: '#3', thumbnail: 'https://via.placeholder.com/50' }
  ]);
  
  const likedSongs = ref([
    { title: 'Liked Song 1', rank: '#1', thumbnail: 'https://via.placeholder.com/50' },
    { title: 'Liked Song 2', rank: '#2', thumbnail: 'https://via.placeholder.com/50' }
  ]);
  
  const selectedCategory = ref('Your Top Songs');
  const selectedContent = ref(topSongs.value);
  
  const selectCategory = (category) => {
    selectedCategory.value = category;
    if (category === 'Your Top Songs') {
      selectedContent.value = topSongs.value;
    } else if (category === 'Your Liked Songs') {
      selectedContent.value = likedSongs.value;
    } else {
      selectedContent.value = [{ name: category }];
    }
  };
  
  const handleScroll = (category, event) => {
    selectCategory(category);
    
    event.target.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
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

}

#allScrolls .secAscroll:hover{
    background-color: rgb(161, 160, 160);
}


  </style>
  