import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from "@/store/index.js"; // Import Pinia store

import HomePage from '../views/HomePage.vue';
import UserProfile from '../views/UserProfile.vue';
import DownloadsPage from '../views/DownloadsPage.vue';
import UserHistory from '../views/UserHistory.vue';
import UserNotifications from '../views/UserNotifications.vue';
import SearchResults from "../views/DevsPage.vue"; 
import AboutPage from "../views/AboutPage.vue"; 
import HelpPage from "../views/HelpPage.vue"; 
import FeedbackPage from "../views/FeedbackPage.vue"; 


import SettingsPage from '../views/SettingsPage.vue'; 
import ProfileSettings from "@/views/ProfileSettings.vue";
import NotificationSettings from "@/views/NotificationsSettings.vue";
import PreferenceSettings from "@/views/PreferenceSettings.vue";
import SecuritySettings from "@/views/SecuritySet.vue";
import YouPage from "../views/YouPage.vue";
import LikedSongsPage from "@/views/LikedSongs.vue";
//import UserTopArtist from "@/views/TopArtist.vue";
import PlaylistPage from "@/views/PlaylistsPage.vue";
import StreamRatePage from "@/views/StreamRate.vue";
import TrendingPage from "@/views/TrendingPage.vue";
import UserTopSongs from "@/views/UserTopSongs.vue";
import ActivePLaylist from "@/views/YouPageThree.vue";
import YouplayingSong from "@/views/YouPageTwo.vue";





const routes = [
  { path: '/', name: 'Home', component: HomePage, },
  { path: '/profile/:useremail', name: 'Profile', component: UserProfile, props: true },
  { path: '/downloads/:useremail', name: 'UserDownloads', component: DownloadsPage, props: true },
  { path: '/history/:useremail', name: 'UserHistory', component: UserHistory, props: true },
  { path: '/notifications/:useremail', name: 'UserNotifications', component: UserNotifications, props: true },
  { path: '/search', name: 'SearchResults', component: SearchResults}, 
  { path: '/about', name: 'About', component: AboutPage }, 
  { path: '/you', name:'YouPage',component:YouPage}, 
  { path: '/help', name: 'HelpPage', component: HelpPage },
  { path: '/feedback', name: 'FeedbackPage', component: FeedbackPage },

  {
    path: "/settings",
    name: "SettingsPage",
    component: SettingsPage,
    children: [
      { path: "", redirect: "/settings/profile" }, // Redirect to profile settings when visiting /settings
      { path: "profile", name: "ProfileSettings", component: ProfileSettings },
      { path: "notifications", name: "NotificationSettings", component: NotificationSettings },
      { path: "preferences", name: "PreferenceSettings", component: PreferenceSettings },
      { path: "security", name: "SecuritySettings", component: SecuritySettings },
    ],
  },


  {
    path: "/you",
    name: "YouPage",
    component: YouPage,
    redirect: () => {
      const userStore = useUserStore();
      return userStore.userId ? `/you/st/${userStore.userId}` : "/login"; 
    },
    children: [
      { path: "yls/:userId", name: "LikedSongsPage", component: LikedSongsPage, props: true },
      { path: "pl/:playlist_id", name: "PlaylistPage", component: PlaylistPage, props: true },
      { path: "str/:userId", name: "StreamRatePage", component: StreamRatePage, props: true },
      { path: "utr/:userId", name: "UserTopArtist", component: UserTopSongs, props: true },
      { path: "tr", name: "TrendingPage", component: TrendingPage },
      { path: "upls/ls/:playlist_id", name: "ActivePLaylist", component: ActivePLaylist, props: true },
      { path: "st/:songId", name: "YouplayingSong", component: YouplayingSong, props: true },
    ],
  }
  


];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
