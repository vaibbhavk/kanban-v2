<template>

    <div class="p-3">
        <h1 class="display-6 mb-4">Edit a list</h1>
        <form v-if="!this.loading" class="row g-3" @submit.prevent="editList">

            <div class="col-12">
                <label for="name" class="form-label">Name</label>
                <input v-model="listFormData.name" type="text" class="form-control" id="name" name="name" required>
            </div>
            <div class="col-12">
                <button type="submit" class="btn btn-primary">Update</button>
            </div>
        </form>
        <Spinner v-else />
    </div>


</template>

<script>
import customFetch from '@/utils/customFetch'
import Spinner from './Spinner.vue'



export default {
    name: "EditList",
    data: function () {
        return {
            listFormData: {
                name: "",
            },
            loading: false
        };
    },
    computed: {},
    mounted: function () {
        this.fetchListById(this.$route.params.id);
    },
    methods: {
        fetchListById(list_id) {
            this.loading = true;
            customFetch(`http://localhost:5000/api/list/${list_id}`, {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("token"),
                },
            }).then(data => {
                this.listFormData.name = data.name;
            }).catch(error => alert(error.message)).finally(() => this.loading = false);
        },
        editList(e) {
            this.edit(this.$route.params.id);
        },
        edit(list_id) {
            customFetch(`http://localhost:5000/api/list/${list_id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem("token"),
                },
                body: JSON.stringify(this.listFormData)
            }).then(data => {
                this.$router.push("/");
                this.listFormData = {
                    ...this.listFormData,
                    name: "",
                };
            }).catch(error => alert(error.message));
        }
    },
    components: { Spinner }
}
</script>