<template>
    <div class="plataforma-layout">
      <BarraLateralPlataforma />
      <div class="plataforma-contenido">
        <EncabezadoPlataforma />
        <TarjetasPlataforma />
      </div>
    </div>
  </template>
  
  <script>
  import BarraLateralPlataforma from './BarraLateralPlataforma.vue';
  import EncabezadoPlataforma from './EncabezadoPlataforma.vue';
  import TarjetasPlataforma from './TarjetasPlataforma.vue';
  
  export default {
    name: 'VistaPlataformaPrincipal',
    components: {
      BarraLateralPlataforma,
      EncabezadoPlataforma,
      TarjetasPlataforma,
    },
  };
  </script>
  
  <style scoped lang="scss">
  .plataforma-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f8f9fa; /* Gris claro de fondo */
}

.plataforma-contenido {
  flex-grow: 1;
  padding: 20px; /* Añadir padding general al contenido */
  padding-left: 270px; /* Para dejar espacio a la barra lateral */
}
  </style>