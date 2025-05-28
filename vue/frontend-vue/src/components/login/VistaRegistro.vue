<script>
import BarraNavegacion from '../BarraNavegacion.vue';
import FormularioRegistro from './FormularioRegistro.vue'; // Importa el nuevo nombre

export default {
  name: 'VistaRegistro',
  components: {
    BarraNavegacion,
    FormularioRegistro
  }
};
</script>

<template>
  <div>
    <BarraNavegacion />
    <FormularioRegistro />
  </div>
</template>