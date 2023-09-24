export const LangMap: Record<string, string> = {
  en: 'English',
  de: 'German',
  fr: 'French',
  es: 'Spanish',
}

export const DEFAULT_TOAST_DURATION = 5000

export const SUPPORT_FILE_TYPES = ['mp3', 'wav']

export const DEFAULT_SAVE_SETTINGS = {
  fileType: 'mp3',
  shouldAsk: true,
  submitSavedFiles: false,
  saveDirectory: '',
  nameTemplate: '{TITLE}',
}

export const DEFAULT_ENV = {
  SERVICE_ACOUSTID_API_KEY: import.meta.env.VITE_SERVICE_ACOUSTID_API_KEY,
  SERVICE_ACOUSTID_USER_KEY: import.meta.env.VITE_SERVICE_ACOUSTID_USER_KEY,
  SERVICE_SHAZAM_API_KEY: import.meta.env.VITE_SERVICE_SHAZAM_API_KEY,
}
