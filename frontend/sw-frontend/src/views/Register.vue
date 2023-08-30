<template>
    <div class="container">
      <div class="row justify-content-center align-items-center vh-100">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h1 class="card-title text-center mb-4">Welcome to Bsc Igyyan</h1>
              <h2 class="card-title text-center mb-4">Register</h2>
              <form @submit.prevent="register">
                <div class="mb-3">
                  <label for="name" class="form-label">Name:</label>
                  <input type="text" v-model="name" name="name" class="form-control" required>
                </div>
                <div class="mb-3">
                  <label for="displayName" class="form-label">Display Name:</label>
                  <input type="text" v-model="displayName" name="displayName" class="form-control" required>
                </div>
                <div class="mb-3">
                  <label for="email" class="form-label">Email:</label>
                  <input type="email" v-model="email" name="email" class="form-control" required>
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password:</label>
                  <input type="password" v-model="password" name="password" class="form-control" required>
                </div>
                <div class="container text-center">
                  <button type="submit" class="btn btn-primary">Register</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';
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