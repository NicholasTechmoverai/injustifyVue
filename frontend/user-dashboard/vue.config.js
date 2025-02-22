// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })

// module.exports = {
//   devServer: {
//     proxy: 'http://localhost:5000'
//   }
// };

module.exports = {
  transpileDependencies: [],  // Set as an empty array or specify dependencies
  devServer: {
    proxy: 'http://localhost:5000'
  }
};


