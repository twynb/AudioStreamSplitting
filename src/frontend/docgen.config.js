const { defineConfig } = require('vue-docgen-cli')

/** @type {import('vue-docgen-cli').DocgenCLIConfig} */
module.exports = defineConfig({
  componentsRoot: 'src/frontend/components',
  components: '**/Base[A-Z]*.vue',
  outDir: 'docs/frontend/components',
})
