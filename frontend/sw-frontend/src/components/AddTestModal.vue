<template>
  <div class="modal fade show d-block" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title">Add New Test</h2>
          <button type="button" class="close" @click="closeModal">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="addTest">
            <!-- Form inputs for Test data -->
            <div class="form-group">
              <label for="title">Title:</label>
              <input type="text" class="form-control" v-model="title" required>
            </div>
            <div class="form-group">
              <label for="content">Content:</label>
              <input type="text" class="form-control" v-model="content" required>
            </div>
            <div class="form-group">
              <label for="type">Type:</label>
              <select class="form-control" v-model="selectedType">
                <option v-for="type in availableType" :key="type" :value="type">{{ type }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="tags">Tags:</label>
              <select class="form-control" v-model="selectedTags" multiple>
                <option v-for="tag in availableTags" :key="tag" :value="tag">{{ tag }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="review">Review:</label>
              <select class="form-control" v-model="selectedReview">
                <option v-for="score in reviewScores" :key="score" :value="score">{{ score }}</option>
              </select>
            </div>
            <div class="text-center">
              <button type="submit" class="btn btn-primary">Add Test</button>
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