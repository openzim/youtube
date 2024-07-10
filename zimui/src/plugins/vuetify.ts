import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import type { Config } from '@/types/Channel'

async function loadVuetify() {
  let primaryColor = '#000000'
  let secondaryColor = '#FFFFFF'

  // Load primary and secondary colors from config.json
  try {
    const response = await fetch('./config.json')
    if (response.ok) {
      const config: Config = await response.json()
      primaryColor = config.mainColor || primaryColor
      secondaryColor = config.secondaryColor || secondaryColor
    } else {
      console.error('Failed to fetch config.json')
    }
  } catch (error) {
    console.error('Error loading config:', error)
  }

  const zimuiTheme = {
    colors: {
      background: secondaryColor,
      surface: secondaryColor,
      primary: primaryColor
    }
  }

  return createVuetify({
    theme: {
      defaultTheme: 'zimuiTheme',
      variations: {
        colors: ['background', 'primary'],
        lighten: 2,
        darken: 2
      },
      themes: {
        zimuiTheme
      }
    }
  })
}

export default loadVuetify
