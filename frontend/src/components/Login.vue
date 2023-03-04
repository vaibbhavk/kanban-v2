<template>

    <div class="p-3">
        <h1 class="display-6 mb-4">Sign in</h1>
        <form class="row g-3" @submit.prevent="loginUser">
            <div class="col-12">
                <label for="email" class="form-label">Email</label>
                <input v-model="loginFormData.email" type="email" class="form-control" id="email" name="email" required>
            </div>
            <div class="col-12">
                <label for="password" class="form-label">Password</label>
                <input v-model="loginFormData.password" type="password" class="form-control" id="password"
                    name="password" required>
            </div>
            <div class="col-12">
                <button type="submit" class="btn btn-primary">Sign in</button>
            </div>
        </form>

        <div class="mt-4">
            <label for="does-not-exist" class="form-label">Don't have an account?&nbsp;</label>
            <router-link to="/register">Sign up</router-link>
        </div>

    </div>


</template>

<script>
import customFetch from '@/utils/customFetch'


export default {
    name: 'Login',
    data: function () {
        return {
            loginFormData: {
                email: "",
                password: "",
            }
        }
    },
    computed: {

    },
    methods: {
        loginUser(e) {
            this.login()
        },
        login() {
            // Login user with email and password
            customFetch("http://localhost:5000/api/user/login", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.loginFormData)
            }).then(data => {
                localStorage.setItem("user", data.username)
                localStorage.setItem("token", data.token)
                this.$store.dispatch('changeAuthState', {
                    value: true
                })
                this.$router.push('/')
                this.loginFormData = {
                    ...this.loginFormData,
                    email: "",
                    password: ""
                }
            }).catch(error => alert(error.message)
            )
        }
    },

}
</script>