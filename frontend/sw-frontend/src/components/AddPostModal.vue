<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h2>Create Post</h2>
        <form @submit.prevent="addPost">
          <!-- Form inputs for post data -->
          <label for="title">Title:</label>
          <input type="text" v-model="title" required>
          
          <label for="content">Content:</label>
          <input type="text" v-model="content" required>

          <label for="tags">Tags:</label>
          <select v-model="selectedTags" multiple>
            <option v-for="tag in availableTags" :key="tag" :value="tag">{{ tag }}</option>
          </select>
          
          <button type="submit">Add Post</button>
        </form>
        <button @click="closeModal">Close</button>
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
  