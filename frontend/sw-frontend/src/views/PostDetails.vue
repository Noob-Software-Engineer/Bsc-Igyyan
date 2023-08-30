<template>
  <div class="container my-4">
    <h2>{{ post.title }}</h2>
    <p>Username: {{ post.created_by.display_name }}</p>
    <p>Tags: {{ post.tag }}</p>
    <p>{{ post.content }}</p> 
    <div v-if="isCurrentUserCreator">
      <button class="btn btn-danger" @click="deletePost">Delete Post</button>
      <button class="btn btn-primary" @click="showEditModal = true">Edit Post</button>
    </div>
    <!-- Edit Post Modal -->
    <edit-post-modal v-if="showEditModal" :post="post" @edit="updatePost" @close="showEditModal = false" />
  </div>
</template>
  
<script>
  import { ref, computed } from 'vue';
  import { useRouter} from 'vue-router';
  import { useStore } from 'vuex';
  import EditPostModal from '@/components/EditPostModal.vue';
  
  export default {
    name: 'PostDetails',
    props: ['id'],
    components: {
      EditPostModal
    },
    setup(props) {
      const BASE_URL = import.meta.env.VITE_API
      const store = useStore();
      const router = useRouter();
      const post = computed(() => store.state.posts.posts.find(p => p.id === props.id));
      const isCurrentUserCreator = computed(() => localStorage.getItem('display_name') === post.value.created_by.display_name);
      const showEditModal = ref(false);

      const deletePost = async () => {
         // Make a delete request to the server to delete the post
        try {
          const url = `${BASE_URL}/posts/${props.id}`;
          const response = await fetch(url, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
              'Content-Type': 'application/json',
            },
          });
          if (response.ok) {
            router.push('../posts')
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
        const url = `${BASE_URL}/posts/${props.id}`;
        const response = await fetch(url, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
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