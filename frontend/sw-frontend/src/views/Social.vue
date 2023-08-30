<template>
  <div>
    <navbar></navbar>
    <div class="container mt-4">
      <h1 class="mb-4">Connect</h1>
      <div class="row">
        <user-card
          v-for="user in users"
          :key="user.id"
          :user="user"
          class="col-lg-4 col-md-6 mb-4"
        />
      </div>
    </div>
  </div>
</template>
  
<script>
  import UserCard from '@/components/UserCard.vue';
  import Navbar from '@/components/Navbar.vue';
  import { onMounted,computed } from 'vue';
  import { useStore } from 'vuex';
  
  export default {
    components: {
      UserCard,
      Navbar,
    },
    name: 'Users',
    setup() {
      const store = useStore();
      const users = computed(() => store.state.users);

      onMounted(async () => {
        await store.dispatch('fetchUsers')
      })
  
      return {
        users,
      };
    },
  };
  </script>