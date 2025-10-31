// src/servicios/estructuraCurso.js
import axios from 'axios';

// === Utilidades ===
function normalizarEstablecimiento(s) {
  if (!s) return '';
  try {
    return decodeURIComponent(String(s)).replace(/-/g, ' ').trim();
  } catch {
    return String(s).replace(/-/g, ' ').trim();
  }
}
function compararIgual(a, b) {
  return String(a || '').trim().toLowerCase() === String(b || '').trim().toLowerCase();
}
function extraerNumero(txt) {
  const m = String(txt || '').match(/(\d{1,2})/);
  return m ? parseInt(m[1], 10) : NaN;
}

// Construye "1° Medio A" a partir de nombre/nivel (sin tocar el back)
function construirNombreDisplay(curso) {
  const nombreRaw = (curso?.nombre || '').trim();
  const nivelCampo = (curso?.nivel || '').trim();

  // "1 medio A", "1° básico B"
  const rx = /^\s*(\d{1,2})\s*(?:°|º)?\s*(b[aá]sico|medio)\s*([A-Z]{1,2})?\s*$/i;
  const m = nombreRaw.match(rx);
  if (m) {
    const n = parseInt(m[1], 10);
    const ciclo = capitalizarCiclo(m[2]);
    const sec = m[3] ? m[3].toUpperCase() : '';
    return `${n}° ${ciclo}${sec ? ` ${sec}` : ''}`;
  }

  const cicloDetectado = detectarCiclo(nombreRaw) || detectarCiclo(nivelCampo);
  const nNombre = extraerNumero(nombreRaw);
  const nNivel = extraerNumero(nivelCampo);
  const n = !Number.isNaN(nNombre) ? nNombre : !Number.isNaN(nNivel) ? nNivel : NaN;

  let sec = '';
  const secMatch = nombreRaw.match(/(?:\s|-)([A-Z]{1,2})\s*$/i);
  if (secMatch) sec = secMatch[1].toUpperCase();

  if (!Number.isNaN(n) && cicloDetectado) return `${n}° ${cicloDetectado}${sec ? ` ${sec}` : ''}`;
  if (!Number.isNaN(n)) return `${n}°${sec ? ` ${sec}` : ''}`;
  return nombreRaw || '—';
}
function detectarCiclo(texto) {
  const t = String(texto || '').toLowerCase();
  if (t.includes('medio')) return 'Medio';
  if (t.includes('básico') || t.includes('basico')) return 'Básico';
  return '';
}
function capitalizarCiclo(s) {
  const t = String(s || '').toLowerCase();
  if (t.startsWith('medio')) return 'Medio';
  if (t.startsWith('básico') || t.startsWith('basico')) return 'Básico';
  return '';
}

// Orden: Básico → Medio → número → sección
function cicloRank(display) {
  const d = String(display || '').toLowerCase();
  if (d.includes('básico') || d.includes('basico')) return 1;
  if (d.includes('medio')) return 2;
  return 99;
}
function numeroDesdeDisplay(display) {
  const m = String(display || '').match(/(\d{1,2})\s*°/);
  return m ? parseInt(m[1], 10) : 999;
}
function extraerSeccion(display) {
  const m = String(display || '').match(/([A-Z]{1,2})\s*$/);
  return m ? m[1] : '';
}

/**
 * Conectado al back:
 *  - Si viene `nombreEst`, intentamos GET /api/cursos/?establecimiento=nombreEst
 *  - Si el back devuelve vacío, traemos todos y filtramos en el front (igualando case-insensitive)
 *  - Si 404 (aún sin endpoint), devolvemos vacío sin romper la UI
 */
export async function obtenerEstructuraCurso(nombreEst) {
  const establecimientoQ = normalizarEstablecimiento(nombreEst);
  let cursosRaw = [];

  try {
    const params = establecimientoQ ? { establecimiento: establecimientoQ } : {};
    const r = await axios.get('/api/cursos/', { params });
    cursosRaw = Array.isArray(r.data) ? r.data : [];

    if (establecimientoQ && cursosRaw.length === 0) {
      // Fallback: algunos backends no filtran, así que traemos todo y filtramos aquí
      const r2 = await axios.get('/api/cursos/');
      const todos = Array.isArray(r2.data) ? r2.data : [];
      cursosRaw = todos.filter((c) => compararIgual(c.establecimiento, establecimientoQ));
    }
  } catch (err) {
    if (err?.response?.status === 404) {
      return { establecimiento: { nombre: establecimientoQ }, cursos: [] };
    }
    throw err;
  }

  const cursos = cursosRaw
    .map((c) => ({ ...c, nombre_display: construirNombreDisplay(c) }))
    .sort((a, b) => {
      const cr = cicloRank(a.nombre_display) - cicloRank(b.nombre_display);
      if (cr !== 0) return cr;
      const nr = numeroDesdeDisplay(a.nombre_display) - numeroDesdeDisplay(b.nombre_display);
      if (nr !== 0) return nr;
      return extraerSeccion(a.nombre_display).localeCompare(extraerSeccion(b.nombre_display));
    });

  const nombreDetectado =
    establecimientoQ || (cursos[0]?.establecimiento ? String(cursos[0].establecimiento) : '');

  return {
    establecimiento: { nombre: nombreDetectado },
    cursos,
  };
}

export async function crearCurso(payload) {
  return (await axios.post('/api/cursos/', payload)).data;
}

// === NUEVO: actualizar un curso (PATCH parcial) ===
export async function actualizarCurso(id, payload) {
  // Si tu back NO usa slash final, cambia a `/api/cursos/${id}`
  const { data } = await axios.patch(`/api/cursos/${id}/`, payload);
  return data;
}