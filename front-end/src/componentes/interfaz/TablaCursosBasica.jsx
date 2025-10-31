import React, { useMemo } from 'react';

const sinAcentos = (s) =>
  (s ?? '').toString().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
const texto = (v) => sinAcentos(v).toLowerCase().trim();

export default function TablaCursosBasica({ cursos = [], busqueda = '', onVerAlumnos }) {
  const filtrados = useMemo(() => {
    const b = texto(busqueda);
    if (!b) return cursos;
    return cursos.filter((c) =>
      [c.nombre_display, c.nombre, c.nivel, c.establecimiento, c.anioEscolar?.toString()]
        .filter(Boolean)
        .some((x) => texto(x).includes(b))
    );
  }, [cursos, busqueda]);

  if (!cursos?.length) {
    return <div className="alert alert-info">No hay cursos registrados.</div>;
  }

  if (!filtrados.length) {
    return <div className="alert alert-warning">Sin resultados para “{busqueda}”.</div>;
  }

  return (
    <div className="table-responsive">
      <table className="table table-hover align-middle">
        <thead className="table-light">
          <tr>
            <th>Nombre</th>
            <th>Nivel</th>
            <th>Año Escolar</th>
            <th>Establecimiento</th>
            {onVerAlumnos ? <th className="text-end">Acciones</th> : null}
          </tr>
        </thead>
        <tbody>
          {filtrados.map((c) => (
            <tr key={c.id}>
              <td>{c.nombre_display || c.nombre || (c.nivel ? `${c.nivel}°` : '—')}</td>
              <td>{c.nivel || '—'}</td>
              <td>{c.anioEscolar ?? '—'}</td>
              <td>{c.establecimiento || '—'}</td>
              {onVerAlumnos ? (
                <td className="text-end">
                  <button
                    className="btn btn-outline-primary btn-sm"
                    onClick={() => onVerAlumnos(c)}
                  >
                    <i className="bi bi-people me-1" />
                    Ver alumnos
                  </button>
                </td>
              ) : null}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}