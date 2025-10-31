import React, { useEffect, useMemo, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import Buscar from '../../componentes/interfaz/Buscar';
import { obtenerAlumnosPorCurso } from '../../servicios/alumnos';

const norm = (s) =>
  (s ?? '').toString().normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();

export default function AlumnosDelCurso() {
  const { id, cursoId } = useParams(); // id = nombre del establecimiento (texto)
  const [alumnos, setAlumnos] = useState([]);
  const [cursoNombre, setCursoNombre] = useState('');
  const [q, setQ] = useState('');
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let vivo = true;
    setCargando(true); setError(null);

    obtenerAlumnosPorCurso(cursoId)
      .then(({ curso, alumnos }) => {
        if (!vivo) return;
        setAlumnos(alumnos);
        setCursoNombre(curso?.nombre || curso?.nombre_display || '');
      })
      .catch((e) => setError(e?.friendlyMessage || e?.message || 'No se pudo cargar'))
      .finally(() => { if (vivo) setCargando(false); });

    return () => { vivo = false; };
  }, [cursoId]);

  const filtrados = useMemo(() => {
    if (!q) return alumnos;
    const b = norm(q);
    return alumnos.filter((a) =>
      [a.run, a.nombreCompleto, a.cursoNombre].filter(Boolean).some((x) => norm(x).includes(b))
    );
  }, [alumnos, q]);

  if (cargando) {
    return <div className="text-center my-5"><div className="spinner-border" role="status" /></div>;
  }
  if (error) {
    return <div className="alert alert-danger m-3">{error}</div>;
  }

  return (
    <div className="container my-4">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="mb-0">Alumnos {cursoNombre ? `- ${cursoNombre}` : ''}</h5>
        <Link
          to={`/establecimientos/${encodeURIComponent(id)}/estructura`}
          className="btn btn-secondary btn-sm"
        >
          Volver a cursos
        </Link>
      </div>

      <Buscar placeholder="Buscar alumno (RUN o nombre)..." valor={q} onCambiar={setQ} />

      <div className="table-responsive">
        <table className="table table-hover align-middle">
          <thead className="table-light">
            <tr>
              <th>RUN</th>
              <th>Nombre</th>
              <th>Curso</th>
            </tr>
          </thead>
          <tbody>
            {filtrados.length === 0 ? (
              <tr>
                <td colSpan={3}>
                  <div className="alert alert-warning m-0">Sin resultados.</div>
                </td>
              </tr>
            ) : (
              filtrados.map((a) => (
                <tr key={a.id}>
                  <td>{a.run || '—'}</td>
                  <td>{a.nombreCompleto || '—'}</td>
                  <td>{a.cursoNombre || '—'}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}