<template>
  <div class="plataforma-layout">
    <BarraLateralPlataforma />
    <div class="plataforma-contenido p-4">
      <EncabezadoPlataforma :titulo="'Editar Valor ID: ' + id" />

      <form @submit.prevent="guardar">
        <div class="form-group mb-3">
          <label>ID</label>
          <input type="text" class="form-control" :value="id" disabled />
        </div>

        <div class="form-group mb-3">
          <label>Valor</label>
          <input
            v-model="valor.valor"
            type="text"
            class="form-control"
            required
            maxlength="100"
          />
        </div>

        <div class="form-group mb-3">
          <label>Fecha y hora de lectura</label>
          <input
            v-model="valor.fecha_hora_lectura"
            type="datetime-local"
            class="form-control"
            required
          />
        </div>

        <div class="form-group mb-4">
          <label>Campo ID</label>
          <input
            v-model.number="valor.campo_id"
            type="number"
            class="form-control"
            required
            min="1"
          />
        </div>

        <button type="submit" class="btn btn-primary me-2">Guardar</button>
        <router-link to="/valores" class="btn btn-secondary">Cancelar</router-link>
      </form>
    </div>
  </div>
</template>

<script>
import BarraLateralPlataforma from '../plataforma/BarraLateralPlataforma.vue';
import EncabezadoPlataforma from '../plataforma/EncabezadoPlataforma.vue';

export default {
  name: 'ActualizarValor',
  components: {
    BarraLateralPlataforma,
    EncabezadoPlataforma,
  },
  data() {
    return {
      id: this.$route.params.id,
      valor: {
        id: '',
        valor: '',
        fecha_hora_lectura: '',
        campo_id: null,
      },
    };
  },
  created() {
    this.cargarValor();
  },
  methods: {
    cargarValor() {
      // Simula cargar desde API con el ID
      // En producción, aquí llamarías fetch/axios a la API para obtener datos
      const datosSimulados = {
        id: this.id,
        valor: '123.45',
        fecha_hora_lectura: '2025-05-29T10:30',
        campo_id: 7,
      };
      this.valor = { ...datosSimulados };
    },
    guardar() {
      // Aquí iría lógica para guardar (PUT/PATCH a API)
      console.log('Guardando valor actualizado:', this.valor);
      alert('Valor actualizado correctamente');
      this.$router.push('/valores');
    },
  },
};
</script>

<style scoped lang="scss">
.plataforma-contenido {
  max-width: 600px;
  margin: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0,0,0,0.1);
  padding: 2rem;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.3rem;
}

.btn {
  min-width: 100px;
}
</style>
