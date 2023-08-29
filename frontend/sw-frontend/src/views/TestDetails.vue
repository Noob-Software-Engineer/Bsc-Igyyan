<template>
    <div>
      <h2>{{ test.title }}</h2>
      <p>Username: {{ test.username }}</p>
      <p>Tags: {{ test.tags.join(', ') }}</p>
      <p>{{ test.content }}</p>
      <button v-if="isCurrentUserCreator" @click="deleteTest">Delete Test</button>
      <button v-if="isCurrentUserCreator" @click="showEditModal = true">Edit Test</button>
      <!-- Edit Test Modal -->
      <edit-test-modal v-if="showEditModal" :test="test" @edit="updateTest" @close="showEditModal = false" />
    </div>
</template>
  
<script>
  import { computed } from 'vue';
  import { useStore } from 'vuex';
  import EditTestModal from '../components/EditTestModal.vue';
  
  export default {
    name: 'testDetails',
    props: ['id'],
    components: {
      EditTestModal
    },
    setup(props) {
      const store = useStore();
      const test = computed(() => store.state.tests.find(p => p.id === props.id));
      const showEditModal = ref(false);
      const isCurrentUser = computed(() => store.state.displayName === test.value.username);
    
      const deleteTest = async () => {
        try {
          const url = `http://localhost:5000/tests/${props.id}`;
          const response = await fetch(url, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${store.state.auth.accessToken}`,
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            router.push('./tests')
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
            'Authorization': `Bearer ${store.state.auth.accessToken}`,
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
        isCurrentUser,
        showEditModal,
        updateTest,
        deleteTest,
      };
    },
  };
</script>

<style>
</style>