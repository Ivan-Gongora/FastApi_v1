<template>
    <div class="plataforma-tarjetas p-4">
      <div class="row row-cols-1 row-cols-md-4 g-4">
        <div class="col">
          <div class="card shadow h-100">
            <div class="card-body text-center">
              <i class="bi bi-diagram-project-fill text-primary mb-3" style="font-size: 2em;"></i>
              <h5 class="card-title">Proyectos</h5>
              <p class="card-text small text-muted">Tus proyectos IoT...</p>
              <p class="card-text display-4">0</p>
              <button class="btn btn-primary btn-sm">Ver más...</button>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card shadow h-100">
            <div class="card-body text-center">
              <i class="bi bi-device-hdd-fill text-success mb-3" style="font-size: 2em;"></i>
              <h5 class="card-title">Dispositivos</h5>
              <p class="card-text small text-muted">Componentes de tus proyectos IoT...</p>
              <p class="card-text display-4">0</p>
              <button class="btn btn-success btn-sm">Ver más...</button>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card shadow h-100">
            <div class="card-body text-center">
              <i class="bi bi-headphones text-info mb-3" style="font-size: 2em;"></i>
              <h5 class="card-title">Sensores</h5>
              <p class="card-text small text-muted">Escuchan a su alrededor...</p>
              <p class="card-text display-4">0</p>
              <button class="btn btn-info btn-sm">Ver más...</button>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card shadow h-100">
            <div class="card-body text-center">
              <i class="bi bi-clipboard-check-fill text-warning mb-3" style="font-size: 2em;"></i>
              <h5 class="card-title">Reportes</h5>
              <p class="card-text small text-muted">Entendiendo lo que las cosas te quieren decir...</p>
              <p class="card-text display-4">0</p>
              <button class="btn btn-warning btn-sm">Ver más...</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TarjetasPlataforma',
  };
  </script>
  
  <style scoped lang="scss">
  .plataforma-tarjetas {
  padding: 20px 0; /* Reducir padding vertical general */
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* Diseño de grid responsivo */
  gap: 20px; /* Espacio entre las tarjetas */
}

.card {
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 8px; /* Bordes redondeados */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); /* Sombra suave */
  transition: transform 0.15s ease-in-out; /* Efecto hover sutil */

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

  .display-4 {
    font-size: 2.5rem;
    color: #333;
    margin-bottom: 10px;
  }

  .btn {
    padding: 10px 20px;
    border-radius: 5px;
    border: none;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.15s ease-in-out;
    font-size: 0.9rem;

    &.btn-primary {
      background-color: #007bff;
      &:hover {
        background-color: #0056b3;
      }
    }

    &.btn-success {
      background-color: #28a745;
      &:hover {
        background-color: #1e7e34;
      }
    }

    &.btn-info {
      background-color: #17a2b8;
      &:hover {
        background-color: #117a8b;
      }
    }

    &.btn-warning {
      background-color: #ffc107;
      color: #212529;
      &:hover {
        background-color: #e0a800;
      }
    }
  }
}
  </style>