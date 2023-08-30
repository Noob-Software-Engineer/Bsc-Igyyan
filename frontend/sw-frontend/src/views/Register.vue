<template>
    <div class="body">
        <div class="heading">
            <h1>Welcome to Bsc Igyyan</h1>
            <h2>Register</h2>
        </div>
        <div class="box">
            <form @submit.prevent="register">
              <label for="name">Name:</label>
              <input type="text" v-model="name" name="name" required>

              <label for="displayName">Display Name:</label>
              <input type="text" v-model="displayName" name="displayName" required>
  
              <label for="email">Email:</label>
              <input type="email" v-model="email" name="email" required>
              
              <label for="password">Password:</label>
              <input type="password" v-model="password" name="password" required>
  
              <div class="container">
                  <button type="submit">Register</button>
              </div>
              
            </form>
  
        </div>
    </div>
</template>

<script>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router'
    export default {
        setup () {
            const name = ref('')
            const displayName = ref('')
            const password = ref('')
            const email = ref('')
            const router = useRouter()
            const register = () => {
                const url = 'http://localhost:5000/auth/register'
                let data = {
                    name: name.value,
                    display_name: displayName.value,
                    password: password.value,
                    email: email.value,
                    role: 'student'
                }
                console.log(JSON.stringify(data))

                fetch(url, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(res => res.json())
                .then(data => {
                    router.push('/login')
                })
            }
        
            return {
                name,
                displayName,
                password,
                email,
                register
            }
        }
    }
</script>

<style>
</style>