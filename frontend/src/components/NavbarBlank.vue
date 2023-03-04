<template>
    <nav class="navbar sticky-top navbar-expand-lg bg-white p-3">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03"
                aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <router-link class="navbar-brand" to="/">{{ title }}</router-link>
        </div>
    </nav>
</template>
  
<script>



export default {
    name: 'NavbarBlank',
    props: ['title'],
}
</script>
  