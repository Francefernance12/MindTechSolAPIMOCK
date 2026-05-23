# File Structure & Request Flow

This document provides a detailed breakdown of the project's directory structure and describes the path a request takes through the system.

## Directory Structure

```text
.
├── backend/                # Flask Backend
│   ├── routes/             # API Blueprints (clients, jobs, health)
│   ├── scripts/            # Utility and maintenance scripts
│   ├── app.py              # Entry point for the server
│   ├── auth.py             # Authentication decorators
│   ├── config.py           # Configuration (API keys, etc.)
│   ├── models.py           # Database schema and connection logic
│   └── database.db         # SQLite database file (generated)
├── frontend/               # React Frontend
│   ├── public/             # Static assets (favicons, etc.)
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Main application screens
│   │   ├── api.js          # Centralized API logic
│   │   └── main.jsx        # Application entry point
│   ├── vite.config.js      # Build configuration
│   └── package.json        # Dependencies and scripts
├── docs/                   # Project documentation
└── data/                   # Sample data and reference files
```

## Request Flow: A Detailed Example

Let's trace what happens when a user views the **Clients** list.

### 1. The Interaction (Frontend)
The user navigates to the `/clients` route in the browser. React Router loads the `Clients.jsx` page component.

### 2. The Trigger (Frontend State)
`Clients.jsx` has a `useEffect` hook that runs when the component mounts. It calls `fetchClients()`.

### 3. The API Call (Frontend Data Layer)
`fetchClients()` calls `getClients()` from `api.js`. This function uses `fetch` to send a `GET` request to `http://localhost:5000/clients` with the `X-API-Key` header.

### 4. Routing (Backend Entry)
The Flask server (`app.py`) receives the request. It looks at the path (`/clients`) and matches it to the `clients_bp` Blueprint.

### 5. Middleware (Backend Security)
The request hits the `@require_api_key` decorator in `auth.py`. If the key is missing or invalid, it returns a `401` or `403` immediately.

### 6. Controller (Backend Logic)
The `get_clients()` function in `routes/clients.py` is executed.
- It calls `get_connection()` from `models.py`.
- It executes the SQL: `SELECT * FROM clients`.
- It transforms the result into a list of dictionaries.

### 7. The Response (Data Serialization)
Flask's `jsonify` turns the list of dictionaries into a JSON string and sends it back to the frontend with a `200 OK` status.

### 8. State Update (Frontend Resolution)
Back in `Clients.jsx`, the promise from `api.js` resolves. The data is passed to `setClients(data)`, which updates the React state.

### 9. Rendering (User Interface)
React detects the state change and re-renders the component. It maps through the `clients` array, creating a `ClientCard` for each record, which the user then sees on the screen.
