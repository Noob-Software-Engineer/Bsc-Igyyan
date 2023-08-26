<template>
    <div class="user-card">
      <h3>{{ user.username }}</h3>
      <p>Skills: {{ user.skills.join(', ') }}</p>
      <p>LinkedIn: <a :href="user.linkedin">{{ user.linkedin }}</a></p>
    </div>
</template>
  
<script>
  export default {
    props: {
      user: Object, // Passed in as a prop from the parent component
    },
  };
</script>
  
<style scoped>
  .user-card {
    border: 1px solid #ccc;
    padding: 16px;
    margin: 16px;
    border-radius: 8px;
  }
</style>