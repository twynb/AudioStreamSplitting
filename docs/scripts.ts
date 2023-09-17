import { writeFileSync } from 'node:fs'
import path from 'node:path'
import { buildDocumentation, documentationToMarkdown } from 'tsdoc-markdown'

export function genTsDocs({ dirPath, inputFiles }: { inputFiles: string[]; dirPath: string }) {
  const entries = buildDocumentation({ inputFiles })

  entries.forEach((entry) => {
    // @ts-expect-error remove `#`
    const md = documentationToMarkdown({ entries: [entry], options: { headingLevel: '' } })
    const data = md.replace(':gear: ', '').trimEnd().split('\n').slice(4).join('\n')
    writeFileSync(path.join(dirPath, `${entry.name}.md`), data, { flag: 'w' })
  })
}
