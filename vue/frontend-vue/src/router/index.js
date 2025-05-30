import { createRouter, createWebHistory } from 'vue-router';
import VistaPrincipal from '../components/VistaPrincipal.vue'; // Ruta a tu vista principal
import VistaRegistro from '../components/login/VistaRegistro.vue'; // Ruta a tu vista de registro
// import VistaDashboard from '../components/dashboard/DashboardView.vue'
import VistaPlataformaPrincipal from '../components/plataforma/VistaPlataformaPrincipal.vue'; // Nuevo nombre
import VistaDispositivos from '../components/dispositivos/VistaDispositivos.vue'; 
import DetalleDispositivo from '../components/dispositivos/DetalleDispositivo.vue';
import VistaMisProyectos from '../components/proyecto/VistaMisProyectos.vue';
import DetalleProyecto from '../components/proyecto/DetalleProyecto.vue'
import MenuSimulacion from '../components/simulador/VistaSimulacionMenu.vue';
import VistaC from '../components/simulador/csvEnviar.vue';
import MenuGestion from '../components/GestionDB/VistaGestionMenu.vue'

import VerValores from '../components/valores/VerValores.vue';
import updateValores from '../components/valores/updateValores.vue';
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
    path: '/detalle-proyecto/:id',
    name: 'DetalleProyecto',
    component: DetalleProyecto
  },

  {
    path: '/dispositivos',
    name: 'VistaDispositivos',
    component: VistaDispositivos
  },
  {
    path: '/detalle-dispositivo/:id',
    name: 'DetalleDispositivo',
    component: DetalleDispositivo
  },
  {
    path: '/menu-simulacion',
    name: 'MenuSimulacion',
    component: MenuSimulacion
  },
  {
    path: '/vista-csv',
    name: 'VistaCsv',
    component: VistaC
  },
  {
    path: '/menu-gestion',
    name: 'MenuGestion',
    component: MenuGestion
  },

  {
    path: '/vista_valores',
    name: 'VerValores',
    component: VerValores
  },

  {
    path: '/actualizar_valores',
    name: 'updateValores',
    component: updateValores
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
