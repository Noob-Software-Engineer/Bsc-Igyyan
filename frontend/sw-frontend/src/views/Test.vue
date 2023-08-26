<template>
    <div>
      <h1>Test</h1>
      <ul>
        <li v-for="test in tests" :key="test.id">
          <router-link :to="'/test/' + test.id">{{ test.title }}</router-link>
          <p>Username: {{ test.username }}</p>
          <p>Tags: {{ test.tags.join(', ') }}</p>
        </li>
      </ul>
    </div>
</template>
  
<script>
  import { computed } from 'vue';
  import { useStore } from 'vuex';
  
  export default {
    name: 'Tests',
    setup() {
      const store = useStore();
      const tests = computed(() => store.state.tests);
  
      return {
        tests,
      };
    },
  };
</script>


<style>
</style>