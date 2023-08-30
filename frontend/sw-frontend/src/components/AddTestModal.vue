<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h2>Add New Test</h2>
        <form @submit.prevent="addTest">
          <!-- Form inputs for Test data -->
          <label for="title">Title:</label>
          <input type="text" v-model="title" required>
          
          <label for="content">Content:</label>
          <input type="text" v-model="content" required>

          <label for="type">Type:</label>
          <select v-model="selectedType">
            <option v-for="type in availableType" :key="type" :value="type">{{ type }}</option>
          </select>

          <label for="tags">Tags:</label>
          <select v-model="selectedTags" multiple>
            <option v-for="tag in availableTags" :key="tag" :value="tag">{{ tag }}</option>
          </select>

          <label for="review">Review:</label>
          <select v-model="selectedReview">
            <option v-for="score in reviewScores" :key="score" :value="score">{{ score }}</option>
          </select>
          
          <button type="submit">Add Test</button>
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
      availableType: Array,
    },
    emits: ['close', 'add'],
    setup(props, { emit }) {
      const title = ref('');
      const content = ref('');
      const selectedTags = ref([]);
      const selectedType = ref('');
      const selectedReview = ref(1);

      const reviewScores = [1,2,3,4,5];
      const availableTags = ['DSA', 'DBMS', 'OS', 'OOP', 'NETWORKING', 'AI', 'ML', 'WEB_DEV', 'OTHER'];
      const availableType = ['PLACEMENT', 'PRACTICE', 'MOCK', 'OTHER'];
  

      const addTest = async () => {
        const newTest = {
            title: title.value,
            content: content.value,
            tags: selectedTags.value,
            type: selectedType.value,
            review: selectedReview.value, // Pass the selected tags
        };

        try {
            const url = 'http://localhost:5000/Tests'; 
            const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${store.state.token.value}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newTest),
            });

            if (response.ok) {
                emit('add', newTest);
                title.value = '';
                content.value = '';
                selectedTags.value = [];
                selectedType.value = '';
                selectedReview.value = 1;
                closeModal();
            } else {
                console.error('Error adding Test:', response.statusText);
            }
        } catch (error) {
            console.error('Error adding Test:', error);
        }
      };
  
      const closeModal = () => {
        emit('close');
      };
  
      return {
        title,
        addTest,
        closeModal,
        selectedTags,
        selectedType,
        selectedReview,
        reviewScores,
      };
    },
  };
  </script>
  
<style scoped>
</style>