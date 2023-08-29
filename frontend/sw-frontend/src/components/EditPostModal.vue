<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h2>Edit Post</h2>
        <form @submit.prevent="editPost">
          <label for="content">Content:</label>
          <input type="text" v-model="editedContent" required>
            
          <button type="submit">Save Changes</button>
        </form>
        <button @click="closeModal">Cancel</button>
      </div>
    </div>
</template>
  
<script>
  import { ref, computed } from 'vue';
  
  export default {
    props: {
      post: Object, // Pass the post to edit
    },
    emits: ['edit', 'close'],
    setup(props, { emit }) {
      const editedContent = ref(props.post.content);
  
      const editPost = () => {
        const editedPost = {
          id: props.post.id,
          content: editedContent.value,
        };
        emit('edit', editedPost);
      };
  
      const closeModal = () => {
        emit('close');
      };
  
      return {
        editedContent,
        editPost,
        closeModal,
      };
    },
  };
  </script>
  
  <style scoped>
  </style>