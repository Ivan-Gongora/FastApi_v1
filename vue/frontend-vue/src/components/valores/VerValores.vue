<template>
  <div class="plataforma-layout">
    <BarraLateralPlataforma />
    <div class="plataforma-contenido">
      <EncabezadoPlataforma titulo="Valores" />

      <div class="tabla-wrapper">
        <h2 class="titulo">Valores Registrados</h2>
        <table class="tabla-valores">
          <thead>
            <tr>
              <th>ID</th>
              <th>Valor</th>
              <th>Fecha y Hora</th>
              <th>Campo ID</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(registro, index) in valores" :key="registro.id">
              <td>{{ registro.id }}</td>
              <td>
                <input v-model="registro.valor" class="editable" type="text" />
              </td>
              <td>
                <input v-model="registro.fecha_hora_lectura" class="editable" type="datetime-local" />
              </td>
              <td>
                <input v-model.number="registro.campo_id" class="editable" type="number" />
              </td>
              <td>
                <button @click="guardar(index)">Guardar</button>
                <button @click="mostrarModalEliminar(registro.id)">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <ModalEliminar
        v-if="mostrarModal"
        :titulo="'¿Está seguro que desea eliminar el registro ID ' + idAEliminar + '?'"
        @confirmar="confirmarEliminar"
        @cancelar="cancelarEliminar"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import ModalEliminar from '../valores/ModalEliminarValores.vue';
import BarraLateralPlataforma from '../plataforma/BarraLateralPlataforma.vue';
import EncabezadoPlataforma from '../plataforma/EncabezadoPlataforma.vue';

export default {
  name: 'TablaValores',
  components: {
    ModalEliminar,
    BarraLateralPlataforma,
    EncabezadoPlataforma,
  },
  setup() {
    const API_BASE_URL = 'http://127.0.0.1:8001';

    const valores = ref([]);
    const logMessages = ref([]);
    const mostrarModal = ref(false);
    const idAEliminar = ref(null);

    const logMessage = (message, type = 'info') => {
      logMessages.value.push({
        text: `[${new Date().toLocaleTimeString()}] ${message}`,
        type: type,
      });
      setTimeout(() => {
        const logElement = document.getElementById('log');
        if (logElement) {
          logElement.scrollTop = logElement.scrollHeight;
        }
      }, 0);
    };

    const cargarValores = async () => {
      logMessage('Cargando valores...');
      try {
        const response = await fetch(`${API_BASE_URL}/valores/`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        valores.value = await response.json();
        logMessage('Valores cargados correctamente.', 'success');
      } catch (error) {
        logMessage(`Error al cargar valores: ${error.message}`, 'error');
      }
    };

    const actualizarValor = async (valorActualizado) => {
    try {
        const url = new URL(`${API_BASE_URL}/valores/`);
        url.searchParams.append('id', valorActualizado.id);

        const response = await fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            valor: valorActualizado.valor,
            fecha_hora_lectura: valorActualizado.fecha_hora_lectura,
            campo_id: valorActualizado.campo_id
        })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        logMessage(`Valor con ID ${valorActualizado.id} actualizado correctamente.`, 'success');
    } catch (error) {
        logMessage(`Error al actualizar valor: ${error.message}`, 'error');
    }
    };

    const guardar = async (index) => {
      const valor = valores.value[index];
      await actualizarValor(valor);
    };

    const eliminarValor = async (id) => {
      try {
        const url = new URL(`${API_BASE_URL}/valores/`);
        url.searchParams.append('id', id);

        const response = await fetch(url, {
          method: 'DELETE'
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        valores.value = valores.value.filter((v) => v.id !== id);
        logMessage(`Valor con ID ${id} eliminado.`, 'success');
      } catch (error) {
        logMessage(`Error al eliminar valor: ${error.message}`, 'error');
      }
    };

    const mostrarModalEliminar = (id) => {
      idAEliminar.value = id;
      mostrarModal.value = true;
    };

    const cancelarEliminar = () => {
      mostrarModal.value = false;
      idAEliminar.value = null;
    };

    const confirmarEliminar = async () => {
      await eliminarValor(idAEliminar.value);
      cancelarEliminar();
    };

    onMounted(cargarValores);

    return {
      valores,
      guardar,
      mostrarModalEliminar,
      confirmarEliminar,
      cancelarEliminar,
      mostrarModal,
      idAEliminar,
    };
  },
};
</script>

<style scoped lang="scss">
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

.titulo {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.tabla-wrapper {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.tabla-valores {
  width: 100%;
  border-collapse: collapse;

  th,
  td {
    border: 1px solid #ddd;
    padding: 8px;
  }

  th {
    background-color: #e9ecef;
    text-align: left;
  }

  .editable {
    width: 100%;
    padding: 4px;
    box-sizing: border-box;
  }

  button {
    margin-right: 5px;
    padding: 4px 8px;
    cursor: pointer;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;

    &:last-child {
      background-color: #dc3545;
    }
  }
}
</style>
