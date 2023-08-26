export default {
    setDisplayName(state, displayName) {
      state.displayName = displayName;
    },
    setRoles(state, roles) {
      state.superAdmin = roles.superAdmin;
      state.admin = roles.admin;
      state.student = roles.student;
    },
  };