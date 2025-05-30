<template>
  <div class="modal visible" id="modal-dispositivo">
    <div class="dialogo-modal">
      <div class="encabezado-modal">
        <h2 class="margen">Nuevo Dispositivo</h2>
      </div>
      <div class="cuerpo-modal">
        <form @submit.prevent="crear" class="formulario">
          <label>Nombre del Dispositivo</label>
          <input v-model="dispositivo.nombre_de_dispositivo" type="text" placeholder="Nombre" required>
          
          <label>Descripción</label>
          <textarea v-model="dispositivo.descripcion" placeholder="Descripción" required></textarea>
          
          <label>Tipo</label>
          <input v-model="dispositivo.tipo" type="text" placeholder="Tipo" required>
          
          <label>Latitud</label>
          <input v-model="dispositivo.latitud" type="number">
          
          <label>Longitud</label>
          <input v-model="dispositivo.longitud" type="number">
          
          <label>Habilitado</label>
          <input v-model="dispositivo.esta_habilitado" type="checkbox">
          
          <label>Proyecto</label>
          <select v-model="dispositivo.proyecto_id">
            <option disabled value="">Seleccionar proyecto</option>
            <option v-for="proyecto in proyectos" :key="proyecto.id" :value="proyecto.id">
              {{ proyecto.nombre }}
            </option>
          </select>

          <div class="pie-modal">
            <input type="submit" value="Crear" class="btn btn-success me-2">
            <input type="button" value="Cancelar" @click="cancelar" class="btn btn-warning">
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

  
<script>
export default {
  name: 'CrearDispositivo',
  emits: ['cerrar', 'crear'],
  data() {
    return {
      dispositivo: {
        nombre_de_dispositivo: '',
        descripcion: '',
        tipo: '',
        latitud: '',
        longitud: '',
        esta_habilitado: false,
        proyecto_id: ''
      },
      proyectos: [
        { id: 1, nombre: 'Proyecto Solar' },
        { id: 2, nombre: 'Red Inteligente' },
        { id: 3, nombre: 'Domótica Escolar' }
      ],
      API_BASE_URL: "http://127.0.0.1:8001"
    };
  },
  methods: {
    async crear() {
      try {
        const res = await fetch(`${this.API_BASE_URL}/dispositivos/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            nombre: this.dispositivo.nombre_de_dispositivo,
            descripcion: this.dispositivo.descripcion,
            tipo: this.dispositivo.tipo,
            latitud: this.dispositivo.latitud !== '' ? Number(this.dispositivo.latitud) : null,
            longitud: this.dispositivo.longitud !== '' ? Number(this.dispositivo.longitud) : null,
            habilitado: this.dispositivo.esta_habilitado,
            proyecto_id: Number(this.dispositivo.proyecto_id)
          })
        });

        if (!res.ok) {
          throw new Error(`Error al crear dispositivo: ${res.status}`);
        }

        const data = await res.json();

        // Emitir el dispositivo creado que viene en data.resultados
        this.$emit('crear', data.resultados);

        // Limpiar formulario
        this.dispositivo = {
          nombre_de_dispositivo: '',
          descripcion: '',
          tipo: '',
          latitud: '',
          longitud: '',
          esta_habilitado: false,
          proyecto_id: ''
        };

        this.$emit('cerrar');

      } catch (error) {
        alert("No se pudo crear el dispositivo: " + error.message);
      }
    },
    cancelar() {
      this.dispositivo = {
        nombre_de_dispositivo: '',
        descripcion: '',
        tipo: '',
        latitud: '',
        longitud: '',
        esta_habilitado: false,
        proyecto_id: ''
      };
      this.$emit('cerrar');
    }
  }
};
</script>

  
  
  <style scoped>
    @import '@/assets/css/dashboard/tabla.css';
    @import '@/assets/css/dashboard/formulario.css';
    @import '@/assets/css/modal.css';
  </style>
  
