<template>
  <div
    class="notifications-container"
    :class="{ 'dark-mode': isDarkMode, collabsedBig: iscollapsedBig }"
  >
    <!-- Header -->
    <div class="notifications-header">
      <h2 class="notifications-title">
        <i class="fas fa-bell"></i> Notification Settings
      </h2>
      <div class="header-actions">
        <button class="save-btn" @click="saveSettings">
          <i class="fas fa-save"></i> Save Changes
        </button>
        <button class="reset-btn" @click="resetToDefaults">
          <i class="fas fa-undo"></i> Reset Defaults
        </button>
      </div>
    </div>

    <div class="notifications-body">
      <!-- Email Notifications Section -->
      <div class="notifications-section">
        <div class="section-header">
          <i class="fas fa-envelope"></i>
          <h3>Email Notifications</h3>
          <div class="section-status">
            {{ emailStatus }}
          </div>
        </div>

        <div class="section-description">
          <p>Customize which email alerts you receive from our service</p>
        </div>

        <div class="notification-options">
          <div
            v-for="(option, key) in emailNotifications"
            :key="key"
            class="notification-item"
          >
            <div class="notification-info">
              <h4 class="notification-label">{{ option.label }}</h4>
              <p class="notification-description">{{ getEmailDescription(key) }}</p>
            </div>
            <label class="toggle-switch">
              <input
                type="checkbox"
                v-model="emailNotifications[key].enabled"
                @change="updateEmailStatus"
              />
              <span class="slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Push Notifications Section -->
      <div class="notifications-section">
        <div class="section-header">
          <i class="fas fa-mobile-alt"></i>
          <h3>Push Notifications</h3>
          <div class="section-status">
            {{ pushStatus }}
          </div>
        </div>

        <div class="section-description">
          <p>Manage notifications that appear on your devices</p>
        </div>

        <div class="notification-options">
          <div
            v-for="(option, key) in deviceNotifications"
            :key="key"
            class="notification-item"
          >
            <div class="notification-info">
              <h4 class="notification-label">{{ option.label }}</h4>
              <p class="notification-description">{{ getPushDescription(key) }}</p>
            </div>
            <label class="toggle-switch">
              <input
                type="checkbox"
                v-model="deviceNotifications[key].enabled"
                @change="updatePushStatus"
              />
              <span class="slider"></span>
            </label>
          </div>
        </div>

        <div class="sound-settings">
          <div class="sound-info">
            <h4 class="sound-label"><i class="fas fa-volume-up"></i> Sound Alerts</h4>
            <p class="sound-description">Play sounds when notifications arrive</p>
          </div>
          <label class="toggle-switch large">
            <input type="checkbox" v-model="enableSoundAlerts" />
            <span class="slider"></span>
          </label>
        </div>

        <div v-if="enableSoundAlerts" class="sound-options">
          <label>Notification Sound</label>
          <div class="sound-selector">
            <div
              v-for="sound in notificationSounds"
              :key="sound.id"
              class="sound-option"
              :class="{ selected: selectedSound === sound.id }"
              @click="selectSound(sound.id)"
            >
              <div class="sound-preview" @click.stop="playSound(sound.file)">
                <i class="fas fa-play"></i>
              </div>
              <span>{{ sound.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Do Not Disturb Section -->
      <div class="notifications-section">
        <div class="section-header">
          <i class="fas fa-moon"></i>
          <h3>Do Not Disturb</h3>
        </div>

        <div class="section-description">
          <p>Silence notifications during specific hours</p>
        </div>

        <div class="dnd-settings">
          <label class="toggle-item large">
            <input type="checkbox" v-model="enableDND" class="toggle-input" />
            <span class="toggle-slider"></span>
            <span class="toggle-label">Enable Do Not Disturb</span>
          </label>

          <div v-if="enableDND" class="dnd-time-range">
            <div class="time-selector">
              <label>From</label>
              <select v-model="dndStartTime" class="time-select">
                <option v-for="(time, index) in times" :key="index" :value="time">
                  {{ time }}
                </option>
              </select>
            </div>
            <div class="time-selector">
              <label>To</label>
              <select v-model="dndEndTime" class="time-select">
                <option v-for="(time, index) in times" :key="index" :value="time">
                  {{ time }}
                </option>
              </select>
            </div>
          </div>

          <div v-if="enableDND" class="dnd-exceptions">
            <h4>Exceptions</h4>
            <div class="exception-options">
              <label class="exception-item">
                <input type="checkbox" v-model="dndAllowCalls" />
                <span class="exception-label">Allow calls from contacts</span>
              </label>
              <label class="exception-item">
                <input type="checkbox" v-model="dndAllowMessages" />
                <span class="exception-label">Allow direct messages</span>
              </label>
              <label class="exception-item">
                <input type="checkbox" v-model="dndAllowUrgent" />
                <span class="exception-label">Allow urgent notifications</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import { useUserStore } from "@/store/index.js";
import socket from "@/services/websocket";

export default {
  name: "NotificationSettings",

  props: {
    currentView: String,
  },

  data() {
    const userStore = useUserStore();
    return {
      userId: computed(() => userStore.userId),
      emailNotifications: {
        newSignIn: { label: "New sign-in activity", enabled: true },
        newFeatures: { label: "New features and updates", enabled: true },
        newGifts: { label: "When I receive gifts", enabled: true },
        weeklyReport: { label: "Weekly summary report", enabled: false },
      },
      deviceNotifications: {
        allNotifications: { label: "All notifications", enabled: true },
        newLikes: { label: "New likes or reactions", enabled: true },
        newComments: { label: "Comments on my posts", enabled: true },
        onlyNewNoty: { label: "Only new notifications", enabled: false },
      },
      enableSoundAlerts: true,
      selectedSound: "chime",
      notificationSounds: [
        { id: "chime", name: "Gentle Chime", file: "chime.mp3" },
        { id: "ding", name: "Classic Ding", file: "ding.mp3" },
        { id: "bell", name: "Soft Bell", file: "bell.mp3" },
        { id: "none", name: "No Sound", file: null },
      ],
      enableDND: false,
      dndStartTime: "10:00 PM",
      dndEndTime: "7:00 AM",
      dndAllowCalls: true,
      dndAllowMessages: false,
      dndAllowUrgent: true,
      times: [
        "12:00 AM",
        "12:30 AM",
        "1:00 AM",
        "1:30 AM",
        "2:00 AM",
        "2:30 AM",
        "3:00 AM",
        "3:30 AM",
        "4:00 AM",
        "4:30 AM",
        "5:00 AM",
        "5:30 AM",
        "6:00 AM",
        "6:30 AM",
        "7:00 AM",
        "7:30 AM",
        "8:00 AM",
        "8:30 AM",
        "9:00 AM",
        "9:30 AM",
        "10:00 AM",
        "10:30 AM",
        "11:00 AM",
        "11:30 AM",
        "12:00 PM",
        "12:30 PM",
        "1:00 PM",
        "1:30 PM",
        "2:00 PM",
        "2:30 PM",
        "3:00 PM",
        "3:30 PM",
        "4:00 PM",
        "4:30 PM",
        "5:00 PM",
        "5:30 PM",
        "6:00 PM",
        "6:30 PM",
        "7:00 PM",
        "7:30 PM",
        "8:00 PM",
        "8:30 PM",
        "9:00 PM",
        "9:30 PM",
        "10:00 PM",
        "10:30 PM",
        "11:00 PM",
        "11:30 PM",
      ],
      isDarkMode: computed(() => userStore.isdarkmode),
    };
  },

  computed: {
    emailStatus() {
      const enabledCount = Object.values(this.emailNotifications).filter(
        (opt) => opt.enabled
      ).length;
      return `${enabledCount}/${Object.keys(this.emailNotifications).length} enabled`;
    },
    pushStatus() {
      const enabledCount = Object.values(this.deviceNotifications).filter(
        (opt) => opt.enabled
      ).length;
      return `${enabledCount}/${Object.keys(this.deviceNotifications).length} enabled`;
    },
  },

  methods: {
    getEmailDescription(key) {
      const descriptions = {
        newSignIn: "Get notified when someone signs in to your account from a new device",
        newFeatures: "Receive updates about new features and improvements",
        newGifts: "Alert me when I receive gifts or rewards",
        weeklyReport: "Weekly summary of your account activity",
      };
      return descriptions[key] || "";
    },
    getPushDescription(key) {
      const descriptions = {
        allNotifications: "Receive all types of push notifications",
        newLikes: "Notify me when someone likes or reacts to my content",
        newComments: "Alert me about new comments on my posts",
        onlyNewNoty: "Only show notifications I haven't seen elsewhere",
      };
      return descriptions[key] || "";
    },
    updateEmailStatus() {
      // Additional logic when email notifications change
    },
    updatePushStatus() {
      // Additional logic when push notifications change
    },
    selectSound(soundId) {
      this.selectedSound = soundId;
    },
    playSound(soundFile) {
      if (soundFile) {
        // Play sound logic
        console.log(`Playing sound: ${soundFile}`);
      }
    },
    saveSettings() {
      // Save settings logic
      console.log("Settings saved");
      socket.emit("updateNotificationSettings", {
        userId: this.userId,
        emailNotifications: this.emailNotifications,
        deviceNotifications: this.deviceNotifications,
        enableSoundAlerts: this.enableSoundAlerts,
        selectedSound: this.selectedSound,
        enableDND: this.enableDND,
        dndStartTime: this.dndStartTime,
        dndEndTime: this.dndEndTime,
        dndAllowCalls: this.dndAllowCalls,
        dndAllowMessages: this.dndAllowMessages,
        dndAllowUrgent: this.dndAllowUrgent,

        newSignIn:this.emailNotifications.newSignIn.enabled,
        newFeatures:this.emailNotifications.newFeatures.enabled,
        newGifts:this.emailNotifications.newGifts.enabled,
        weeklyReport:this.emailNotifications.weeklyReport.enabled,
        allNotifications:this.deviceNotifications.allNotifications.enabled,
        newLikes:this.deviceNotifications.newLikes.enabled,
        newComments:this.deviceNotifications.newComments.enabled,
        onlyNewNoty:this.deviceNotifications.onlyNewNoty.enabled,
        

      });
      socket.on("notificationSettingsUpdated", (response) => {
        if (response.success) {
          console.log("Notification settings updated successfully");
        } else {
          console.error("Failed to update notification settings");
        }
      });
    },
    resetToDefaults() {
      // Reset to defaults logic
      this.emailNotifications = {
        newSignIn: { label: "New sign-in activity", enabled: true },
        newFeatures: { label: "New features and updates", enabled: true },
        newGifts: { label: "When I receive gifts", enabled: true },
        weeklyReport: { label: "Weekly summary report", enabled: false },
      };
      this.deviceNotifications = {
        allNotifications: { label: "All notifications", enabled: true },
        newLikes: { label: "New likes or reactions", enabled: true },
        newComments: { label: "Comments on my posts", enabled: true },
        onlyNewNoty: { label: "Only new notifications", enabled: false },
      };
      this.enableSoundAlerts = true;
      this.selectedSound = "chime";
      this.enableDND = false;
      this.dndStartTime = "10:00 PM";
      this.dndEndTime = "7:00 AM";
      this.dndAllowCalls = true;
      this.dndAllowMessages = false;
      this.dndAllowUrgent = true;

      socket.emit("updateNotificationSettings", {
        emailNotifications: this.emailNotifications,
        deviceNotifications: this.deviceNotifications,
        enableSoundAlerts: this.enableSoundAlerts,
        selectedSound: this.selectedSound,
        enableDND: this.enableDND,
        dndStartTime: this.dndStartTime,
        dndEndTime: this.dndEndTime,
        dndAllowCalls: this.dndAllowCalls,
        dndAllowMessages: this.dndAllowMessages,
        dndAllowUrgent: this.dndAllowUrgent,
      });
      socket.on("notificationSettingsUpdated", (response) => {
        if (response.success) {
          console.log("Notification settings reset to defaults successfully");
        } else {
          console.error("Failed to reset notification settings");
        }
      });
      // Resetting the settings in the store
      const userStore = useUserStore();
      userStore.updateNotificationSettings({
        emailNotifications: this.emailNotifications,
        deviceNotifications: this.deviceNotifications,
        enableSoundAlerts: this.enableSoundAlerts,
        selectedSound: this.selectedSound,
        enableDND: this.enableDND,
        dndStartTime: this.dndStartTime,
        dndEndTime: this.dndEndTime,
        dndAllowCalls: this.dndAllowCalls,
        dndAllowMessages: this.dndAllowMessages,
        dndAllowUrgent: this.dndAllowUrgent,
      });

      console.log("Reset to defaults");
    },
  },
};
</script>

<style scoped>
/* Base Styles */
.notifications-container {
  --primary-color: #4285f4;
  --primary-light: #e8f0fe;
  --primary-dark: #3367d6;
  --text-primary: #202124;
  --text-secondary: #5f6368;
  --bg-color: #ffffff;
  --card-bg: #ffffff;
  --border-color: #dadce0;
  --hover-color: #f1f3f4;
  --success-color: #34a853;
  --error-color: #ea4335;
  --warning-color: #fbbc05;
  --dnd-color: #9c27b0;
  font-family: "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", sans-serif;
  background-color: var(--bg-color);
  color: var(--text-primary);
  transition: all 0.3s ease;
}

/* Dark Mode */
.notifications-container.dark-mode {
  --primary-color: #8ab4f8;
  --primary-light: #202124;
  --text-primary: #e8eaed;
  --text-secondary: #9aa0a6;
  --bg-color: #121212;
  --card-bg: #1e1e1e;
  --border-color: #3c4043;
  --hover-color: #2d2d2d;
}

/* Header Styles */
.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.notifications-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--primary-color);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

/* Button Styles */
.save-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.save-btn:hover {
  background-color: var(--primary-dark);
  transform: translateY(-1px);
}

.reset-btn {
  background-color: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.reset-btn:hover {
  background-color: var(--hover-color);
  color: var(--text-primary);
}

/* Section Styles */
.notifications-section {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
  margin-bottom: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.notifications-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  position: relative;
}

.section-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.section-header i {
  color: var(--primary-color);
  font-size: 1.25rem;
}

.section-status {
  position: absolute;
  right: 0;
  top: 0;
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  background-color: var(--border-color);
  color: var(--text-secondary);
}

.section-description {
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* Notification Options */
.notification-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.notification-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-radius: 8px;
  background-color: var(--bg-color);
  transition: background-color 0.3s;
}

.notification-item:hover {
  background-color: var(--hover-color);
}

.notification-info {
  flex: 1;
}

.notification-label {
  font-size: 0.9375rem;
  font-weight: 500;
  margin: 0 0 0.25rem;
}

.notification-description {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  margin: 0;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
  margin-left: 1rem;
}

.toggle-switch.large {
  width: 60px;
  height: 30px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--border-color);
  transition: 0.4s;
  border-radius: 24px;
}

.toggle-switch.large .slider {
  border-radius: 30px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

.toggle-switch.large .slider:before {
  height: 24px;
  width: 24px;
  left: 3px;
  bottom: 3px;
}

input:checked + .slider {
  background-color: var(--primary-color);
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.toggle-switch.large input:checked + .slider:before {
  transform: translateX(30px);
}

/* Sound Settings */
.sound-settings {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-radius: 8px;
  background-color: var(--bg-color);
  margin-bottom: 1.5rem;
}

.sound-info {
  flex: 1;
}

.sound-label {
  font-size: 0.9375rem;
  font-weight: 500;
  margin: 0 0 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sound-label i {
  color: var(--primary-color);
}

.sound-description {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  margin: 0;
}

.sound-options {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.sound-options label {
  display: block;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.sound-selector {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.75rem;
}

.sound-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.3s;
}

.sound-option:hover {
  border-color: var(--primary-color);
}

.sound-option.selected {
  border-color: var(--primary-color);
  background-color: var(--primary-light);
  color: var(--primary-color);
}

.sound-preview {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--primary-light);
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.sound-option.selected .sound-preview {
  background-color: var(--primary-color);
  color: white;
}

.sound-preview:hover {
  transform: scale(1.1);
}

.sound-option span {
  font-size: 0.8125rem;
  text-align: center;
}

/* Do Not Disturb */
.dnd-settings {
  margin-top: 1rem;
}

.toggle-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  position: relative;
}

.toggle-item.large {
  padding: 0.75rem;
  background-color: var(--primary-light);
  border-radius: 8px;
}

.toggle-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: relative;
  display: inline-block;
  width: 42px;
  height: 22px;
  background-color: var(--border-color);
  transition: 0.4s;
  border-radius: 22px;
  flex-shrink: 0;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

.toggle-input:checked + .toggle-slider {
  background-color: var(--dnd-color);
}

.toggle-input:checked + .toggle-slider:before {
  transform: translateX(20px);
}

.toggle-label {
  flex: 1;
  font-size: 0.9375rem;
}

.dnd-time-range {
  display: flex;
  gap: 1rem;
  margin: 1.5rem 0;
}

.time-selector {
  flex: 1;
}

.time-selector label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.8125rem;
  color: var(--text-secondary);
}

.time-select {
  width: 100%;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-color);
  color: var(--text-primary);
  font-size: 0.875rem;
}

.dnd-exceptions {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.dnd-exceptions h4 {
  margin: 0 0 1rem;
  font-size: 0.9375rem;
}

.exception-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.exception-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
}

.exception-item input {
  margin: 0;
}

.exception-label {
  font-size: 0.875rem;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .notifications-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .dnd-time-range {
    flex-direction: column;
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .notifications-container {
    padding: 1rem;
  }

  .sound-selector {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
