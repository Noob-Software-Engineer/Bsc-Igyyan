<template>
  <div class="search-bar">
    <div class="input-group">
      <input
        class="form-control"
        v-model="searchTerm"
        @input="searchTests"
        placeholder="Search for tests by title..."
      />
      <div class="input-group-append">
        <button class="btn btn-primary" type="button" @click="searchTests">
          Search
        </button>
      </div>
    </div>
    <ul class="list-group mt-2" v-if="searchResults.length > 0">
      <li class="list-group-item" v-for="test in searchResults" :key="test.id">
        {{ test.title }}
      </li>
    </ul>
    <p class="mt-2" v-else>No results found.</p>
  </div>
</template>
  
<script>
  import { ref, computed, watchEffect } from 'vue';
  import { useStore } from 'vuex';
  
  export default {
    name: 'SearchBarTest',
    props: ['delay'],
    setup(props) {
      const store = useStore();
      const searchTerm = ref('');
      const searchResults = ref([]);
      
      // Create a computed property that watches the searchTerm and fetches results accordingly
      const fetchResults = computed(() => {
        // Delay search by a given time (props.delay)
        watchEffect(async () => {
          if (searchTerm.value.length >= 3) {
            // Fetch posts based on search term
            const url = `http://localhost:5000/tests/${searchTerm.value}`;
            const response = await fetch(url, {
              method: 'GET',
              headers: {
                'Authorization': `Bearer ${store.state.token.value}`,
                'Content-Type': 'application/json',
              },
            });
  
            if (response.ok) {
              const data = await response.json();
              searchResults.value = data;
            } else {
              console.error('Error fetching search results:', response.statusText);
              searchResults.value = [];
            }
          } else {
            searchResults.value = [];
          }
        });
      });
  
      return {
        searchTerm,
        searchResults,
        fetchResults,
      };
    },
  };
</script>
  
<style scoped>
/* Your component styles */
</style>