<template>
  <div class="plataforma-encabezado bg-light p-3 shadow-sm">
    <h1 class="mb-0">{{ titulo }}</h1>
  </div>
</template>

<script>
export default {
  name: 'EncabezadoPlataforma',
  props: {
    titulo: {
      type: String,
      default: 'Panel de Control'
    }
  }
};
</script>
  
  <style scoped lang="scss">
  .plataforma-encabezado {
  background-color: #fff;
  padding: 20px;
  margin-bottom: 30px; /* Espacio debajo del encabezado */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* Sombra sutil */
  border-bottom: 1px solid #eee;
}

h1 {
  font-size: 1.75rem;
  color: #333;
  margin-bottom: 0;
}
  </style>
