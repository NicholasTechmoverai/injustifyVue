<template>
  <div class="error-container">
    <div class="error-box">
      <h1 class="injustifyLogoR">Injustify</h1>

      <h1 class="error-code">404</h1>
      <p class="error-message">Oops! The page you're looking for doesn't exist.</p>
      <RouterLink to="/" class="home-button">Go to Homepage</RouterLink>
    </div>
  </div>
</template>

<script>
// import { RouterLink } from "vue-router";
export default {
  name: "NotFoundPage",
};
</script>

<style scoped>
.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.error-box {
  text-align: center;
  padding: 40px;
  background: rgb(131, 128, 128);
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
}

.error-code {
  font-size: 96px;
  color: #ff4c4c;
  margin: 0;
}

.error-message {
  font-size: 18px;
  color: #555;
  margin: 20px 0;
}

.home-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #2e86de;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.home-button:hover {
  background-color: #1b4f9c;
}
</style>
