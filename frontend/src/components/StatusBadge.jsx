const colors = {
    success:  { bg: "#dcfce7", text: "#16a34a" },
    failed:   { bg: "#fee2e2", text: "#dc2626" },
    print:    { bg: "#eff6ff", text: "#2563eb" },
    voip:     { bg: "#faf5ff", text: "#7c3aed" },
    docuware: { bg: "#fff7ed", text: "#ea580c" },
    it:       { bg: "#f0fdf4", text: "#15803d" },
  };
  
  export default function StatusBadge({ status }) {
    const scheme = colors[status] || { bg: "#f3f4f6", text: "#374151" };
    return (
      <span style={{
        background: scheme.bg,
        color: scheme.text,
        padding: "2px 10px",
        borderRadius: 99,
        fontSize: 12,
        fontWeight: 600,
      }}>
        {status}
      </span>
    );
  }