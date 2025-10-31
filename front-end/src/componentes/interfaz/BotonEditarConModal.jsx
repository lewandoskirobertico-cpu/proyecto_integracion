// src/componentes/interfaz/BotonEditarConModal.jsx
import React, { useMemo } from 'react';
import BotonCrearConModal from './BotonCrearConModal';

/**
 * Botón para EDITAR reutilizando el mismo modal de crear.
 * - Abre con los valores actuales del registro.
 * - Llama a onGuardar(payload) cuando confirmas.
 */
export default function BotonEditarConModal({
  registro,
  campos = [],
  titulo = 'Editar curso',
  textoBoton = 'Editar',
  icono = 'bi-pencil-square',
  className = 'btn btn-sm btn-outline-secondary',
  transformarValores,
  onGuardar,
  onExito,
}) {
  // Mapea los campos del modal a los valores del registro
  const valoresIniciales = useMemo(() => {
    const v = {};
    campos.forEach((c) => {
      v[c.name] = registro?.[c.name] ?? '';
    });
    return v;
  }, [registro, campos]);

  return (
    <BotonCrearConModal
      titulo={titulo}
      textoBoton={textoBoton}
      icono={icono}
      className={className}
      tamanoModal="modal-lg"
      campos={campos}
      valoresIniciales={valoresIniciales}
      transformarValores={transformarValores}
      onGuardar={onGuardar}
      onExito={onExito}
    />
  );
}