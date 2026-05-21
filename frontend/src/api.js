// Flask Server info
const BASE_URL = "http://localhost:5000";
const API_KEY  = "mindtech-dev-key-123";

const headers = {
  "Content-Type": "application/json",
  "X-API-Key": API_KEY,
};

// Helper — centralises error handling for every request
async function request(path, options = {}) {
    // make request to the flask server for API data.
    // Here Frontend talks with backend by using fetch. Using a simple get request and returning a promised data
  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    // response.ok is true for 200-299, false for 4xx/5xx
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `HTTP ${response.status}`);
  }
  
  // Data from backend returns as a json
  return response.json();
}

// API Routes
// --- Clients ---
export const getClients    = ()           => request("/clients");
export const getClient     = (id)         => request(`/clients/${id}`);
export const createClient  = (data)       => request("/clients", { method: "POST", body: JSON.stringify(data) });
export const updateClient  = (id, data)   => request(`/clients/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteClient  = (id)         => request(`/clients/${id}`, { method: "DELETE" });

// --- Jobs ---
export const getJobs = () => request("/jobs");