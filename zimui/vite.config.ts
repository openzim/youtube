import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import legacy from '@vitejs/plugin-legacy'
import { viteStaticCopy } from 'vite-plugin-static-copy'

// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    vue({
      template: {
        compilerOptions: {
          // Video.js 10 and the ogv.js fallback are native custom elements.
          isCustomElement: (tag) =>
            ['video-player', 'video-skin', 'ogvjs-video'].includes(tag)
        }
      }
    }),
    vuetify({ autoImport: true }),
    legacy({
      targets: ['fully supports es6'],
      modernPolyfills: true
    }),
    viteStaticCopy({
      targets: [
        {
          src: 'node_modules/ogv/dist/*',
          dest: 'assets/ogvjs' // ogv.js needs its workers and wasm files at runtime
        }
      ]
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  optimizeDeps: {
    include: [
      'vuetify/components/VOverlay',
      'vuetify/components/VDialog',
      'vuetify/components/VMenu',
      'vuetify/components/VSelect',
      'vuetify/components/VTooltip'
    ]
  },
  server: {
    port: 5173
  },
  preview: {
    port: 5173
  },
  build: {
    outDir: '../scraper/src/youtube2zim/zimui',
    emptyOutDir: true,
  }
})
