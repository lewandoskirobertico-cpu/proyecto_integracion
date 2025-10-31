// src/servicios/sostenedor.mock.js

// === Ajusta estos datos cuando tengas los reales ===
const DUENO_RUT    = "76.123.456-7";          // RUT del dueño/sostenedor
const DUENO_NOMBRE = "Dueño del Colegio XYZ"; // Nombre del dueño/sostenedor
const EST_RBD      = "12345";                  // RBD del establecimiento (si no tienes, deja "N/A")
const EST_NOMBRE   = "Colegio XYZ";            // Nombre del colegio (tu establecimiento)
const EST_TIPO     = "URBANO";                 // "URBANO" | "RURAL"
const TIENE_PIE    = true;                     // Convenio PIE del establecimiento
// ====================================================

export async function obtenerDatosSostenedorMock() {
  // simulamos latencia
  await new Promise((r) => setTimeout(r, 200));

  // Aunque sea 1 colegio, mantenemos el mismo formato de respuesta
  // para no tocar tu front ni tus componentes.
  return {
    rut: DUENO_RUT,
    nombre: DUENO_NOMBRE,
    estado_convenio: TIENE_PIE ? "VIGENTE" : "SIN CONVENIO",
    establecimientos: [
      { id: 1, rbd: EST_RBD, nombre: EST_NOMBRE, tipo: EST_TIPO, convenio_pie: TIENE_PIE },
    ],
  };
}