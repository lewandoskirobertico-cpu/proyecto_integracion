// src/paginas/Sostenedor/DatosDelSostenedor.jsx
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import InsigniaEstado from "../../componentes/interfaz/InsigniaEstado";
import Buscar from "../../componentes/interfaz/Buscar";
import { obtenerDatosSostenedorMock } from "../../servicios/sostenedor.mock";

export default function DatosDelSostenedor() {
  const [datos, setDatos] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [busqueda, setBusqueda] = useState("");

  useEffect(() => {
    (async () => {
      const d = await obtenerDatosSostenedorMock();
      setDatos(d);
      setCargando(false);
    })();
  }, []);

  if (cargando) {
    return (
      <div className="d-flex justify-content-center align-items-center vh-100">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    );
  }

  if (!datos) {
    return (
      <div className="container py-4">
        <div className="alert alert-danger text-center">
          No fue posible cargar los datos institucionales.
        </div>
      </div>
    );
  }

  // Filtrar por nombre o RBD (aunque haya 1, así ya queda listo para escalar)
  const establecimientosFiltrados = datos.establecimientos.filter((e) =>
    e.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
    String(e.rbd).toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div className="container py-4">
      {/* Encabezado */}
      <div className="text-center mb-4">
        <h1 className="fw-bold text-primary">Datos Institucional</h1>
        <p className="text-muted">Dueño del Colegio (Sostenedor) y establecimiento asociado</p>
      </div>

      {/* Tarjeta del dueño/sostenedor */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <div className="row g-3">
            <div className="col-md-4">
              <div className="p-3 border rounded bg-light">
                <h6 className="text-muted mb-1">RUT Dueño</h6>
                <p className="fw-semibold">{datos.rut}</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-3 border rounded bg-light">
                <h6 className="text-muted mb-1">Nombre del Dueño</h6>
                <p className="fw-semibold">{datos.nombre}</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-3 border rounded bg-light">
                <h6 className="text-muted mb-1">Estado Convenio PIE</h6>
                <InsigniaEstado estado={datos.estado_convenio} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Buscador (queda por si agregas más colegios en el futuro) */}
      <Buscar valor={busqueda} onCambiar={setBusqueda} />

      {/* Tabla del establecimiento (singular) */}
      <div className="card shadow-sm">
        <div className="card-header bg-primary text-white">
          <h5 className="mb-0">Establecimiento</h5>
        </div>
        <div className="table-responsive">
          <table className="table table-hover align-middle mb-0">
            <thead className="table-light">
              <tr>
                <th>RBD</th>
                <th>Nombre</th>
                <th>Tipo</th>
                <th>Convenio PIE</th>
                <th className="text-end">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {establecimientosFiltrados.length > 0 ? (
                establecimientosFiltrados.map((e) => (
                  <tr key={e.id}>
                    <td>{e.rbd}</td>
                    <td>{e.nombre}</td>
                    <td>
                      <span className={`badge ${e.tipo === "URBANO" ? "bg-info" : "bg-success"}`}>
                        {e.tipo}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${e.convenio_pie ? "bg-primary" : "bg-secondary"}`}>
                        {e.convenio_pie ? "SI" : "NO"}
                      </span>
                    </td>
                    <td className="text-end">
                      <Link
                        className="btn btn-outline-primary btn-sm"
                        to={`/establecimientos/${e.id}/estructura`}
                      >
                        <i className="bi bi-arrow-right-circle me-1"></i> Ingresar
                      </Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="text-center text-muted">
                    No se encontró el establecimiento.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}