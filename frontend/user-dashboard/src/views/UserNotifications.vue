<template>
  <div class="notifications-container">
    <h2 v-if="notifications.length > 0">Your Notifications</h2>
    <div v-else class="empty-notifications">
      <p>No new notifications</p>
    </div>

    <div class="notification-list">
      <div 
        v-for="(notification, index) in notifications" 
        :key="index" 
        class="notification-item"
        :class="{
          'unread': !notification.read,
          'notification-new-activity': notification.type === 'new-sign-in',
          'notification-security': notification.type === 'password-change',
          'notification-new-content': notification.type === 'new-playlist' || 
                                      notification.type === 'new-song',
          'notification-feature': notification.type === 'new-feature'
        }"
        @click="markAsRead(notification.id)"
      >
        <div class="notification-icon">
          <i v-if="notification.type === 'new-sign-in'" class="fas fa-user-shield"></i>
          <i v-if="notification.type === 'password-change'" class="fas fa-lock"></i>
          <i v-if="notification.type === 'new-playlist'" class="fas fa-list-music"></i>
          <i v-if="notification.type === 'new-song'" class="fas fa-music"></i>
          <i v-if="notification.type === 'new-feature'" class="fas fa-star"></i>
        </div>
        
        <div class="notification-content">
          <h3>{{ notification.title }}</h3>
          <p>{{ notification.message }}</p>
          <small class="notification-time">{{ formatTime(notification.timestamp) }}</small>
        </div>
        
        <button 
          class="notification-dismiss" 
          @click.stop="dismissNotification(notification.id)"
        >
          &times;
        </button>
      </div>
    </div>
    
    <button 
      v-if="notifications.length > 0" 
      class="clear-all-btn" 
      @click="clearAllNotifications"
    >
      Clear All Notifications
    </button>
  </div>
</template>

<script>
export default {
  name: 'NotificationCenter',
  data() {
    return {
      notifications: [
        {
          id: 1,
          type: 'new-sign-in',
          title: 'New Sign-In Activity',
          message: 'Your account was accessed from a new device in New York, NY.',
          timestamp: new Date(Date.now() - 3600000),
          read: false
        },
        {
          id: 2,
          type: 'password-change',
          title: 'Password Changed',
          message: 'Your account password was successfully updated.',
          timestamp: new Date(Date.now() - 86400000),
          read: false
        },
        {
          id: 3,
          type: 'new-playlist',
          title: 'New Playlist Available',
          message: 'Check out the new "Summer Hits 2023" playlist curated for you!',
          timestamp: new Date(Date.now() - 172800000),
          read: true
        },
        {
          id: 4,
          type: 'new-song',
          title: 'Check Out This New Song',
          message: 'Your favorite artist just released a new single!',
          timestamp: new Date(Date.now() - 259200000),
          read: true
        },
        {
          id: 5,
          type: 'new-feature',
          title: 'New Feature Available',
          message: 'Try our new collaborative playlist feature!',
          timestamp: new Date(Date.now() - 604800000),
          read: true
        }
      ]
    }
  },
  methods: {
    formatTime(timestamp) {
      // Format the time as "X hours/days ago"
      const now = new Date();
      const diff = now - timestamp;
      
      const seconds = Math.floor(diff / 1000);
      const minutes = Math.floor(seconds / 60);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);
      
      if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
      if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
      if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
      return 'Just now';
    },
    markAsRead(id) {
      const notification = this.notifications.find(n => n.id === id);
      if (notification) {
        notification.read = true;
      }
    },
    dismissNotification(id) {
      this.notifications = this.notifications.filter(n => n.id !== id);
    },
    clearAllNotifications() {
      this.notifications = [];
    }
  }
}
</script>

<style scoped>
.notifications-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.empty-notifications {
  text-align: center;
  padding: 40px 0;
  color: #888;
}

.notification-list {
  margin-top: 20px;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.notification-item.unread {
  background-color: #f0f7ff;
  border-left: 4px solid #4a90e2;
}

.notification-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.notification-new-activity {
  border-left: 4px solid #ff6b6b;
}

.notification-security {
  border-left: 4px solid #4ecdc4;
}

.notification-new-content {
  border-left: 4px solid #ff9f43;
}

.notification-feature {
  border-left: 4px solid #a55eea;
}

.notification-icon {
  font-size: 20px;
  margin-right: 15px;
  color: #555;
}

.notification-content {
  flex: 1;
}

.notification-content h3 {
  margin: 0 0 5px 0;
  font-size: 16px;
  color: #333;
}

.notification-content p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.notification-time {
  display: block;
  margin-top: 5px;
  color: #999;
  font-size: 12px;
}

.notification-dismiss {
  background: none;
  border: none;
  font-size: 18px;
  color: #999;
  cursor: pointer;
  padding: 0 5px;
}

.notification-dismiss:hover {
  color: #ff6b6b;
}

.clear-all-btn {
  display: block;
  width: 100%;
  padding: 10px;
  margin-top: 20px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 5px;
  color: #555;
  cursor: pointer;
  transition: background-color 0.2s;
}

.clear-all-btn:hover {
  background-color: #e0e0e0;
}
</style>