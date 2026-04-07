import '@/styles/layers.css'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import axios from 'axios'
import { createVuetify } from 'vuetify'
import type { Config } from '@/types/Channel'

async function loadVuetify() {
  let primaryColor = '#000000'
  let secondaryColor = '#FFFFFF'

  // Load primary and secondary colors from config.json
  try {
    const response = await axios.get('./config.json')
    if (response.status === axios.HttpStatusCode.Ok) {
      const config: Config = response.data
      primaryColor = config.mainColor || primaryColor
      secondaryColor = config.secondaryColor || secondaryColor
    }
  } catch (error) {
    console.error('Error loading config:', error)
  }

  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches

  // Light Theme
  const zimuiLight = {
    dark: false,
    colors: {
      background: '#FFFFFF',
      surface: '#FFFFFF',
      primary: primaryColor,
      secondary: secondaryColor,
      onPrimary: '#FFFFFF',
      onSurface: '#000000'
    }
  }

  // Dark Theme
  const zimuiDark = {
    dark: true,
    colors: {
      background: '#121212',
      surface: '#1E1E1E',
      primary: primaryColor,
      secondary: secondaryColor,
      onPrimary: '#FFFFFF',
      onSurface: '#FFFFFF'
    }
  }

  return createVuetify({
    theme: {
      defaultTheme: prefersDark ? 'zimuiDark' : 'zimuiLight',
      variations: {
        colors: ['primary', 'secondary'],
        lighten: 2,
        darken: 2
      },
      themes: {
        zimuiLight,
        zimuiDark
      }
    }
  })
}

export default loadVuetify
