// // vue/frontend-vue/vue.config.js

// module.exports = {
//   // Esto le dice a Vue que prefije todas las URLs de sus activos
//   // (JS, CSS, imágenes, etc.) con '/static/' cuando se compile.
//   publicPath: '/static/',
//   // Puedes añadir otras configuraciones aquí si las necesitas,
//   // pero 'publicPath' es la clave para este problema.
// };
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
