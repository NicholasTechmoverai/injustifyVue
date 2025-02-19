<template>
    <div>
      <h2>Security Settings</h2>
      <div id="passwordAndSecurity">
        <label>Old Password:</label>
        <input type="password" placeholder="•••••••" />
  
        <label>New Password:</label>
        <input type="password" placeholder="•••••••" />
  
        <label>Confirm New Password:</label>
        <input type="password" placeholder="•••••••" />
  
        <button>Save</button>
      </div>
  
      <div id="twoFactorAuth">
        <h3>Two-Factor Authentication</h3>
        <label>
          <input type="checkbox" />
          Enable Two-Factor Authentication
        </label>
        <button>Generate Code</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "SecuritySettings",
  };
  </script>
  
  <style scoped>
  /* Add your styling here */
  </style>
  