<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h2>Edit Test</h2>
        <form @submit.prevent="editTest">
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
      test: Object, // Pass the test to edit
    },
    emits: ['edit', 'close'],
    setup(props, { emit }) {
      const editedContent = ref(props.test.content);
  
      const editTest = () => {
        const editedTest = {
          id: props.test.id,
          content: editedContent.value,
        };
        emit('edit', editedTest);
      };
  
      const closeModal = () => {
        emit('close');
      };
  
      return {
        editedContent,
        editTest,
        closeModal,
      };
    },
  };
  </script>
  
  <style scoped>
  </style>