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
    vue(),
    vuetify({ autoImport: true }),
    legacy({
      targets: ['fully supports es6'],
      modernPolyfills: true
    }),
    viteStaticCopy({
      targets: [
        {
          src: 'node_modules/ogv/dist/*',
          dest: 'assets/ogvjs' // videojs-ogvjs-plugin needs access to ogvjs files at runtime
        }
      ]
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173
  },
  preview: {
    port: 5173
  }
})
