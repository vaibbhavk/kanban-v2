<template>
  <Navbar title="Kanban V2" :fetchAllListsCardsByUser="this.fetchAllListsCardsByUser" />

  <div class="container-fluid" @dragend="handleDragEnd">
    <div v-if="!this.loading" class="row row-cols-sm-1 row-cols-md-2 row-cols-xl-5 min-vh-100">
      <List v-for="list in lists" :key="list.list_id" :list_id="list.list_id" :name="list.name" :cards="list.cards"
        :fetchAllListsCardsByUser="this.fetchAllListsCardsByUser" @drop="onDrop($event, list.list_id)" @dragover.prevent
        @dragenter.prevent />

      <div class="text-center" v-show="this.totalLists < 5">
        <router-link to="/list/add">
          <i class="bi bi-plus-square icon-style"></i>
        </router-link>
      </div>
    </div>
    <Spinner v-else class="m-3" />
  </div>
</template>

<script>
// @ is an alias to /src
import List from '@/components/List.vue'
import Card from '@/components/Card.vue'
import customFetch from '@/utils/customFetch'
import Spinner from '@/components/Spinner.vue'
import Navbar from '@/components/Navbar.vue'


export default {
  name: 'DashboardView',
  components: {
    List,
    Card,
    Spinner,
    Navbar,

  },
  data: function () {
    return {
      lists: [],
      totalLists: 6,
      loading: false,
    }
  },
  mounted: function () {
    this.fetchAllListsCardsByUser()
  },
  methods: {
    fetchAllListsCardsByUser() {
      this.loading = true
      // fetch all the lists and cards of the logged in user
      customFetch("http://localhost:5000/api/lists", {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem("token"),
        },
      }).then(data => {
        this.lists = data
        this.totalLists = data.length
      }
      ).catch(error => alert(error.message)).finally(() => this.loading = false)
    },
    onDrop(evt, list_id) {
      this.$store.dispatch('changeDragStarted', {
        value: false
      })

      const itemID = evt.dataTransfer.getData('cardID')


      // fetch all the list_ids and cards of the logged in user
      customFetch(`http://localhost:5000/api/card/${itemID}/${list_id}`, {
        method: 'PATCH',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem("token"),
        },
      }).then(data => { }).catch(error => alert(error.message)).finally(() => this.fetchAllListsCardsByUser())
    },
    handleDragEnd(e) {
      this.$store.dispatch('changeDragStarted', {
        value: false
      })
    }
  },
}
</script>


<style scoped>
.icon-style {
  font-size: 4rem;
}
</style>