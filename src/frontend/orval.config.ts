import { defineConfig } from 'orval'

export default defineConfig({
  api: {
    input: {
      target: '../backend/api/api.yaml',
      validation: false,
    },
    output: {
      mode: 'single',
      target: './models/api.ts',
      client: 'axios',
    },
    hooks: {
      afterAllFilesWrite: 'eslint --fix',
    },
  },
})
