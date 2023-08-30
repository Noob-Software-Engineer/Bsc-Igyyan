<template>
    <div class="container">
      <div class="row justify-content-center align-items-center vh-100">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h1 class="card-title text-center mb-4">Welcome to Bsc Igyyan</h1>
              <form @submit.prevent="login">
                <div class="mb-3">
                  <label for="name" class="form-label">Name:</label>
                  <input type="text" v-model="name" name="name" class="form-control" required>
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password:</label>
                  <input type="password" v-model="password" name="password" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary">Log in</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>


<script>
    import { ref } from 'vue';
    import {useRouter} from 'vue-router';
    import { useStore } from 'vuex';
    import jwt_decode from "jwt-decode";
    export default {
        setup () {
            const store = useStore()
            const router = useRouter()
            const name = ref('')
            const password = ref('')
            const BASE_URL = import.meta.env.VITE_API
            const login = () => {
                const url = `${BASE_URL}/auth/login`
                let data = {
                    name: name.value,
                    password: password.value
                }       
                fetch(url, {
                    method: 'POST',
                    // credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data),
                })
                .then(res => res.json())
                .then(data => {
                    var decoded = jwt_decode(data.access_token);
                    localStorage.setItem('display_name', decoded.sub.name)
                    localStorage.setItem('role', decoded.sub.role)
                    localStorage.setItem('token',data.access_token);
                    console.log(store)
                    
                    router.push('/posts')

                })
            }
        
            return {
                name,
                password,
                login
            }
        }
    }
</script>


<style>
</style>