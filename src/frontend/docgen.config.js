const { defineConfig } = require('vue-docgen-cli')

/** @type {import('vue-docgen-cli').DocgenCLIConfig} */
module.exports = defineConfig({
  componentsRoot: 'src/frontend/components',
  components: '**/Base[A-Z]*.vue',
  outDir: 'docs/frontend/components',
  templates: {
    props(props) {
      let md = '| Name | Description | Type | Default |\n | ----------- | ----------- |----------- |----------- |\n'

      props.forEach(({ name, description, required, type, defaultValue, tags }) => {
        let typeCol = type.elements?.length
          ? type.elements.map(e => e.name.replaceAll('\"', '\'')).join(', ')
          : type.name
        if (!required)
          typeCol += ' (optional)'

        md += `|${name}| ${description ?? ''}|${typeCol}|${defaultValue?.value ?? ''}|\n`
      })

      return md
    },
  },
})
