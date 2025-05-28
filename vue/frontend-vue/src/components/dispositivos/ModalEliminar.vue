<template>
 
   <!-- Modal Confirmar Eliminación -->
   <div class="modal advertencia" id="avisoEliminar">
    <div class="dialogo-modal-reducido">
      <div class="encabezado-modal"></div>
      <div class="cuerpo-modal">
        <p>{{ titulo }}</p>
      </div>
      <div class="pie-modal">
      <button class="button-modal" @click="$emit('confirmar')">Sí</button>
      <button class="button-modal" @click="$emit('cancelar')">No</button>
      </div>
    </div>
  </div>
</template>


  <script>
  export default {
    name: 'ModalEliminar',
    props: {
    titulo: {
      type: String,
      default: 'Panel de Control'
    }
  }
  };
  </script>
  


<style scoped>
@import '@/assets/css/dashboard/tabla.css';
@import '@/assets/css/dashboard/formulario.css';
@import '@/assets/css/modal.css';
</style>

