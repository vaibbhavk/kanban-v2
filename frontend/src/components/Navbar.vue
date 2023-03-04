<template>
    <nav class="navbar sticky-top navbar-expand-lg bg-white p-2">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03"
                aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <router-link class="navbar-brand" to="/">{{ title }}</router-link>
            <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/">Dashboard</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/summary">Summary</router-link>
                    </li>
                </ul>

                <div class="me-3" v-show="this.$store.state.showExportAlert">
                    <div class="p-0 m-0 alert alert-info" role="alert">
                        Your data will be exported shortly!
                    </div>
                </div>

                <span v-if="this.$store.state.userDetail" class="navbar-text me-3">
                    Hey, {{ this.$store.state.userDetail }}!
                </span>

                <form class="row g-3 me-1" @submit.prevent="exportData"
                    v-show="this.$store.state.isAuthenticated && this.$route.name === 'dashboard'">
                    <div>
                        <button type="submit" class="btn btn-outline-primary">Export</button>
                    </div>
                </form>

                <label class="btn btn-outline-primary" for="import-file-selector"
                    v-show="this.$store.state.isAuthenticated && this.$route.name === 'dashboard'">
                    <input id="import-file-selector" @change="onFileChanged" type="file" name="file" accept=".csv"
                        class="d-none">
                    Import
                </label>

                <form class="row g-3 ms-1" @submit.prevent="logoutUser" v-show="this.$store.state.isAuthenticated">
                    <div>
                        <button type="submit" class="btn btn-outline-primary">Logout</button>
                    </div>
                </form>
            </div>
        </div>
    </nav>
</template>
  
<script>

import { saveAs } from 'file-saver'
import customFetch from '@/utils/customFetch'


export default {
    name: 'Navbar',
    props: ['title', 'fetchAllListsCardsByUser'],


    data: function () {
        return {
            selected: null,
        }
    },
    mounted() {
        if (localStorage.getItem('user')) {
            this.$store.dispatch('changeUserDetailState', {
                value: localStorage.getItem('user')
            })
        }
    },
    methods: {
        getUser() {
            customFetch('http://localhost:5000/api/user', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem("token"),
                },
            })
                .then((data) => {
                    console.log(data)
                    this.$store.dispatch('changeUserDetailState', {
                        value: data
                    })
                })
                .catch((error) => {
                    alert(error.message)
                })
        },
        logoutUser(e) {
            this.logout()
        },
        async logout() {
            customFetch('http://localhost:5000/api/user/logout', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem("token"),
                },
            })
                .then((data) => {
                    localStorage.removeItem("token")
                    localStorage.removeItem("user")
                    this.$store.dispatch('changeAuthState', {
                        value: false
                    })
                    this.$store.dispatch('changeUserDetailState', {
                        value: null
                    })
                    this.$router.push('/login')
                })
                .catch((error) => {
                    alert(error.message)
                })
        },

        exportData(e) {
            this.exportToCSV()
        },
        exportToCSV() {
            this.$store.dispatch('changeExportAlertState', {
                value: true
            })
            setTimeout(() => {
                this.$store.dispatch('changeExportAlertState', {
                    value: false
                })
            }, 3000);
            // export the user's lists and cards to csv
            customFetch("http://localhost:5000/api/export", {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem("token"),
                },
            }, 'b').then(data => {
                saveAs(data, 'export.csv')
            }).catch(error => alert(error.message))
        },
        onFileChanged(event) {
            if (event.target.files[0].type !== 'text/csv') {
                return alert("Invalid file")
            }
            if (event.target.files[0]) {
                this.uploadCSVFile(event.target.files[0])
            }
            event.target.value = ''
            // this.selected = event.target.files[0];
        },
        uploadFile(e) {
            this.uploadCSVFile(e)
        },
        uploadCSVFile(file) {
            const formData = new FormData();
            formData.append('file', file);

            customFetch("http://localhost:5000/api/import", {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem("token"),
                },
                body: formData
            }).then(data => {

            }).catch(error =>
                alert(error.message)
            ).finally(() => {
                this.fetchAllListsCardsByUser()
            })
        }

    }
}
</script>
  