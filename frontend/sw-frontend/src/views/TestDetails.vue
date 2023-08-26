<template>
    <div>
      <h2>{{ test.title }}</h2>
      <p>Username: {{ test.username }}</p>
      <p>Tags: {{ test.tags.join(', ') }}</p>
      <p>{{ test.content }}</p>
    </div>
</template>
  
<script>
  import { computed } from 'vue';
  import { useStore } from 'vuex';
  
  export default {
    name: 'testDetails',
    props: ['id'],
    setup(props) {
      const store = useStore();
      const test = computed(() => store.state.tests.find(p => p.id === props.id));

      const isCurrentUser = computed(() => store.state.displayName === test.value.username);
    
      const deleteTest = async () => {
        // Make a delete request to the server to delete the profile
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

  
      return {
        test,
        isCurrentUser,
        deleteTest,
      };
    },
  };
</script>

<style>
</style>