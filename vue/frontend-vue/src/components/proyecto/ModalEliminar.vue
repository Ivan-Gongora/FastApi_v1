<template>
<!-- Modal Confirmar Eliminación -->
  <div class="modal advertencia" id="avisoEliminar">
    <div class="dialogo-modal-reducido">
      <div class="encabezado-modal"></div>
      <div class="cuerpo-modal">
        <p>¿Estás seguro de que deseas eliminar este proyecto?, esta acción no tiene modo de revertirse.</p>
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
    name: 'ModalEliminarProyecto',
  };
  </script>

<style scoped>
@import '@/assets/css/dashboard/tabla.css';
@import '@/assets/css/dashboard/formulario.css';
@import '@/assets/css/modal.css';
</style>
 
  
