<template>
  <div class="modal fade show d-block" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title">Edit Post</h2>
          <button type="button" class="close" @click="closeModal">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="editPost">
            <div class="form-group">
              <label for="content">Content:</label>
              <input type="text" class="form-control" v-model="editedContent" required>
            </div>
            <div class="text-center">
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
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