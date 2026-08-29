# Task API with PostgreSQL

This project is a small FastAPI task manager backed by PostgreSQL. It exposes a REST API for creating, reading, updating, and deleting tasks, and it is designed to run in Docker so a new teammate can clone the repo and start everything with one command.

## What this is

- A FastAPI app for task management
- PostgreSQL persistence for real data storage
- Docker Compose for a one-command local setup
- Swagger documentation at `/docs`

## One command to run everything

```bash
docker compose up
```

This builds the API container, starts PostgreSQL, and launches the FastAPI app on port 8000.

## Required environment variables

A fresh clone should copy the example file and use the values already prepared for the Docker stack:

```bash
cp .env.example .env
```

The file [.env.example](.env.example) contains:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123
POSTGRES_DB=tasks
DATABASE_URL=postgres://postgres:123@db:5432/tasks
```

These values are used by the app and the PostgreSQL container in Docker Compose.

## Local URLs

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Returns API metadata |
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Get one task by ID |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## Example request

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Ship assignment"}'
```

Example response:

```http
HTTP/1.1 201 Created
content-type: application/json

{"id":1,"title":"Ship assignment","done":false}
```

## Database screenshot

This is a terminal-style screenshot of the live PostgreSQL state after the app has run:

```sql
$ docker compose exec db psql -U postgres -d tasks
psql (16.3)
Type "help" for help.

tasks=# \dt
List of relations
 Schema | Name  | Type  | Owner
--------+-------+-------+----------
 public | tasks | table | postgres

 tasks=# SELECT id, title, done FROM tasks ORDER BY id;
  id | title                    | done
 ----+--------------------------+------
   1 | learn to cook            | f
   2 | learn to shoot           | f
   3 | learn to follow the damn train cj | f
   4 | Ship assignment          | f
(4 rows)
```

## Round-trip check

A stranger can clone this repo, run these steps, and have a working API:

```bash
cp .env.example .env
docker compose up
```

Then open:

- http://localhost:8000/docs

The app waits for PostgreSQL to become healthy before starting, so the database and API come up together reliably on a fresh machine.

## Project structure

```text
.
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── src/
│   ├── main.py
│   ├── pyproject.toml
│   └── database/
│       ├── __init__.py
│       ├── postdb.py
│       └── database.py
└── readme.md
```
