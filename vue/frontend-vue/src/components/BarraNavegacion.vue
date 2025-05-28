<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Plataforma IoT</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navegacionPrincipal" aria-controls="navegacionPrincipal" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navegacionPrincipal">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Acerca de</router-link>
          </li>
        
        </ul>
        <form class="d-flex me-2">
          <input class="form-control me-2" type="search" placeholder="Buscar" aria-label="Buscar">
          <button class="btn btn-outline-light" type="submit">Buscar</button>
        </form>
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="#">Cerrar Sesión</a>
          </li>
          <li class="nav-item">
            <router-link to="/registros" class="nav-link btn btn-success ms-2">Registrarse</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'BarraNavegacion'
}
</script>
  
  <style scoped>
  .navbar {
    background-color: #007bff; /* Example blue color */
    color: white;
    padding: 15px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .logo {
    font-size: 1.5em;
    font-weight: bold;
  }
  
  .menu a {
    color: white;
    text-decoration: none;
    margin-left: 15px;
  }
  
  .search-bar {
    display: flex;
    align-items: center;
  }
  
  .search-bar input {
    padding: 8px;
    border: none;
    border-radius: 5px 0 0 5px;
  }
  
  .search-bar button {
    background-color: #0056b3;
    color: white;
    border: none;
    padding: 8px 10px;
    border-radius: 0 5px 5px 0;
    cursor: pointer;
  }
  
  .search-bar button img {
    width: 16px;
    height: 16px;
    vertical-align: middle;
  }
  
  .auth {
    display: flex; /* Ensure items are in a row */
    align-items: center; /* Vertically align items */
  }
  
  .auth a {
    color: white;
    text-decoration: none;
  }
  
  .auth a:first-child {
    margin-right: 15px; /* Add margin to the right of the first link */
  }
  </style>
