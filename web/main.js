// web/main.js

document.addEventListener('DOMContentLoaded', async () => {
    const proyectoSelect = document.getElementById('proyecto_select');
    const dispositivoSelect = document.getElementById('dispositivo_select');
    const numSensoresInput = document.getElementById('num_sensores');
    const generarMapeoBtn = document.getElementById('generar_mapeo_btn');
    const sensoresMapeoContainer = document.getElementById('sensores_mapeo_container');
    const csvFileInput = document.getElementById('csv_file');
    const csvPreviewDiv = document.getElementById('csv_preview');
    const startSimulationBtn = document.getElementById('start_simulation_btn');
    const logElement = document.getElementById('log');

    // --- ESTA ES LA LÍNEA MÁS IMPORTANTE A ACTUALIZAR ---
    // Si tu backend FastAPI se ejecuta en el puerto 8001, y todas las rutas tienen /api
    const API_BASE_URL = 'http://127.0.0.1:8001/api';

    let todosLosSensoresDisponibles = [];
    let todosLosCamposDisponibles = {};
    let csvHeaders = [];

    // Funciones de Utilidad 
    function logMessage(message, type = 'info') {
        const p = document.createElement('p');
        p.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        p.classList.add(type);
        logElement.appendChild(p);
        logElement.scrollTop = logElement.scrollHeight;
    }

    // --- FUNCIÓN PARA OBTENER Y MOSTRAR PREVISUALIZACIÓN DEL CSV DESDE EL BACKEND ---
    async function displayCsvPreviewFromBackend(file) {
        csvPreviewDiv.innerHTML = 'Cargando previsualización del CSV desde el servidor...';
        csvPreviewDiv.style.display = 'block';
        csvHeaders = []; // Limpiar encabezados anteriores

        if (!file) {
            csvPreviewDiv.innerHTML = 'No hay archivo CSV seleccionado.';
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_BASE_URL}/csv-preview/`, { // <--- Endpoint actualizado
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                csvHeaders = data.header; // Guardar los encabezados
                let previewText = '';
                if (csvHeaders && csvHeaders.length > 0) {
                    previewText += csvHeaders.join(', ') + '\n';
                }
                if (data.preview_rows && data.preview_rows.length > 0) {
                    data.preview_rows.forEach(row => {
                        previewText += row.join(', ') + '\n';
                    });
                }
                if (data.message === "El archivo CSV está vacío.") {
                    previewText = "El archivo CSV está vacío.";
                } else if (data.preview_rows.length === 5) {
                    previewText += '...\n';
                }

                csvPreviewDiv.textContent = `Contenido del CSV:\n\n${previewText}`;
                logMessage(`Previsualización de "${file.name}" cargada desde el backend.`, 'success');

            } else {
                const errorData = await response.json();
                csvPreviewDiv.innerHTML = `Error al obtener previsualización: ${errorData.detail || response.statusText}`;
                logMessage(`Error al obtener previsualización del CSV desde el backend: ${errorData.detail || response.statusText}`, 'error');
            }
        } catch (error) {
            csvPreviewDiv.innerHTML = `Error de red al conectar con el backend para la previsualización: ${error.message}`;
            logMessage(`Error de red para previsualización: ${error.message}`, 'error');
        }
    }

    // --- Funciones para Cargar Dropdowns (con endpoints actualizados) ---
    async function cargarProyectos() {
        logMessage('Cargando proyectos...');
        try {
            const response = await fetch(`${API_BASE_URL}/proyectos`); // <--- Endpoint actualizado
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const proyectos = await response.json();
            proyectoSelect.innerHTML = '<option value="">Selecciona un proyecto</option>';
            proyectos.forEach(p => {
                const option = document.createElement('option');
                option.value = p.id;
                option.textContent = p.nombre;
                proyectoSelect.appendChild(option);
            });
            proyectoSelect.disabled = false;
            logMessage('Proyectos cargados.', 'success');
        } catch (error) {
            logMessage(`Error al cargar proyectos: ${error.message}`, 'error');
            proyectoSelect.innerHTML = '<option value="">Error al cargar</option>';
        }
    }

    async function cargarDispositivos(proyectoId) {
        dispositivoSelect.innerHTML = '<option value="">Cargando dispositivos...</option>';
        dispositivoSelect.disabled = true;
        if (!proyectoId) {
            dispositivoSelect.innerHTML = '<option value="">Selecciona un proyecto primero</option>';
            return;
        }
        logMessage(`Cargando dispositivos para proyecto ${proyectoId}...`);
        try {
            const response = await fetch(`${API_BASE_URL}/proyectos/${proyectoId}/dispositivos`); // <--- Endpoint actualizado
            if (!response.ok) {
                if (response.status === 404) {
                    dispositivoSelect.innerHTML = '<option value="">No hay dispositivos para este proyecto</option>';
                    return;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const dispositivos = await response.json();
            dispositivoSelect.innerHTML = '<option value="">Selecciona un dispositivo</option>';
            dispositivos.forEach(d => {
                const option = document.createElement('option');
                option.value = d.id;
                option.textContent = d.nombre;
                dispositivoSelect.appendChild(option);
            });
            dispositivoSelect.disabled = false;
            logMessage('Dispositivos cargados.', 'success');
        } catch (error) {
            logMessage(`Error al cargar dispositivos: ${error.message}`, 'error');
            dispositivoSelect.innerHTML = '<option value="">Error al cargar</p>';
        }
    }

    async function cargarSensoresYCamposParaDispositivo(dispositivoId) {
        todosLosSensoresDisponibles = [];
        todosLosCamposDisponibles = {};
        if (!dispositivoId) {
            logMessage('No se seleccionó un dispositivo.', 'warning');
            return;
        }
        logMessage(`Cargando sensores y campos para dispositivo ${dispositivoId}...`);
        try {
            const responseSensores = await fetch(`${API_BASE_URL}/dispositivos/${dispositivoId}/sensores`); // <--- Endpoint actualizado
            if (!responseSensores.ok) {
                 if (responseSensores.status === 404) {
                     logMessage(`No hay sensores para el dispositivo ID ${dispositivoId}.`, 'warning');
                     return;
                 }
                throw new Error(`HTTP error! status: ${responseSensores.status}`);
            }
            todosLosSensoresDisponibles = await responseSensores.json();

            for (const sensor of todosLosSensoresDisponibles) {
                const responseCampos = await fetch(`${API_BASE_URL}/sensores/${sensor.id}/campos`); // <--- Endpoint actualizado
                if (!responseCampos.ok) {
                    logMessage(`No hay campos para el sensor ID ${sensor.id}.`, 'warning');
                    todosLosCamposDisponibles[sensor.id] = [];
                    continue;
                }
                todosLosCamposDisponibles[sensor.id] = await responseCampos.json();
            }
            logMessage('Sensores y campos cargados.', 'success');
            if (numSensoresInput.value > 0) {
                generarCamposMapeo();
            }
        } catch (error) {
            logMessage(`Error al cargar sensores/campos: ${error.message}`, 'error');
        }
    }

    // --- Funciones para Mapeo Dinámico ---
    function generarCamposMapeo() {
        sensoresMapeoContainer.innerHTML = '';
        const numSensores = parseInt(numSensoresInput.value);

        if (isNaN(numSensores) || numSensores <= 0) {
            sensoresMapeoContainer.innerHTML = '<p class="warning">Ingresa un número válido de sensores (debe ser 1 o más).</p>';
            return;
        }

        if (todosLosSensoresDisponibles.length === 0 && dispositivoSelect.value) {
            sensoresMapeoContainer.innerHTML = '<p class="warning">No hay sensores disponibles para el dispositivo seleccionado. Asegúrate de haber seleccionado un dispositivo con sensores.</p>';
            return;
        }
        if (!dispositivoSelect.value) {
             sensoresMapeoContainer.innerHTML = '<p class="warning">Selecciona un dispositivo primero para poder configurar los sensores.</p>';
             return;
        }
        if (csvHeaders.length === 0) {
            sensoresMapeoContainer.innerHTML = '<p class="error">Por favor, carga un archivo CSV para ver los encabezados y configurar el mapeo.</p>';
            return;
        }

        for (let i = 0; i < numSensores; i++) {
            const mappingItem = document.createElement('div');
            mappingItem.classList.add('sensor-mapping-item');
            mappingItem.dataset.index = i;

            const sensorDiv = document.createElement('div');
            const sensorSelect = document.createElement('select');
            sensorSelect.id = `sensor_select_${i}`;
            sensorSelect.innerHTML = '<option value="">Selecciona un sensor</option>';
            todosLosSensoresDisponibles.forEach(s => {
                const option = document.createElement('option');
                option.value = s.id;
                option.textContent = s.nombre;
                sensorSelect.appendChild(option);
            });
            sensorDiv.innerHTML = `<label for="sensor_select_${i}">Sensor #${i+1}:</label>`;
            sensorDiv.appendChild(sensorSelect);
            mappingItem.appendChild(sensorDiv);

            const campoDiv = document.createElement('div');
            const campoSelect = document.createElement('select');
            campoSelect.id = `campo_select_${i}`;
            campoSelect.disabled = true;
            campoSelect.innerHTML = '<option value="">Selecciona un sensor primero</option>';
            campoDiv.innerHTML = `<label for="campo_select_${i}">Campo del Sensor #${i+1}:</label>`;
            campoDiv.appendChild(campoSelect);
            mappingItem.appendChild(campoDiv);

            sensorSelect.addEventListener('change', () => {
                const selectedSensorId = sensorSelect.value;
                campoSelect.innerHTML = '<option value="">Cargando campos...</option>';
                campoSelect.disabled = true;
                if (selectedSensorId && todosLosCamposDisponibles[selectedSensorId]) {
                    const campos = todosLosCamposDisponibles[selectedSensorId];
                    campoSelect.innerHTML = '';

                    if (campos.length > 0) {
                        campoSelect.innerHTML = '<option value="">Selecciona un campo</option>';
                        campos.forEach(c => {
                            const option = document.createElement('option');
                            option.value = c.id;
                            option.textContent = c.nombre;
                            sensorSelect.appendChild(option);
                            campoSelect.appendChild(option);
                        });
                    } else {
                        campoSelect.innerHTML = '<option value="">No hay campos para este sensor</option>';
                    }
                    campoSelect.disabled = false;
                } else {
                    campoSelect.innerHTML = '<option value="">Selecciona un sensor primero</option>';
                }
            });

            sensoresMapeoContainer.appendChild(mappingItem);
        }
        if (numSensores > 0) {
            logMessage(`Generados ${numSensores} campos de mapeo de sensores.`, 'info');
        }
    }


    // --- Event Listeners ---
    proyectoSelect.addEventListener('change', () => {
        const selectedProyectoId = proyectoSelect.value;
        cargarDispositivos(selectedProyectoId);
        dispositivoSelect.innerHTML = '<option value="">Selecciona un proyecto primero</option>';
        dispositivoSelect.disabled = true;
        sensoresMapeoContainer.innerHTML = '<p class="warning">Selecciona un dispositivo primero para poder configurar los sensores.</p>';
    });

    dispositivoSelect.addEventListener('change', () => {
        const selectedDispositivoId = dispositivoSelect.value;
        cargarSensoresYCamposParaDispositivo(selectedDispositivoId);
        sensoresMapeoContainer.innerHTML = '<p class="warning">Define el número de sensores y haz clic en "Configurar Mapeo".</p>';
    });

    generarMapeoBtn.addEventListener('click', generarCamposMapeo);

    csvFileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            displayCsvPreviewFromBackend(file);
        } else {
            csvPreviewDiv.textContent = '';
            csvPreviewDiv.style.display = 'none';
            csvHeaders = [];
            logMessage('No se seleccionó ningún archivo CSV.', 'warning');
        }
    });

    startSimulationBtn.addEventListener('click', async () => {
        logElement.innerHTML = '';
        const csvFile = csvFileInput.files[0];
        const selectedProyectoId = proyectoSelect.value;
        const selectedDispositivoId = dispositivoSelect.value;

        if (!csvFile) {
            logMessage('Por favor, selecciona un archivo CSV.', 'error');
            return;
        }
        if (!selectedProyectoId || !selectedDispositivoId) {
            logMessage('Por favor, selecciona un Proyecto y un Dispositivo.', 'error');
            return;
        }
        if (csvHeaders.length === 0) {
            logMessage('No se pudo obtener la cabecera del CSV. Por favor, asegúrate de que el archivo es válido y vuelve a intentarlo.', 'error');
            return;
        }

        const mapeos = [];
        const mappingItems = sensoresMapeoContainer.querySelectorAll('.sensor-mapping-item');
        if (mappingItems.length === 0) {
            logMessage('Por favor, configura al menos un mapeo de sensor.', 'error');
            return;
        }

        for (const item of mappingItems) {
            const sensorSelect = item.querySelector('select[id^="sensor_select_"]');
            const campoSelect = item.querySelector('select[id^="campo_select_"]');

            const sensorId = sensorSelect.value;
            const campoId = campoSelect.value;
            const campoNombre = campoSelect.options[campoSelect.selectedIndex].text;

            if (!sensorId || !campoId || !campoNombre) {
                logMessage(`Error en la configuración del mapeo: Todos los campos (Sensor, Campo) deben estar llenos para cada sensor configurado.`, 'error');
                return;
            }

            mapeos.push({
                sensor_id: parseInt(sensorId),
                campo_id: parseInt(campoId),
                campo_nombre: campoNombre
            });
        }

        if (mapeos.length === 0) {
            logMessage('No se configuró ningún mapeo de sensor válido.', 'error');
            return;
        }

        logMessage('Iniciando simulación...');
        logMessage(`Archivo seleccionado: ${csvFile.name}`);
        logMessage(`Proyecto: ${selectedProyectoId}, Dispositivo: ${selectedDispositivoId}`);
        logMessage(`Mapeos a enviar: ${JSON.stringify(mapeos, null, 2)}`);

        const formData = new FormData();
        formData.append('file', csvFile);
        formData.append('sensor_mappings', JSON.stringify(mapeos));
        formData.append('proyecto_id', selectedProyectoId);
        formData.append('dispositivo_id', selectedDispositivoId);


        try {
            const fastapiEndpoint = `${API_BASE_URL}/simular/`; // <--- Endpoint actualizado

            const response = await fetch(fastapiEndpoint, {
                method: 'POST',
                body: formData
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
    });

    // Cargar proyectos al inicio
    cargarProyectos();
});