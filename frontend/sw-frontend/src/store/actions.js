import state from "./state";
const BASE_URL = import.meta.env.VITE_API

export default {
  
    async fetchPosts({commit}) {
      try {
        const token = localStorage.getItem('token'); 
        const headers = {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json', 
        };
  
        const response = await fetch(`${BASE_URL}/posts`, {
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
        const token = localStorage.getItem('token'); 
        const headers = {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json', 
        };
  
        const response = await fetch(`${BASE_URL}/tests`, {
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
        const token = localStorage.getItem('token'); 
        const headers = {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json', 
        };
  
        const response = await fetch(`${BASE_URL}/auth`, {
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