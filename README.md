# MindTech Internal Platform

Internal tool for managing clients, running automated data sync, and logging job history. This project is a full-stack application designed to mock an API for managing clients and jobs, featuring a Python Flask backend and a React frontend built with Vite.

## Project Overview

MindTech Internal Platform provides a centralized interface for managing client data and tracking automated jobs. It is built with a focus on ease of deployment and developer productivity, utilizing a SQLite database for simplicity and a robust RESTful API.

## Stack
- **Frontend**: React (v19) + Vite
- **Backend**: Flask + Python
- **Database**: SQLite
- **Scheduler**: APScheduler for background tasks

## Documentation Catalog

Detailed documentation for various aspects of the system can be found in the `docs/` directory:

- [API Reference](docs/api.md): Detailed endpoint specifications and authentication details.
- [Architecture Overview](docs/architecture.md): High-level system design and component interactions.
- [Data Flow](docs/data_flow.md): Description of how data moves through the system.
- [Database Schema](docs/database_schema.md): Detailed layout of the SQLite database tables.
- [Architectural Decisions](docs/decisions.md): Log of key technical decisions made during development.
- [Developer Guide](docs/developer_guide.md): Information for developers on setting up and contributing to the project.
- [Structure and Flow](docs/structure_and_flow.md): In-depth look at the codebase organization and logical flow.
- [Structured Code Review](docs/structured_code_review.md): Results and notes from architectural code reviews.

## Setup

### Backend
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment: `cp .env.example .env` (fill in your `API_KEY`)
4. Initialize the database: `python models.py`
5. Seed sample data: `python seed.py`
6. Start the API and scheduler: `python app.py`

The backend server runs on `http://127.0.0.1:5000` by default.

### Frontend
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

The frontend application is accessible at `http://localhost:5173`.

## Environment Variables
- `API_KEY`: Required. Protects all client/job endpoints. Default dev key: `mindtech-dev-key-123`.
- `RATE_LIMIT`: Optional. Default "30 per minute".
