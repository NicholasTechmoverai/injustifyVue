<template>
    <div>
      <h2>Preferences</h2>
      <div id="preferences-stcsd">
        <label class="toggle ThemeToggle">
          <span><i class="fa-solid fa-sun"></i> Light</span>
          <input type="checkbox" id="themeToggle" checked />
          <span class="slider mode-toggle"></span>
          <span><i class="fa-solid fa-moon"></i> Dark</span>
        </label>
      </div>
  
      <div id="languageSelect">
        <label>Language preference</label>
        <select>
          <option>English</option>
          <option>Spanish</option>
          <option>French</option>
        </select>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "PreferenceSettings",
  };
  </script>
  
  <style scoped>
  /* Add your styling here */
  </style>
  