<template>
  <div class="search-bar">
    <div class="input-group">
      <input
        class="form-control"
        v-model="searchTerm"
        placeholder="Search for posts by title..."
      />
      <div class="input-group-append">
        <button class="btn btn-primary" type="button" @click="fetchResults">
          Search
        </button>
      </div>
    </div>
    <ul class="list-group mt-2" v-if="searchResults.length > 0" >
      <li class="list-group-item" v-for="post in searchResults.posts" :key="post.id">
        {{ post.title }}
      </li>
    </ul>
    <p class="mt-2" v-else>No results found.</p>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'SearchBarPost',
  props: ['delay'],
  setup(props) {
    const store = useStore();
    const searchTerm = ref('');
    const searchResults = ref([]);

    // Watcher for fetching search results
    
    const fetchResults = async () => {
      if (searchTerm.value.length >= 3) {
        const url = `http://localhost:5000/posts?title=${searchTerm.value}`;
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
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
    };
    watch(searchTerm, async (newSearchTerm) => {
      if (newSearchTerm.length >= 3) {
        const url = `http://localhost:5000/posts?title=${newSearchTerm}`;
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
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

    

    return {
      searchTerm,
      searchResults,
      fetchResults
    };
  },
};
</script>

<style scoped>
/* Your component styles */
</style>
  