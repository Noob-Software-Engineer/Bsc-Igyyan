<template>
  <div class="modal fade show d-block" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title">Create Post</h2>
          <button type="button" class="close" @click="closeModal">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="addPost">
            <!-- Form inputs for post data -->
            <div class="form-group">
              <label for="title">Title:</label>
              <input type="text" class="form-control" v-model="title" required>
            </div>
            <div class="form-group">
              <label for="content">Content:</label>
              <input type="text" class="form-control" v-model="content" required>
            </div>
            <div class="form-group">
              <label for="tags">Tags:</label>
              <select class="form-control" v-model="selectedTags">
                <option v-for="tag in availableTags" :key="tag" :value="tag">{{ tag }}</option>
              </select>
            </div>
            <div class="text-center">
              <button type="submit" class="btn btn-primary">Add Post</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
  import { ref } from 'vue';
  
  export default {
    props: {
      show: Boolean,
      availableTags: Array,
    },
    emits: ['close', 'add'],
    setup(props, { emit }) {
      const title = ref('');
      const content = ref('');
      const selectedTags = ref('');
      const availableTags = ['job', 'internship', 'aptitude', 'programming', 'interview_tips', 'resume_building', 'career_advice']
  
      const addPost = () => {
          const newPost = {
            title: title.value,
            content: content.value,
            tag: selectedTags.value, // Pass the selected tags
        };
        console.log(selectedTags.value);
        emit('add', newPost);
      }
  
      const closeModal = () => {
        emit('close');
      };
  
      return {
        title,
        content,
        addPost,
        closeModal,
        selectedTags,
        availableTags,
      };
    },
  };
  </script>
  
<style scoped>
</style>
  