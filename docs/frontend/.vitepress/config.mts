import path from 'node:path'
import fs from 'node:fs'
import { defineConfig } from 'vitepress'

const __dirname = path.resolve(__filename, '..', '..')

const components = fs.readdirSync(path.join(__dirname, 'components'))
const componentsSidebarItems = components
  .filter((f) => {
    const [name, ext] = f.split('.')
    return name !== 'index' && ext === 'md'
  }).map((f) => {
    const name = f.split('.')[0]
    return { text: name, link: `${name}` }
  })

export default defineConfig({
  lang: 'en-US',
  title: 'AudioSplitter',
  description: 'Just playing around.',

  lastUpdated: true,
  cleanUrls: true,

  head: [['link', { rel: 'icon', type: 'image/x-icon', href: '/logo.ico' }]],
  themeConfig: {
    logo: '/logo.ico',
    nav: [
      {
        text: 'Components',
        link: '/components/BaseBadge',
        activeMatch: '/components/',
      },
    ],
    sidebar: {
      '/components/': {
        base: '/components/',
        items: [
          {
            text: 'Components',
            collapsed: false,
            items: componentsSidebarItems,
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