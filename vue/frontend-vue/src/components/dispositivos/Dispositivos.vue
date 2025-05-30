<template>
  <div class="plataforma-layout">
    <BarraLateralPlataforma />
    <div class="plataforma-contenido">
      <EncabezadoPlataforma titulo="Dispositivos" />

      <div v-if="dispositivos.length">
        <table class="tabla">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Tipo</th>
              <th>Latitud</th>
              <th>Longitud</th>
              <th>Habilitado</th>
              <th>Proyecto ID</th>
              <th>Fecha Creación</th>
              <th colspan="2">Opciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(disp) in dispositivos" :key="disp.id">
              <td>{{ disp.id }}</td>
              <td>{{ disp.nombre }}</td>
              <td>{{ disp.descripcion }}</td>
              <td>{{disp.tipo}}</td>
              <td>{{disp.latitud}}</td>
              <td>{{disp.longitud}}</td>
              <td>{{disp.habilitado}}</td>
              <td>{{disp.proyecto_id}}</td>
              <td>{{ new Date(disp.fecha_creacion).toLocaleDateString() }}</td>
              <td class="opciones">
                <router-link :to="`/detalle-dispositivo/${disp.id}`"><span class="ion-eye"></span></router-link>
              </td>
              <td class="opciones">
                <a @click="abrirModalEliminar(disp.id)"><span class="ion-trash-a"></span></a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <h2 class="margen">Aún no hay dispositivos registrados.</h2>
      </div>

      <div class="centrado">
        <button class="btn btn-info" @click="abrirModalCrear">Nuevo Dispositivo</button>
      </div>

      <!-- Modal Crear Dispositivo -->
      <CrearDispositivo
        v-if="mostrarModalCrear"
        @crear="crearDispositivo"
        @cerrar="cerrarModalCrear"
      />

      <!-- Modal Confirmar Eliminación -->
      <ModalEliminar
        v-if="mostrarModalEliminar"
        :titulo="'¿Está seguro que desea eliminar el registro ID ' + idAEliminar + '?'"
        @confirmar="confirmarEliminar"
        @cancelar="cerrarModalEliminar"
      />
    </div>
  </div>
</template>


<script>
import { ref, onMounted } from "vue";
import BarraLateralPlataforma from "../plataforma/BarraLateralPlataforma.vue";
import EncabezadoPlataforma from "../plataforma/EncabezadoPlataforma.vue";
import CrearDispositivo from "../dispositivos/CrearDispositivo.vue";
import ModalEliminar from "../dispositivos/ModalEliminar.vue";

export default {
  name: "ListaDispositivos",
  components: {
    BarraLateralPlataforma,
    EncabezadoPlataforma,
    CrearDispositivo,
    ModalEliminar,
  },
  setup() {
    const API_BASE_URL = "http://127.0.0.1:8001";

    const dispositivos = ref([]);
    const mostrarModalCrear = ref(false);
    const mostrarModalEliminar = ref(false);
    const idAEliminar = ref(null);

    // Cargar dispositivos (GET)
    const cargarDispositivos = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/dispositivos`);
    if (!res.ok) throw new Error(`Error: ${res.status}`);
    const data = await res.json();
    dispositivos.value = data.map(d => ({
      id: d.id,
      nombre: d.nombre,
      descripcion: d.descripcion,
      tipo: d.tipo,
      latitud: d.latitud,
      longitud: d.longitud,
      habilitado: d.habilitado,
      fecha_creacion: d.fecha_creacion,
      proyecto_id: d.proyecto_id,
    }));
  } catch (error) {
    alert("Error cargando dispositivos: " + error.message);
  }
};

const crearDispositivo = (nuevoDispositivo) => {
  dispositivos.value.push(nuevoDispositivo); // Puedes hacer una petición POST aquí también
  cerrarModalCrear();
};

    // Eliminar dispositivo (DELETE)
    const eliminarDispositivo = async (id) => {
      try {
        const res = await fetch(`${API_BASE_URL}/dispositivos/${id}`, {
          method: "DELETE",
        });
        if (!res.ok) throw new Error(`Error: ${res.status}`);
        dispositivos.value = dispositivos.value.filter((d) => d.id !== id);
        cerrarModalEliminar();
      } catch (error) {
        alert("Error eliminando dispositivo: " + error.message);
      }
    };

    const abrirModalEliminar = (id) => {
      idAEliminar.value = id;
      mostrarModalEliminar.value = true;
    };

    const cerrarModalEliminar = () => {
      mostrarModalEliminar.value = false;
      idAEliminar.value = null;
    };

    const confirmarEliminar = () => {
      eliminarDispositivo(idAEliminar.value);
    };

    const abrirModalCrear = () => {
      mostrarModalCrear.value = true;
    };

    const cerrarModalCrear = () => {
      mostrarModalCrear.value = false;
    };

    onMounted(cargarDispositivos);

    return {
      dispositivos,
      mostrarModalCrear,
      mostrarModalEliminar,
      idAEliminar,
      abrirModalEliminar,
      cerrarModalEliminar,
      confirmarEliminar,
      abrirModalCrear,
      cerrarModalCrear,
      crearDispositivo,
    };
  },
};
</script>

<style scoped>
@import '@/assets/css/dashboard/tabla.css';
@import '@/assets/css/dashboard/formulario.css';
@import '@/assets/css/modal.css';
/* Estilos adicionales si quieres */
</style>
