<template>
  <div class="modal advertencia" id="avisoEliminar">
    <div class="dialogo-modal-reducido">
      <div class="encabezado-modal">
        <h5>Confirmar Eliminación</h5>
      </div>
      <div class="cuerpo-modal">
        <p>{{ titulo }}</p>
      </div>
      <div class="pie-modal">
        <button class="button-modal btn-confirmar" @click="$emit('confirmar')">Sí</button>
        <button class="button-modal btn-cancelar" @click="$emit('cancelar')">No</button>
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
      default: '¿Estás seguro de que deseas eliminar este elemento?',
    },
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialogo-modal-reducido {
  background: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.encabezado-modal h5 {
  margin: 0 0 10px;
}

.cuerpo-modal {
  margin-bottom: 20px;
}

.pie-modal {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.button-modal {
  padding: 6px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-confirmar {
  background-color: #dc3545;
  color: white;
}

.btn-cancelar {
  background-color: #6c757d;
  color: white;
}
</style>
