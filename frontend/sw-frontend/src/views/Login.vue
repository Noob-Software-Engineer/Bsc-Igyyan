# Roles are not set up properly. Using boolean values, with everyone as students. Also, check the console.log(s)(there are multiple) 
# in the setup function

<template>
    <div class="body">
        <div class="heading">
            <h1>Welcome to Bsc Igyyan</h1>
            <h1>Login</h1>
        </div>
        <div class="box">
            <form @submit.prevent="login">
                <label for="displayName">Display Name:</label>
                <input type="text" v-model="displayName" name="displayName" required>

                <label for="password">Password:</label>
                <input type="password" v-model="password" name="password" required>

                <button type="submit">Log in</button>
            </form>
        </div>
    </div>
</template>


<script>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router'
    import { useStore } from 'vuex';
    import jwt_decode from "jwt-decode";
    export default {
        setup () {
            const store = useStore
            const router = useRouter()
            const displayName = ref('')
            const password = ref('')
            const login = () => {
                const url = 'http://localhost:5000/auth/login'
                let data = {
                    displayName: displayName.value,
                    password: password.value
                }

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
                    var decoded = jwt_decode(data.access_token);
                    console.log(decoded)
                    store.commit('setDisplayName', decoded.displayName)
                    store.commit('setRoles', {
                        superAdmin: false,
                        admin: false,
                        student: true,
                    })
                    
                    console.log(store)
                    localStorage.setItem('auth', decoded.auth_level)
                    localStorage.setItem('displayName', decoded.displayName)
                    
                    router.push('/')

                })
            }
        
            return {
                displayName,
                password,
                login
            }
        }
    }
</script>


<style>
</style>