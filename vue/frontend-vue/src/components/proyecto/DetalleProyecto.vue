<template>
    <div class="plataforma-layout">
      <BarraLateralPlataforma />
      <div class="plataforma-contenido">
        <EncabezadoPlataforma :titulo="proyecto.nombre" />
        <div class="contenedor-main">
          <!-- Formulario de proyecto -->
          <form @submit.prevent="modificar" class="formulario izquierda">
            <label>Nombre del Proyecto</label>
            <input v-model="proyecto.nombre" type="text" required />
  
            <label>Descripción</label>
            <textarea v-model="proyecto.descripcion" required></textarea>
  
            <label>Usuario ID</label>
            <input :value="proyecto.usuario_id" type="number" disabled />


                <!-- Botón solo visible para admins -->
                <div v-if="tipo_usuario === 'admin'" class="centrado">
                    <input
                    @click="mostrarModalCrear = true"
                    class="btn btn-info"
                    type="button"
                 value="Guardar Cambios" 
                    style="color: white;"
                    >
                </div>


  
            <input type="submit" value="Guardar Cambios" class="btn btn-info" style="color: white;" />
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import BarraLateralPlataforma from '../plataforma/BarraLateralPlataforma.vue';
  import EncabezadoPlataforma from '../plataforma/EncabezadoPlataforma.vue';
  
  const API_BASE_URL = "http://localhost:8001";
  
  export default {
    name: 'DetalleProyecto',
    components: {
      BarraLateralPlataforma,
      EncabezadoPlataforma
    },
    data() {
      return {
        proyecto: {
          id: null,
          nombre: '',
          descripcion: '',
          usuario_id: null
        }
      };
    },
    mounted() {
      const proyectoId = this.$route.params.id;
      if (proyectoId) {
        this.cargarProyecto(proyectoId);
      } else {
        alert('No se encontró ID del proyecto en la ruta.');
      }
    },
    methods: {
      async cargarProyecto(id) {
        try {
          const res = await fetch(`${API_BASE_URL}/proyectos/${id}`);
          if (!res.ok) throw new Error(`Error al cargar proyecto: ${res.status}`);
          const data = await res.json();
          this.proyecto = {
            id: data.id,
            nombre: data.nombre,
            descripcion: data.descripcion,
            usuario_id: data.usuario_id
          };
        } catch (error) {
          alert(error.message);
        }
      },
      async modificar() {
        const { nombre, descripcion, usuario_id } = this.proyecto;

        if (!nombre || !descripcion) {
            alert("Por favor, completa todos los campos");
            return;
        }

        try {
            const res = await fetch(`${API_BASE_URL}/actualizar_proyecto/${this.proyecto.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, descripcion, usuario_id })
            });

            if (!res.ok) {
            const errorData = await res.json().catch(() => null);
            throw new Error(errorData?.message || `Error al actualizar proyecto: ${res.status}`);
            }

            alert("Proyecto actualizado correctamente");
            this.cargarProyecto(this.proyecto.id);
        } catch (error) {
            alert(error.message);
        }
        }

    }
  };
  </script>
  
  <style scoped lang="scss">
  @import '@/assets/css/dashboard/tabla.css';
  @import '@/assets/css/dashboard/formulario.css';
  @import '@/assets/css/dashboard/ver_dispositivo.css';
  
  .plataforma-layout {
    display: flex;
    min-height: 100vh;
    background-color: #f8f9fa;
  }
  
  .plataforma-contenido {
    flex-grow: 1;
    padding: 20px;
    padding-left: 270px;
  }
  </style>
