export default {
    setPosts(state, posts) {
      state.posts = posts;
    },
    setTests(state, tests) {
      state.tests = tests;
    },
    setUsers(state, users) {
      state.users = users
    },
    updatePost(state, updatedPost) {
      const index = state.posts.findIndex(post => post.id === updatedPost.id);
      if (index !== -1) {
        // Replace the old post with the updated post
        state.posts[index] = updatedPost;
      }
    },
    updateTest(state, updatedTest) {
      const index = state.tests.findIndex(test => test.id === updatedTest.id);
      if (index !== -1) {
        // Replace the old test with the updated test
        state.tests[index] = updatedTest;
      }
    },
}
