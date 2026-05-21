import { useState, useEffect } from "react";
import { getJobs } from "../api";
import StatusBadge from "../components/StatusBadge";

export default function Jobs() {
  const [jobs,    setJobs]    = useState([]);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState(null);

  useEffect(() => {
    async function fetchJobs() {
      try {
        const data = await getJobs();
        setJobs(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchJobs();
  }, []);

  if (loading) return <p>Loading jobs...</p>;
  if (error)   return <p style={{ color: "red" }}>Error: {error}</p>;

  return (
    <div>
      <h1>Job Logs</h1>
      {jobs.length === 0 ? <p>No job logs yet.</p> : (
        <table style={styles.table}>
          <thead>
            <tr>
              {["ID", "Script", "Status", "Message", "Ran At"].map(h => (
                <th key={h} style={styles.th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {jobs.map(job => (
              <tr key={job.job_id}>
                <td style={styles.td}>{job.job_id}</td>
                <td style={styles.td}>{job.script_name}</td>
                <td style={styles.td}><StatusBadge status={job.status} /></td>
                <td style={styles.td}>{job.message}</td>
                <td style={styles.td}>{job.ran_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

const styles = {
  table: { width: "100%", borderCollapse: "collapse" },
  th:    { textAlign: "left", padding: "10px 12px", borderBottom: "2px solid #e5e7eb", fontSize: 13 },
  td:    { padding: "10px 12px", borderBottom: "1px solid #f3f4f6", fontSize: 14 },
};