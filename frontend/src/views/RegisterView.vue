<template>
    <NavbarBlank title="Kanban V2" />
    <div class="container-fluid">
        <Register />
    </div>
</template>
  
<script>
// @ is an alias to /src
import NavbarBlank from '@/components/NavbarBlank.vue';
import Register from '@/components/Register.vue'

export default {
    name: 'RegisterView',
    components: {
        Register,
        NavbarBlank
    },

}
</script>
  