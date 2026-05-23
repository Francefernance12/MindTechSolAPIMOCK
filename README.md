# MindTech Internal Platform

Internal tool for managing clients, running automated data sync, and logging job history.

## Stack
- Frontend: React + Vite (port 5173)
- Backend: Flask + Python (port 5000)
- Database: SQLite
- Scheduler: APScheduler

## Setup

### Backend
cd backend
pip install -r requirements.txt
cp .env.example .env        # fill in your API_KEY
python models.py            # create tables
python seed.py              # seed sample data
python app.py               # start API + scheduler

### Frontend
cd frontend
npm install
npm run dev

## API Docs
See docs/api.md

## Environment Variables
API_KEY     — required, protects all client/job endpoints
RATE_LIMIT  — optional, default "30 per minute"