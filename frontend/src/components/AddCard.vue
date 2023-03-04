<template>
    <div class="p-3">
        <h1 class="display-6 mb-4">Add a card</h1>
        <form class="row g-3" @submit.prevent="addCard">
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
                <button type="submit" class="btn btn-primary">Add</button>
            </div>
        </form>

    </div>


</template>

<script>
import customFetch from '@/utils/customFetch'


const completedMapping = {
    true: 1,
    false: 0
}


export default {
    name: 'AddCard',
    data: function () {
        return {
            cardFormData: {
                title: "",
                content: "",
                deadline: "",
                completed: false,
                list: 0
            },
            list_id: this.$route.params.id
        }
    },
    computed: {

    },
    methods: {
        addCard(e) {
            this.add()
        },
        add() {
            customFetch("http://localhost:5000/api/card", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem("token"),
                },
                body: JSON.stringify({
                    ...this.cardFormData,
                    completed: completedMapping[this.cardFormData.completed],
                    list: this.list_id
                })
            }).then(data => {
                this.$router.push('/')
                this.cardFormData = {
                    ...this.cardFormData,
                    title: "",
                    content: "",
                    deadline: "",
                    completed: "",
                    list: ""
                }
            }).catch(error => { alert(error.message) }
            )
        }
    },

}
</script>
