export default function InsigniaEstado({ estado }) {
  const ok = String(estado || "").toUpperCase() === "VIGENTE";
  const clase = ok ? "bg-success" : "bg-secondary";
  return <span className={`badge ${clase}`}>{estado || "SIN CONVENIO"}</span>;
}