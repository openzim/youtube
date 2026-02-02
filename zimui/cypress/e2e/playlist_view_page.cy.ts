describe('playlist view', () => {
  beforeEach(() => {
    cy.intercept('GET', '/channel.json', { fixture: 'channel/channel.json' }).as('getChannel')
    cy.intercept('GET', '/playlists.json', { fixture: 'channel/playlists.json' }).as('getPlaylists')
    cy.visit('/#/playlists')
    cy.wait('@getChannel')
    cy.wait('@getPlaylists')
  })

  it('loads the playlist view', () => {
    cy.intercept('GET', '/playlists/timelapses-QgGI.json', {
      fixture: 'channel/playlists/timelapses-QgGI.json'
    }).as('getPlaylist')
    cy.contains('View full playlist').click()
    cy.wait('@getPlaylist')

    cy.contains('.playlist-title', 'Timelapses').should('be.visible')
    cy.contains('.playlist-channel', 'openZIM_testing').should('be.visible')
    cy.contains('.playlist-description', 'A playlist of timelapse videos.').should('be.visible')
    cy.get('.playlist-info').within(() => {
      cy.contains('2 videos').should('be.visible')
      cy.contains('Published on Jun 4, 2024').should('be.visible')
      cy.contains('Total Duration:').should('be.visible')
    })

    cy.contains('.v-card-title', 'Timelapse').should('be.visible')
    cy.contains('.v-card-title', 'Cloudy Sky Time Lapse').should('be.visible')
  })
})
