<template>
  <div id="app">
    <!-- Barra de navegación (si es global) -->
    <router-view></router-view> <!-- Aquí se renderizarán las vistas -->
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>