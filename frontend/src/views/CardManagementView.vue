<template>
    <Navbar title="Kanban V2" />

    <div class="container-fluid">
        <div v-if='this.name === "add_card"'>
            <AddCard />
        </div>
        <div v-else>
            <EditCard />
        </div>
    </div>
</template>
  
<script>
// @ is an alias to /src

import AddCard from '@/components/AddCard.vue'
import EditCard from '@/components/EditCard.vue'
import Navbar from '@/components/Navbar.vue'

export default {
    name: 'CardManagementView',
    components: {
        AddCard,
        EditCard,
        Navbar
    },
    data: function () {
        return {
            name: this.$route.name
        }
    },
    mounted: function () {
    },
    methods: {

    },
}
</script>
  
  
  