<template>
  <div>
    <ModalProyecto
      v-if="mostrarModal"
      @cerrar="mostrarModal = false"
      @crear="crearProyecto"
    />

    <div v-if="proyectos.length">
      <table class="tabla">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Dispositivos</th>
            <th>Sensores</th>
            <th colspan="2">Opciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="proyecto in proyectos" :key="proyecto.id">
            <td>{{ proyecto.nombre }}</td>
            <td>{{ truncarDescripcion(proyecto.descripcion) }}</td>
            <td>{{ proyecto.dispositivos ?? 0 }}</td>
            <td>{{ proyecto.sensores ?? 0 }}</td>
            <td class="opciones">
              <router-link :to="`/detalle-proyecto/${proyecto.id}`">
                <span class="ion-eye"></span>
              </router-link>
            </td>
            <td class="opciones">
              <a @click="confirmarEliminacion(proyecto.id)">
                <span class="ion-trash-a"></span>
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <h2 class="margen">Aún no cuentas con Proyectos...</h2>
    </div>

    <div class="centrado">
      <input @click="mostrarModal = true" class="btn btn-info" type="button" value="Nuevo Proyecto" style="color: white;">
    </div>

    <ModalEliminarProyecto
      :class="{ modal: true, advertencia: true, visible: mostrarModalEliminar }"
      @cancelar="cerrarModalEliminar"
      @confirmar="eliminar"
    />
  </div>
</template>

<script>
import ModalProyecto from './ModalProyecto.vue';
import ModalEliminarProyecto from './ModalEliminar.vue';

const API_BASE_URL = 'http://localhost:8001'; // Asegúrate de apuntar a tu backend

export default {
  name: 'MisProyectos',

  components: {
    ModalProyecto,
    ModalEliminarProyecto
  },

  data() {
    return {
      proyectos: [],
      mostrarModal: false,
      mostrarModalEliminar: false,
      proyectoEliminarId: null,
    };
  },

  methods: {
    truncarDescripcion(desc) {
      return desc.split(' ').slice(0, 10).join(' ') + '...';
    },

    confirmarEliminacion(id) {
      this.proyectoEliminarId = id;
      this.mostrarModalEliminar = true;
    },

    cerrarModalEliminar() {
      this.mostrarModalEliminar = false;
      this.proyectoEliminarId = null;
    },

    async eliminar() {
      try {
        const res = await fetch(`${API_BASE_URL}/proyectos/${this.proyectoEliminarId}`, {
          method: 'DELETE',
        });

        if (!res.ok) throw new Error('Error al eliminar el proyecto');

        this.proyectos = this.proyectos.filter(p => p.id !== this.proyectoEliminarId);
        this.mostrarModalEliminar = false;
      } catch (err) {
        alert('Error: ' + err.message);
      }
    },

    async crearProyecto(nuevoProyecto) {
      try {
        const res = await fetch(`${API_BASE_URL}/proyectos/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(nuevoProyecto),
        });

        if (!res.ok) throw new Error('Error al crear el proyecto');

        const proyectoCreado = await res.json();
        this.proyectos.push(proyectoCreado);
        this.mostrarModal = false;
      } catch (err) {
        alert('Error: ' + err.message);
      }
    },

    async cargarProyectos() {
      try {
        const res = await fetch(`${API_BASE_URL}/proyectos/`);
        if (!res.ok) throw new Error('Error al cargar los proyectos');

        this.proyectos = await res.json();
      } catch (err) {
        alert('Error: ' + err.message);
      }
    }
  },

  mounted() {
    this.cargarProyectos();
  }
};
</script>

<style scoped>
@import '@/assets/css/dashboard/tabla.css';
@import '@/assets/css/dashboard/formulario.css';
@import '@/assets/css/modal.css';
</style>
