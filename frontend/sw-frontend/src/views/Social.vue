<template>
    <div class="user-list">
      <h1>Connect</h1>
      <user-card v-for="user in users" :key="user.id" :user="user" />
    </div>
</template>
  
<script>
  import UserCard from '@/components/UserCard.vue';
  import { computed } from 'vue';
  import { useStore } from 'vuex';
  
  export default {
    components: {
      UserCard,
    },
    name: 'Users',
    setup() {
      const store = useStore();
      const users = computed(() => store.state.users);

      onCreated(async () => {
        await store.dispatch('fetchUsers')
      })
  
      return {
        users,
      };
    },
  };
  </script>