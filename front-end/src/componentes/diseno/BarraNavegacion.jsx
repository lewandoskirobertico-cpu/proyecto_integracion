import { Link } from "react-router-dom";

export default function BarraNavegacion() {
  return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary border-bottom">
      <div className="container">
        <Link className="navbar-brand" to="/">Sistema PIE</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navPrincipal">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div id="navPrincipal" className="collapse navbar-collapse">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item"><Link className="nav-link" to="/sostenedor">Datos Institucional </Link></li>
          </ul>
        </div>
      </div>
    </nav>
  );
}