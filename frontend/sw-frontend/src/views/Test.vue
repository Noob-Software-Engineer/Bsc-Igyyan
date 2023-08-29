<template>
    <div>
      <search-bar-test :delay="500"></search-bar-test>
      <h1>Test</h1>
      <ul>
        <li v-for="test in tests" :key="test.id">
          <router-link :to="'/test/' + test.id">{{ test.title }}</router-link>
          <p>Username: {{ test.username }}</p>
          <p>Tags: {{ test.tags.join(', ') }}</p>
        </li>
      </ul>
      <button @click="showAddTestModal = true">Add New Test</button>
      <!-- Add Test Modal -->
      <add-test-modal v-if="showAddTestModal" @add="addTest" @close="showAddTestModal = false" />
    </div>
</template>
  
<script>
  import { computed } from 'vue';
  import { useStore } from 'vuex';
  import AddTestModal from '@/components/AddTestModal.vue';
import SearchBarTest from '@/components/SearchBarTest.vue';
  
  export default {
    name: 'Tests',
    components: {
    AddTestModal,
    SearchBarTest
},
    setup() {
      const store = useStore();
      const tests = computed(() => store.state.tests);
      const showAddTestModal = ref(false);

      onCreated(async () => {
        await store.dispatch('fetchTests')
      })

      const addTest = async (newTest) => {
        try {
        // Send the new Test data to the backend
        const url = 'http://localhost:5000/tests'; 
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${store.state.token.value}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newTest),
        });

        if (response.ok) {
          tests.value.push(newTest); // Add the new Test to the Tests array
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