<template>
  <div>
 <ModalProyecto v-if="mostrarModal" @cerrar="mostrarModal = false" @crear="crearProyecto" />

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
            <td>{{ proyecto.dispositivos }}</td>
            <td>{{ proyecto.sensores }}</td>
            <td class="opciones">
              <router-link :to="`/detalle-proyecto/${proyecto.id}`"><span class="ion-eye"></span></router-link>
            </td>
            <td class="opciones">
              <a @click="confirmarEliminacion(proyecto.id)"><span class="ion-trash-a"></span></a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <h2 class="margen">Aún no cuentas con Proyectos..</h2>
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
      this.proyectoEliminarId  = null;
    },

    // metodo para controlar la eliminación 
    eliminar() {
      fetch(`/proyecto/${this.proyectoEliminarId}/eliminar`, {
        method: 'GET',
      })
        .then(response => response.text())
        .then(msg => {
          alert(msg + '\nLa página se refrescará en 3 segundos...');
          setTimeout(() => window.location.reload(), 3000);
        })
        .catch(err => {
          alert('Error: ' + err);
        });
      this.mostrarModalEliminar = false;
    },
    crearProyecto(proyecto) {
      // lógica para enviar proyecto al backend
      this.proyectos.push(proyecto); // Simulado
      this.mostrarModal = false;
    },
  },
  mounted() {
    // Simular obtención de datos
    this.proyectos = [
      {
        id: 1,
        nombre: 'Proyecto Alpha',
        descripcion: 'Este es un ejemplo largo de descripción de proyecto que debería truncarse.',
        dispositivos: 5,
        sensores: 3,
      },
      {
        id: 2,
        nombre: 'Proyecto Prueba',
        descripcion: 'Este es un ejemplo corto de descrippción',
        dispositivos: 3,
        sensores: 2,
      },
      {
  id: 3,
  nombre: 'Sistema de Riego Inteligente',
  descripcion: 'Automatiza el riego de cultivos usando sensores de humedad y clima.',
  dispositivos: 5,
  sensores: 4,
},
{
  id: 4,
  nombre: 'Control de Iluminación',
  descripcion: 'Gestiona el encendido y apagado de luces según presencia o tiempo programado.',
  dispositivos: 2,
  sensores: 1,
},
{
  id: 5,
  nombre: 'Monitor de Energía Doméstica',
  descripcion: 'Visualiza el consumo eléctrico en tiempo real y recibe alertas por exceso.',
  dispositivos: 4,
  sensores: 3,
},
{
  id: 6,
  nombre: 'Alerta de Inundaciones',
  descripcion: 'Sistema de detección de inundaciones para zonas vulnerables usando sensores ultrasónicos.',
  dispositivos: 3,
  sensores: 5,
}

    ];
  },
};
</script>

<style scoped>


@import '@/assets/css/dashboard/tabla.css';
@import '@/assets/css/dashboard/formulario.css';
@import '@/assets/css/modal.css';
</style>

