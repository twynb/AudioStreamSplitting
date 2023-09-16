import { defineConfig } from 'vitepress'

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
        text: 'Backend',
        link: '/backend/',
        activeMatch: '/backend/',
      },
      {
        text: 'Frontend',
        link: '/frontend/',
        activeMatch: '/frontend/',
      },
    ],
    sidebar: {
      '/backend/': {
        base: '/backend/',
        items: [],
      },
      '/frontend/': {
        base: '/frontend/',
        items: [
          {
            text: 'Components',
            collapsed: false,
            items: [
              { text: 'BaseBadge', link: 'components/BaseBadge' },
              { text: 'BaseButton', link: 'components/BaseButton' },
              { text: 'BaseProgress', link: 'components/BaseProgress' },
            ],
          },
        ],
      },
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/4lex0017/AudioStreamSplitting' },
    ],
    footer: {
      message: 'Released under the GNU License.',
    },
  },
})
