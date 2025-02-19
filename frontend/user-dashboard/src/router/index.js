import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import UserProfile from '../views/UserProfile.vue';
import DownloadsPage from '../views/DownloadsPage.vue';
import UserHistory from '../views/UserHistory.vue';
import UserNotifications from '../views/UserNotifications.vue';
import SearchResults from "../views/SearchResults.vue"; 
import About from "../views/About.vue"; 
import SettingsPage from '../views/SettingsPage.vue'; 
import ProfileSettings from "@/views/ProfileSettings.vue";
import NotificationSettings from "@/views/NotificationsSettings.vue";
import PreferenceSettings from "@/views/PreferenceSettings.vue";
import SecuritySettings from "@/views/SecuritySet.vue";

const routes = [
  { path: '/:useremail', name: 'Home', component: HomePage, props: true },
  { path: '/profile/:useremail', name: 'Profile', component: UserProfile, props: true },
  { path: '/downloads/:useremail', name: 'UserDownloads', component: DownloadsPage, props: true },
  { path: '/history/:useremail', name: 'UserHistory', component: UserHistory, props: true },
  { path: '/notifications/:useremail', name: 'UserNotifications', component: UserNotifications, props: true },
  { path: '/search', name: 'SearchResults', component: SearchResults}, 
  { path: '/about', name: 'About', component: About }, 

  // Settings Route with child routes and working redirect to profile
  {
    path: "/settings",
    name: "SettingsPage",
    component: SettingsPage,
    children: [
      { path: "profile", name: "ProfileSettings", component: ProfileSettings },
      { path: "notifications", name: "NotificationSettings", component: NotificationSettings },
      { path: "preferences", name: "PreferenceSettings", component: PreferenceSettings },
      { path: "security", name: "SecuritySettings", component: SecuritySettings },
    ],
  },


];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
