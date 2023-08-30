<template>
  <div>
    <div class="container my-4">
      <h2>{{ test.title }}</h2>
      <p>Username: {{ test.created_by.display_name}}</p>
      <p>Tags: {{ test.tag}}</p>
      <p>{{ test.content }}</p>
      <div class="mt-2" v-if="isCurrentUserCreator">
        <button class="btn btn-danger mr-2" @click="deleteTest">Delete Test</button>
        <button class="btn btn-primary" @click="showEditModal = true">Edit Test</button>
      </div>
      <!-- Edit Test Modal -->
      <edit-test-modal v-if="showEditModal" :test="test" @edit="updateTest" @close="showEditModal = false" />
    </div>
  </div>
</template>
  
<script>
  import { ref, computed } from 'vue';
  import { useRouter} from 'vue-router';
  import { useStore } from 'vuex';
  import EditTestModal from '@/components/EditTestModal.vue';
  
  export default {
    name: 'testDetails',
    props: ['id'],
    components: {
      EditTestModal
    },
    setup(props) {
      const store = useStore();
      const router = useRouter();
      const test = computed(() => store.state.tests.tests.find(p => p.id === props.id));
      const showEditModal = ref(false);
      const isCurrentUserCreator = computed(() => localStorage.getItem('display_name') === test.value.created_by.display_name);
    
      const deleteTest = async () => {
        try {
          const url = `http://localhost:5000/tests/${props.id}`;
          const response = await fetch(url, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            router.push('../tests')
            // Handle successful deletion, e.g., navigate back to the home page
          } else {
            console.error('Error deleting profile:', response.statusText);
          }
        } catch (error) {
          console.error('Error deleting profile:', error);
        }
      };
      const updateTest = async (editedTest) => {
      try {
        const url = `http://localhost:5000/tests/${props.id}`;
        const response = await fetch(url, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(editedTest),
        });

        if (response.ok) {
          store.commit('updateTest', editedTest)
          Object.assign(test.value, editedTest)
          showEditModal.value = false; // Close the modal
        } else {
          console.error('Error updating test:', response.statusText);
        }
      } catch (error) {
        console.error('Error updating test:', error);
      }
    }; 

  
      return {
        test,
        isCurrentUserCreator,
        showEditModal,
        updateTest,
        deleteTest,
      };
    },
  };
</script>

<style>
</style>