<template>
  <div class="container py-5 bg-light">
    <div class="row justify-content-center align-items-center">
      <div class="col-md-6 text-center">
        <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">
          <div class="carousel-indicators">
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
            <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
          </div>
          <div class="carousel-inner">
            <div class="carousel-item active">
              <img :src="imagenGrafica" class="d-block w-100 rounded shadow-sm" alt="Gráfica">
            </div>
            <div class="carousel-item">
              <img :src="imagenEstadistica" class="d-block w-100 rounded shadow-sm" alt="Estadística">
            </div>
            <div class="carousel-item">
              <img :src="imagenAnalisis" class="d-block w-100 rounded shadow-sm" alt="Análisis">
            </div>
          </div>
          <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Anterior</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Siguiente</span>
          </button>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card p-4 shadow">
          <h2 class="mb-3 text-center">Inicio de Sesión</h2>
          <div class="mb-3">
            <label for="usuario" class="form-label">Usuario:</label>
            <input type="text" class="form-control" id="usuario" v-model="usuario">
          </div>
          <div class="mb-3">
            <label for="contrasena" class="form-label">Contraseña:</label>
            <input type="password" class="form-control" id="contrasena" v-model="contrasena">
          </div>
          <div class="d-grid">
            <router-link to="/plataforma" class="nav-link btn btn-success ms-2">
       <button class="btn btn-primary" type="button">Iniciar sesión</button></router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import imagenAnalisis1 from '@/assets/inicio/analisis.png';
import imagenEstadistica1 from '@/assets/inicio/estadistica.jpg';
import imagenGrafica1 from '@/assets/inicio/grafico-diagramas.jpg'; // Asegúrate de usar el nombre de archivo correcto

export default {
  name: 'SeccionPrincipal',
  data() {
    return {
      imagenGrafica: imagenGrafica1,
      imagenEstadistica: imagenEstadistica1,
      imagenAnalisis: imagenAnalisis1,
      usuario: '',
      contrasena: ''
    };
  }
}
</script>

<style scoped>
/* Ajusta el ancho del carrusel si es necesario */
.carousel {
  max-width: 400px;
  margin: 0 auto; /* Centrar el carrusel */
}
</style>