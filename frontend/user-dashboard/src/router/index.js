import { createRouter, createWebHistory } from 'vue-router';
//import { useUserStore } from "@/store/index.js"; // Import Pinia store

import AccountVerify from '@/views/AccountVerify.vue';
import HomePage from '../views/HomePage.vue';
import UserProfile from '../views/UserProfile.vue';
import DownloadsPage from '../views/DownloadsPage.vue';
import AnalyticsPage from '../views/AnalyticsPage.vue';
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
//import ActivePLaylist from "@/views/YouPageThree.vue";
import YouplayingSong from "@/views/YouPageTwo.vue";
import DownloadStreams from "@/views/downloadsSelectorContainer.vue"




const routes = [
  { path: '/verify/auth', name: 'AccountVerifyPage', component: AccountVerify}, 
  { path: '/', name: 'Home', component: HomePage, },
  { path: '/profile/:useremail', name: 'Profile', component: UserProfile, props: true },
  { path: '/downloads/:useremail', name: 'UserDownloads', component: DownloadsPage, props: true },
  { path: '/analytics/:useremail', name: 'AnalyticsPage', component: AnalyticsPage, props: true },
  { path: '/notifications/:useremail', name: 'UserNotifications', component: UserNotifications, props: true },
  { path: '/search', name: 'SearchResults', component: SearchResults}, 
  { path: '/about', name: 'About', component: AboutPage }, 
  { path: '/you', name:'YouPage',component:YouPage}, 
  { path: '/help', name: 'HelpPage', component: HelpPage },
  { path: '/feedback', name: 'FeedbackPage', component: FeedbackPage },
  {
    path: '/',
    name: 'DownloadStreams',
    component: DownloadStreams,
    props: route => ({ uuid: route.query.dwn })
  },
  

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
    
    children: [
      { path: "stream/:songUrl", name: "YouplayingSong", component: YouplayingSong, props: true },
      { path: "xy/yls/:userId", name: "LikedSongsPage", component: LikedSongsPage, props: true },
      { path: "xy/pl/:userId", name: "PlaylistPage", component: PlaylistPage, props: true },
      { path: "xy/str/:userId", name: "StreamRatePage", component: StreamRatePage, props: true },
      { path: "xy/utr/:userId", name: "UserTopSongs", component: UserTopSongs, props: true },
      { path: "tr", name: "TrendingPage", component: TrendingPage },
    ],
  },
  


];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
