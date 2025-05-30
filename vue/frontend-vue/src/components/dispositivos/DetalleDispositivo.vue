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

        <!-- Tabla de sensores -->
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
        <ModalEliminar
          titulo="Esta por eliminar un sensor, esta acción no tiene modo de revertirse."
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

const API_BASE_URL = "http://localhost:8001"; // Cambia por tu URL real

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
        id: null,
        nombre_de_dispositivo: '',
        descripcion: '',
        tipo: '',
        latitud: null,
        longitud: null,
        esta_habilitado: false,
        fecha_creacion: '',
        proyecto_id: null,
      },
      sensores: [],
      proyectos: [
        { id: 1, nombre: 'Proyecto Solar' },
        { id: 2, nombre: 'Red Inteligente' },
        { id: 3, nombre: 'Domótica Escolar' }
      ],
      mostrarModalEliminar: false,
      urlEliminar: null,
      idEliminar: null,
    };
  },
  mounted() {
    // Obtener el id dinámico desde la ruta
    const dispositivoId = this.$route.params.id;
    if (dispositivoId) {
      this.cargarDispositivo(dispositivoId);
      this.cargarSensores(dispositivoId);
    } else {
      alert('No se encontró ID del dispositivo en la ruta.');
    }
  },
  methods: {
    async cargarDispositivo(id) {
      try {
        const res = await fetch(`${API_BASE_URL}/dispositivos/${id}`);
        if (!res.ok) throw new Error(`Error al cargar dispositivo: ${res.status}`);
        const data = await res.json();
        this.dispositivo = {
          id: data.id,
          nombre_de_dispositivo: data.nombre,
          descripcion: data.descripcion,
          tipo: data.tipo,
          latitud: data.latitud,
          longitud: data.longitud,
          esta_habilitado: data.habilitado,
          fecha_creacion: data.fecha_creacion,
          proyecto_id: data.proyecto_id,
        };
      } catch (error) {
        alert(error.message);
      }
    },
    async cargarSensores(dispositivoId) {
      try {
        const res = await fetch(`${API_BASE_URL}/sensores?dispositivo_id=${dispositivoId}`);
        if (!res.ok) throw new Error(`Error al cargar sensores: ${res.status}`);
        const data = await res.json();
        this.sensores = data.map(sensor => ({
          id: sensor.id,
          nombre_de_sensor: sensor.nombre,
          tipo: sensor.tipo,
          fecha_creacion: sensor.fecha_creacion,
          esta_habilitado: sensor.habilitado,
          dispositivo_id: sensor.dispositivo_id,
          unidad_medida_id: sensor.unidad_medida_id,
        }));
      } catch (error) {
        alert(error.message);
      }
    },
    async modificar() {
      try {
        const dispActualizar = {
          nombre: this.dispositivo.nombre_de_dispositivo,
          descripcion: this.dispositivo.descripcion,
          tipo: this.dispositivo.tipo,
          latitud: this.dispositivo.latitud,
          longitud: this.dispositivo.longitud,
          habilitado: this.dispositivo.esta_habilitado,
          proyecto_id: this.dispositivo.proyecto_id,
        };

        const res = await fetch(`${API_BASE_URL}/dispositivos/${this.dispositivo.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(dispActualizar),
        });

        if (!res.ok) {
          throw new Error(`Error al actualizar dispositivo: ${res.status}`);
        }
        alert("Dispositivo actualizado correctamente");
        this.cargarDispositivo(this.dispositivo.id);
      } catch (error) {
        alert(error.message);
      }
    },
    confirmarEliminar(sensorId) {
      this.urlEliminar = `${API_BASE_URL}/sensores/${sensorId}/eliminar`;
      this.idEliminar = sensorId;
      this.mostrarModalEliminar = true;
    },
    cerrarModalEliminar() {
      this.mostrarModalEliminar = false;
      this.idEliminar = null;
      this.urlEliminar = null;
    },
    async eliminarDispositivo() {
      try {
        const res = await fetch(this.urlEliminar, { method: "DELETE" });
        if (!res.ok) throw new Error(`Error al eliminar sensor: ${res.status}`);
        alert("Sensor eliminado, recargando...");
        this.cargarSensores(this.dispositivo.id);
      } catch (error) {
        alert(error.message);
      } finally {
        this.cerrarModalEliminar();
      }
    },
  },
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
  padding: 20px;
  padding-left: 270px; /* espacio para barra lateral */
}
</style>
