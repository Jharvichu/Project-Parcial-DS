import axios from 'axios';

// Creamos una instancia centralizada de Axios
const api = axios.create({
  baseURL: 'http://localhost:8000/api', // La URL base de tu backend de Python
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;