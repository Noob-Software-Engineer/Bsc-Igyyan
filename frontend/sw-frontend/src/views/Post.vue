<template>
  <div>
    <navbar></navbar>
    <div class="container">
      <h1 class="my-4">Posts</h1>
      <div class="mb-4">
        <search-bar-post :delay="500"></search-bar-post>
      </div>
      <ul class="list-group">
        <li v-for="post in posts.posts" :key="post.id" class="list-group-item">
          <router-link :to='"/posts/" + post.id'>{{ post.title }}</router-link>
          <p class="mb-0">Username: {{ post.created_by.display_name }}</p>
          <p>Tags: {{ post.tag}}</p>
        </li>
      </ul>
      <button @click="showAddPostModal = true" class="btn btn-primary mt-4">Add New Post</button>
      <!-- Add Post Modal -->
      <add-post-modal v-if="showAddPostModal" @add="addPost" @close="showAddPostModal = false" />
    </div>
  </div>
</template>
  
<script>
  import { onMounted,ref, computed } from 'vue';
  import { useStore } from 'vuex';
  import AddPostModal from '@/components/AddPostModal.vue';
  import SearchBarPost from '@/components/SearchBarPost.vue';
  import Navbar from '@/components/Navbar.vue';
  
  export default {
    name: 'Posts',
    components: {
    AddPostModal,
    SearchBarPost,
    Navbar,
},
    setup() {
      const store = useStore();
      const posts = computed(() => store.state.posts);
      const showAddPostModal = ref(false);

      onMounted(async () => {
        await store.dispatch('fetchPosts')
      })
      const addPost = async (newPost) => {
        try {
        // Send the new post data to the backend
        const url = 'http://localhost:5000/posts'; 
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newPost),
        });

        if (response.ok) {
          store.dispatch('fetchPosts');
          showAddPostModal.value = false; // Close the modal
        } else {
          console.error('Error adding post:', response.statusText);
        }
      } catch (error) {
        console.error('Error adding post:', error);
      }
      };
  
      return {
        posts,
        showAddPostModal,
        addPost
      };
    },
  };
</script>


<style>
</style>