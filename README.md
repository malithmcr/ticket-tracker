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
- [ ] Seed data

### Nice to have
- [x] Live updates
- [x] UI feedback
- [x] Additional UI polish
- [x] Tests

## Getting started

### 1. Clone and configure

```bash
cp .env.example .env
```

Edit `.env` if you want different Postgres credentials. Defaults work with Docker Compose.

### 2. Start the app

```bash
docker compose up --build
```

App: http://localhost:8000  
Login: http://localhost:8000/accounts/login/

Migrations run automatically on container start.


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

# Django shell
docker compose exec web python manage.py shell

# Create a superuser (optional)
docker compose exec web python manage.py createsuperuser

# Stop
docker compose down
```

After changing Python view code, restart the web container so Gunicorn reloads:

```bash
docker compose restart web
```