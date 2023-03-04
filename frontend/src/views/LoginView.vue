<template>
    <NavbarBlank title="Kanban V2" />
    <div class="container-fluid">
        <Login />
    </div>
</template>
  
<script>
// @ is an alias to /src
import Login from '@/components/Login.vue'
import NavbarBlank from '@/components/NavbarBlank.vue';

export default {
    name: 'LoginView',
    components: {
    Login,
    NavbarBlank
},

}
</script>
  