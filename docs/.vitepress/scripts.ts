import { existsSync, mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'
import type { DocEntry } from 'tsdoc-markdown'
import { buildDocumentation } from 'tsdoc-markdown'

export function genTsDocs({ dirPath, inputFiles }: { inputFiles: string[]; dirPath: string }) {
  const entries = buildDocumentation({ inputFiles })

  if (!existsSync(dirPath))
    mkdirSync(dirPath)

  entries.forEach((entry) => {
    const md = genMD(entry)
    const targetPath = path.join(dirPath, `${entry.name}.md`)
    writeFileSync(targetPath, md, { flag: 'w' })
  })
}

function genMD(entry: DocEntry) {
  // entry.name === 'useRandomColor' && console.log(JSON.stringify(entry, null, 4))
  const md = []

  md.push(`# ${entry.name}`)
  md.push(`${entry.documentation}`)

  const params = entry.jsDocs.filter(d => d.name === 'param')
  if (params.length) {
    md.push('## Parameters')
    md.push('| Name | Description |')
    md.push('|------|-------------|')

    params.forEach((d) => {
      const [name, desc] = d.text.filter(t => t.kind !== 'space')
      md.push(`|${name?.text}|${desc?.text}|`)
    })
  }

  // TODO Make this section better
  if (entry.type) {
    const returns = entry.jsDocs.find(d => d.name === 'returns')

    md.push('## Returns')
    md.push(returns?.text?.[0]?.text)
    md.push(`\`\`\`\n${entry.type}\n\`\`\``)
  }

  const examples = entry.jsDocs.filter(d => d.name === 'example')
  if (examples.length) {
    md.push('## Examples')
    examples.forEach(e => e.text.forEach(t => md.push(t.text)))
  }

  return md.join('\n')
}
