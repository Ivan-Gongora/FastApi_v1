<template>
  <div class="plataforma-layout">
    <BarraLateralPlataforma />
    <div class="plataforma-contenido">
      <EncabezadoPlataforma />
      <div class="plataforma-tarjetas p-4">
        <div class="container-simulacion-csv">
          <h1>Simulador de Sensores IoT Avanzado</h1>

          <label for="proyecto_select">Seleccionar Proyecto:</label>
          <select id="proyecto_select" v-model="selectedProyectoId" :disabled="!proyectos.length">
            <option value="">{{ proyectos.length ? 'Selecciona un proyecto' : 'Cargando proyectos...' }}</option>
            <option v-for="proyecto in proyectos" :key="proyecto.id" :value="proyecto.id">
              {{ proyecto.nombre }}
            </option>
          </select>

          <label for="dispositivo_select">Seleccionar Dispositivo:</label>
          <select id="dispositivo_select" v-model="selectedDispositivoId" :disabled="!dispositivos.length">
            <option value="">
              {{ selectedProyectoId ? (dispositivos.length ? 'Selecciona un dispositivo' : 'No hay dispositivos para este proyecto') : 'Selecciona un proyecto primero' }}
            </option>
            <option v-for="dispositivo in dispositivos" :key="dispositivo.id" :value="dispositivo.id">
              {{ dispositivo.nombre }}
            </option>
          </select>

          <hr />

          <label for="num_sensores">¿Cuántos tipos de sensores vas a configurar? (según el CSV):</label>
          <input type="number" id="num_sensores" v-model.number="numSensores" min="1" />
          <button @click="generarCamposMapeo">Configurar Mapeo de Sensores</button>

          <div id="sensores_mapeo_container" class="mapping-section">
            <p v-if="!selectedDispositivoId" class="warning">
              Selecciona un dispositivo primero para poder configurar los sensores.
            </p>
            <p v-else-if="csvHeaders.length === 0" class="error">
              Por favor, carga un archivo CSV para ver los encabezados y configurar el mapeo.
            </p>
            <p v-else-if="todosLosSensoresDisponibles.length === 0" class="warning">
              No hay sensores disponibles para el dispositivo seleccionado. Asegúrate de haber seleccionado un dispositivo con sensores.
            </p>
            <p v-else-if="sensorMappings.length === 0 && numSensores > 0" class="warning">
              Define el número de sensores y haz clic en "Configurar Mapeo".
            </p>

            <div class="sensor-mapping-item" v-for="(mapping, index) in sensorMappings" :key="index">
              <div>
                <label :for="`sensor_select_${index}`">Sensor #{{ index + 1 }}:</label>
                <select :id="`sensor_select_${index}`" v-model="mapping.sensor_id" @change="cargarCamposParaMapeo(mapping, index)">
                  <option value="">Selecciona un sensor</option>
                  <option v-for="sensor in todosLosSensoresDisponibles" :key="sensor.id" :value="sensor.id">
                    {{ sensor.nombre }}
                  </option>
                </select>
              </div>
              <div>
                <label :for="`campo_select_${index}`">Campo del Sensor #{{ index + 1 }}:</label>
                <select :id="`campo_select_${index}`" v-model="mapping.campo_id" :disabled="!mapping.sensor_id">
                  <option value="">
                    {{ mapping.sensor_id ? (todosLosCamposDisponibles[mapping.sensor_id] && todosLosCamposDisponibles[mapping.sensor_id].length ? 'Selecciona un campo' : 'No hay campos para este sensor') : 'Selecciona un sensor primero' }}
                  </option>
                  <option v-for="campo in todosLosCamposDisponibles[mapping.sensor_id]" :key="campo.id" :value="campo.id">
                    {{ campo.nombre }}
                  </option>
                </select>
              </div>
              <div>
                <label :for="`csv_header_select_${index}`">Columna CSV (#{{ index + 1 }}):</label>
                <select :id="`csv_header_select_${index}`" v-model="mapping.csv_column_name">
                  <option value="">Selecciona una columna CSV</option>
                  <option v-for="header in csvHeaders" :key="header" :value="header">
                    {{ header }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <hr />

          <label for="csv_file">Seleccionar Archivo CSV:</label>
          <input type="file" id="csv_file" accept=".csv" @change="handleFileUpload" />
          <div id="csv_preview" v-if="csvPreviewText">{{ csvPreviewText }}</div>

          <button @click="startSimulation">Iniciar Simulación</button>

          <h2>Log de Simulación:</h2>
          <pre id="log"><p v-for="(logItem, index) in logMessages" :key="index" :class="logItem.type">{{ logItem.text }}</p></pre>
        </div>
      </div>
    </div>
  </div>
</template>



<script setup>
import { ref, onMounted, watch } from 'vue';
import BarraLateralPlataforma from '../plataforma/BarraLateralPlataforma.vue';
import EncabezadoPlataforma from '../plataforma/EncabezadoPlataforma.vue';

// Configuration
const API_BASE_URL = 'http://127.0.0.1:8001/api';

// Reactive State
const proyectos = ref([]);
const dispositivos = ref([]);
const todosLosSensoresDisponibles = ref([]);
const todosLosCamposDisponibles = ref({}); // { sensorId: [campos] }
const csvHeaders = ref([]);
const selectedProyectoId = ref('');
const selectedDispositivoId = ref('');
const numSensores = ref(2);
const sensorMappings = ref([]); // [{ sensor_id: null, campo_id: null, csv_column_name: null }]
const csvFile = ref(null);
const csvPreviewText = ref('');
const logMessages = ref([]);

// Utility Functions
const logMessage = (message, type = 'info') => {
  logMessages.value.push({
    text: `[${new Date().toLocaleTimeString()}] ${message}`,
    type: type,
  });
  // Ensure log scrolls to bottom
  const logElement = document.getElementById('log');
  if (logElement) {
    logElement.scrollTop = logElement.scrollHeight;
  }
};

// --- API Interactions ---
const displayCsvPreviewFromBackend = async (file) => {
  csvPreviewText.value = 'Cargando previsualización del CSV desde el servidor...';
  csvHeaders.value = [];

  if (!file) {
    csvPreviewText.value = 'No hay archivo CSV seleccionado.';
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/csv-preview/`, {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      csvHeaders.value = data.header || [];
      let preview = '';
      if (csvHeaders.value.length > 0) {
        preview += csvHeaders.value.join(', ') + '\n';
      }
      if (data.preview_rows && data.preview_rows.length > 0) {
        data.preview_rows.forEach((row) => {
          preview += row.join(', ') + '\n';
        });
      }
      if (data.message === 'El archivo CSV está vacío.') {
        preview = 'El archivo CSV está vacío.';
      } else if (data.preview_rows.length === 5) {
        preview += '...\n';
      }
      csvPreviewText.value = `Contenido del CSV:\n\n${preview}`;
      logMessage(`Previsualización de "${file.name}" cargada desde el backend.`, 'success');
      // After loading CSV, try to re-generate mapping fields if device is selected
      if (selectedDispositivoId.value) {
        generarCamposMapeo();
      }
    } else {
      const errorData = await response.json();
      csvPreviewText.value = `Error al obtener previsualización: ${errorData.detail || response.statusText}`;
      logMessage(`Error al obtener previsualización del CSV desde el backend: ${errorData.detail || response.statusText}`, 'error');
    }
  } catch (error) {
    csvPreviewText.value = `Error de red al conectar con el backend para la previsualización: ${error.message}`;
    logMessage(`Error de red para previsualización: ${error.message}`, 'error');
  }
};

const cargarProyectos = async () => {
  logMessage('Cargando proyectos...');
  try {
    const response = await fetch(`${API_BASE_URL}/proyectos`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    proyectos.value = await response.json();
    logMessage('Proyectos cargados.', 'success');
  } catch (error) {
    logMessage(`Error al cargar proyectos: ${error.message}`, 'error');
    proyectos.value = [];
  }
};

const cargarDispositivos = async (proyectoId) => {
  dispositivos.value = []; // Clear previous devices
  selectedDispositivoId.value = ''; // Reset selected device
  todosLosSensoresDisponibles.value = []; // Clear sensors and fields
  todosLosCamposDisponibles.value = {};
  sensorMappings.value = []; // Clear mappings

  if (!proyectoId) {
    logMessage('No se seleccionó un proyecto.', 'warning');
    return;
  }
  logMessage(`Cargando dispositivos para proyecto ${proyectoId}...`);
  try {
    const response = await fetch(`${API_BASE_URL}/proyectos/${proyectoId}/dispositivos`);
    if (!response.ok) {
      if (response.status === 404) {
        logMessage(`No hay dispositivos para el proyecto ID ${proyectoId}.`, 'warning');
        return;
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    dispositivos.value = await response.json();
    logMessage('Dispositivos cargados.', 'success');
  } catch (error) {
    logMessage(`Error al cargar dispositivos: ${error.message}`, 'error');
  }
};

const cargarSensoresYCamposParaDispositivo = async (dispositivoId) => {
  todosLosSensoresDisponibles.value = [];
  todosLosCamposDisponibles.value = {};
  sensorMappings.value = []; // Clear mappings if device changes

  if (!dispositivoId) {
    logMessage('No se seleccionó un dispositivo.', 'warning');
    return;
  }
  logMessage(`Cargando sensores y campos para dispositivo ${dispositivoId}...`);
  try {
    const responseSensores = await fetch(`${API_BASE_URL}/dispositivos/${dispositivoId}/sensores`);
    if (!responseSensores.ok) {
      if (responseSensores.status === 404) {
        logMessage(`No hay sensores para el dispositivo ID ${dispositivoId}.`, 'warning');
        return;
      }
      throw new Error(`HTTP error! status: ${responseSensores.status}`);
    }
    todosLosSensoresDisponibles.value = await responseSensores.json();

    for (const sensor of todosLosSensoresDisponibles.value) {
      const responseCampos = await fetch(`${API_BASE_URL}/sensores/${sensor.id}/campos`);
      if (!responseCampos.ok) {
        logMessage(`No hay campos para el sensor ID ${sensor.id}.`, 'warning');
        todosLosCamposDisponibles.value[sensor.id] = [];
        continue;
      }
      todosLosCamposDisponibles.value[sensor.id] = await responseCampos.json();
    }
    logMessage('Sensores y campos cargados.', 'success');
    // After loading sensors/fields, trigger mapping generation
    generarCamposMapeo();
  } catch (error) {
    logMessage(`Error al cargar sensores/campos: ${error.message}`, 'error');
  }
};

const cargarCamposParaMapeo = (mapping, index) => {
  // This function is now mostly handled by the v-model and computed properties
  // The relevant logic for updating available fields is in `todosLosCamposDisponibles`
  // and the reactivity of Vue will handle the <select> options automatically.
  // We just need to ensure the campo_id is reset if the sensor changes.
  mapping.campo_id = null; // Reset selected field when sensor changes
};

// --- Dynamic Mapping Generation ---
const generarCamposMapeo = () => {
  sensorMappings.value = []; // Clear previous mappings

  const num = parseInt(numSensores.value);

  if (isNaN(num) || num <= 0) {
    logMessage('Ingresa un número válido de sensores (debe ser 1 o más).', 'warning');
    return;
  }

  if (!selectedDispositivoId.value) {
    logMessage('Selecciona un dispositivo primero para poder configurar los sensores.', 'warning');
    return;
  }

  if (todosLosSensoresDisponibles.value.length === 0) {
    logMessage('No hay sensores disponibles para el dispositivo seleccionado.', 'warning');
    return;
  }

  if (csvHeaders.value.length === 0) {
    logMessage('Por favor, carga un archivo CSV para ver los encabezados y configurar el mapeo.', 'error');
    return;
  }

  for (let i = 0; i < num; i++) {
    sensorMappings.value.push({
      sensor_id: null,
      campo_id: null,
      csv_column_name: null,
    });
  }
  if (num > 0) {
    logMessage(`Generados ${num} campos de mapeo de sensores.`, 'info');
  }
};

// --- Event Handlers ---
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  csvFile.value = file; // Store the file in reactive state
  if (file) {
    displayCsvPreviewFromBackend(file);
  } else {
    csvPreviewText.value = '';
    csvHeaders.value = [];
    logMessage('No se seleccionó ningún archivo CSV.', 'warning');
  }
};

const startSimulation = async () => {
  logMessages.value = []; // Clear log on new simulation attempt

  if (!csvFile.value) {
    logMessage('Por favor, selecciona un archivo CSV.', 'error');
    return;
  }
  if (!selectedProyectoId.value || !selectedDispositivoId.value) {
    logMessage('Por favor, selecciona un Proyecto y un Dispositivo.', 'error');
    return;
  }
  if (csvHeaders.value.length === 0) {
    logMessage('No se pudo obtener la cabecera del CSV. Por favor, asegúrate de que el archivo es válido y vuelve a intentarlo.', 'error');
    return;
  }

  const mapeosValidos = [];
  for (const mapping of sensorMappings.value) {
    if (mapping.sensor_id && mapping.campo_id && mapping.csv_column_name) {
      // Find the campo_nombre from todosLosCamposDisponibles
      const sensorCampos = todosLosCamposDisponibles.value[mapping.sensor_id] || [];
      const selectedCampo = sensorCampos.find(c => c.id === mapping.campo_id);
      if (selectedCampo) {
        mapeosValidos.push({
          sensor_id: parseInt(mapping.sensor_id),
          campo_id: parseInt(mapping.campo_id),
          campo_nombre: selectedCampo.nombre, // Get the name from the loaded data
          csv_column_name: mapping.csv_column_name,
        });
      } else {
        logMessage(`Error: Campo del sensor seleccionado no encontrado para sensor ID ${mapping.sensor_id} y campo ID ${mapping.campo_id}.`, 'error');
      }
    } else {
      logMessage(`Error en la configuración del mapeo: Todos los campos (Sensor, Campo, Columna CSV) deben estar llenos para cada sensor configurado.`, 'error');
      return; // Stop if any mapping is invalid
    }
  }

  if (mapeosValidos.length === 0) {
    logMessage('No se configuró ningún mapeo de sensor válido.', 'error');
    return;
  }

  logMessage('Iniciando simulación...');
  logMessage(`Archivo seleccionado: ${csvFile.value.name}`);
  logMessage(`Proyecto: ${selectedProyectoId.value}, Dispositivo: ${selectedDispositivoId.value}`);
  logMessage(`Mapeos a enviar: ${JSON.stringify(mapeosValidos, null, 2)}`);

  const formData = new FormData();
  formData.append('file', csvFile.value);
  formData.append('sensor_mappings', JSON.stringify(mapeosValidos));
  formData.append('proyecto_id', selectedProyectoId.value);
  formData.append('dispositivo_id', selectedDispositivoId.value);

  try {
    const fastapiEndpoint = `${API_BASE_URL}/simular/`;

    const response = await fetch(fastapiEndpoint, {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      logMessage('Simulación completada con éxito:', 'success');
      logMessage(JSON.stringify(data, null, 2));
    } else {
      const errorData = await response.json();
      const errorMessage = errorData.detail ? (typeof errorData.detail === 'string' ? errorData.detail : (errorData.detail.message || JSON.stringify(errorData.detail))) : JSON.stringify(errorData);
      const errorDetails = errorData.detail && typeof errorData.detail === 'object' && errorData.detail.details ? errorData.detail.details : 'No hay detalles adicionales.';

      logMessage(`Error en la simulación: ${response.status} ${response.statusText}`, 'error');
      logMessage(`Mensaje: ${errorMessage}`, 'error');
      logMessage(`Detalles: ${errorDetails}`, 'error');
    }
  } catch (error) {
    logMessage(`Error de red o CORS: ${error.message}. Asegúrate de que el servidor FastAPI está corriendo y la configuración CORS es correcta.`, 'error');
  }
};

// --- Watchers ---
watch(selectedProyectoId, (newId) => {
  cargarDispositivos(newId);
});

watch(selectedDispositivoId, (newId) => {
  cargarSensoresYCamposParaDispositivo(newId);
});

// Lifecycle Hook
onMounted(() => {
  cargarProyectos();
});
</script>

<style scoped lang="scss">
// @import '@/assets/styles/plataforma.scss'; // Assuming you consolidate platform styles here

.container-simulacion-csv {
  max-width: 800px;
  margin: auto;
  padding: 25px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

label {
  display: block;
  margin-top: 15px;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

input[type='file'],
select,
input[type='number'],
button {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 1em;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  margin-top: 20px;
  padding: 12px 20px;
  border-radius: 5px;
  font-size: 1.1em;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #0056b3;
  }
}

.mapping-section {
  border: 1px dashed #a0a0a0;
  padding: 15px;
  margin-top: 20px;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.sensor-mapping-item {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 5px;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);

  > div {
    flex: 1;
    min-width: 250px;
  }
}

#csv_preview {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #d4edda;
  background-color: #d4edda;
  overflow-x: auto;
  white-space: pre;
  font-family: monospace;
  font-size: 0.9em;
  border-radius: 5px;
  color: #155724;
  max-height: 200px;
  overflow-y: auto;
}

#log {
  margin-top: 30px;
  padding: 15px;
  border: 1px solid #eee;
  background-color: #f9f9f9;
  height: 250px;
  overflow-y: scroll;
  white-space: pre-wrap;
  font-family: monospace;
  font-size: 0.9em;
  border-radius: 5px;

  p {
    margin: 0;
    padding: 2px 0;
  }
}

.error {
  color: #dc3545;
}
.success {
  color: #28a745;
}
.info {
  color: #007bff;
}
.warning {
  color: #ffc107;
}

hr {
  border: none;
  border-top: 1px solid #eee;
  margin: 30px 0;
}

// Inherit platform layout styles
.plataforma-layout {
  display: flex;
}

.plataforma-contenido {
  flex: 1;
  margin-left: 250px; /* Igual que barra lateral */
  background-color: #f8f9fa;
  min-height: 100vh;
}

.plataforma-tarjetas {
  padding: 20px 0;
  /* Not a grid in this context, but keeping padding for consistency */
}
</style>