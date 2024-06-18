describe('video player page', () => {
  beforeEach(() => {
    cy.intercept('GET', '/channel.json', { fixture: 'channel/channel.json' }).as('getChannel')
    cy.intercept('GET', '/playlists/uploads_from_openzim_testing-917Q.json', {
      fixture: 'channel/playlists/uploads_from_openzim_testing-917Q.json'
    }).as('getUploads')
    cy.visit('/')
    cy.wait('@getChannel')
    cy.wait('@getUploads')
  })

  it('loads the video and related information', () => {
    cy.intercept('GET', '/videos/timelapse-9Tgo.json', {
      fixture: 'channel//videos/timelapse-9Tgo.json'
    }).as('getVideo')
    cy.contains('.v-card-title ', 'Timelapse').click()
    cy.wait('@getVideo')

    cy.url().should('include', '/watch')
    cy.contains('.video-title', 'Timelapse')
    cy.contains('.video-date', 'Published on Jun 4, 2024')
    cy.contains('.video-channel', 'openZIM_testing')
    cy.contains('.video-description', 'This is a short video of a timelapse.')
  })
})
