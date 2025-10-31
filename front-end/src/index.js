// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// Bootstrap y estilos
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './estilos/personalizado.css';

// Todas las llamadas a /api/... van a Django (ajusta si usas otro host/puerto)
axios.defaults.baseURL = process.env.REACT_APP_API_BASE || 'http://127.0.0.1:8000';
axios.defaults.headers.common['Accept'] = 'application/json';
// axios.defaults.withCredentials = true; // si usas sesión/CSRF

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

reportWebVitals();