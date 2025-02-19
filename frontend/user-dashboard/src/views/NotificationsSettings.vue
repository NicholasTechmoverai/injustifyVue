<template>
  <div  class="notifications-container">
    <!-- Header -->
    <div class="notifications-header">
      <h2>Notifications</h2>
    </div>

    <div class="notifications-body">
      <!-- Email Notifications Section -->
      <div class="notifications-section">
        <h3>Email Alerts</h3>
        <div class="notifications-content">
          <h2 class="section-title">Email me when:</h2>
          <div class="toggle-group">
            <div v-for="(option, key) in emailNotifications" :key="key">
              <label class="toggle">
                <span>{{ option.label }}</span>
                <input type="checkbox" v-model="emailNotifications[key].enabled">
                <span class="slider"></span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Device Notifications Section -->
      <div class="notifications-section">
        <h3>Device Notifications</h3>
        <div class="notifications-content">
          <div class="toggle-group">
            <div v-for="(option, key) in deviceNotifications" :key="key">
              <label class="toggle">
                <span>{{ option.label }}</span>
                <input type="checkbox" v-model="deviceNotifications[key].enabled">
                <span class="slider"></span>
              </label>
            </div>
          </div>
          <div class="toggle-sound">
            <label class="toggle">
              <span>Enable sound alerts</span>
              <input type="checkbox" v-model="enableSoundAlerts">
              <span class="slider"></span>
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "NotificationSettings",

  props: {
    currentView: String,
  },
  data() {
    return {
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
    };
  },
};
</script>

<style scoped>
/* General Container */
.notifications-container {
  width: 100%;
  max-width: 600px;
  padding: 10px;
  border-radius: 10px;
  background-color: #e9e9e9;
  box-sizing: border-box;
}

/* Section Styling */
.notifications-header {
  text-align: center;
  margin-bottom: 20px;
}

.notifications-section {
  margin-bottom: 20px;
  padding: 15px;
  background: #f4f4f4;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

/* Toggle Buttons */
.toggle-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toggle {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #e9e9e9;
  padding: 8px 12px;
  border-radius: 5px;
}

.toggle input {
  display: none;
}

.toggle .slider {
  width: 40px;
  height: 20px;
  background: #ccc;
  border-radius: 20px;
  position: relative;
  transition: background 0.3s ease;
}

.toggle input:checked + .slider {
  background: #4caf50;
}
</style>
