<template>
    <div>
      <h1>Posts</h1>
      <search-bar-post :delay="500"></search-bar-post>
      <ul>
        <li v-for="post in posts" :key="post.id">
          <router-link :to="'/post/' + post.id">{{ post.title }}</router-link>
          <p>Username: {{ post.username }}</p>
          <p>Tags: {{ post.tags.join(', ') }}</p>
        </li>
      </ul>
      <button @click="showAddPostModal = true">Add New Post</button>
      <!-- Add Post Modal -->
      <add-post-modal v-if="showAddPostModal" @add="addPost" @close="showAddPostModal = false" />
    </div>
</template>
  
<script>
  import { computed } from 'vue';
  import { useStore } from 'vuex';
  import AddPostModal from '@/components/AddPostModal.vue';
  import SearchBarPost from '@/components/SearchBarPost.vue';
  
  export default {
    name: 'Posts',
    components: {
    AddPostModal,
    SearchBarPost
},
    setup() {
      const store = useStore();
      const posts = computed(() => store.state.posts);
      const showAddPostModal = ref(false);

      onCreated(async () => {
        await store.dispatch('fetchPosts')
      })
      const addPost = async (newPost) => {
        try {
        // Send the new post data to the backend
        const url = 'http://localhost:5000/posts'; 
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${store.state.token.value}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newPost),
        });

        if (response.ok) {
          posts.value.push(newPost); // Add the new post to the posts array
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