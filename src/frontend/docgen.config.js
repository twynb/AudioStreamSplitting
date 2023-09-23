const { defineConfig } = require('vue-docgen-cli')

/** @type {import('vue-docgen-cli').DocgenCLIConfig} */
module.exports = defineConfig({
  componentsRoot: 'src/frontend/components',
  components: '**/[A-Z]*.vue',
  outDir: 'docs/frontend/components',
  templates: {
    props(props) {
      const md = []
      md.push('## Props')
      md.push('| Name | Description | Type | Default |')
      md.push('| ---- | ----------- |----- |-------- |')

      props.forEach(({ name, description, required, type, defaultValue }) => {
        let typeCol = type.elements?.length
          ? type.elements.map(e => e.name.replaceAll('\"', '\'')).join(', ')
          : type.name
        if (!required)
          typeCol += ' (optional)'

        md.push(`|${name}| ${description ?? ''}|${typeCol}|${defaultValue?.value ?? ''}|`)
      })

      return md.join('\n')
    },
  },
})
