# System Architecture

This document describes the high-level design and interaction between the components of the MindTechSolAPIMOCK application.

## High-Level Overview

The application follows a standard **Client-Server** architecture:

1.  **Frontend (Client)**: A React Single Page Application (SPA) that provides a user interface for managing clients and viewing job logs.
2.  **Backend (Server)**: A Python Flask REST API that handles business logic, authentication, and data persistence.
3.  **Database (Storage)**: An SQLite database that stores persistent application data.

## Component Breakdown

### 1. Frontend (React + Vite)
- **Framework**: React 19.
- **Build Tool**: Vite for fast development and optimized production builds.
- **Routing**: `react-router-dom` for client-side navigation between pages.
- **API Interaction**: A centralized `api.js` helper uses the `fetch` API to communicate with the backend.
- **Styling**: Vanilla CSS for simplicity and performance.

### 2. Backend (Flask)
- **Framework**: Flask.
- **Routing**: Organized into **Blueprints** (`routes/clients.py`, `routes/jobs.py`, etc.) for modularity.
- **Authentication**: Custom `@require_api_key` decorator validates an `X-API-Key` header on protected routes.
- **Rate Limiting**: `flask-limiter` protects endpoints from excessive requests.
- **CORS**: `flask-cors` allows the frontend SPA to make cross-origin requests during development.

### 3. Database (SQLite)
- **Engine**: SQLite (serverless, file-based).
- **Interface**: Standard `sqlite3` Python library.
- **Connection Management**: A central `get_connection()` function in `models.py` ensures consistent configuration (e.g., enabling foreign keys).

## Data Flow

1.  **Request**: The User interacts with the React UI (e.g., clicks "Add Client").
2.  **API Call**: React triggers an async call in `api.js`, which sends an HTTP request to the Flask backend.
3.  **Logic & DB**: Flask receives the request, validates the API key, performs business logic, and executes SQL queries against SQLite.
4.  **Response**: Flask returns a JSON response (e.g., `201 Created`).
5.  **State Update**: React receives the JSON, updates its internal state, and automatically re-renders the UI to reflect the change.

## Security
- **API Key**: A static secret key is shared between the frontend and backend.
- **Input Validation**: The backend validates required fields and data types before committing to the database.
- **SQL Injection**: Queries use parameterized inputs (e.g., `?` placeholders) to prevent SQL injection attacks.
