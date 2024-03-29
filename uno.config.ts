import type { Theme } from 'unocss/preset-mini'
import {
  defineConfig,
  presetAttributify,
  presetIcons,
  presetUno,
} from 'unocss'

import transformerDirectives from '@unocss/transformer-directives'
import transformerVariantGroup from '@unocss/transformer-variant-group'

export default defineConfig({
  shortcuts: [
    {
      'flex-center': 'flex justify-center items-center',
      'flex-col-center': 'flex flex-col justify-center items-center',
      'wh-full': 'w-full h-full',
      'absolute-center': 'absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2',
    },
  ],
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.3,
      warn: true,
      extraProperties: { display: 'inline-block' },
    }),
  ],
  transformers: [
    transformerDirectives(),
    transformerVariantGroup(),
  ],
  preflights: [
    {
      getCSS: () => `
        :root {
          --background: 0,0%,100%;
          --foreground: 222.2,47.4%,11.2%;
          --muted: 210,40%,96.1%;
          --muted-foreground: 215.4,16.3%,46.9%;
          --popover: 0,0%,100%;
          --popover-foreground: 222.2,47.4%,11.2%;
          --border: 214.3,31.8%,91.4%;
          --input: 214.3,31.8%,91.4%;
          --card: 0,0%,100%;
          --card-foreground: 222.2,47.4%,11.2%;
          --primary: 222.2,47.4%,11.2%;
          --primary-foreground: 210,40%,98%;
          --secondary: 210,40%,96.1%;
          --secondary-foreground: 222.2,47.4%,11.2%;
          --accent: 210,40%,96.1%;
          --accent-foreground: 222.2,47.4%,11.2%;
          --destructive: 0,100%,50%;
          --destructive-foreground: 210,40%,98%;
          --ring: 215,20.2%,65.1%;
          --radius: 0.5rem;
          --neon: 79, 36%, 50%;
          --neon-dark: 79, 36%, 42%;
        }

        .dark {
          --background: 224,71%,4%;
          --foreground: 213,31%,91%;
          --muted: 223,47%,11%;
          --muted-foreground: 215.4,16.3%,56.9%;
          --accent: 216,34%,17%;
          --accent-foreground: 210,40%,98%;
          --popover: 224,71%,4%;
          --popover-foreground: 215,20.2%,65.1%;
          --border: 216,34%,17%;
          --input: 216,34%,17%;
          --card: 224,71%,4%;
          --card-foreground: 213,31%,91%;
          --primary: 210,40%,98%;
          --primary-foreground: 222.2,47.4%,1.2%;
          --secondary: 222.2,47.4%,11.2%;
          --secondary-foreground: 210,40%,98%;
          --destructive: 0,63%,31%;
          --destructive-foreground: 210,40%,98%;
          --ring: 216,34%,17%;
          --radius: 0.5rem;
          --neon: 81, 96%, 55%;
          --neon-dark: 81, 96%, 45%;
        }
      `,
    },
  ],
  theme: {
    colors: {
      border: 'hsl(var(--border))',
      input: 'hsl(var(--input))',
      ring: 'hsl(var(--ring))',
      background: 'hsl(var(--background))',
      foreground: 'hsl(var(--foreground))',
      primary: {
        DEFAULT: 'hsl(var(--primary))',
        foreground: 'hsl(var(--primary-foreground))',
      },
      secondary: {
        DEFAULT: 'hsl(var(--secondary))',
        foreground: 'hsl(var(--secondary-foreground))',
      },
      destructive: {
        DEFAULT: 'hsl(var(--destructive))',
        foreground: 'hsl(var(--destructive-foreground))',
      },
      muted: {
        DEFAULT: 'hsl(var(--muted))',
        foreground: 'hsl(var(--muted-foreground))',
      },
      accent: {
        DEFAULT: 'hsl(var(--accent))',
        foreground: 'hsl(var(--accent-foreground))',
      },
      neon: {
        DEFAULT: 'hsl(var(--neon))',
        dark: 'hsl(var(--neon-dark))',
      },
    },
    borderRadius: {
      lg: 'var(--radius)',
      md: 'calc(var(--radius) - 2px)',
      sm: 'calc(var(--radius) - 4px)',
    },
  } satisfies Theme,
})
