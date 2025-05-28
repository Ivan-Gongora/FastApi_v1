<template>
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow">
            <div class="card-body p-5">
              <h2 class="text-center mb-4">Crear cuenta</h2>
              <form>
                <div class="mb-3">
                  <label for="username" class="form-label">Nombre de usuario</label>
                  <input type="text" class="form-control" id="username" v-model="username" required>
                </div>
                <div class="mb-3">
                  <label for="email" class="form-label">Correo electrónico</label>
                  <input type="email" class="form-control" id="email" v-model="email" required>
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Contraseña</label>
                  <input type="password" class="form-control" id="password" v-model="password" required>
                </div>
                <div class="mb-3">
                  <label for="confirmPassword" class="form-label">Confirmar contraseña</label>
                  <input type="password" class="form-control" id="confirmPassword" v-model="confirmPassword" required>
                </div>
                <div class="d-grid">
                  <button type="submit" class="btn btn-primary">Registrar</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'FormularioRegistro',
    data() {
      return {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      };
    },
    methods: {
      // Aquí puedes agregar la lógica para el registro
    }
  };
  </script>
  
  <style scoped>
  /* Puedes agregar estilos personalizados aquí si es necesario */
  </style>