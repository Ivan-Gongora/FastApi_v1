<template>
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow">
            <div class="card-body p-5">
              <h2 class="text-center mb-4">Crear cuenta</h2>
              <form @submit.prevent="registrarUsuario">
                <div class="mb-3">
                  <div class="mb-3">
                  <label for="nombre" class="form-label">Nombre</label>
                  <input type="text" class="form-control" id="nombre" v-model="nombre" required>
                </div>
                <div class="mb-3">
                  <label for="apellido" class="form-label">Apellido</label>
                  <input type="text" class="form-control" id="apellido" v-model="apellido" required>
                </div>
                  <label for="username" class="form-label">Nombre de usuario</label>
                  <input type="text" class="form-control" id="username" v-model="nombre_usuario" required>
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
                <div v-if="error" class="mt-3 text-danger text-center">
                {{ error }}
              </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  const API_BASE_URL = 'http://127.0.0.1:8001';
  export default {
    name: 'FormularioRegistro',
    data() {
    return {
      username: '',
      nombre: '',
      apellido: '',
      email: '',
      password: '',
      confirmPassword: '',
      error: ''
      };
    }
    ,methods: {
  async registrarUsuario(event) {
    event.preventDefault();

    if (this.password !== this.confirmPassword) {
   
      this.error = 'Las contraseñas no coinciden.';
    return;
    }
    // Se obtienen los datos a enviar en el body desde el formulario 
    const payload = {
      nombre_usuario: this.nombre_usuario,
      nombre: this.nombre,
      apellido: this.apellido,
      email: this.email,
      contrasena: this.password,
      activo: true
    };

    try {
      const response = await fetch(`${API_BASE_URL}/crear_usuario/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (data.resultados && data.resultados[0].status === "success") {
        alert("Usuario registrado correctamente");
        // limpiar los campos
        this.nombre_usuario = ''
        this.nombre = ''
        this.apellido = ''
        this.email = ''
        this.password = ''
      

         // Redirigir a plataforma principal
         this.$router.push('/');
      } else {
        this.error= "Error: " + (data.resultados?.[0]?.message || data.message);
      }

    } catch (error) {
      console.error("Error en la solicitud:", error);
      this.error = "Error en el registro";
    }
  }
}

  };
  </script>
  
  <style scoped>

  </style>
