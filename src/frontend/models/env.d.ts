/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_NAME: string
  readonly VITE_SERVICE_ACOUSTID_API_KEY: string
  readonly VITE_SERVICE_ACOUSTID_USER_KEY: string
  readonly VITE_SERVICE_SHAZAM_API_KEY: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
