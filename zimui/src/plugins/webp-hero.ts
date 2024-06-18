import { WebpMachine, detectWebpSupport } from 'webp-hero'
import 'webp-hero/dist-cjs/polyfills.js'

export const triggerWebpPolyfill = () => {
  detectWebpSupport().then((support_webp) => {
    if (!support_webp) {
      const webpMachine = new WebpMachine()
      webpMachine.polyfillDocument()
    }
  })
}
