import path from 'node:path'
import fs from 'node:fs'
import { defineConfig } from 'vitepress'
import { genTsDocs } from './scripts'

/**
 * Paths
 */
const projectPath = path.resolve(__filename, '..', '..', '..')

const srcFrontendPath = path.join(projectPath, 'src', 'frontend')
const srcComposablesPath = path.join(srcFrontendPath, 'composables')

const docsFrontendPath = path.join(projectPath, 'docs', 'frontend')
const docsComponentsPath = path.join(docsFrontendPath, 'components')
const docsComposablesPath = path.join(docsFrontendPath, 'composables')

const docsComponents = fs.readdirSync(docsComponentsPath)
const componentsSidebarItems = docsComponents
  .filter((f) => {
    const [name, ext] = f.split('.')
    return name !== 'index' && ext === 'md'
  }).map((f) => {
    const name = f.split('.')[0]
    return { text: name, link: `/${name}` }
  })

const srcComposables = fs.readdirSync(srcComposablesPath)
genTsDocs({
  dirPath: docsComposablesPath,
  inputFiles: srcComposables.map(f => path.join(srcComposablesPath, f)),
})
const docsComposables = fs.readdirSync(docsComposablesPath)
const composablesSidebarItems = docsComposables
  .filter((f) => {
    const [name, ext] = f.split('.')
    return name !== 'index' && ext === 'md'
  }).map((f) => {
    const name = f.split('.')[0]
    return { text: name, link: `/${name}` }
  })

export default defineConfig({
  lang: 'en-US',
  title: 'AudioSplitter',

  lastUpdated: true,
  cleanUrls: true,

  ignoreDeadLinks: true,
  base: 'audiosplitter',

  head: [['link', { rel: 'icon', type: 'image/x-icon', href: '/logo.ico' }]],
  themeConfig: {
    logo: '/logo.ico',
    nav: [
      {
        text: 'Backend',
        link: '/backend/_build/markdown/',
        activeMatch: '/backend/',
      },
      {
        text: 'Frontend',
        link: '/frontend/components/BaseBadge',
        activeMatch: '/frontend/',
      },
      {
        text: 'v1.0.0',
        items: [
          {
            text: 'Contributing',
            link: 'https://github.com/4lex0017/AudioStreamSplitting/blob/main/CONTRIBUTING.md',
          },
        ],
      },
    ],
    sidebar: {
      '/frontend/': {
        base: '/frontend/',
        items: [
          {
            text: 'Components',
            base: '/frontend/components',
            collapsed: false,
            items: componentsSidebarItems,
          },
          {
            text: 'Composables',
            base: '/frontend/composables',
            collapsed: false,
            items: composablesSidebarItems,
          },
        ],
      },
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/4lex0017/AudioStreamSplitting' },
    ],
    footer: {
      message: 'Released under the GNU GPLv3 License.',
      copyright: 'Phat Nguyen (chubetho), Christina Reichel (ChrisItisdud), 4lex0017, JosuaE-FHWS',
    },
  },
})
