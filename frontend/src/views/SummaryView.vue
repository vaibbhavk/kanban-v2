<template>
  <Navbar title="Kanban V2" />

  <div class="container-fluid">
    <div v-if="!this.loading" class="row row-cols-sm-1 row-cols-md-2 row-cols-lg-3">
      <SummaryPerList v-for="s in summary" :key="s.list_id" :s="s" />
    </div>
    <Spinner v-else class="m-3" />


  </div>
</template>

<script>
// @ is an alias to /src
import Navbar from '@/components/Navbar.vue'
import Spinner from '@/components/Spinner.vue'
import SummaryPerList from '@/components/SummaryPerList.vue'
import customFetch from '@/utils/customFetch'

export default {
  name: 'SummaryView',
  components: {
    SummaryPerList,
    Spinner,
    Navbar
  },
  data: function () {
    return {
      summary: [],
      loading: false
    }
  },
  mounted: function () {
    this.getUserSummary()
  },
  methods: {
    getUserSummary() {
      this.loading = true
      // get summary of the logged in user
      customFetch("http://localhost:5000/api/user/summary", {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem("token"),
        },
      }).then(data => {
        this.summary = data
      }
      ).catch(error => alert(error.message)).finally(() => this.loading = false)
    }
  }
}
</script>
