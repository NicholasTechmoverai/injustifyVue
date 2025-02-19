<template>
    <div>
      <h2>Notification Settings</h2>
      <div id="email-set-Noty">
        <h3>Email Alerts</h3>
        <div id="chk-type">
          <label class="toggle">
            <span>New sign-in activity</span>
            <input type="checkbox" checked />
            <span class="slider"></span>
          </label>
          <label class="toggle">
            <span>New features and updates</span>
            <input type="checkbox" checked />
            <span class="slider"></span>
          </label>
        </div>
      </div>
  
      <div id="noty-set-Noty">
        <h3>Device Notifications</h3>
        <label class="toggle">
          <span>All notifications</span>
          <input type="checkbox" checked />
          <span class="slider"></span>
        </label>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "NotificationSettings",
  };
  </script>
  
  <style scoped>
  /* Add your styling here */
  </style>
  