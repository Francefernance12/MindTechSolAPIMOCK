import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import Clients from "./pages/Clients";
import Jobs    from "./pages/Jobs";

export default function App() {
  // Structure:
    // Navbar
    // Main contents(Home, Jobs)
  return (
    <BrowserRouter>
      <nav style={styles.nav}>
        <span style={styles.brand}>MindTech</span>
        <NavLink to="/"      style={navStyle} end>Clients</NavLink>
        <NavLink to="/jobs"  style={navStyle}>Jobs</NavLink>
      </nav>

      <main style={styles.main}>
        <Routes>
          <Route path="/"     element={<Clients />} />
          <Route path="/jobs" element={<Jobs />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

// CSS Styling
const navStyle = ({ isActive }) => ({
  marginLeft: 16,
  fontWeight: isActive ? 700 : 400,
  color: isActive ? "#1D9E75" : "inherit",
  textDecoration: "none",
});

const styles = {
  nav:   { display: "flex", alignItems: "center", padding: "12px 24px", borderBottom: "1px solid #e5e7eb" },
  brand: { fontWeight: 700, fontSize: 18, marginRight: 16 },
  main:  { padding: "24px" },
};