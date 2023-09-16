/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_NAME: string
  readonly VITE_SERVICE_ACOUSTID_API_KEY: string
  readonly VITE_SERVICE_SHAZAM_API_KEY: string
  readonly VITE_OUTPUT_FILE_NAME_TEMPLATE: string
  readonly VITE_SAVE_DIRECTORY: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
