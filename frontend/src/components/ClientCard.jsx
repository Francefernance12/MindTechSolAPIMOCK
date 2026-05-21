import StatusBadge from "./StatusBadge";

export default function ClientCard({ client, onDelete }) {
  return (
    <div style={styles.card}>
      <div style={styles.row}>
        <strong>{client.company_name}</strong>
        <StatusBadge status={client.service_type} />
      </div>
      <p style={styles.email}>{client.contact_email}</p>
      <button onClick={onDelete} style={styles.delete}>Delete</button>
    </div>
  );
}

const styles = {
  card:   { border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, marginBottom: 12, maxWidth: 480 },
  row:    { display: "flex", justifyContent: "space-between", alignItems: "center" },
  email:  { color: "#6b7280", margin: "4px 0 12px", fontSize: 14 },
  delete: { padding: "4px 12px", background: "#fee2e2", color: "#dc2626", border: "none", borderRadius: 4, cursor: "pointer" },
};