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
              <select class="form-control" v-model="selectedTags" multiple>
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
      const selectedTags = ref([]);
      const availableTags = ['JOB', 'INTERNSHIP', 'APTITUDE', 'PROGRAMMING', 'INTERVIEW_TIPS', 'RESUME_BUILDING', 'CAREER_ADVICE']
  

      const addPost = async () => {
        const newPost = {
            title: title.value,
            content: content.value,
            tags: selectedTags.value, // Pass the selected tags
        };

        try {
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
                emit('add', newPost);
                title.value = '';
                content.value = '';
                selectedTags.value = []; // Emit the 'add' event to the parent component
                closeModal();
            } else {
                console.error('Error adding post:', response.statusText);
            }
        } catch (error) {
            console.error('Error adding post:', error);
        }
      };
  
      const closeModal = () => {
        emit('close');
      };
  
      return {
        title,
        addPost,
        closeModal,
        selectedTags,
      };
    },
  };
  </script>
  
<style scoped>
</style>
  