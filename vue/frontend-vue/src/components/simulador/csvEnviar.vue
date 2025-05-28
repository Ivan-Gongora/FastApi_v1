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
const numSensores = ref(2); // Initial value for number of sensors
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
  // Using nextTick to ensure DOM is updated before scrolling
  // or Vue might not have rendered the new log entry yet.
  setTimeout(() => { // Using setTimeout as a simple nextTick substitute
    const logElement = document.getElementById('log');
    if (logElement) {
      logElement.scrollTop = logElement.scrollHeight;
    }
  }, 0);
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
      } else if (data.preview_rows.length === 5) { // Assuming 5 is the max preview rows
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
    // *** CRITICAL FIX: Ensure your FastAPI endpoint for /proyectos returns 'descripcion' and 'usuario_id' ***
    // This is the source of your ResponseValidationError
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
    generarCamposMapeo(); // Call this to populate mappings after sensors/fields are loaded
  } catch (error) {
    logMessage(`Error al cargar sensores/campos: ${error.message}`, 'error');
  }
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
      csv_column_name: null, // This was missing in your Vue version for the structure
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
    // Ensure all mapping fields are selected
    if (mapping.sensor_id && mapping.campo_id && mapping.csv_column_name) {
      // Find the campo_nombre from todosLosCamposDisponibles
      const sensorCampos = todosLosCamposDisponibles.value[mapping.sensor_id] || [];
      const selectedCampo = sensorCampos.find(c => c.id === mapping.campo_id);

      if (selectedCampo) {
        mapeosValidos.push({
          sensor_id: parseInt(mapping.sensor_id),
          campo_id: parseInt(mapping.campo_id),
          campo_nombre: selectedCampo.nombre, // Get the name from the loaded data
          csv_column_name: mapping.csv_column_name, // This should be present now
        });
      } else {
        logMessage(`Error: Campo del sensor seleccionado no encontrado para sensor ID ${mapping.sensor_id} y campo ID ${mapping.campo_id}.`, 'error');
        return; // Stop if there's an internal inconsistency
      }
    } else {
      logMessage(`Error en la configuración del mapeo: Todos los campos (Sensor, Campo, Columna CSV) deben estar llenos para cada sensor configurado.`, 'error');
      return; // Stop if any mapping is incomplete
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

// Lifecycle Hook - Called when the component is mounted
onMounted(() => {
  cargarProyectos();
});
</script>

<template>
  <div class="simulacion-view">
    <BarraLateralPlataforma />
    <div class="main-content">
      <EncabezadoPlataforma />
      <div class="container-fluid">
        <h2>Simulación de Datos IoT</h2>

        <div class="form-section">
          <h3>1. Selecciona Proyecto y Dispositivo</h3>
          <div class="form-group">
            <label for="proyecto_select">Proyecto:</label>
            <select id="proyecto_select" v-model="selectedProyectoId">
              <option value="">Selecciona un proyecto</option>
              <option v-for="proyecto in proyectos" :key="proyecto.id" :value="proyecto.id">{{ proyecto.nombre }}</option>
            </select>
          </div>

          <div class="form-group">
            <label for="dispositivo_select">Dispositivo:</label>
            <select id="dispositivo_select" v-model="selectedDispositivoId" :disabled="!selectedProyectoId">
              <option value="">Selecciona un dispositivo</option>
              <option v-for="dispositivo in dispositivos" :key="dispositivo.id" :value="dispositivo.id">{{ dispositivo.nombre }}</option>
            </select>
          </div>
        </div>

        <div class="form-section">
          <h3>2. Carga Archivo CSV</h3>
          <input type="file" id="csv_file" @change="handleFileUpload" accept=".csv" />
          <pre id="csv_preview">{{ csvPreviewText }}</pre>
        </div>

        <div class="form-section">
          <h3>3. Configura Mapeo de Sensores</h3>
          <div class="form-group">
            <label for="num_sensores">Número de Sensores a Mapear:</label>
            <input type="number" id="num_sensores" v-model.number="numSensores" min="1" />
            <button @click="generarCamposMapeo">Configurar Mapeo</button>
          </div>

          <div id="sensores_mapeo_container">
            <div v-for="(mapping, index) in sensorMappings" :key="index" class="sensor-mapping-item">
              <label>Sensor #{{ index + 1 }}:</label>
              <select v-model="mapping.sensor_id" @change="mapping.campo_id = null">
                <option :value="null">Selecciona un sensor</option>
                <option v-for="sensor in todosLosSensoresDisponibles" :key="sensor.id" :value="sensor.id">{{ sensor.nombre }}</option>
              </select>

              <label>Campo del Sensor #{{ index + 1 }}:</label>
              <select v-model="mapping.campo_id" :disabled="!mapping.sensor_id">
                <option :value="null">Selecciona un campo</option>
                <option v-for="campo in todosLosCamposDisponibles[mapping.sensor_id] || []" :key="campo.id" :value="campo.id">{{ campo.nombre }}</option>
              </select>

              <label>Columna CSV #{{ index + 1 }}:</label>
              <select v-model="mapping.csv_column_name" :disabled="csvHeaders.length === 0">
                <option :value="null">Selecciona columna CSV</option>
                <option v-for="header in csvHeaders" :key="header" :value="header">{{ header }}</option>
              </select>
            </div>
            <p v-if="sensorMappings.length === 0 && selectedDispositivoId && csvHeaders.length > 0">
              Define el número de sensores y haz clic en "Configurar Mapeo".
            </p>
            <p v-else-if="sensorMappings.length === 0 && !selectedDispositivoId">
              Selecciona un dispositivo primero para poder configurar los sensores.
            </p>
            <p v-else-if="sensorMappings.length === 0 && csvHeaders.length === 0">
              Por favor, carga un archivo CSV para ver los encabezados y configurar el mapeo.
            </p>
          </div>
        </div>

        <div class="form-section">
          <h3>4. Iniciar Simulación</h3>
          <button @click="startSimulation" :disabled="!selectedProyectoId || !selectedDispositivoId || !csvFile || sensorMappings.length === 0">
            Iniciar Simulación
          </button>
        </div>

        <div class="log-section">
          <h3>Registro de Eventos</h3>
          <div id="log" class="log-output">
            <p v-for="(msg, i) in logMessages" :key="i" :class="msg.type">{{ msg.text }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Agrega tus estilos aquí */
.simulacion-view {
  display: flex;
  height: 100vh;
}
.main-content {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto; /* Enable scrolling for the main content */
}
.container-fluid {
  max-width: 900px;
  margin: 0 auto;
}
.form-section {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
select, input[type="number"], input[type="file"] {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}
button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
#csv_preview {
  background-color: #e9e9e9;
  border: 1px solid #ccc;
  padding: 10px;
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap; /* Preserves whitespace and wraps text */
  font-family: monospace;
  font-size: 0.9em;
  margin-top: 10px;
}
.sensor-mapping-item {
  border: 1px dashed #a0a0a0;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 5px;
  background-color: #fafafa;
}
.sensor-mapping-item label, .sensor-mapping-item select {
  margin-bottom: 8px;
}
.log-output {
  background-color: #333;
  color: #eee;
  padding: 15px;
  border-radius: 8px;
  max-height: 250px;
  overflow-y: scroll;
  font-family: monospace;
  font-size: 0.85em;
}
.log-output p {
  margin: 0;
  padding: 2px 0;
}
.log-output .info { color: #eee; }
.log-output .success { color: #4CAF50; }
.log-output .warning { color: #FFC107; }
.log-output .error { color: #F44336; }
</style>