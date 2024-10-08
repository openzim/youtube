describe('home page for a channel', () => {
  beforeEach(() => {
    cy.intercept('GET', '/channel.json', { fixture: 'channel/channel.json' }).as('getChannel')
    cy.intercept('GET', '/home_playlists.json', {
      fixture: 'channel/home_playlists.json'
    }).as('getHomePlaylists')
    cy.visit('/')
    cy.wait('@getChannel')
    cy.wait('@getHomePlaylists')
  })

  it('loads the videos tab', () => {
    cy.contains('Uploads from openZIM_testing').should('be.visible')
    cy.contains('Trailers').should('be.visible')
    cy.contains('Timelapses').should('be.visible')
    cy.contains('Coffee').should('be.visible')
  })

  it('loads the playlist tab', () => {
    cy.intercept('GET', '/playlists.json', { fixture: 'channel/playlists.json' }).as('getPlaylists')
    cy.contains('.v-btn__content', 'Playlists').click()
    cy.url().should('include', '/playlists')
    cy.wait('@getPlaylists')

    cy.contains('3 playlists').should('be.visible')
    cy.contains('Timelapses').should('be.visible')
    cy.contains('Trailers').should('be.visible')
    cy.contains('Coffee').should('be.visible')
  })

  it('opens and loads "About Channel" dialog', () => {
    cy.contains('.v-btn__content', 'About Channel').click()
    cy.contains('Description for openZIM_testing').should('be.visible')
    cy.contains('Jun 4, 2024').should('be.visible')
  })
})
