<template>
    <div class="col p-3 border">
        <div class="d-flex justify-content-between text-bg-light align-items-center p-1">
            <span class="fs-4 d-inline-block text-truncate">
                {{ name }}
            </span>

            <div class="dropdown text-end">
                <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                    aria-expanded="false">
                </button>
                <ul class="dropdown-menu dropdown-menu-dark">
                    <li>
                        <router-link :to="`/list/edit/${list_id}`" class="dropdown-item">Edit</router-link>
                    </li>
                    <li>
                        <router-link :to="`/list/delete/${list_id}`" class="dropdown-item">Delete</router-link>
                    </li>
                    <li>
                        <button @click="exportDataByList(e, list_id)" class="dropdown-item">Export</button>
                    </li>
                </ul>
            </div>
        </div>

        <DropCard v-show="dragStarted" class="sticky-top" />


        <Card v-for="card in cards" :key="card.card_id" :list_id="list_id" :card_id="card.card_id" :title="card.title"
            :content="card.content" :deadline="card.deadline" :completed="card.completed"
            :fetchAllListsCardsByUser="this.fetchAllListsCardsByUser" draggable="true"
            @dragstart="startDrag($event, card)" dragStarted="dragStarted" />

        <div class="text-center p-3 mt-4">
            <router-link :to="`/card/${list_id}/add`">
                <i class="bi bi-plus-square icon-style"></i>
            </router-link>
        </div>

    </div>
</template>

<script>
import customFetch from '@/utils/customFetch'
import Card from './Card.vue'
import DropCard from './DropCard.vue'

export default {
    name: 'List',
    components: {
        Card,
        DropCard,
    },
    data: function () {
        return {

        }
    },
    computed: {
        dragStarted() {
            return this.$store.state.dragStarted
        }
    },
    props: ['list_id', 'name', 'cards', "fetchAllListsCardsByUser"],
    methods: {
        startDrag(evt, card) {
            evt.dataTransfer.dropEffect = 'move'
            evt.dataTransfer.effectAllowed = 'move'
            evt.dataTransfer.setData('cardID', card.card_id)
            this.$store.dispatch('changeDragStarted', {
                value: true
            })
        },
        exportDataByList(e, list_id) {
            this.exportByListToCSV(list_id)
        },
        exportByListToCSV(list_id) {
            this.$store.dispatch('changeExportAlertState', {
                value: true
            })
            setTimeout(() => {
                this.$store.dispatch('changeExportAlertState', {
                    value: false
                })
            }, 3000);
            // export the user's lists and cards by list_id to csv
            customFetch(`http://localhost:5000/api/export/${list_id}`, {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem("token"),
                },
            }, 'b').then(data => {
                setTimeout(() => {
                }, 1000);
                saveAs(data, `export_${list_id}.csv`)
            }).catch(error => alert(error.message))
        }
    }

}
</script>

<style scoped>
.icon-style {
    font-size: 2rem;
}
</style>