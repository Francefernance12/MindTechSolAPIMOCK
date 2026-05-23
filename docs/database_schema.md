# Database Schema

The project uses **SQLite** for data storage. The database file is located at `backend/database.db`.

## Tables

### 1. `clients`
Stores information about companies and their primary contact details.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `client_id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for each client. |
| `company_name` | TEXT | NOT NULL | The official name of the company. |
| `contact_email` | TEXT | UNIQUE | Primary contact email address. |
| `service_type` | TEXT | | Category of service (e.g., 'print', 'voip', 'it'). |
| `created_at` | TEXT | DEFAULT (datetime('now')) | Timestamp of when the record was created. |

### 2. `jobs`
Stores logs of automated scripts or tasks executed for specific clients.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `job_id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for each job log. |
| `client_id` | INTEGER | FOREIGN KEY (clients) | Reference to the client the job was run for. |
| `script_name` | TEXT | NOT NULL | The name of the script that was executed. |
| `status` | TEXT | NOT NULL, CHECK(status IN ('success', 'failed')) | Outcome of the job. |
| `ran_at` | TEXT | DEFAULT (datetime('now')) | Timestamp of when the job was executed. |
| `message` | TEXT | | Optional log message or error detail. |

## Relationships

- **One-to-Many**: One `client` can have many `jobs`.
- **Foreign Key**: `jobs.client_id` references `clients.client_id`.
- **Cascade Delete**: The schema is configured with `ON DELETE CASCADE`. If a client is deleted, all associated job logs in the `jobs` table are automatically removed to maintain data integrity.

## Initialization

The schema is defined and initialized in `backend/models.py`. Running this script will create the `database.db` file and the necessary tables if they do not already exist.
