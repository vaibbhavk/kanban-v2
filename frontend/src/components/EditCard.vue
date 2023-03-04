<template>
    <div class="p-3">
        <h1 class="display-6 mb-4">Edit a card</h1>
        <form v-if="!this.loading" class="row g-3" @submit.prevent="editCard">
            <div class="col-12">
                <label for="list" class="form-label">List</label>

                <select v-model="cardFormData.list" class="form-select" id="list" name="list" required>
                    <option v-for="list in lists" :value="list.list_id">
                        {{ list.name }}
                    </option>
                </select>
            </div>

            <div class="col-12">
                <label for="title" class="form-label">Title</label>
                <input v-model="cardFormData.title" type="text" class="form-control" id="title" name="title" required>
            </div>
            <div class="col-12">
                <label for="content" class="form-label">Content</label>
                <input v-model="cardFormData.content" type="text" class="form-control" id="content" name="content">
            </div>
            <div class="col-12">
                <label for="deadline" class="form-label">Deadline</label>
                <input v-model="cardFormData.deadline" type="date" class="form-control" id="deadline" name="content"
                    required>
            </div>
            <div class="col-12">
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" v-model="cardFormData.completed" id="completed">
                    <label class="form-check-label" for="completed">
                        Completed
                    </label>
                </div>
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


const completedMapping = {
    1: true,
    0: false
}

const completedMappingRev = {
    true: 1,
    false: 0
}

export default {
    name: "EditCard",
    data: function () {
        return {
            cardFormData: {
                title: "",
                content: "",
                deadline: "",
                completed: false,
                list: 0,
            },
            list_id: this.$route.params.list_id,
            card_id: this.$route.params.card_id,
            lists: [],
            loading: false

        };
    },
    computed: {},
    mounted: function () {
        this.fetchAllListsCardsByUser();
        this.fetchCardById(this.card_id);
    },
    methods: {
        fetchAllListsCardsByUser() {
            this.loading = true;
            // fetch all the lists and cards of the logged in user
            customFetch("http://localhost:5000/api/lists", {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("token"),
                },
            }).then(data => {
                this.lists = data;
            }).catch(error => alert(error.message)).finally(() => this.loading = false);
        },
        fetchCardById(card_id) {
            customFetch(`http://localhost:5000/api/card/${card_id}`, {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("token"),
                },
            }).then(data => {
                this.cardFormData.title = data.title;
                this.cardFormData.content = data.content;
                this.cardFormData.deadline = data.deadline;
                this.cardFormData.completed = completedMapping[data.completed];
                this.cardFormData.list = data.list;
            }).catch(error => alert(error.message));
        },
        editCard(e) {
            this.edit(this.list_id, this.card_id);
        },
        edit(list_id, card_id) {
            customFetch(`http://localhost:5000/api/card/${card_id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem("token"),
                },
                body: JSON.stringify({
                    ...this.cardFormData,
                    completed: completedMappingRev[this.cardFormData.completed],
                })
            }).then(data => {
                this.$router.push("/");
                this.cardFormData = {
                    ...this.cardFormData,
                    title: "",
                    content: "",
                    deadline: "",
                    completed: false,
                    list: 0
                };
            }).catch(error => alert(error.message));
        }
    },
    components: { Spinner }
}
</script>