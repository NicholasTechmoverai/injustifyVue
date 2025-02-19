<template>
    <section id="settings" class="main_tabs">
      <div id="settings-header" class="card">
        <h2>Settings</h2>
        <div id="settings-scroll-select">
          <router-link to="/settings/profile">Profile</router-link>
          <router-link to="/settings/notifications">Notifications</router-link>
          <router-link to="/settings/preferences">Preferences</router-link>
          <router-link to="/settings/security">Security</router-link>
          <div class="dropdown">
            <button>More</button>
            <div class="dropdown-content">
              <a href="#">Help</a>
              <a href="#">About</a>
              <a href="#">Feedback</a>
            </div>
          </div>
        </div>
      </div>
      <div id="settings-body">
        <router-view></router-view> <!-- Render the child route component here -->
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: "SettingsPage",
    data() {
      return {};
    },
  };
  </script>
  
  <style scoped>
  .main_tabs {
    padding: 20px;
  }
  .card {
    background: #fff;
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  #settings-scroll-select {
    display: flex;
    gap: 10px;
  }
  button {
    padding: 10px;
    border: none;
    cursor: pointer;
    background: #ddd;
    border-radius: 5px;
  }
  button.active {
    background: #007bff;
    color: white;
  }
  .dropdown {
    position: relative;
  }
  .dropdown-content {
    display: none;
    position: absolute;
    background: white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    padding: 10px;
    border-radius: 5px;
  }
  .dropdown:hover .dropdown-content {
    display: block;
  }
  </style>
  