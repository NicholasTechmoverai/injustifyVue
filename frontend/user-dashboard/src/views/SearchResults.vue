<template>
  <div>
    <h3>Search Articles:</h3>

    <!-- ✅ Input Field for Live Search -->
    <input type="text" v-model="query" placeholder="Search articles..." />

    <p v-if="query">Showing results for: "{{ query }}"</p>
    <p v-else>Type to search articles.</p>

    <!-- ✅ Pass query to ResultsView -->
    <ResultsView :query="query" />
  </div>
</template>

<script>
import ResultsView from './ResultsView.vue';
import { ref } from 'vue';

export default {
  name: "SearchResults",
  components: { ResultsView },

  setup() {
    const query = ref(""); // ✅ Reactive search query

    return { query };
  }
};
</script>
