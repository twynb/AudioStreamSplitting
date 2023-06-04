import {
  defineConfig,
  presetAttributify,
  presetIcons,
  presetUno,
} from 'unocss'

import transformerDirectives from '@unocss/transformer-directives'
import transformerVariantGroup from '@unocss/transformer-variant-group'

export default defineConfig({
  shortcuts: [],
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.25,
      warn: true,
    }),
  ],
  transformers: [
    transformerDirectives(),
    transformerVariantGroup(),
  ],
  theme: {
    colors: {
      'primary': '#C8BCF6',
      'light-gray-1': '#F5F5F5',
      'light-gray-2': '#EFEFEF',
      'light-gray-3': '#C0BFBD',
      'dark-shade': '#1F1F22',
      'dark-gray': '#09090A',
    },
  },
})
