# MindTech Internal API

Base URL: http://localhost:5000
Authentication: All client and job endpoints require an `X-API-Key` header.

---

## Authentication

Include this header on every request to /clients and /jobs:
X-API-Key: your-api-key

Missing key → 401. Wrong key → 403.

---

## Health

### GET /health/live
Checks if the API is running. No auth required.
Response 200: { "status": "alive" }

### GET /health/ready
Checks if the API can handle requests (DB connected). No auth required.
Response 200: { "status": "ready", "db": "connected" }
Response 500: { "status": "not ready", "db": "<error>" }

---

## Clients

### GET /clients
Returns all clients.
Response 200: [ { "client_id": 1, "company_name": "...", "contact_email": "...", "service_type": "...", "created_at": "..." } ]

### GET /clients/:id
Returns one client by ID.
Response 200: { client object }
Response 404: { "error": "Client not found" }

### POST /clients
Creates a new client.
Required fields: company_name, contact_email
Optional fields: service_type

Body:
{
  "company_name": "Acme Corp",
  "contact_email": "info@acme.com",
  "service_type": "print"
}

Response 201: { "message": "Client created", "client_id": 7 }
Response 400: { "error": "company_name and contact_email are required" }

### PUT /clients/:id
Updates an existing client. Only send the fields you want to change.

Body (partial update is fine):
{ "service_type": "voip" }

Response 200: { "message": "Client updated" }
Response 404: { "error": "Client not found" }

### DELETE /clients/:id
Deletes a client and all their job logs (cascade).
Response 200: { "message": "Client deleted" }
Response 404: { "error": "Client not found" }

---

## Jobs

### GET /jobs
Returns all job run logs, newest first.
Response 200: [ { "job_id": 1, "client_id": null, "script_name": "sync_clients.py", "status": "success", "message": "...", "ran_at": "..." } ]

---

## Status Codes

| Code | Meaning                          |
|------|----------------------------------|
| 200  | OK                               |
| 201  | Created                          |
| 400  | Bad request — missing/invalid data |
| 401  | Missing API key                  |
| 403  | Invalid API key                  |
| 404  | Resource not found               |
| 429  | Too many requests                |
| 500  | Server error                     |