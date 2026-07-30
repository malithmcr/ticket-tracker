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
- [ ] Tests

## Getting started

### TODO

Usefull commands
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py check