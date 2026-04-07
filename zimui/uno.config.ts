import { defineConfig } from 'unocss'
import { presetVuetify } from 'unocss-preset-vuetify'

export default defineConfig({
  presets: [presetVuetify()],
  outputToCssLayers: {
    cssLayerName: (layer) => (layer === 'properties' ? null : `uno.${layer}`)
  }
})
