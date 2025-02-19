<template>
    <div>
      <h3>History for {{ useremail }}</h3>
      <ul>
        <li v-for="item in history" :key="item.id">{{ item.action }} - {{ item.date }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: "UserHistory",
    props: ['useremail'],
    data() {
      return { history: [] };
    },
    mounted() {
      axios.get(`http://127.0.0.1:5000/api/history/${this.useremail}`)
        .then(response => this.history = response.data.history)
        .catch(error => console.error(error));
    }
  };
  </script>
  