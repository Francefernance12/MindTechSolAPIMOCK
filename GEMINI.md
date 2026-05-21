# MindTechSolAPIMOCK

This project is a full-stack application designed to mock an API for managing clients and jobs. It features a Python Flask backend and a React frontend built with Vite.

## Architecture Overview

- **Backend**: Python Flask application serving a RESTful API.
  - **Database**: SQLite (`backend/database.db`).
  - **Routing**: Organized into Blueprints in `backend/routes/`.
  - **Authentication**: API Key based. Endpoints are protected with a custom `@require_api_key` decorator.
  - **Rate Limiting**: Implemented via `flask-limiter`.
- **Frontend**: React (v19) application using Vite for development and building.
  - **Routing**: Client-side routing with `react-router-dom`.
  - **Components**: Located in `frontend/src/components/`.
  - **Pages**: Located in `frontend/src/pages/`.

## Project Structure

- `backend/`: Core backend logic.
  - `app.py`: Entry point for the Flask server.
  - `models.py`: Database schema and connection management.
  - `seed.py`: Script to populate the database with initial data and test transactions.
  - `routes/`: API endpoint definitions (clients, jobs, health).
- `frontend/`: React frontend application.
  - `src/api.js`: Centralized API interaction logic.
- `docs/`: Documentation, including `api.md` (API reference).
- `data/`: Sample data and logs.

## Building and Running

### Backend
1.  **Environment Setup**:
    ```bash
    cd backend
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install flask flask-cors flask-limiter
    ```
2.  **Initialize Database**:
    ```bash
    python models.py
    ```
3.  **Seed Data**:
    ```bash
    python seed.py
    ```
4.  **Run Server**:
    ```bash
    python app.py
    ```
    The server runs on `http://127.0.0.1:5000` by default.

### Frontend
1.  **Install Dependencies**:
    ```bash
    cd frontend
    npm install
    ```
2.  **Run Development Server**:
    ```bash
    npm run dev
    ```
3.  **Build for Production**:
    ```bash
    npm run build
    ```

## Development Conventions

- **API Authentication**: Most backend routes require an `X-API-KEY` header. The default development key is `mindtech-dev-key-123`.
- **Database**: Use `get_connection()` from `backend/models.py` to interact with the SQLite database. Ensure connections are closed after use.
- **Error Handling**: Follow the pattern in `routes/` for consistent JSON error responses and appropriate HTTP status codes.
- **Frontend State**: Managed locally within components or through React hooks.
- **Code Style**:
  - Python: Follow PEP 8 (inferred).
  - JavaScript/React: ESLint is configured in `frontend/eslint.config.js`.

## API Endpoints (Brief)

- `GET /health`: Check API status.
- `GET /clients`: Retrieve all clients.
- `POST /clients`: Create a new client.
- `GET /jobs`: Retrieve job logs.
- `POST /jobs`: Log a new job.

Refer to `docs/api.md` for detailed endpoint specifications.
