import { createRouter, createWebHistory } from 'vue-router';
import VistaPrincipal from '../components/VistaPrincipal.vue'; // Ruta a tu vista principal
import VistaRegistro from '../components/login/VistaRegistro.vue'; // Ruta a tu vista de registro
// import VistaDashboard from '../components/dashboard/DashboardView.vue'
import VistaPlataformaPrincipal from '../components/plataforma/VistaPlataformaPrincipal.vue'; // Nuevo nombre
import VistaDispositivos from '../components/dispositivos/VistaDispositivos.vue'; 
import DetalleDispositivo from '../components/dispositivos/DetalleDispositivo.vue';
import VistaMisProyectos from '../components/proyecto/VistaMisProyectos.vue';

const routes = [
  {
    path: '/',
    name: 'Inicio',
    component: VistaPrincipal
  },
  {
    path: '/registros',
    name: 'Registros',
    component: VistaRegistro
  },
  {
    path: '/plataforma',
    name: 'Plataforma',
    component: VistaPlataformaPrincipal // Nuevo nombre
  },
  {
    path: '/mis-proyectos',
    name: 'VistaMisProyectos',
    component: VistaMisProyectos
  },
  {
    path: '/dispositivos',
    name: 'VistaDispositivos',
    component: VistaDispositivos
  },
  {
    path: '/detalle-dispositivo',
    name: 'DetalleDispositivo',
    component: DetalleDispositivo
  }


  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
