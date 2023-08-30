<template>
  <div>
    <navbar></navbar>
    <div class="container my-4">
      <h1>Test</h1>
      <search-bar-test :delay="500"></search-bar-test>
      <ul class="list-group">
        <li v-for="test in tests.tests" :key="test.id" class="list-group-item">
          <router-link :to="'/test/' + test.id">{{ test.title }}</router-link>
          <p>Username: {{ test.created_by.display_name }}</p>
          <p>Type: {{ test.type }}</p>
          <p>Tags: {{ test.tag }}</p>
        </li>
      </ul>
      <button class="btn btn-primary mt-2" @click="showAddTestModal = true">Add New Test</button>
      <!-- Add Test Modal -->
      <add-test-modal v-if="showAddTestModal" @add="addTest" @close="showAddTestModal = false" />
    </div>
  </div>
</template>
  
<script>
  import { onMounted,ref, computed } from 'vue';
  import { useStore } from 'vuex';
  import AddTestModal from '@/components/AddTestModal.vue';
  import SearchBarTest from '@/components/SearchBarTest.vue';
  import Navbar from '@/components/Navbar.vue';
  
  export default {
    name: 'Tests',
    components: {
    AddTestModal,
    SearchBarTest,
    Navbar
},
    setup() {
      const store = useStore();
      const tests = computed(() => store.state.tests);
      const showAddTestModal = ref(false);

      onMounted(async () => {
        await store.dispatch('fetchTests')
      })

      const addTest = async (newTest) => {
        try {
        // Send the new Test data to the backend
        const url = 'http://localhost:5000/tests'; 
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newTest),
        });

        if (response.ok) {
          store.dispatch('fetchTests');
          showAddTestModal.value = false; // Close the modal
        } else {
          console.error('Error adding Test:', response.statusText);
        }
      } catch (error) {
        console.error('Error adding Test:', error);
      }
      };
  
      return {
        tests,
        showAddTestModal,
        addTest
      };
    },
  };
</script>


<style>
</style>