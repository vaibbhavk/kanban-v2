<template>
    <div class="card shadow my-4 mx-2">
        <div class="card-body">
            <h5 class="card-title">{{ title }}</h5>

            <p class="card-text">{{ content }}</p>
            <h6 class="card-subtitle mb-2 text-muted blockquote-footer">
                {{ deadline }}
            </h6>

            <i v-if="completed === 1" class="bi bi-check-square square-icon-style text-success"></i>
            <i v-else class="bi bi-x-square square-icon-style text-warning"></i>

            <div class="dropdown text-end">
                <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                    aria-expanded="false">
                </button>
                <ul class="dropdown-menu dropdown-menu-dark">
                    <li>
                        <router-link :to="`/card/${list_id}/edit/${card_id}`" class="dropdown-item">Edit</router-link>
                    </li>
                    <li>
                        <button class="dropdown-item" @click="deleteCard(e, card_id)">Delete</button>
                    </li>
                </ul>
            </div>
        </div>
    </div>


</template>

<script>
import customFetch from '@/utils/customFetch'

export default {
    name: 'Card',
    props: ['title', 'content', 'deadline', 'completed', "dragStarted", "card_id", "list_id", "fetchAllListsCardsByUser"],
    methods: {
        deleteCard(e, card_id) {
            this.delete(card_id)
        },
        delete(card_id) {
            customFetch(`http://localhost:5000/api/card/${card_id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem("token"),
                },
            }).then(data => {
                this.fetchAllListsCardsByUser()
            }).catch(error => alert(error.message)
            )
        },
    }
}
</script>

<style scoped>
.square-icon-style {
    font-size: 1.5rem;
}
</style>