// src/componentes/interfaz/Buscar.jsx
import React, { useEffect, useRef, useState } from 'react';

export default function Buscar({
  // Compatibilidad + API universal
  value,            // preferido
  valor,            // compatibilidad
  onChange,         // preferido
  onCambiar,        // compatibilidad

  placeholder = 'Buscar…',
  debounceMs = 0,           // 0 = sin debounce; 200–300 recomendado para backend
  onDebouncedChange,        // si requieres callback solo cuando termina el debounce
  onSubmit,                 // Enter
  onClear,                  // callback al limpiar
  autoFocus = false,
  className = '',
  size = 'md',              // 'sm' | 'md' | 'lg'
  icon = 'bi-search',       // clase de Bootstrap Icons (solo el nombre, sin el prefijo 'bi ')
  clearButton = true,
  name,
  id,
  'aria-label': ariaLabel,
}) {
  const controlledValue = value ?? valor ?? '';
  const [inner, setInner] = useState(controlledValue);
  const inputRef = useRef(null);

  // Sincroniza el valor interno cuando cambia desde el padre
  useEffect(() => {
    setInner(controlledValue);
  }, [controlledValue]);

  // Disparo de eventos con debounce
  useEffect(() => {
    // si no hay debounce, avisa inmediatamente
    if (!debounceMs) {
      (onChange || onCambiar)?.(inner);
      return;
    }
    const t = setTimeout(() => {
      onDebouncedChange?.(inner);
      (onChange || onCambiar)?.(inner); // opcional mantener ambos
    }, debounceMs);
    return () => clearTimeout(t);
  }, [inner, debounceMs]); // eslint-disable-line react-hooks/exhaustive-deps

  const sizeClass =
    size === 'sm' ? 'form-control form-control-sm' :
    size === 'lg' ? 'form-control form-control-lg' :
    'form-control';

  const handleChange = (e) => {
    const v = e.target.value;
    setInner(v);
    if (!debounceMs) (onChange || onCambiar)?.(v);
  };

  const handleClear = () => {
    setInner('');
    (onChange || onCambiar)?.('');
    onDebouncedChange?.('');
    onClear?.();
    inputRef.current?.focus();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      e.preventDefault();
      if (clearButton) handleClear();
    }
    if (e.key === 'Enter') {
      onSubmit?.(inner);
    }
  };

  return (
    <div className={`input-group mb-3 ${className}`}>
      <span className="input-group-text bg-primary text-white">
        <i className={`bi ${icon}`} aria-hidden="true"></i>
      </span>
      <input
        ref={inputRef}
        type="search"
        className={sizeClass}
        placeholder={placeholder}
        value={inner}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        autoFocus={autoFocus}
        name={name}
        id={id}
        aria-label={ariaLabel || placeholder}
      />
      {clearButton && inner && (
        <button
          className="btn btn-outline-secondary"
          type="button"
          onClick={handleClear}
          aria-label="Limpiar búsqueda"
          title="Limpiar"
        >
          <i className="bi bi-x-circle"></i>
        </button>
      )}
    </div>
  );
}