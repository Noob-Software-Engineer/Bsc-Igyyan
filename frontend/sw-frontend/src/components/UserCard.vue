<template>
  <div class="card user-card">
    <div class="card-body">
      <h3 class="card-title">{{ user.username }}</h3>
      <p class="card-text">Skills: {{ user.skills.join(', ') }}</p>
      <p class="card-text">
        LinkedIn:
        <a :href="user.linkedin" target="_blank" class="btn btn-primary">Visit LinkedIn</a>
      </p>
    </div>
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