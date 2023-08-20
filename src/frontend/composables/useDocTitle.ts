export function useDocTitle(title: string, prefix = 'Audio Splitter | ') {
  if (!document)
    return

  document.title = prefix + title
}
