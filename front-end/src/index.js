// ✅ Todas las importaciones al inicio
import React from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';
import Cookies from 'js-cookie'; // 👈 Agrega aquí, junto con los demás imports
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// Bootstrap y estilos
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './estilos/personalizado.css';

// ✅ Configuración de axios
axios.defaults.baseURL = process.env.REACT_APP_API_URL || 'http://34.227.79.113:8000';
axios.defaults.headers.common['Accept'] = 'application/json';
axios.defaults.withCredentials = true;

axios.interceptors.request.use((config) => {
  const token = Cookies.get('csrftoken');
  if (token) {
    config.headers['X-CSRFToken'] = token;
  }
  return config;
});

// ✅ Render de React
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

reportWebVitals();

