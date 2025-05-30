<template>
  <div class="plataforma-layout">
    <BarraLateralPlataforma />
    <div class="plataforma-contenido">
      <EncabezadoPlataforma />
      <div class="plataforma-tarjetas p-4">
        <div class="row row-cols-1 row-cols-md-2 g-4">
          <div class="col">
            <div class="card shadow h-100">
              <div class="card-body text-center">
                <i class="bi bi-graph-up text-info mb-3" style="font-size: 2em;"></i>
                <h5 class="card-title">Proyectos</h5>
                <p class="card-text small text-muted">Proyecto.</p>
                <router-link to="/mis-proyectos" class="btn btn-info btn-sm">Ir al simulador</router-link>
              </div>
            </div>
          </div>
          <div class="col">
            <div class="card shadow h-100">
              <div class="card-body text-center">
                <i class="bi bi-file-earmark-spreadsheet-fill text-secondary mb-3" style="font-size: 2em;"></i>
                <h5 class="card-title">dispositivos</h5>
                <p class="card-text small text-muted">Envía datos de sensores desde un archivo CSV.</p>
                <router-link to="/dispositivos" class="btn btn-secondary btn-sm">Subir archivo CSV</router-link>
              </div>
            </div>
          </div>
          <div class="col">
            <div class="card shadow h-100">
              <div class="card-body text-center">
                <i class="bi bi-file-earmark-spreadsheet-fill text-secondary mb-3" style="font-size: 2em;"></i>
                <h5 class="card-title">Valores</h5>
                <p class="card-text small text-muted">Envía datos de sensores desde un archivo CSV.</p>
                <router-link to="/vista_valores" class="btn btn-secondary btn-sm">Subir archivo CSV</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped lang="scss">
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
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.card {
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.15s ease-in-out;

  &:hover {
    transform: translateY(-3px);
  }

  .card-body {
    text-align: center;
    padding: 25px;
  }

  i {
    font-size: 2.5em;
    margin-bottom: 15px;
    display: block;
  }

  .card-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #555;
    margin-bottom: 8px;
  }

  .card-text {
    color: #777;
    font-size: 0.9rem;
    margin-bottom: 15px;
  }

  .btn {
    padding: 10px 20px;
    border-radius: 5px;
    border: none;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.15s ease-in-out;
    font-size: 0.9rem;

    &.btn-info {
      background-color: #17a2b8;
      &:hover {
        background-color: #117a8b;
      }
    }

    &.btn-secondary {
      background-color: #6c757d;
      &:hover {
        background-color: #5a6268;
      }
    }
  }
}
</style>

<script>
  import BarraLateralPlataforma from '../plataforma/BarraLateralPlataforma.vue';
  import EncabezadoPlataforma from '../plataforma/EncabezadoPlataforma.vue';

export default {
  name: 'VistaSimulacionMenu',
  components: {
    BarraLateralPlataforma,
    EncabezadoPlataforma,
  },
};
</script>
