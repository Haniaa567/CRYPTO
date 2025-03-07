import Keycloak from 'keycloak-js';

// Keycloak configuration options


export const keycloak = new Keycloak({
  url: 'http://localhost:8080/', // URL to your Keycloak server
  realm: 'HEXVAULT', // Name of your Keycloak realm
  clientId: 'Client', // Your client ID in Keycloak
});

export const initKeycloak = () => {
  return keycloak.init({
      onLoad: 'check-sso',
      silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
      pkceMethod: 'S256',
      checkLoginIframe: false,
      flow: 'standard',
      responseMode: 'query' 
  }).catch(error => {
      console.error('Keycloak init error:', error);
  });
};
