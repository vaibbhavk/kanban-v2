<template>
    <div class="p-3">
        <div v-if="!this.loading">
            <h3 class="mb-4">Move cards to another list then delete the list
            </h3>
            <form class=" row g-3" @submit.prevent="moveCards">
                <div class="col-12">
                    <label for="list" class="form-label">List</label>

                    <select v-model="list" class="form-select" id="list" name="list" required>
                        <option v-for="list in lists" :value="list.list_id">
                            {{ list.name }}
                        </option>
                    </select>
                </div>

                <div class="col-12">
                    <button type="submit" class="btn btn-primary">Move and Delete</button>
                </div>
            </form>
        </div>
        <Spinner v-else />
        <div>
            <h3 class="mb-4 mt-4">Delete the list along with cards
            </h3>

            <form class="row g-3" @submit.prevent="deleteList">
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">Delete</button>
                </div>
            </form>

        </div>
    </div>

</template>

<script>
import customFetch from '@/utils/customFetch'
import Spinner from './Spinner.vue'


export default {
    name: "DeleteListConfirm",
    data: function () {
        return {
            list_id: this.$route.params.id,
            list: null,
            lists: [],
            loading: false
        };
    },
    mounted: function () {
        this.fetchAllListsCardsByUser();
    },
    methods: {
        fetchAllListsCardsByUser() {
            this.loading = true
            // fetch all the lists and cards of the logged in user
            customFetch("http://localhost:5000/api/lists", {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("token"),
                },
            }).then(data => {
                this.lists = data.filter(list => list.list_id != this.list_id);
            }).catch(error => alert(error.message)).finally(() =>
                this.loading = false
            );
        },
        moveCards(e) {
            this.move(this.list_id, this.list);
        },
        move(from_list_id, to_list_id) {
            const data = {
                from_list_id,
                to_list_id
            };
            customFetch("http://localhost:5000/api/cards", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem("token"),
                },
                body: JSON.stringify(data)
            }).then(data => {
                this.$router.push("/");
            }).catch(response => response.json().then((error) => {
                alert(error.message);
            }));
        },
        deleteList(e) {
            this.delete(this.list_id);
        },
        delete(list_id) {
            customFetch(`http://localhost:5000/api/list/${list_id}`, {
                method: "DELETE",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("token"),
                },
            }).then(response => {
                this.$router.push("/");
            }).catch(error => alert(error.message));
        },
    },
    components: { Spinner }
}
</script>