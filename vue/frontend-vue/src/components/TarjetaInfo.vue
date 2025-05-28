<template>
  <div class="card shadow-sm">
    <div class="card-body text-center">
      <h5 class="card-title">{{ titulo }}</h5>
      <p class="card-text">{{ contenido }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TarjetaInfo',
  props: {
    titulo: {
      type: String,
      required: true
    },
    contenido: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
/* Estilos personalizados si son necesarios */
.card {
  min-width: 250px; /* Evita que las tarjetas se encojan demasiado */
}
</style>