<template>
    <div class="results-container">
      <p>Found {{ filteredTitles.length }} results for "{{ query }}"</p>
      <ul v-if="filteredTitles.length">
        <li v-for="post in filteredTitles" :key="post.id" class="result-item">
          <h4>{{ post.title }}</h4>
          <p>{{ post.description }}</p>
          <span class="tags">Tags: {{ post.tags.join(', ') }}</span>
        </li>
      </ul>
      <p v-else>No results found.</p>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue';
  import titles from '../assets/post-data.json'; // ✅ Ensure correct path
  
  export default {
    props: {
      query: String,
    },
    setup(props) {
      const filteredTitles = computed(() => {
        if (!props.query) return titles; // ✅ Show all if no input
  
        return titles.filter(post =>
          post.title.toLowerCase().includes(props.query.toLowerCase()) || 
          post.description.toLowerCase().includes(props.query.toLowerCase()) // ✅ Search both title & description
        );
      });
  
      return { filteredTitles };
    },
  };
  </script>
  
  <style scoped>
  .results-container {
    margin-top: 20px;
  }
  
  .result-item {
    border-bottom: 1px solid #ddd;
    padding: 10px 0;
  }
  
  .tags {
    font-size: 12px;
    color: #888;
  }
  </style>
  