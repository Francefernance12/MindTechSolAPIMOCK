import { useState, useEffect } from "react";
import { getClients, createClient, deleteClient } from "../api";
import ClientCard from "../components/ClientCard";

export default function Clients() {
  // Three states every data-fetching component needs
  const [clients, setClients] = useState([]);   // the data (ID/COMPANY_NAME/SERVICE_TYPE/CONTACT_EMAIL)
  const [loading, setLoading] = useState(true); // are we waiting?
  const [error,   setError]   = useState(null); // did something go wrong?

  // Form state
  const [form, setForm] = useState({ company_name: "", contact_email: "", service_type: "" });
  const [saving, setSaving] = useState(false);

  // useEffect runs after the component mounts — good place to fetch data.
  // The empty [] means "run once on mount, not on every re-render."
  useEffect(() => {
    fetchClients();
  }, []);

  async function fetchClients() {
    try {
      setLoading(true);
      setError(null);
      const data = await getClients();
      setClients(data);  // Stays in Clients hook. Use to render Client's data in components.
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false); // always runs — clears spinner whether success or fail
    }
  }

  async function handleCreate() {
    if (!form.company_name || !form.contact_email) return;
    try {
      setSaving(true);
      await createClient(form);
      setForm({ company_name: "", contact_email: "", service_type: "" }); // reset form
      await fetchClients(); // refresh list
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm("Delete this client?")) return;
    try {
      await deleteClient(id);
      await fetchClients();
    } catch (err) {
      setError(err.message);
    }
  }

  // Render states explicitly — never skip loading or error UI
  if (loading) return <p>Loading clients...</p>;
  if (error)   return <p style={{ color: "red" }}>Error: {error}</p>;

  return (
    <div>
      <h1>Clients</h1>

      {/* Add client form */}
      <div style={styles.form}>
        <input
          placeholder="Company name"
          value={form.company_name}
          onChange={e => setForm({ ...form, company_name: e.target.value })}
          style={styles.input}
        />
        <input
          placeholder="Contact email"
          value={form.contact_email}
          onChange={e => setForm({ ...form, contact_email: e.target.value })}
          style={styles.input}
        />
        <input
          placeholder="Service type"
          value={form.service_type}
          onChange={e => setForm({ ...form, service_type: e.target.value })}
          style={styles.input}
        />
        <button onClick={handleCreate} disabled={saving} style={styles.button}>
          {saving ? "Saving..." : "Add Client"}
        </button>
      </div>

      {/* Client list */}
      {clients.length === 0
        ? <p>No clients yet.</p>
        : clients.map(client => (
            <ClientCard
              key={client.client_id}
              client={client}
              onDelete={() => handleDelete(client.client_id)}
            />
          ))
      }
    </div>
  );
}

const styles = {
  form:   { display: "flex", gap: 8, marginBottom: 24, flexWrap: "wrap" },
  input:  { padding: "8px 12px", border: "1px solid #d1d5db", borderRadius: 6, fontSize: 14 },
  button: { padding: "8px 16px", background: "#1D9E75", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer" },
};