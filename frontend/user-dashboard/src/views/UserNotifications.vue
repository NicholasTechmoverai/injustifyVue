<template>
  <div class="Maincontainer notification-center" :class="{ 'dark-mode': isDarkMode }">
    <!-- Sidebar Navigation -->
    <div class="sidebar" :class="{ 'dark-sidebar': isDarkMode }">
      <div class="sidebar-header">
        <h2><i class="fas fa-bell"></i> Notifications</h2>
      </div>
      <div class="sidebar-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          :class="{ active: activeTab === tab.value }"
          @click="activeTab = tab.value"
        >
          <i :class="tab.icon"></i>
          <span>{{ tab.label }}</span>
          <span v-if="tab.value === 'unread'" class="badge">{{ unreadCount }}</span>
        </button>
      </div>
      <div class="sidebar-footer">
        <button class="mark-all-read" @click="markAllAsRead">
          <i class="fas fa-check-double"></i> Mark all as read
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="main-content">
      <!-- Filter Bar -->
      <div class="filter-bar">
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search notifications..."
          />
        </div>
        <div class="filter-controls">
          <div class="filter-group">
            <label><i class="fas fa-filter"></i> Filter by:</label>
            <select v-model="activeFilter">
              <option v-for="filter in filters" :key="filter.value" :value="filter.value">
                {{ filter.label }}
              </option>
            </select>
          </div>
          <div class="sort-group">
            <label><i class="fas fa-sort"></i> Sort by:</label>
            <select v-model="sortBy">
              <option value="newest">Newest first</option>
              <option value="oldest">Oldest first</option>
              <option value="priority">Priority</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Notification Grid -->
      <div class="notification-grid">
        <div
          v-for="notification in filteredNotifications"
          :key="notification.id"
          class="notification-card"
          :class="{
            unread: !notification.read,
            priority: notification.priority,
            music: notification.type === 'music',
            social: notification.type === 'social',
            system: notification.type === 'system',
          }"
          @click="handleNotificationClick(notification)"
        >
          <div class="notification-header">
            <div class="notification-icon">
              <i :class="getNotificationIcon(notification)"></i>
            </div>
            <div class="notification-meta">
              <h3>{{ notification.title }}</h3>
              <span class="notification-time">{{ formatTime(notification.time) }}</span>
            </div>
            <button
              class="dismiss-btn"
              @click.stop="dismissNotification(notification.id)"
            >
              <i class="fas fa-times"></i>
            </button>
          </div>

          <div class="notification-body">
            <p class="notification-message">{{ notification.message }}</p>

            <!-- Music Content -->
            <div v-if="notification.type === 'music'" class="music-content">
              <div class="album-art-container">
                <div class="album-art">
                  <img :src="notification.song.albumArt" alt="Album cover" />
                  <button class="play-btn" @click.stop="playPreview(notification.song)">
                    <i class="fas fa-play"></i>
                  </button>
                </div>
                <div class="song-controls">
                  <button @click.stop="addToQueue(notification.song)">
                    <i class="fas fa-list-ol"></i> Add to queue
                  </button>
                  <button @click.stop="addToPlaylist(notification.song.id)">
                    <i class="fas fa-plus"></i> Add to playlist
                  </button>
                </div>
              </div>
              <div class="song-details">
                <h4>{{ notification.song.title }}</h4>
                <p>{{ notification.song.artist }}</p>
                <div class="song-stats">
                  <span
                    ><i class="fas fa-clock"></i> {{ notification.song.duration }}</span
                  >
                  <span
                    ><i class="fas fa-calendar-alt"></i>
                    {{ notification.song.releaseDate }}</span
                  >
                  <span
                    ><i class="fas fa-headphones"></i>
                    {{ notification.song.plays }} plays</span
                  >
                </div>
              </div>
            </div>

            <!-- Social Content -->
            <div v-if="notification.type === 'follow'" class="social-content">
              <div class="user-avatar">
                <img :src="notification.user.avatar" :alt="notification.user.name" />
              </div>
              <div class="user-info">
                <h4>{{ notification.user.name }}</h4>
                <p>{{ notification.user.bio }}</p>
              </div>
              <button class="follow-btn" @click.stop="followBack(notification.userId)">
                <i class="fas fa-user-plus"></i> Follow back
              </button>
            </div>
          </div>

          <div class="notification-footer">
            <button
              v-if="!notification.read"
              class="mark-read-btn"
              @click.stop="markAsRead(notification.id)"
            >
              <i class="fas fa-check"></i> Mark as read
            </button>
            <div class="notification-tags">
              <span v-if="notification.priority" class="tag priority-tag">
                <i class="fas fa-exclamation-circle"></i> Priority
              </span>
              <span class="tag type-tag">
                {{ notification.type }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredNotifications.length === 0" class="empty-state">
        <div class="empty-state-content">
          <i class="fas fa-bell-slash"></i>
          <h3>No notifications found</h3>
          <p>You're all caught up with your notifications!</p>
          <button class="refresh-btn" @click="refreshNotifications">
            <i class="fas fa-sync-alt"></i> Refresh
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "@/store/index.js";
import { computed } from "vue";

export default {
  name: "EnhancedNotificationCenter",
  data() {
    const userStore = useUserStore();

    return {
      isDarkMode: computed(() => userStore.isdarkmode),
      iscollapsedBig: computed(() => userStore.iscollapsedBig),
      activeTab: "all",
      activeFilter: "all",
      sortBy: "newest",
      searchQuery: "",
      tabs: [
        { label: "All", value: "all", icon: "fas fa-bell" },
        { label: "Unread", value: "unread", icon: "fas fa-envelope" },
        { label: "Music", value: "music", icon: "fas fa-music" },
        { label: "Social", value: "social", icon: "fas fa-users" },
        { label: "System", value: "system", icon: "fas fa-cog" },
      ],
      filters: [
        { label: "All notifications", value: "all" },
        { label: "Music updates", value: "music" },
        { label: "Social interactions", value: "social" },
        { label: "System messages", value: "system" },
        { label: "Priority", value: "priority" },
      ],
      notifications: [
        {
          id: 1,
          type: "music",
          title: "New Album Release",
          message: "Your favorite artist just dropped a new album - check it out now!",
          time: new Date(Date.now() - 1000 * 60 * 15), // 15 minutes ago
          read: false,
          priority: true,
          song: {
            id: "album123",
            title: "Midnight Dreams",
            artist: "Stellar Echo",
            albumArt: "https://i.scdn.co/image/ab67616d00001e02fc9a3c2975171e70b1e9a6f8",
            duration: "45:22",
            releaseDate: "Today",
            plays: "2.4M",
          },
        },
        {
          id: 2,
          type: "music",
          title: "New Single Available",
          message: "A new single from an artist you follow has been released",
          time: new Date(Date.now() - 1000 * 60 * 60 * 3), // 3 hours ago
          read: false,
          song: {
            id: "single456",
            title: "Electric Love",
            artist: "Neon Waves",
            albumArt: "https://i.scdn.co/image/ab67616d00001e0258a27fd1a6fb4c87e1e8cf0a",
            duration: "3:45",
            releaseDate: "Today",
            plays: "856K",
          },
        },
        {
          id: 3,
          type: "follow",
          title: "New Follower",
          message: "You have a new follower on your profile",
          time: new Date(Date.now() - 1000 * 60 * 60 * 5), // 5 hours ago
          read: false,
          userId: "user789",
          user: {
            name: "DJ Pulse",
            avatar: "https://randomuser.me/api/portraits/men/32.jpg",
            bio: "Electronic Music Producer",
          },
        },
        {
          id: 4,
          type: "system",
          title: "Subscription Update",
          message: "Your premium subscription has been renewed successfully",
          time: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 day ago
          read: true,
        },
      ],
    };
  },
  computed: {
    unreadCount() {
      return this.notifications.filter((n) => !n.read).length;
    },
    filteredNotifications() {
      let filtered = [...this.notifications];

      // Apply tab filter
      if (this.activeTab === "unread") {
        filtered = filtered.filter((n) => !n.read);
      } else if (this.activeTab !== "all") {
        filtered = filtered.filter((n) => n.type === this.activeTab);
      }

      // Apply additional filters
      if (this.activeFilter !== "all") {
        if (this.activeFilter === "priority") {
          filtered = filtered.filter((n) => n.priority);
        } else {
          filtered = filtered.filter((n) => n.type === this.activeFilter);
        }
      }

      // Apply search
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(
          (n) =>
            n.title.toLowerCase().includes(query) ||
            n.message.toLowerCase().includes(query) ||
            (n.type === "music" &&
              (n.song.title.toLowerCase().includes(query) ||
                n.song.artist.toLowerCase().includes(query)))
        );
      }

      // Apply sorting
      switch (this.sortBy) {
        case "newest":
          return filtered.sort((a, b) => b.time - a.time);
        case "oldest":
          return filtered.sort((a, b) => a.time - b.time);
        case "priority":
          return filtered.sort(
            (a, b) => (b.priority || 0) - (a.priority || 0) || b.time - a.time
          );
        default:
          return filtered;
      }
    },
  },
  methods: {
    markAsRead(id) {
      const notification = this.notifications.find((n) => n.id === id);
      if (notification) {
        notification.read = true;
      }
    },
    markAllAsRead() {
      this.notifications.forEach((n) => (n.read = true));
    },
    dismissNotification(id) {
      this.notifications = this.notifications.filter((n) => n.id !== id);
    },
    handleNotificationClick(notification) {
      if (!notification.read) {
        this.markAsRead(notification.id);
      }

      // Handle navigation based on notification type
      switch (notification.type) {
        case "music":
          this.$router.push(`/music/${notification.song.id}`);
          break;
        case "follow":
          this.$router.push(`/artist/${notification.userId}`);
          break;
        case "system":
          this.$router.push("/account/subscription");
          break;
      }
    },
    playPreview(song) {
      // Implement play preview functionality
      console.log("Playing preview:", song.title);
    },
    addToQueue(song) {
      // Implement add to queue functionality
      console.log("Adding to queue:", song.title);
    },
    addToPlaylist(songId) {
      // Implement add to playlist functionality
      console.log("Adding song to playlist:", songId);
    },
    followBack(userId) {
      // Implement follow back functionality
      console.log("Following user:", userId);
      this.dismissNotification(this.notifications.find((n) => n.userId === userId).id);
    },
    refreshNotifications() {
      // Implement refresh functionality
      console.log("Refreshing notifications...");
    },
    getNotificationIcon(notification) {
      switch (notification.type) {
        case "music":
          return "fas fa-music";
        case "follow":
          return "fas fa-user-plus";
        case "system":
          return "fas fa-cog";
        default:
          return "fas fa-bell";
      }
    },
    formatTime(date) {
      const now = new Date();
      const diff = now - date;

      const minute = 60 * 1000;
      const hour = 60 * minute;
      const day = 24 * hour;
      const week = 7 * day;

      if (diff < minute) return "Just now";
      if (diff < hour) return `${Math.floor(diff / minute)}m ago`;
      if (diff < day) return `${Math.floor(diff / hour)}h ago`;
      if (diff < week) return `${Math.floor(diff / day)}d ago`;
      return date.toLocaleDateString();
    },
  },
};
</script>

<style scoped>
.notification-center {
  display: grid;
  grid-template-columns: 280px 1fr;
  min-height: 100vh;
  background-color: #f5f7fa;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
}

.dark-mode {
  background-color: #121212;
  color: #e0e0e0;
}

/* Sidebar Styles */
.sidebar {
  background-color: white;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.dark-sidebar {
  background-color: #1e1e1e;
  border-right-color: #333;
}

.sidebar-header {
  padding: 24px;
  border-bottom: 1px solid #e0e0e0;
}

.dark-sidebar .sidebar-header {
  border-bottom-color: #333;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 12px;
}

.sidebar-tabs {
  flex: 1;
  padding: 16px 0;
  overflow-y: auto;
}

.sidebar-tabs button {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 12px 24px;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  gap: 12px;
  font-size: 15px;
  color: #555;
  transition: all 0.2s ease;
}

.dark-sidebar .sidebar-tabs button {
  color: #aaa;
}

.sidebar-tabs button i {
  width: 24px;
  text-align: center;
}

.sidebar-tabs button.active {
  color: #4361ee;
  background-color: rgba(67, 97, 238, 0.1);
  font-weight: 500;
}

.dark-sidebar .sidebar-tabs button.active {
  color: #6d8aff;
  background-color: rgba(109, 138, 255, 0.1);
}

.sidebar-tabs button .badge {
  margin-left: auto;
  background-color: #4361ee;
  color: white;
  border-radius: 10px;
  padding: 2px 8px;
  font-size: 12px;
  font-weight: 500;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #e0e0e0;
}

.dark-sidebar .sidebar-footer {
  border-top-color: #333;
}

.mark-all-read {
  width: 100%;
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  background-color: #4361ee;
  color: white;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background-color 0.2s ease;
}

.mark-all-read:hover {
  background-color: #3a56d4;
}

.mark-all-read:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* Main Content Styles */
.main-content {
  padding: 24px;
  overflow-y: auto;
  max-height: 100vh;
}

.filter-bar {
  margin-bottom: 24px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 24px;
  align-items: center;
}

.search-box {
  position: relative;
  max-width: 500px;
}

.search-box i {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

.search-box input {
  width: 100%;
  padding: 12px 16px 12px 44px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 15px;
  transition: all 0.2s ease;
}

.dark-mode .search-box input {
  background-color: #2a2a2a;
  border-color: #444;
  color: #e0e0e0;
}

.search-box input:focus {
  outline: none;
  border-color: #4361ee;
  box-shadow: 0 0 0 2px rgba(67, 97, 238, 0.2);
}

.filter-controls {
  display: flex;
  gap: 16px;
}

.filter-group,
.sort-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label,
.sort-group label {
  font-size: 14px;
  color: #666;
}

.dark-mode .filter-group label,
.dark-mode .sort-group label {
  color: #999;
}

.filter-group select,
.sort-group select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ddd;
  background-color: white;
  font-size: 14px;
  cursor: pointer;
}

.dark-mode .filter-group select,
.dark-mode .sort-group select {
  background-color: #2a2a2a;
  border-color: #444;
  color: #e0e0e0;
}

/* Notification Grid Styles */
.notification-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 20px;
}

.notification-card {
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
  border-left: 4px solid transparent;
  display: flex;
  flex-direction: column;
}

.dark-mode .notification-card {
  background-color: #1e1e1e;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.notification-card.unread {
  border-left-color: #4361ee;
  background-color: #f8faff;
}

.dark-mode .notification-card.unread {
  background-color: #1a223f;
}

.notification-card.priority {
  box-shadow: 0 0 0 2px rgba(255, 196, 0, 0.3);
}

.notification-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.dark-mode .notification-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.notification-card.music {
  border-top: 4px solid #4361ee;
}

.notification-card.social {
  border-top: 4px solid #4cc9f0;
}

.notification-card.system {
  border-top: 4px solid #7209b7;
}

.notification-header {
  padding: 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.dark-mode .notification-header {
  border-bottom-color: #333;
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4361ee;
  flex-shrink: 0;
}

.dark-mode .notification-icon {
  background-color: #333;
}

.notification-card.music .notification-icon {
  color: #4361ee;
  background-color: rgba(67, 97, 238, 0.1);
}

.notification-card.social .notification-icon {
  color: #4cc9f0;
  background-color: rgba(76, 201, 240, 0.1);
}

.notification-card.system .notification-icon {
  color: #7209b7;
  background-color: rgba(114, 9, 183, 0.1);
}

.notification-meta {
  flex: 1;
}

.notification-meta h3 {
  margin: 0 0 4px;
  font-size: 16px;
  font-weight: 600;
}

.notification-time {
  font-size: 13px;
  color: #999;
}

.dark-mode .notification-time {
  color: #777;
}

.dismiss-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.dismiss-btn:hover {
  background-color: #f0f0f0;
  color: #666;
}

.dark-mode .dismiss-btn:hover {
  background-color: #333;
  color: #e0e0e0;
}

.notification-body {
  padding: 16px;
  flex: 1;
}

.notification-message {
  margin: 0 0 16px;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.dark-mode .notification-message {
  color: #aaa;
}

/* Music Content Styles */
.music-content {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 16px;
  margin-top: 12px;
}

.album-art-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.album-art {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 1/1;
}

.album-art img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(67, 97, 238, 0.9);
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.album-art:hover .play-btn {
  opacity: 1;
}

.song-controls {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.song-controls button {
  padding: 6px 8px;
  border-radius: 6px;
  border: none;
  background-color: #f0f0f0;
  color: #333;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.dark-mode .song-controls button {
  background-color: #333;
  color: #e0e0e0;
}

.song-controls button:hover {
  background-color: #e0e0e0;
}

.dark-mode .song-controls button:hover {
  background-color: #444;
}

.song-details {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.song-details h4 {
  margin: 0 0 4px;
  font-size: 16px;
}

.song-details p {
  margin: 0 0 8px;
  color: #666;
  font-size: 14px;
}

.dark-mode .song-details p {
  color: #aaa;
}

.song-stats {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #999;
}

.song-stats i {
  margin-right: 4px;
}

/* Social Content Styles */
.social-content {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-top: 12px;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.dark-mode .social-content {
  background-color: #252525;
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info {
  flex: 1;
}

.user-info h4 {
  margin: 0 0 4px;
  font-size: 15px;
}

.user-info p {
  margin: 0;
  font-size: 13px;
  color: #666;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.dark-mode .user-info p {
  color: #aaa;
}

.follow-btn {
  padding: 8px 12px;
  border-radius: 6px;
  border: none;
  background-color: #4cc9f0;
  color: white;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.follow-btn:hover {
  background-color: #3ab7dd;
}

/* Notification Footer Styles */
.notification-footer {
  padding: 12px 16px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dark-mode .notification-footer {
  border-top-color: #333;
}

.mark-read-btn {
  padding: 6px 12px;
  border-radius: 6px;
  border: none;
  background-color: #f0f0f0;
  color: #333;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.dark-mode .mark-read-btn {
  background-color: #333;
  color: #e0e0e0;
}

.mark-read-btn:hover {
  background-color: #e0e0e0;
}

.dark-mode .mark-read-btn:hover {
  background-color: #444;
}

.notification-tags {
  display: flex;
  gap: 8px;
}

.tag {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.priority-tag {
  background-color: #fff3bf;
  color: #e67700;
}

.dark-mode .priority-tag {
  background-color: #332800;
  color: #ffc107;
}

.type-tag {
  background-color: #f0f0f0;
  color: #666;
  text-transform: capitalize;
}

.dark-mode .type-tag {
  background-color: #333;
  color: #aaa;
}

/* Empty State Styles */
.empty-state {
  grid-column: 1 / -1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-state-content {
  max-width: 400px;
}

.empty-state i {
  font-size: 48px;
  color: #ccc;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 600;
}

.empty-state p {
  margin: 0 0 16px;
  color: #999;
  font-size: 15px;
}

.refresh-btn {
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  background-color: #4361ee;
  color: white;
  font-size: 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background-color: #3a56d4;
}

/* Responsive Adjustments */
@media (max-width: 1200px) {
  .notification-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  }
}

@media (max-width: 992px) {
  .notification-center {
    grid-template-columns: 240px 1fr;
  }

  .filter-bar {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .notification-center {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none;
  }

  .music-content {
    grid-template-columns: 100px 1fr;
  }
}

@media (max-width: 576px) {
  .notification-grid {
    grid-template-columns: 1fr;
  }

  .main-content {
    padding: 16px;
  }

  .music-content {
    grid-template-columns: 1fr;
  }

  .album-art-container {
    flex-direction: row;
    align-items: center;
  }

  .song-controls {
    flex-direction: row;
  }
}
</style>
