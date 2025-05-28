<template>
  <div>
    <BarraNavegacion />
    <SeccionPrincipal />
    <div class="container my-4">
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div class="col">
      <TarjetaInfo
        titulo="Monitoreo en Tiempo Real"
        contenido="Visualiza datos de tus dispositivos IoT al instante y toma decisiones informadas."
      />
    </div>
    <div class="col">
      <TarjetaInfo
        titulo="Análisis de Datos Avanzado"
        contenido="Explora tendencias, patrones y obtén insights valiosos de la información recopilada."
      />
    </div>
    <div class="col">
      <TarjetaInfo
        titulo="Alertas y Notificaciones"
        contenido="Recibe notificaciones personalizadas sobre eventos importantes de tus dispositivos."
      />
    </div>
      </div>
    </div>
  </div>
</template>

<script>
import BarraNavegacion from './BarraNavegacion.vue';
import SeccionPrincipal from './SeccionPrincipal.vue';
import TarjetaInfo from './TarjetaInfo.vue';

export default {
  name: 'VistaPrincipal',
  components: {
    BarraNavegacion,
    SeccionPrincipal,
    TarjetaInfo
  }
}
</script>

