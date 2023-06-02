import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Components({ dts: true, dirs: ['./components'], version: 3 }),
    AutoImport({
      imports: ['vue', 'pinia', 'vue-i18n', 'vue-router'],
      dts: true,
      vueTemplate: true,
      dirs: ['./composables', './store']
    })
  ],
  root: 'src/frontend',
  build: {
    outDir: '../../gui',
    emptyOutDir: true,
    watch: null,
    rollupOptions: {
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]'
      }
    }
  }
})
