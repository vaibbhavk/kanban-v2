<template>
    <Navbar title="Kanban V2" />
    <div class="container-fluid">

        <div v-if='this.name === "add_list"'>
            <AddList />
        </div>
        <div v-else-if='this.name === "delete_list"'>
            <DeleteListConfirm />
        </div>
        <div v-else>
            <EditList />
        </div>
    </div>
</template>
  
<script>
// @ is an alias to /src

import AddList from '@/components/AddList.vue'
import EditList from '@/components/EditList.vue'
import DeleteListConfirm from '@/components/DeleteListConfirm.vue'
import Navbar from '@/components/Navbar.vue'

export default {
    name: 'ListManagementView',
    components: {
        AddList,
        EditList,
        DeleteListConfirm,
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
  
  
  