export function handleAppInit() {
  useDarkToggle()
  loadEnv()

  if (import.meta.env.MODE === 'production') {
    disableContextMenu()
    disableDevTool()
    disableReload()
    disableScrollZoom()
    disableFindInPage()
  }

  function disableContextMenu() {
    document.addEventListener('contextmenu', (e) => {
      e.preventDefault()
    })
  }

  function disableDevTool() {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'F12'
      || (e.ctrlKey && e.shiftKey && ['i', 'I'].includes(e.key))
      )
        e.preventDefault()
    })
  }

  function disableReload() {
    document.addEventListener('keydown', (e) => {
      if (
        (e.ctrlKey && ['r', 'R'].includes(e.key))
      )
        e.preventDefault()
    })
  }

  function disableScrollZoom() {
    document.addEventListener('wheel', (e) => {
      if (e.ctrlKey || e.metaKey)
        e.preventDefault()
    }, { passive: false })
  }

  function disableFindInPage() {
    document.addEventListener('keydown', (e) => {
      if (
        (e.ctrlKey && ['f', 'F'].includes(e.key))
      )
        e.preventDefault()
    })
  }

  function loadEnv() {
    const env = JSON.parse(localStorage.getItem('env') ?? '{}') as Record<string, string>
    for (const [key, value] of Object.entries(env))
      axios.post('/env/set', { key, value })
  }
}
