// src/servicios/alumnos.js
import axios from 'axios';

const API_BASE =
  import.meta?.env?.VITE_API_BASE_URL ||
  process.env.REACT_APP_API_URL ||
  'http://127.0.0.1:8000/api';

function unpack(data) {
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data.results)) return data.results; // DRF paginado
  return [];
}

export async function obtenerAlumnosPorCurso(cursoId) {
  // Trae el curso (para encabezado)
  const { data: curso } = await axios.get(`${API_BASE}/cursos/${cursoId}/`);

  // Trae alumnos por curso
  const { data } = await axios.get(`${API_BASE}/estudiantes/?curso=${cursoId}`);
  const rows = unpack(data);

  const alumnos = rows.map((a) => ({
    id: a.id,
    run: a.run ?? '',
    nombreCompleto: a.nombres_apellidos ?? '',
    // El serializer ya trae 'curso' anidado; si no, usamos el nombre del curso obtenido
    cursoNombre: a.curso?.nombre || a.curso?.nombre_display || curso?.nombre || '',
  }));

  return { curso, alumnos };
}
