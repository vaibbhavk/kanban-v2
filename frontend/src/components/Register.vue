<template>

    <div class="p-3">
        <h1 class="display-6 mb-4">Sign up</h1>
        <form class="row g-3" @submit.prevent="registerUser">
            <div class="col-12">
                <label for="username" class="form-label">Username</label>
                <input v-model="registerFormData.username" type="text" class="form-control" id="username" required>
            </div>
            <div class="col-12">
                <label for="email" class="form-label">Email</label>
                <input v-model="registerFormData.email" type="email" class="form-control" id="email" required>
            </div>
            <div class="col-12">
                <label for="password" class="form-label">Password</label>
                <input v-model="registerFormData.password" type="password" class="form-control" id="password" required>
            </div>
            <div class="col-12">
                <button type="submit" class="btn btn-primary">Sign up</button>
            </div>
        </form>

        <div class="mt-4">
            <label for="does-not-exist" class="form-label">Already have an account?&nbsp;</label>
            <router-link to="/login">Sign in</router-link>
        </div>

    </div>


</template>

<script>
import customFetch from '@/utils/customFetch'


export default {
    name: 'Register',
    data: function () {
        return {
            registerFormData: {
                username: "",
                email: "",
                password: "",
            }
        }
    },
    computed: {

    },
    methods: {
        registerUser(e) {
            this.register()
        },
        register() {
            // Register user with username, email and password
            customFetch("http://localhost:5000/api/user/register", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.registerFormData)
            }).then(data => {
                this.registerFormData = {
                    ...this.registerFormData,
                    username: "",
                    email: "",
                    password: ""
                }
                this.$router.push('/login')

            }).catch(error => alert(error.message))
        }
    },

}
</script>