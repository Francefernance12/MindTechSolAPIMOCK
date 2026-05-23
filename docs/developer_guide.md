# Developer Guide

Welcome to the MindTechSolAPIMOCK project! This guide is designed to help you get up to speed quickly and start contributing to the codebase.

## Getting Started

1.  **Clone the repo**: Make sure you have the code locally.
2.  **Setup the Backend**: Follow the instructions in the `GEMINI.md` or `README.md` to create a virtual environment, install dependencies, and initialize the database.
3.  **Setup the Frontend**: Use `npm install` in the `frontend` directory.
4.  **Run both**: You'll need two terminals open — one for the Flask server (`python app.py`) and one for the Vite dev server (`npm run dev`).

## Running with Docker

If you have Docker installed, you can skip the manual setup and run everything in containers. This is the fastest way to see the application in action exactly as it's intended to be showcased.

1.  **Build and Start**: Open a terminal in the project root and run:
    ```bash
    docker-compose up --build
    ```
2.  **What happens?**:
    - Docker builds a **Backend image** using the `backend/Dockerfile`, installs Python, sets up the database, and seeds it.
    - Docker builds a **Frontend image** using the `frontend/Dockerfile`, compiles the React app, and sets up an Nginx server to serve it.
    - `docker-compose` then links them together and starts both containers.
3.  **Access the App**:
    - **Frontend**: Go to `http://localhost:8080`.
    - **Backend API**: Accessible at `http://localhost:5000`.
4.  **Stop**: Press `Ctrl+C` in the terminal, or run `docker-compose down` to stop and remove the containers.

## Core Concepts to Understand

### 1. The Backend (Python/Flask)
- **Blueprints**: Instead of putting all routes in `app.py`, we use Blueprints. Look in `backend/routes/` to see how endpoints are grouped by resource (e.g., clients, jobs).
- **Authentication**: Most routes are protected by the `@require_api_key` decorator. If you're testing an endpoint in Postman or cURL, you **must** include the `X-API-Key` header.
- **Database**: We use raw SQL with the `sqlite3` library. Always use `get_connection()` from `models.py` and remember to close the connection when you're done.

### 2. The Frontend (React)
- **Hooks**: We use `useState` for data and `useEffect` for triggering API calls when a component loads.
- **Components vs. Pages**: `pages/` are the main screens reached via a URL. `components/` are smaller, reusable UI pieces (like `ClientCard`).
- **Props**: Data is passed down from pages to components via props.

## Coding Standards

- **Consistency**: Follow the existing style. Look at how variables are named and how functions are structured.
- **Error Handling**: 
    - **Backend**: Always return a JSON object with an `error` key and an appropriate HTTP status code (400, 404, 500, etc.).
    - **Frontend**: Always handle loading and error states in your components. Never leave the user wondering if the page is broken.
- **Comments**: Write clear, concise comments for complex logic. You don't need to comment obvious code, but explain the *why* behind non-trivial decisions.

## Where to start?

If you want to make a change:
1.  **Adding a field**: 
    - Update `models.py` (database schema).
    - Update the corresponding route in `routes/` (backend logic).
    - Update the frontend component (UI).
2.  **Fixing a bug**:
    - Try to reproduce it first.
    - Check the `logs/` or terminal output for error messages.
    - Use `print()` in Python or `console.log()` in React to trace data.

## Useful Commands

- **Backend**: `python seed.py` (Reset/populate your local data).
- **Frontend**: `npm run lint` (Check for code style issues).

## Resetting the Database

If you need to completely wipe the database and start fresh (useful for debugging schema changes or clearing test data):

1.  **Delete the database file**: Remove `backend/database.db`.
2.  **Recreate the schema**: Run `python models.py` from the `backend` directory.
3.  **Repopulate data**: Run `python seed.py` to add the initial sample clients and logs.

**Note**: In the Docker environment, the database is recreated every time the container is built unless you uncomment the volume mapping in `docker-compose.yml`.

Happy coding!
