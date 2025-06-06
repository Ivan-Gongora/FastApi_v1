<template>
  <div>
    <div v-if="proyectos.length">
      <table class="tabla">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            
            <div v-if="tipo_usuario === 'admin'">
            <th colspan="2">Opciones</th>
            </div>
          </tr>
        </thead>
        <tbody>
          <tr v-for="proyecto in proyectos" :key="proyecto.id">
            <td>{{ proyecto.nombre }}</td>
            <td>{{ truncarDescripcion(proyecto.descripcion) }}</td>
            <div v-if="tipo_usuario === 'admin'">
            <td class="opciones">
            <!-- Mostrar solo si el usuario es admin -->
          
                <router-link :to="`/detalle-proyecto/${proyecto.id}`">
                  <span class="ion-eye"></span>
                </router-link>


            </td>
            <td class="opciones">
              <a @click="confirmarEliminacion(proyecto.id,this.id_usuario )">
                <span class="ion-trash-a"></span>
              </a>
            </td>

          </div>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <h2 class="margen">Aún no cuentas con Proyectos..</h2>
    </div>

  <!-- Botón solo visible para admins -->
  <div v-if="tipo_usuario === 'admin'" class="centrado">
    <input
      @click="mostrarModalCrear = true"
      class="btn btn-info"
      type="button"
      value="Nuevo Proyecto"
      style="color: white;"
    >
  </div>


    <!-- Modales -->
    <ModalEliminarProyecto
      :class="{ modal: true, advertencia: true, visible: mostrarModalEliminar }"
      @cancelar="cerrarModalEliminar"
      @confirmar="eliminar(proyectoEliminarId, usuarioId)"
    />

    <ModalProyecto  
      v-if="mostrarModalCrear"
      @crear="crearProyecto"
      @cerrar="cerrarModalCrear"
      :class="{ visible: mostrarModalCrear }"
    />
  </div>
</template>

<script>
import ModalProyecto from './CrearProyecto.vue';
import ModalEliminarProyecto from './ModalEliminar.vue';

const API_BASE_URL = 'http://127.0.0.1:8001';

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
      mostrarModalCrear: false,
      id_usuario: null,
      usuarioId: null,
      tipo_usuario: null,
      error: '',
      resultado: null // Guardamos el resultado globalmente para acceso en el template
    };
  },
  methods: {
    truncarDescripcion(descripcion) {
      if (!descripcion || typeof descripcion !== 'string') {
        return 'Sin descripción';
      }
      return descripcion.split(' ').slice(0, 10).join(' ') + '...';
    },
    confirmarEliminacion(id, id_usuario) {
      this.proyectoEliminarId = id;
      this.usuarioId = id_usuario;
      this.mostrarModalEliminar = true;




    },
    cerrarModalEliminar() {
      this.mostrarModalEliminar = false;
      this.proyectoEliminarId = null;
    },
    eliminar(id, usuarioId) {
      fetch(`${API_BASE_URL}/eliminar_proyecto?id=${id}&usuarioId=${usuarioId}`, {
        method: 'DELETE',
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Error al eliminar el proyecto.');
          }
          return response.text();
        })
        .then(msg => {
          alert(msg);

          // Elimina el proyecto del array local sin recargar la página
          this.proyectos = this.proyectos.filter(p => p.id !== id);

          this.cerrarModalEliminar();
        })
        .catch(err => {
          alert('Error: ' + err.message);
          this.cerrarModalEliminar();
        });
    },
    crearProyecto(proyecto) {
      this.proyectos.push(proyecto); // Simulación local
      this.mostrarModalCrear = false;
    },
    cerrarModalCrear() {
      this.mostrarModalCrear = false;
    }
  },
  mounted() {
    const resultado = JSON.parse(localStorage.getItem('resultado'));

    if (resultado && resultado.usuario) {
      this.resultado = resultado; 
      this.id_usuario = resultado.usuario.id;
      this.tipo_usuario = resultado.usuario.tipo_usuario;

      if (this.tipo_usuario === 'admin') {
        // Admin ve todos los proyectos
        fetch(`${API_BASE_URL}/proyectos`)
          .then(res => res.json())
          .then(data => {
            this.proyectos = data;
          })
          .catch(error => {
            console.error('Error al obtener proyectos:', error);
          });
      } else {
        // Usuario común: solo sus proyectos
        fetch(`${API_BASE_URL}/proyectos/usuario/${this.id_usuario}`)
          .then(res => res.json())
          .then(data => {
            this.proyectos = data;
          })
          .catch(error => {
            console.error('Error al obtener proyectos:', error);
          });
      }
    } else {
      console.error('No se encontró información del usuario en localStorage.');
    }
  }
};
</script>

<style scoped>
@import '@/assets/css/dashboard/tabla.css';
@import '@/assets/css/dashboard/formulario.css';
@import '@/assets/css/modal.css';
</style>
