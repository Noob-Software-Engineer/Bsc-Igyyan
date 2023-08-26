<template>
    <div>
      <h2>{{ post.title }}</h2>
      <p>Username: {{ post.username }}</p>
      <p>Tags: {{ post.tags.join(', ') }}</p>
      <p>{{ post.content }}</p> 
      <!-- Show delete button if the user is the creator -->
      <button v-if="isCurrentUserCreator" @click="deletePost">Delete Post</button>
    </div>
</template>
  
<script>
  import { computed } from 'vue';
  import { useStore } from 'vuex';
  
  export default {
    name: 'PostDetails',
    props: ['id'],
    setup(props) {
      const store = useStore();
      const post = computed(() => store.state.posts.find(p => p.id === props.id));
      const isCurrentUserCreator = computed(() => store.state.displayName === post.value.username)

      const deletePost = async () => {
         // Make a delete request to the server to delete the post
        try {
          const url = `http://localhost:5000/posts/${props.id}`;
          const response = await fetch(url, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${store.state.auth.accessToken}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            router.push('./posts')
            // Handle successful deletion, e.g., navigate back to the list
          } else {
            console.error('Error deleting post:', response.statusText);
          }
        } catch (error) {
          console.error('Error deleting post:', error);
        }
      };
  
      return {
        post,
        isCurrentUserCreator,
        deletePost,
      };
    },
  };
</script>

<style>
</style>