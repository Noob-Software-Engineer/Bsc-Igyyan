import state from "./state";

export default {
    async fetchPosts({commit}) {
      try {
        const token = state.accessToken; 
        const headers = {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json', 
        };
  
        const response = await fetch('http://localhost:5000/posts', {
          headers,
        });
  
        if (response.ok) {
          const data = await response.json();
          commit('setPosts', data);
        } else {
          console.error('Error fetching posts:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    },

    async fetchTests({commit}) {
      try {
        const token = state.accessToken; 
        const headers = {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json', 
        };
  
        const response = await fetch('http://localhost:5000/tests', {
          headers,
        });
  
        if (response.ok) {
          const data = await response.json();
          commit('setTests', data);
        } else {
          console.error('Error fetching posts:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    },
    async fetchUsers({commit}) {
      try {
        const token = state.accessToken; 
        const headers = {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json', 
        };
  
        const response = await fetch('http://localhost:5000/users', {
          headers,
        });
  
        if (response.ok) {
          const data = await response.json();
          commit('setUsers', data);
        } else {
          console.error('Error fetching posts:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    },

  };