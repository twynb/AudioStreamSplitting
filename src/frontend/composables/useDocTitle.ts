export function useDocTitle(title: string, prefix = `${import.meta.env.VITE_APP_NAME} | `) {
  if (!document)
    return

  document.title = prefix + title
}
