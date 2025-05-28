<template>
  <div class="plataforma-tarjetas p-4">
    <div class="row row-cols-1 row-cols-md-2 g-4">
      <!-- Tarjeta: Base de Datos -->
      <div class="col">
        <div class="card shadow h-100">
          <div class="card-body text-center">
            <i class="bi bi-database-fill-gear text-primary mb-3" style="font-size: 2.5em;"></i>
            <h5 class="card-title">Gestión de Base de Datos</h5>
     
            <p class="card-text small text-muted">Proyectos, dispositivos y sensores.</p>
               <router-link to="/menu-gestion" ><button class="btn btn-primary btn-sm">Ir a la Base de Datos</button></router-link>
          </div>
        </div>
      </div>

      <!-- Tarjeta: Simulación de Datos -->
      <div class="col">
        <div class="card shadow h-100">
          <div class="card-body text-center">
            <i class="bi bi-upload text-success mb-3" style="font-size: 2.5em;"></i>
                  
            <h5 class="card-title">Simulación de Datos</h5>
            <p class="card-text small text-muted">Simular datos como de un sensor o enviar datos desde un .csv.</p>
             <router-link to="/menu-simulacion" ><button class="btn btn-success btn-sm">Ir a Simulación</button></router-link>
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
  padding: 20px 0;
}

.card {
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.15s ease-in-out;

  &:hover {
    transform: translateY(-3px);
  }

  .card-body {
    text-align: center;
    padding: 30px;
  }

  i {
    font-size: 2.5em;
    margin-bottom: 15px;
    display: block;
  }

  .card-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #343a40;
    margin-bottom: 12px;
  }

  .card-text {
    color: #6c757d;
    font-size: 0.95rem;
    margin-bottom: 20px;
  }

  .btn {
    padding: 10px 20px;
    border-radius: 6px;
    font-size: 0.95rem;
  }
}
</style>
