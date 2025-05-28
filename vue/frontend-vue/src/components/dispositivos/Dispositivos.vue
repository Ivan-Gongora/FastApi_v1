<template>
   <!-- Tabla de dispositivos -->
    <div v-if="dispositivos.length > 0">
      <table class="tabla">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Sensores</th>
            <th>Tipo</th>
            <th>Latitud</th>
            <th>Longitud</th>
            <th>Habilitado</th>
            <th colspan="2">Opciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dispositivo in dispositivos" :key="dispositivo.id">
            <td>{{ dispositivo.nombre_de_dispositivo }}</td>
            <td>{{ truncarDescripcion(dispositivo.descripcion) }}</td>
            <td>{{ dispositivo.sensor_set_count }}</td>
            <td>{{ dispositivo.tipo }}</td>
            <td>{{ dispositivo.latitud }}</td>
            <td>{{ dispositivo.longitud }}</td>
            <td class="centrado">
              <input type="checkbox" :checked="dispositivo.esta_habilitado" disabled>
            </td>
            <td class="opciones">
              <!-- Tabla de dispositivos <a :href="`/dashboard/detalle-dispositivo/${dispositivo.id}`"-->
            
                <router-link to="/detalle-dispositivo" class="ion-eye"></router-link>
        
            </td>
            <td class="opciones">
              <a @click="confirmarEliminar(dispositivo.id)">
                <span class="ion-trash-a"></span>
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <h2 class="margen">Aun no cuentas con Dispositivos..</h2>
    </div>

 
  <CrearDispositivo 
  v-if="mostrarModalCrear"
  @crear="crearDispositivo"
  @cerrar="cerrarModalCrear"
  :class="{ visible: mostrarModalCrear }"
/>
  <!-- Modal Confirmar Eliminación -->
  <ModalEliminar titulo = "Esta por eliminar un dispositivo, esta acción no tiene modo de revertirse."
  :class="{ modal: true, advertencia: true, visible: mostrarModalEliminar }"
  @confirmar="eliminarDispositivo"
  @cancelar="mostrarModalEliminar = false"
   />

    <!-- Botón Nuevo Dispositivo -->
    <div class="centrado">
      <input @click="abrirModalCrear" class="btn btn-info" type="button" value="Nuevo Dispositivo" style="color: white;">
    </div>

  
  
</template>

<script>

import CrearDispositivo from './CrearDispositivo.vue';
import ModalEliminar from './ModalEliminar.vue';

export default {
  name: 'ListaDispositivos',
  components: {
    CrearDispositivo,
    ModalEliminar
  },
  data() {
    return {
      mostrarModalCrear: false,
      mostrarModalEliminar: false,
      idEliminar: null,
      dispositivos: []  // Comienza como un array vacío
    }
  },
  mounted() {
    // Simular obtención de datos
    this.dispositivos = [
      {
        id: 1,
        nombre_de_dispositivo: 'Termómetro Inteligente',
        descripcion: 'Termómetro inteligente con conexión Wi-Fi para monitoreo remoto.',
        sensor_set_count: 5,
        tipo: 'Temperatura',
        latitud: '19.4326',
        longitud: '-99.1332',
        esta_habilitado: true
      },
      {
        id: 2,
        nombre_de_dispositivo: 'Higrómetro',
        descripcion: 'Dispositivo para medir la humedad ambiental.',
        sensor_set_count: 3,
        tipo: 'Humedad',
        latitud: '19.4312',
        longitud: '-99.1345',
        esta_habilitado: false
      },
      {
        id: 3,
        nombre_de_dispositivo: 'Estación Meteorológica',
        descripcion: 'Estación completa para monitoreo de clima en tiempo real.',
        sensor_set_count: 8,
        tipo: 'Clima',
        latitud: '19.4315',
        longitud: '-99.1350',
        esta_habilitado: true
      }
    ];
  },
  methods: {
    abrirModalCrear() {
      this.mostrarModalCrear = true;
    },
    cerrarModalCrear() {
      this.mostrarModalCrear = false;
      this.nuevoDispositivo = { nombre: '', descripcion: '' };
    },
    confirmarEliminar(id) {
      this.idEliminar = id;
      this.mostrarModalEliminar = true;
    },
    cerrarModalEliminar() {
      this.mostrarModalEliminar = false;
      this.idEliminar = null;
    },
    eliminarDispositivoConfirmado() {
      console.log(`Eliminar dispositivo con ID ${this.idEliminar}`);
      this.dispositivos = this.dispositivos.filter(dispositivo => dispositivo.id !== this.idEliminar);
      this.cerrarModalEliminar();
    },
    crearDispositivo(dispositivo) {
      console.log('Crear nuevo dispositivo', dispositivo);
      this.dispositivos.push(dispositivo);
      this.cerrarModalCrear();
    },
    truncarDescripcion(descripcion) {
      if (!descripcion) return '';
      const palabras = descripcion.split(' ');
      return palabras.length > 7 ? palabras.slice(0, 7).join(' ') + '...' : descripcion;
    }
  }
}


</script>

<style scoped>
@import '@/assets/css/dashboard/tabla.css';
@import '@/assets/css/dashboard/formulario.css';
@import '@/assets/css/modal.css';
/* Agrega estilos específicos si quieres */
</style>

