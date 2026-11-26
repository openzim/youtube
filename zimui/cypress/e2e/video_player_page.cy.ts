describe('video player page', () => {
  beforeEach(() => {
    cy.viewport(1366, 768)
    cy.intercept('GET', '/channel.json', { fixture: 'channel/channel.json' }).as('getChannel')
    cy.intercept('GET', '/playlists/uploads_from_openzim_testing-917Q.json', {
      fixture: 'channel/playlists/uploads_from_openzim_testing-917Q.json'
    }).as('getPlaylist')
    cy.intercept('GET', '/home_playlists.json', {
      fixture: 'channel/home_playlists.json'
    }).as('getHomePlaylists')
    cy.intercept('GET', '/videos/sample/video.webm', {
      fixture: 'channel/videos/sample/video.webm,null'
    }).as('getVideoFile')
    cy.visit('/')
    cy.wait('@getChannel')
    cy.wait('@getHomePlaylists')
  })

  it('loads the video and related information', () => {
    cy.intercept('GET', '/videos/timelapse-9Tgo.json', {
      fixture: 'channel/videos/timelapse-9Tgo.json'
    }).as('getVideo')
    cy.contains('.v-card-title ', 'Timelapse').click()
    cy.wait('@getVideo')
    cy.wait('@getPlaylist')
    cy.wait('@getVideoFile')

    cy.url().should('include', '/watch')
    cy.contains('.video-title', 'Timelapse')
    cy.contains('.video-date', 'Published on Jun 4, 2024')
    cy.contains('.video-channel', 'openZIM_testing')
    cy.contains('.video-description', 'This is a short video of a timelapse.')

    cy.get('video').should('have.prop', 'paused', false)
  })

  it('loads the playlist panel', () => {
    cy.intercept('GET', '/playlists.json', { fixture: 'channel/playlists.json' }).as('getPlaylists')
    cy.intercept('GET', '/playlists/timelapses-QgGI.json', {
      fixture: 'channel/playlists/timelapses-QgGI.json'
    }).as('getPlaylist')
    cy.intercept('GET', '/videos/timelapse-9Tgo.json', {
      fixture: 'channel/videos/timelapse-9Tgo.json'
    }).as('getVideo1')
    cy.intercept('GET', '/videos/cloudy_sky_time_lapse-k02q.json', {
      fixture: 'channel/videos/cloudy_sky_time_lapse-k02q.json'
    }).as('getVideo2')

    cy.contains('.v-btn__content', 'Playlists').click()
    cy.wait('@getPlaylists')

    cy.contains('.v-card-title ', 'Timelapses').click()
    cy.url().should('include', 'watch/timelapse-9Tgo?list=timelapses-QgGI')

    cy.wait('@getPlaylist')
    cy.wait('@getVideo1')
    cy.wait('@getVideoFile')

    cy.contains('Timelapses').should('be.visible')
    cy.contains('openZIM_testing - 1/2').should('be.visible')
    cy.get('video').should('have.prop', 'paused', false)

    cy.contains('Cloudy Sky Time Lapse').click()
    cy.contains('openZIM_testing - 2/2').should('be.visible')
    cy.get('video').should('have.prop', 'paused', false)
  })

  it('controls playback with the Video.js 10 skin', () => {
    cy.intercept('GET', '/videos/timelapse-9Tgo.json', {
      fixture: 'channel/videos/timelapse-9Tgo.json'
    }).as('getVideo')
    cy.contains('.v-card-title ', 'Timelapse').click()
    cy.wait('@getVideo')
    cy.wait('@getPlaylist')
    cy.wait('@getVideoFile')

    cy.get('video-player video').should('have.prop', 'paused', false)
    cy.get('video').should(($video) => {
      expect($video[0].readyState).to.be.greaterThan(0)
    })

    const playButton = () => cy.get('video-skin').shadow().find('media-play-button').last()

    // The packaged Video.js 10 skin exposes its controls in a shadow root.
    playButton().click({ force: true })
    cy.get('video').should('have.prop', 'paused', true)
    playButton().click({ force: true })
    cy.get('video').should('have.prop', 'paused', false)
    playButton().click({ force: true })
    cy.get('video').should('have.prop', 'paused', true)

    cy.get('video')
      .invoke('prop', 'currentTime')
      .then((beforeSeek) => {
        cy.get('video-skin').shadow().find('media-container').first().type('{rightarrow}', {
          force: true
        })
        cy.get('video').should(($video) => {
          expect($video[0].currentTime).to.be.greaterThan(beforeSeek as number)
        })
      })

    cy.get('video-skin').shadow().find('media-fullscreen-button').should('exist')
  })

  it('falls back to ogv.js when WebM is not supported natively', () => {
    cy.window().then((win) => {
      const nativeCanPlayType = win.HTMLMediaElement.prototype.canPlayType
      win.HTMLMediaElement.prototype.canPlayType = function (type: string) {
        return type.startsWith('video/') ? '' : nativeCanPlayType.call(this, type)
      }
    })

    cy.intercept('GET', '/videos/timelapse-9Tgo.json', {
      fixture: 'channel/videos/timelapse-9Tgo.json'
    }).as('getVideo')
    cy.contains('.v-card-title ', 'Timelapse').click()
    cy.wait('@getVideo')
    cy.wait('@getPlaylist')
    cy.wait('@getVideoFile')

    cy.get('ogvjs-video').should('exist')
    cy.get('video').should('not.exist')
    cy.get('ogvjs-video').should(($element) => {
      const element = $element[0] as HTMLElement & { adapter: { src: string } }
      expect(element.adapter.src).to.include('video.webm')
    })
  })
})
