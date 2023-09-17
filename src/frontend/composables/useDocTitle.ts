/**
 * Set the document's title with an optional prefix.
 *
 * @param title - The title to set.
 * @param prefix - An optional prefix to prepend to the title.
 */
export function useDocTitle(title: string, prefix = `${import.meta.env.VITE_APP_NAME} | `) {
  if (!document)
    return

  document.title = prefix + title
}
