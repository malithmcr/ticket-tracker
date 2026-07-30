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
- [ ] Project setup and Docker
- [ ] Authentication
- [ ] Customer and Agent roles
- [ ] Ticket model and CRUD
- [ ] Customer ticket access and isolation
- [ ] Comments
- [ ] Agent ticket management
- [ ] Status and priority
- [ ] Assignment
- [ ] Search and filtering
- [ ] Pagination
- [ ] Dashboard
- [ ] Seed data
- [ ] Core tests

### Nice to have
- [ ] Live updates
- [ ] UI feedback
- [ ] Additional UI polish
- [ ] Tests

## Getting started

### TODO

Usefull commands
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py check