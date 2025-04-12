<template>
  <div id="youSectionA">
    <!-- Scrollable Categories -->
    <div id="sectionAscroll" :class="{ 'darktheme-2': isDarkMode }">
      <div id="allScrolls">
        <div class="secAscroll" @click="handleScroll('yls', $event)">
          <router-link :to="`/you/xy/yls/${userId}`">You liked songs</router-link>
        </div>

        <div class="secAscroll" @click="handleScroll('pl', $event)">
          <router-link :to="`/you/xy/pl/${userId}`">Your playlists</router-link>
        </div>

        <div class="secAscroll" @click="handleScroll('str', $event)">
          <router-link :to="`/you/xy/str/${userId}`">Stream rate</router-link>
        </div>

        <div class="secAscroll" @click="handleScroll('utr', $event)">
          <router-link :to="`/you/xy/utr/${userId}`">Your top songs</router-link>
        </div>

        <div class="secAscroll" @click="handleScroll('tr', $event)">
          <router-link to="/you/tr">Trending</router-link>
        </div>
      </div>
    </div>

    <!-- Dynamic Content Section -->
    <router-view></router-view>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useUserStore } from "@/store/index.js";
import { useRoute } from "vue-router";

const userStore = useUserStore();
const route = useRoute();
const userId = computed(() => userStore.userId);
const isDarkMode = computed(() => userStore.isdarkmode);

const selectedCategory = ref(null);

const handleScroll = (category, event) => {
  selectedCategory.value = category;

  event.currentTarget.scrollIntoView({
    behavior: "smooth",
    block: "nearest",
    inline: "center",
  });
  return {
    isDarkMode,
  };
};

// Watch route changes to update the active state
watch(
  () => route.params.category,
  (newCategory) => {
    selectedCategory.value = newCategory || null;
  }
);
</script>

<style scoped>
/* Highlight active category */
.secAscroll.active {
  background-color: #444;
  color: white;
  border-radius: 5px;
}
</style>

<style scoped>
#allScrolls::-webkit-scrollbar {
  display: none;
}

#youSectionA {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 350px;
  height: 85vh !important;
  overflow-x: hidden;
  padding: 3px 0;
  box-sizing: border-box;
}

#sectionYourTopPlaylistsongs {
  min-height: 250px;
  height: auto;
  overflow-y: auto;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.7);
}

#youSectionA > div {
  border-radius: 3px;
  padding: 5px;
  box-sizing: border-box;
}

#youSectionA #sectionAplaylists {
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

#youSectionA #sectionAplaylists #sectionAplaylistBody > div:hover {
  background: linear-gradient(
    to right,
    rgba(128, 128, 128, 0.057) 20%,
    rgba(128, 128, 128, 0.325) 40%,
    rgba(128, 128, 128, 0.6) 60%,
    rgba(128, 128, 128, 0.3) 80%,
    rgba(128, 128, 128, 0) 100%
  );
}

#youSectionA #selected_type_view {
  min-height: 250px !important;
  height: 250px;
  overflow-y: auto;
  position: relative;
  display: flex;
  flex-direction: column;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.703);
}

#youSectionA .songs {
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

#youSectionA .songs:hover {
  background: linear-gradient(
    to right,
    gray 20%,
    rgba(128, 128, 128, 0.9) 40%,
    rgba(128, 128, 128, 0.6) 60%,
    rgba(128, 128, 128, 0.3) 80%,
    rgba(128, 128, 128, 0) 100%
  );
}

#youSectionA .songs img {
  height: 100% !important;
  object-fit: cover;
}

#youSectionA .songs {
  background: linear-gradient(
    to left,
    gray 20%,
    rgba(128, 128, 128, 0.9) 40%,
    rgba(128, 128, 128, 0.6) 60%,
    rgba(128, 128, 128, 0.3) 80%,
    rgba(128, 128, 128, 0) 100%
  );
}
#sectionAscroll {
  background: #dcdcde;
  position: sticky;
  top: 0;
  z-index: 99;
}
#allScrolls {
  display: flex;
  flex-direction: row;
  gap: 5px;
  overflow-y: auto;
  z-index: 99;
  font-weight: bold;
  color: rgb(214, 207, 207);
}

#allScrolls .secAscroll {
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

#allScrolls .secAscroll:hover {
  background-color: rgb(161, 160, 160);
}

#allScrolls .secAscroll a {
  text-decoration: none;
  color: inherit;
}

a.router-link-active {
  font-weight: bold;
  text-shadow: 0px 1px 3px rgb(0, 0, 0);
  text-decoration: underline !important;
  color: rgb(75, 75, 190) !important;
}
.darktheme-2 {
  background: #2c2c2c !important;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
  color: #e7e7e7 !important;
}
</style>
<style scoped>
/* Base Container */
#youSectionA {
  --primary-light: #6366f1;
  --primary-dark: #818cf8;
  --transition-speed: 0.3s;
}

/* Navigation Bar */
#sectionAscroll {
  backdrop-filter: blur(10px);
  border-bottom: 1px solid;
  @apply bg-opacity-80;
}

#sectionAscroll.darktheme-2 {
  border-bottom-color: rgba(255, 255, 255, 0.08);
  @apply bg-gray-900 bg-opacity-80;
}

#sectionAscroll:not(.darktheme-2) {
  border-bottom-color: rgba(0, 0, 0, 0.08);
  @apply bg-white bg-opacity-80;
}

/* Navigation Items */
#allScrolls {
  scrollbar-width: none;
  mask-image: linear-gradient(
    to right,
    transparent,
    black 20px,
    black 90%,
    transparent
  );
}

.secAscroll {
  position: relative;
  transition: all var(--transition-speed) ease;
}

.secAscroll a {
  position: relative;
  transition: all var(--transition-speed) ease;
  @apply px-3 py-2 rounded-lg;
}

/* Active State */
.secAscroll a.router-link-active {
  @apply font-semibold;
}

.secAscroll:hover a {
  transform: translateY(-2px);
}

/* Underline Animation */
.secAscroll::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-light), var(--primary-dark));
  border-radius: 3px 3px 0 0;
  transition: all var(--transition-speed) ease;
  transform: translateX(-50%);
}

.secAscroll:hover::after,
.secAscroll.router-link-active::after {
  width: 70%;
}

/* Dark Mode Specifics */
.darktheme-2 .secAscroll a {
  @apply text-gray-300;
}

.darktheme-2 .secAscroll:hover a {
  @apply text-white;
}

.darktheme-2 .secAscroll a.router-link-active {
  @apply text-primary-400;
}

:not(.darktheme-2) .secAscroll a {
  @apply text-gray-600;
}

:not(.darktheme-2) .secAscroll:hover a {
  @apply text-gray-900;
}

:not(.darktheme-2) .secAscroll a.router-link-active {
  @apply text-primary-600;
}

/* Content Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive Adjustments */
@media (max-width: 640px) {
  #allScrolls {
    mask-image: none;
    padding: 0 16px;
  }
  
  .secAscroll a {
    @apply px-2 py-1 text-sm;
  }
  
  .secAscroll::after {
    height: 2px;
  }
}
</style>