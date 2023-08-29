<template>
    <nav>
      <ul>
        <li><router-link to="/posts">Posts</router-link></li>
        <li><router-link to="/tests">Tests</router-link></li>
        <li><router-link to="/social">Social</router-link></li>
        <!-- <li><router-link to="/profile">Profile</router-link></li> -->
      </ul>
    </nav>
</template>
  
<script>
  export default {
    name: 'Navbar',
  };
</script>