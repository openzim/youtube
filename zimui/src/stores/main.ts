import { defineStore } from 'pinia'
import axios, { AxiosError } from 'axios'
import type { Channel } from '@/types/Channel'
import type { Playlist, Playlists } from '@/types/Playlists'
import type { Video } from '@/types/Videos'

export type RootState = {
  channel: Channel | null
  isLoading: boolean
  errorMessage: string
  errorDetails: string
}

export const useMainStore = defineStore('main', {
  state: () =>
    ({
      channel: null,
      isLoading: false,
      errorMessage: '',
      errorDetails: ''
    }) as RootState,
  getters: {},
  actions: {
    async fetchChannel() {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./channel.json').then(
        (response) => {
          this.isLoading = false
          this.channel = response.data as Channel
        },
        (error) => {
          this.isLoading = false
          this.channel = null
          this.errorMessage = 'Failed to load channel data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchPlaylist(title: string) {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get(`./playlists/${title}.json`).then(
        (response) => {
          this.isLoading = false
          this.checkResponseObject(response.data, 'Playlist not found.')
          return response.data as Playlist
        },
        (error) => {
          this.isLoading = false
          this.errorMessage = 'Failed to load playlist data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchPlaylists() {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./playlists.json').then(
        (response) => {
          this.isLoading = false
          return response.data as Playlists
        },
        (error) => {
          this.isLoading = false
          this.errorMessage = 'Failed to load playlists data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchVideo(slug: string) {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get(`./videos/${slug}.json`).then(
        (response) => {
          this.isLoading = false
          this.checkResponseObject(response.data, 'Video not found.')
          const video: Video = response.data
          return video
        },
        (error) => {
          this.isLoading = false
          this.errorMessage = 'Failed to load video data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    checkResponseObject(response: unknown, msg: string = '') {
      if (response === null || typeof response !== 'object') {
        if (msg !== '') {
          this.errorDetails = msg
        }
        throw new Error('Invalid response object.')
      }
    },
    handleAxiosError(error: AxiosError<object>) {
      if (axios.isAxiosError(error) && error.response) {
        const status = error.response.status
        switch (status) {
          case 400:
            this.errorDetails =
              'HTTP 400: Bad Request. The server could not understand the request.'
            break
          case 404:
            this.errorDetails =
              'HTTP 404: Not Found. The requested resource could not be found on the server.'
            break
          case 500:
            this.errorDetails =
              'HTTP 500: Internal Server Error. The server encountered an unexpected error.'
            break
        }
      }
    },
    setErrorMessage(message: string) {
      this.errorMessage = message
    }
  }
})
