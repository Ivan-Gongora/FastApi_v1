<template>
    <div class="plataforma-layout">
      <BarraLateralPlataforma />
      <div class="plataforma-contenido">
        <EncabezadoPlataforma :titulo="dispositivo.nombre_de_dispositivo" />
        <div class="contenedor-main">
           <!-- Formulario datos del dispositivos -->
        <form @submit.prevent="modificar" class="formulario izquierda">
        <label>Nombre del Dispositivo</label>
        <input v-model="dispositivo.nombre_de_dispositivo" type="text" required>
        <label>Descripción</label>
        <textarea v-model="dispositivo.descripcion" required></textarea>
        <label>Tipo</label>
        <input v-model="dispositivo.tipo" type="text" required>
        <label>Latitud</label>
        <input v-model="dispositivo.latitud" type="number">
        <label>Longitud</label>
        <input v-model="dispositivo.longitud" type="number">
        <label>Habilitado</label>
        <input v-model="dispositivo.esta_habilitado" type="checkbox">
        <label>Proyecto</label>
        <select v-model="dispositivo.proyecto_id">
          <option disabled value="">Seleccione un proyecto</option>
          <option v-for="proyecto in proyectos" :key="proyecto.id" :value="proyecto.id">
            {{ proyecto.nombre }}
          </option>
        </select>
          <input type="submit" value="Guardar Cambios" class="btn btn-info" style="color: white;">
       </form>

         <!-- Tabla de dispositivos -->
    <div class="contenedor-sensores">
    <div v-if="sensores.length > 0">
      <table class="tabla">
        <thead>
          <tr>
                    <th>Nombre</th>
                    <th>Tipo</th>
                    <th>Habilitado</th>
                    <th colspan="2">Opciones</th>
        </tr>
        </thead>
        <tbody>
            <tr v-for="sensor in sensores" :key="sensor.id">
            <td>{{ sensor.nombre_de_sensor }}</td>
            <td>{{ sensor.tipo }}</td>
            <td class="centrado">
                <input type="checkbox" :checked="sensor.esta_habilitado" disabled>
            </td>
            <td class="opciones">
                <a @click="confirmarEliminar(sensor.id)">
                <span class="ion-trash-a"></span>
                
                </a>
            </td>
            </tr>

        </tbody>
      </table>
    </div>

    <div v-else>
            <h2 class="margen">Este dispositivo aún no cuenta con sensores.</h2>
    </div>
    <div class="centrado">
              <router-link :to="`/form-sensor/${dispositivo.id}`" class="btn btn-info" style="color: white;">Nuevo Sensor</router-link>
    </div>

      </div>
      <!-- Modal Confirmar Eliminación -->
  <ModalEliminar titulo ="Esta por eliminar un sensor, esta acción no tiene modo de revertirse."
  :class="{ modal: true, advertencia: true, visible: mostrarModalEliminar }"
  @confirmar="eliminarDispositivo"
  @cancelar="mostrarModalEliminar = false"
   />
      </div>
    </div>
    </div>

  </template>

  <script>
  import BarraLateralPlataforma from '../plataforma/BarraLateralPlataforma.vue';
  import EncabezadoPlataforma from '../plataforma/EncabezadoPlataforma.vue';
  import ModalEliminar from './ModalEliminar.vue';
 
  
  export default {
    name: 'DetalleDispositivo',
    components: {
      BarraLateralPlataforma,
      EncabezadoPlataforma,
      ModalEliminar
    },
    data() {
  return {
    dispositivo: {
      id: 1,
      nombre_de_sensor: '',
      tipo: '',
      fecha_creacion: '',
      esta_habilitado: true,
      dispositivo_id: null
    },
    sensores: [],
    mostrarModal: true,
    urlEliminar: null,
    mostrarModalEliminar: false,

      // Datos simulados de la base de datos
      proyectos: [
        { id: 1, nombre: 'Proyecto Solar' },
        { id: 2, nombre: 'Red Inteligente' },
        { id: 3, nombre: 'Domótica Escolar' }
      ]
    
  }
}
,
mounted() {
  this.sensores = [
    {
      id: 1,
      nombre_de_sensor: 'ht22',
      tipo: 'Temperatura',
      fecha_creacion: '2025-05-01',
      esta_habilitado: true,
      dispositivo_id: 1
    }
  ];

  this.dispositivo = {
    id: 1,
    nombre_de_dispositivo: 'Termómetro Inteligente',
    descripcion: 'Termómetro inteligente con conexión Wi-Fi para monitoreo remoto.',
    sensor_set_count: 5,
    tipo: 'Temperatura',
    latitud: '19',
    longitud: '-99',
    esta_habilitado: true,
    proyecto_id: 1
  };
}

,
    methods: {
  modificar() {

    console.log("Modificando...", this.dispositivo);

  },
  cancelar() {
 
  },
  confirmarEliminar(sensorId) {
    this.urlEliminar = `http://localhost:8000/dashboard/sensores/${sensorId}/eliminar`;
    this.abrirModalEliminar(sensorId);
  },
  abrirModalEliminar(id) {
    this.idEliminar = id;
    this.mostrarModalEliminar = true;
  },
  cerrarModalEliminar() {
    this.mostrarModalEliminar = false;
    this.idEliminar = null;
  },
  
  
  eliminar() {
    fetch(this.urlEliminar, {
      method: "GET",
    }).then(response => {
      if (response.ok) {
        alert("Sensor eliminado. La página se recargará.");
        setTimeout(() => location.reload(), 3000);
      } else {
        alert("Error al eliminar el sensor.");
      }
    });
    this.cerrarModalEliminar();
  }
}

  };
  </script>
  
  <style scoped lang="scss">


    @import '@/assets/css/dashboard/tabla.css';
    @import '@/assets/css/dashboard/formulario.css';
    @import '@/assets/css/dashboard/ver_dispositivo.css';
    @import '@/assets/css/modal.css';

  .plataforma-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f8f9fa; /* Gris claro de fondo */
}

.plataforma-contenido {
  flex-grow: 1;
  padding: 20px; /* Añadir padding general al contenido */
  padding-left: 270px; /* Para dejar espacio a la barra lateral */
}
  </style>


