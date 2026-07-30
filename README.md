## Architecture
![preview](./docs/preview.png)

## Goals
Given the time constraint, I will prioritise:

1. Correctness and security
2. A complete core user experience
3. Maintainable architecture
4. Performance for the expected scale
5. UX improvements and bonus features


## Stack
- Django
- PostgreSQL 
- uv - package manager (why: faster than pip and it replaces multiple other tools)
- HTMX - Server-rendered UI enhancements and dynamic interactions, keeping the application simple and avoiding unnecessary SPA complexity
- TailwindCSS - CSS framework
- DaisyUI - Tailwind component library to speed up UI development
- Ruff - Python linter
- pytest - testing framework
- Docker and Docker compose
- Gunicorn
- Faker - Seeding

## Implementation plan
### Must have
- [x] Project setup and Docker
- [x] Authentication
- [x] Customer and Agent roles
- [x] Ticket model and CRUD
- [x] Customer ticket access and isolation
- [x] Comments
- [x] Agent ticket management
- [x] Status and priority
- [x] Assignment
- [x] Search and filtering
- [x] Pagination
- [x] Dashboard
- [x] Seed data

### Nice to have
- [x] Live updates
- [x] UI feedback
- [x] Additional UI polish
- [x] Tests

## Live demo

Deployed on Railway: [Open the app](https://ticket-tracker-production-241c.up.railway.app/) · [Login](https://ticket-tracker-production-241c.up.railway.app/accounts/login/)

Demo logins (same as local seed data): `customer1` or `agent1` / `password123` — full list in the table under **Useful commands**.

## Getting started

### 1. Clone and configure

```bash
cp .env.example .env
```

Edit `.env` if you want different Postgres credentials. Defaults work with Docker Compose. `SECRET_KEY` and `DEBUG` come from `.env` (not production-ready as-is).

On Railway, set `SECRET_KEY`, `DEBUG=False`, and either `DATABASE_URL` (Railway Postgres) or the `POSTGRES_*` vars. Do not set `PORT` (Railway provides it). `ALLOWED_HOSTS` / CSRF pick up `RAILWAY_PUBLIC_DOMAIN` automatically.

### 2. Start the app

```bash
docker compose up --build
```

App: http://localhost:8000  
Login: http://localhost:8000/accounts/login/

Migrations run automatically on container start.

| Role | Usernames | Password |
|------|-----------|----------|
| Customer | `customer1`, `customer2`, `customer3` | `password123` |
| Agent | `agent1`, `agent2` | `password123` |

### Useful commands

```bash
# Run tests
docker compose exec web sh -c "uv sync --frozen --group dev && python -m pytest"

# Lint
docker compose exec web python -m ruff check tickets config

# Migration
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py check

# Seed data
docker compose exec web python manage.py seed_data

# Django shell
docker compose exec web python manage.py shell

# Create a superuser (optional)
docker compose exec web python manage.py createsuperuser

# Stop
docker compose down
```

`seed_data` is safe to re-run because existing seed tickets are skipped.

| Role | Usernames | Password |
|------|-----------|----------|
| Customer | `customer1`, `customer2`, `customer3` | `password123` |
| Agent | `agent1`, `agent2` | `password123` |

After changing Python view code, restart the web container so Gunicorn reloads:

```bash
docker compose restart web
```

### AI Usage
Boilerplate: Dockerfile, compose, pytest conftest, login template scaffolding
HTMX is somehow new to me so had to look it up. I would do this with react if I had time but because of the time restriction I have used HTMX but I got suck a few times and had to use AI and stackoverflow to debug and understand what am I doing wrong. Fixing some grammar on README

# If I had 3 more hours, I'd add

- Form / UX feedback — Surface validation errors and success messages when comments fail or ticket updates succeed (today invalid POSTs mostly just redirect).
- Real live updates
- UI polish
- Add mroe tests to fix gaps
- Email (or in-app) notifications
- Customer list pagination
- Extract shared ticket-query helpers



