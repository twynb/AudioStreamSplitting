export function useDocTitle(title: string, prefix = 'Audio SS | ') {
  if (!document)
    return

  document.title = prefix + title
}
