<template>

    <div class="p-3">
        <h1 class="display-6 mb-4">Add a list</h1>
        <form class="row g-3" @submit.prevent="addList">
            <div class="col-12">
                <label for="name" class="form-label">Name</label>
                <input v-model="listFormData.name" type="text" class="form-control" id="name" name="name" required>
            </div>
            <div class="col-12">
                <button type="submit" class="btn btn-primary">Add</button>
            </div>
        </form>

    </div>


</template>

<script>
import customFetch from '@/utils/customFetch'

export default {
    name: 'AddList',
    data: function () {
        return {
            listFormData: {
                name: "",
            }
        }
    },
    computed: {

    },
    methods: {
        addList(e) {
            this.add()
        },
        add() {
            customFetch("http://localhost:5000/api/list", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem("token"),
                },
                body: JSON.stringify(this.listFormData)
            }).then(data => {
                this.$router.push('/')
                this.listFormData = {
                    ...this.listFormData,
                    name: "",
                }

            }).catch(error =>
                alert(error.message)
            )
        }
    },

}
</script>