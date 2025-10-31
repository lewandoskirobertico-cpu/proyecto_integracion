import { BrowserRouter, Routes, Route } from "react-router-dom";
import BarraNavegacion from "./componentes/diseno/BarraNavegacion";
import DatosDelSostenedor from "./paginas/Sostenedor/DatosDelSostenedor";
import EstructuraDeCurso from "./paginas/Establecimientos/EstructuraDeCurso";
import AlumnosDelCurso from "./paginas/alumnos/AlumnosDelCurso";

function App() {
  return (
    <BrowserRouter>
      <BarraNavegacion />
      <main>
        <Routes>
          <Route path="/" element={<DatosDelSostenedor />} />
          <Route path="/sostenedor" element={<DatosDelSostenedor />} />
          {/* Cursos del establecimiento (tu pantalla actual) */}
          <Route path="/establecimientos/:id/estructura" element={<EstructuraDeCurso />} />
          {/* Alumnos de un curso específico */}
          <Route
            path="/establecimientos/:id/cursos/:cursoId/alumnos"
            element={<AlumnosDelCurso />}
          />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;