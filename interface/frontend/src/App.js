import Landingpage from './pages/Landingpage';
import EncryptDecrypt from './pages/EncryptDecrypt';
import Passwordtesting from './pages/Passwordtesting';
import Timeprediction from './pages/Timeprediction';
import Attacks from './pages/Attacks';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { keycloak, initKeycloak } from './utils/Keycloak';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import { I18nextProvider } from 'react-i18next';
import i18n from './i18n'; // Import the i18n configuration

function App() {
  const handleOnEvent = (event, error) => {
    console.log('onKeycloakEvent', event, error);
  };

  return (
    <ReactKeycloakProvider
      authClient={keycloak}
      onEvent={handleOnEvent}
      initOptions={{
        onLoad: 'check-sso',
        silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
        pkceMethod: 'S256',
        checkLoginIframe: false
      }}
    >
      <I18nextProvider i18n={i18n}>
        <BrowserRouter>
          <Routes>
            <Route exact path="/" element={<Landingpage />} />
            <Route path="/EncryptDecrypt" element={<EncryptDecrypt />} />
            <Route path="/Attacks" element={<Attacks />} />
            <Route path="/Timeprediction" element={<Timeprediction />} />
            <Route path="/Passwordtesting" element={<Passwordtesting />} />
          </Routes>
        </BrowserRouter>
      </I18nextProvider>
    </ReactKeycloakProvider>
  );
}

export default App;
