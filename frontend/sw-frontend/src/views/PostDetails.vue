<template>
    <div>
      <h2>{{ post.title }}</h2>
      <p>Username: {{ post.username }}</p>
      <p>Tags: {{ post.tags.join(', ') }}</p>
      <p>{{ post.content }}</p> 
      <!-- Show delete button if the user is the creator -->
      <button v-if="isCurrentUserCreator" @click="deletePost">Delete Post</button>
      <button v-if="isCurrentUserCreator" @click="showEditModal = true">Edit Post</button>
      <!-- Edit Post Modal -->
      <edit-post-modal v-if="showEditModal" :post="post" @edit="updatePost" @close="showEditModal = false" />
    </div>
</template>
  
<script>
  import { computed } from 'vue';
  import { useStore } from 'vuex';
  import EditPostModal from '../components/EditPostModal.vue';
  
  export default {
    name: 'PostDetails',
    props: ['id'],
    components: {
      EditPostModal
    },
    setup(props) {
      const store = useStore();
      const post = computed(() => store.state.posts.find(p => p.id === props.id));
      const isCurrentUserCreator = computed(() => store.state.displayName === post.value.username);
      const showEditModal = ref(false);

      const deletePost = async () => {
         // Make a delete request to the server to delete the post
        try {
          const url = `http://localhost:5000/posts/${props.id}`;
          const response = await fetch(url, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${store.state.token.value}`,
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

      const updatePost = async (editedPost) => {
      try {
        const url = `http://localhost:5000/posts/${props.id}`;
        const response = await fetch(url, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${store.state.token.value}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(editedPost),
        });

        if (response.ok) {
          store.commit('updatePost', editedPost)
          Object.assign(post.value, editedPost)
          showEditModal.value = false; // Close the modal
        } else {
          console.error('Error updating post:', response.statusText);
        }
      } catch (error) {
        console.error('Error updating post:', error);
      }
    }; 

      return {
        post,
        isCurrentUserCreator,
        showEditModal,
        updatePost,
        deletePost,
      };
    },
  };
</script>

<style>
</style>