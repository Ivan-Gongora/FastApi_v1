<template>
    <div class="plataforma-layout">
      <BarraLateralPlataforma />
      <div class="plataforma-contenido">
        <EncabezadoPlataforma titulo="Dispositivos" />
        <ListaDispositivos />
      </div>
    </div>
  </template>
  
  <script>
  import BarraLateralPlataforma from '../plataforma/BarraLateralPlataforma.vue';
//import EncabezadoPlataforma from '../plataforma/EncabezadoPlataforma.vue';
  import ListaDispositivos from '../dispositivos/Dispositivos.vue';
  
  export default {

    name: 'VistaDispositivos',
    components: {
      BarraLateralPlataforma,
      //EncabezadoPlataforma,
      ListaDispositivos
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