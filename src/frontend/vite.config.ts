/// <reference types="vitest" />
import path from 'node:path'
import { defineConfig } from 'vite'
import Vue from '@vitejs/plugin-vue'
import Pages from 'vite-plugin-pages'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'
import UnoCSS from 'unocss/vite'
import VueI18n from '@intlify/unplugin-vue-i18n/vite'

export default defineConfig({
  root: 'src/frontend',

  plugins: [
    Vue(),

    Pages({ dirs: 'pages' }),

    AutoImport({
      imports: [
        'vue',
        'vue-router',
        'pinia',
        'vue-i18n',
      ],
      dts: 'auto-imports.d.ts',
      dirs: ['composables', 'stores'],
      vueTemplate: true,
    }),

    Components({
      dts: 'components.d.ts',
      dirs: ['components'],
    }),

    UnoCSS({ configFile: 'uno.config.ts' }),

    VueI18n({
      runtimeOnly: true,
      compositionOnly: true,
      fullInstall: true,
      include: [path.resolve(__dirname, 'locales/**')],
    }),
  ],

  build: {
    outDir: '../../gui',
    emptyOutDir: true,
    watch: null,
    rollupOptions: {
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]',
      },
    },
  },

  test: {
    environment: 'jsdom',
  },
})
