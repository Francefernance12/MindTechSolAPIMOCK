# Architectural & Technology Decisions

This document outlines the rationale behind the key technology choices and architectural patterns used in this project.

## 1. Backend: Flask (Python)
- **Decision**: Use Flask instead of Django or FastAPI.
- **Rationale**: 
    - **Simplicity**: Flask is a micro-framework that stays out of the way. For a mock API, we don't need the "batteries included" complexity of Django.
    - **Speed of Development**: We can set up modular routing with Blueprints in minutes.
    - **Familiarity**: Python is the industry standard for backend automation scripts, which this project simulates.

## 2. Frontend: React + Vite
- **Decision**: Use React (v19) with Vite.
- **Rationale**: 
    - **Modern Tooling**: Vite provides a significantly faster development experience (HMR) and smaller build bundles compared to older tools like Create React App.
    - **React Ecosystem**: React's component-based architecture makes it easy to build a clean, interactive UI like the Client dashboard.
    - **Hooks**: Using standard React hooks (`useState`, `useEffect`) allows for straightforward state management without the overhead of Redux.

## 3. Database: SQLite
- **Decision**: Use SQLite instead of PostgreSQL or MongoDB.
- **Rationale**: 
    - **Zero Setup**: SQLite is serverless and file-based. It requires no configuration, installation, or separate background process to run.
    - **Portability**: The entire database is a single file (`database.db`), making it perfect for a project that needs to be easily shared or containerized.
    - **Relational Integrity**: Even for a mock project, maintaining foreign key relationships between Clients and Jobs is important for data consistency.

## 4. API Security: Static API Key
- **Decision**: Use a shared `X-API-Key` header for authentication.
- **Rationale**: 
    - **Appropriate Security**: For a mock/internal tool, full OAuth2 or JWT implementation is overkill.
    - **Ease of Use**: It provides a basic layer of protection while remaining easy to use with simple `fetch` calls or tools like Postman.

## 5. Deployment: Docker (Showcase)
- **Decision**: Containerize with a production-optimized multi-stage build.
- **Rationale**: 
    - **"Works on My Machine"**: Docker ensures that the exact same environment (Python version, Node version, Nginx config) is used regardless of where the app is running.
    - **Simulated Production**: Using Nginx to serve the frontend and Gunicorn for the backend provides a more realistic performance profile for a showcase app than running development servers inside containers.
