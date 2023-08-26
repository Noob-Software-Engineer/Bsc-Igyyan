export default {
    setDisplayName(state, displayName) {
      state.displayName = displayName;
    },
    setRoles(state, roles) {
      state.superAdmin = roles.superAdmin;
      state.admin = roles.admin;
      state.student = roles.student;
    },
    setPosts(state, posts) {
      state.posts = posts;
    },
    setTests(state, tests) {
      state.tests = tests;
    },
    setUsers(state, users) {
      state.users = users
    }
  };