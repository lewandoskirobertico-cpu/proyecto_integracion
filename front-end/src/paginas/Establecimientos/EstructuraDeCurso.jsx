// src/paginas/Establecimientos/EstructuraDeCurso.jsx
import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Buscar from '../../componentes/interfaz/Buscar';
import BotonCrearConModal from '../../componentes/interfaz/BotonCrearConModal';
import { obtenerEstructuraCurso, crearCurso, actualizarCurso } from '../../servicios/estructuraCurso';
import BotonEditarConModal from '../../componentes/interfaz/BotonEditarConModal';

function normalizarParamEst(s) {
  try {
    return decodeURIComponent(s ?? '').replace(/-/g, ' ').trim();
  } catch {
    return String(s ?? '').replace(/-/g, ' ').trim();
  }
}
function normalizarTexto(str) {
  return (str ?? '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

export default function EstructuraDeCurso() {
  const navigate = useNavigate();
  const { id } = useParams();
  const nombreEstParam = normalizarParamEst(id);

  const [data, setData] = useState({ establecimiento: { nombre: nombreEstParam }, cursos: [] });
  const [busqueda, setBusqueda] = useState('');
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');

  async function cargarDatos() {
    setCargando(true);
    setError('');
    try {
      const res = await obtenerEstructuraCurso(nombreEstParam);
      setData(res);
    } catch (err) {
      const msg = err?.message
        ? `No se pudo cargar la estructura de curso. Detalle: ${err.message}`
        : 'No se pudo cargar la estructura de curso.';
      setError(msg);
      console.error('[EstructuraDeCurso] Error:', err);
    } finally {
      setCargando(false);
    }
  }

  useEffect(() => {
    cargarDatos();
  }, [nombreEstParam]);

  const cursosFiltrados = useMemo(() => {
    const q = normalizarTexto(busqueda);
    if (!q) return data.cursos;
    return data.cursos.filter((c) => {
      const cursoNombre = normalizarTexto(c.nombre ?? '');
      const nivel = normalizarTexto(c.nivel ?? '');
      const anio = normalizarTexto((c.anio_escolar ?? '').toString());
      const est = normalizarTexto(c.establecimiento ?? '');
      const display = normalizarTexto(c.nombre_display ?? '');
      return (
        cursoNombre.includes(q) ||
        nivel.includes(q) ||
        anio.includes(q) ||
        est.includes(q) ||
        display.includes(q)
      );
    });
  }, [busqueda, data.cursos]);

  function irAlumnos(curso) {
    navigate(`/establecimientos/${id}/cursos/${curso.id}/alumnos`);
  }

  // ⬇️ Nuevo: navegación al apoyo personal
  function irApoyoPersonal(curso) {
    navigate(`/establecimientos/${id}/cursos/${curso.id}/apoyo-personal`);
  }

  return (
    <div className="container py-4">
      <div className="row justify-content-center">
        <div className="col-12 col-lg-11 col-xl-10" style={{ maxWidth: '1100px' }}>
          <div className="d-flex flex-column flex-md-row align-items-md-center justify-content-md-between mb-3 gap-2">
            <h2 className="h4 mb-0 text-center text-md-start">
              Cursos – {data?.establecimiento?.nombre ?? nombreEstParam ?? '—'}
            </h2>
            <div className="d-flex gap-2 justify-content-center justify-content-md-end">
              <button type="button" className="btn btn-outline-secondary" onClick={cargarDatos}>
                <i className="bi bi-arrow-clockwise me-1" aria-hidden="true"></i>
                Refrescar
              </button>

              <BotonCrearConModal
                textoBoton="Agregar curso"
                icono="bi-plus-lg"
                titulo="Agregar curso"
                tamanoModal="modal-lg"
                valoresIniciales={{
                  nombre: '',
                  nivel: '',
                  anio_escolar: '',
                  establecimiento: data?.establecimiento?.nombre ?? nombreEstParam ?? '',
                }}
                campos={[
                  { name: 'nombre', label: 'Curso (nombre)', required: true, placeholder: 'Ej: 1 medio A', col: 'col-md-6' },
                  { name: 'nivel', label: 'Nivel', placeholder: 'Ej: 1 medio', col: 'col-md-6' },
                  { name: 'anio_escolar', label: 'Año escolar', type: 'number', attrs: { min: 1900, max: 2100 }, col: 'col-md-6' },
                  { name: 'establecimiento', label: 'Establecimiento', placeholder: 'Ej: Liceo X', col: 'col-md-6' },
                ]}
                transformarValores={(vals) => ({
                  nombre: String(vals.nombre ?? '').trim(),
                  ...(vals.nivel ? { nivel: String(vals.nivel).trim() } : {}),
                  ...(vals.anio_escolar ? { anio_escolar: Number(vals.anio_escolar) } : {}),
                  ...(vals.establecimiento ? { establecimiento: String(vals.establecimiento).trim() } : {}),
                })}
                onGuardar={async (payload) => await crearCurso(payload)}
                onExito={async () => { await cargarDatos(); }}
              />
            </div>
          </div>

          <div className="mb-3">
            <Buscar
              valor={busqueda}
              onCambiar={setBusqueda}
              placeholder="Buscar: curso, nivel, año escolar o establecimiento…"
            />
          </div>

          {error ? (
            <div className="alert alert-danger" role="alert">{error}</div>
          ) : null}

          {cargando ? (
            <div className="d-flex align-items-center gap-2 text-muted justify-content-center">
              <div className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></div>
              <span>Cargando cursos…</span>
            </div>
          ) : (
            <div className="table-responsive-md">
              <table className="table table-hover table-sm align-middle ">
                <thead className="table-light">
                  <tr>
                    <th className="text-nowrap">Curso</th>
                    <th className="text-nowrap">Nivel</th>
                    <th className="text-center text-nowrap">Año escolar</th>
                    <th className="text-nowrap">Establecimiento</th>
                    <th className="text-center text-nowrap">Habilitado Subv.</th>
                    <th className="text-center text-nowrap">JECD</th>
                    <th className="text-center text-nowrap">Matr. Vig.</th>
                    <th className="text-center text-nowrap">Matr. Post.</th>
                    <th className="text-center text-nowrap">Alumnos</th>
                    {/* ⬇️ Nuevo encabezado */}
                    <th className="text-center text-nowrap">Apoyo personal</th>
                    <th className="text-center text-nowrap">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {cursosFiltrados.length ? (
                    cursosFiltrados.map((c) => (
                      <tr key={c.id}>
                        <td className="text-nowrap">{c.nombre ?? c.nombre_display ?? (c.nivel ? `${c.nivel}°` : '—')}</td>
                        <td className="text-nowrap">{c.nivel ?? '—'}</td>
                        <td className="text-center text-nowrap">{c.anio_escolar ?? '—'}</td>
                        <td className="text-nowrap">{c.establecimiento ?? '—'}</td>
                        <td className="text-center"><span className="badge text-bg-secondary">NO</span></td>
                        <td className="text-center"><span className="badge text-bg-success">Si</span></td>
                        <td className="text-center">0</td>
                        <td className="text-center">0</td>

                        {/* Botón alumnos */}
                        <td className="text-center">
                          <button
                            type="button"
                            className="btn btn-sm btn-outline-primary"
                            onClick={() => irAlumnos(c)}
                            title="Ver alumnos"
                          >
                            <i className="bi bi-people-fill" aria-hidden="true"></i>
                          </button>
                        </td>

                        {/* ⬇️ Nuevo botón apoyo personal */}
                        <td className="text-center">
                          <button
                            type="button"
                            className="btn btn-sm btn-outline-success"
                            onClick={() => irApoyoPersonal(c)}
                            title="Ver apoyo personal"
                          >
                            <i className="bi bi-person-heart" aria-hidden="true"></i>
                          </button>
                        </td>

                        <td className="text-center">
                          <BotonEditarConModal
                            registro={c}
                            titulo="Editar curso"
                            textoBoton="Editar"
                            icono="bi-pencil-square"
                            className="btn btn-sm btn-outline-secondary"
                            campos={[
                              { name: 'nombre', label: 'Curso (nombre)', required: true, placeholder: 'Ej: 1 Básico B', col: 'col-md-6' },
                              { name: 'nivel', label: 'Nivel', placeholder: 'Ej: Básica / Media', col: 'col-md-6' },
                              { name: 'anio_escolar', label: 'Año escolar', type: 'number', attrs: { min: 1900, max: 2100 }, col: 'col-md-6' },
                            ]}
                            transformarValores={(vals) => ({
                              ...(vals.nombre !== '' ? { nombre: String(vals.nombre).trim() } : {}),
                              ...(vals.nivel !== '' ? { nivel: String(vals.nivel).trim() } : {}),
                              ...(vals.anio_escolar !== '' ? { anio_escolar: Number(vals.anio_escolar) } : {}),
                            })}
                            onGuardar={(payload) => actualizarCurso(c.id, payload)}
                            onExito={cargarDatos}
                          />
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={11} className="text-center text-muted">
                        Aún no hay cursos cargados para este establecimiento.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
