<template>
    <!-- Modal Crear Proyecto -->
    <div class="modal" id="modal-proyecto">
      <div class="dialogo-modal">
        <div class="encabezado-modal">
          <h2 class="margen">Nuevo Proyecto</h2>
        </div>
        <div class="cuerpo-modal">
          <form @submit.prevent="crear" class="formulario">
            <label>Nombre del Proyecto</label>
            <input v-model="proyecto.nombre" type="text" placeholder="Nombre" required />
  
            <label>Descripción</label>
            <textarea v-model="proyecto.descripcion" placeholder="Descripción" required></textarea>
  
            <div class="pie-modal">
              <input type="submit" value="Crear" class="btn btn-success me-2" />
              <input type="button" value="Cancelar" @click="cancelar" class="btn btn-warning" />
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>

const API_BASE_URL = 'http://127.0.0.1:8001';
  export default {
    name: 'ModalProyecto',
    emits: ['cerrar', 'crear'],
    data() {
      return {
        proyecto: {
          nombre: '',
          descripcion: '',
          usuario_id: null
        }
      };
    },
    mounted() {
      const resultado = JSON.parse(localStorage.getItem('resultado'));
      if (resultado && resultado.usuario) {
        this.proyecto.usuario_id = resultado.usuario.id;
      }
    },
    methods: {
      crear() {
      // Llama a la API para crear el proyecto
      fetch(`${API_BASE_URL}/crear_proyecto`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.proyecto)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Error al crear el proyecto');
        }
        return response.json();
      })
      .then(data => {
        // Si la creación fue exitosa, emitir evento y resetear formulario
        this.$emit('crear', data); 
        this.resetearFormulario();
        this.$emit('cerrar');
      })
      .catch(error => {
        console.error('Error:', error);
      
      });
    }
    ,
      cancelar() {
        this.resetearFormulario();
        this.$emit('cerrar');
      },
      resetearFormulario() {
        this.proyecto = {
          nombre: '',
          descripcion: '',
          usuario_id: this.proyecto.usuario_id
        };
      },
      crearDispositivo(dispositivo) {
      console.log('Crear nuevo dispositivo', dispositivo);
      this.proyecto.push(dispositivo);
      this.cerrarModalCrear();
    }
    }
  };
  </script>
  
  <style scoped>
  @import '@/assets/css/dashboard/tabla.css';
  @import '@/assets/css/dashboard/formulario.css';
  @import '@/assets/css/modal.css';
  </style>
  