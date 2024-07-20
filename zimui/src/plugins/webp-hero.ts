import {
  WebpMachine,
  detectWebpSupport,
  loadBinaryData,
  convertDataURIToBinary,
  isBase64Url
} from 'webp-hero'
import { Webp } from 'webp-hero/libwebp/dist/webp'
import 'webp-hero/dist-cjs/polyfills.js'

const webp = new Webp()

export async function polyfillThumbnail(src: string): Promise<string> {
  const isWebpSupport = await detectWebpSupport()
  try {
    if (!isWebpSupport) {
      const webpMachine = new WebpMachine({ webp })
      const webpData = isBase64Url(src) ? convertDataURIToBinary(src) : await loadBinaryData(src)
      const pngData = await webpMachine.decode(webpData)
      if (pngData) return pngData
    }
  } catch (error) {
    console.error(`Error polyfilling thumbnail "${src}": `, error)
  }
  return src
}
