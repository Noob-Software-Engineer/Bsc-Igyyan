<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link" to="/posts" exact>Posts</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/tests" exact>Tests</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/social" exact>Social</router-link>
        </li>
        <!-- <li class="nav-item">
          <router-link class="nav-link" to="/profile" exact>Profile</router-link>
        </li> -->
      </ul>
    </div>
  </nav>
</template>

  
<script>
  export default {
    name: 'Navbar',
  };
</script>