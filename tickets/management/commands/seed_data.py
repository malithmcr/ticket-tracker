from datetime import timedelta
from random import choice, randint

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from tickets.models import Comment, Ticket

User = get_user_model()

DEFAULT_PASSWORD = "password123"
SEED_TITLE_PREFIX = "SEED:" #this marks seeded tickets so a second run can skip creating more

CUSTOMERS = [
    ("customer1", "customer1@example.com"),
    ("customer2", "customer2@example.com"),
    ("customer3", "customer3@example.com"),
]

AGENTS = [
    ("agent1", "agent1@example.com"),
    ("agent2", "agent2@example.com"),
]


class Command(BaseCommand):
    help = (
        "Create demo customers, agents, tickets, and comments. "
        "Safe to re-run: existing seeded users/tickets are left alone."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--tickets",
            type=int,
            default=40,
            help="Number of seed tickets to create when none exist (default: 40).",
        )

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(42)

        agents_group = self._ensure_agents_group()
        customers = [
            self._ensure_user(username, email)
            for username, email in CUSTOMERS
        ]
        agents = [
            self._ensure_user(username, email, agents_group=agents_group)
            for username, email in AGENTS
        ]

        existing_seed_tickets = Ticket.objects.filter(
            title__startswith=SEED_TITLE_PREFIX
        ).count()

        if existing_seed_tickets:
            self.stdout.write(
                self.style.WARNING(
                    f"Found {existing_seed_tickets} existing seed tickets; "
                    "skipping ticket/comment creation."
                )
            )
        else:
            created_tickets = self._create_tickets(
                fake=fake,
                customers=customers,
                agents=agents,
                count=options["tickets"],
            )
            self._create_comments(
                fake=fake,
                tickets=created_tickets,
                agents=agents,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created {len(created_tickets)} tickets with comments."
                )
            )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Seed data ready."))
        self.stdout.write(f"Password for all demo users: {DEFAULT_PASSWORD}")
        self.stdout.write(
            "Customers: " + ", ".join(username for username, _ in CUSTOMERS)
        )
        self.stdout.write(
            "Agents: " + ", ".join(username for username, _ in AGENTS)
        )

    def _ensure_agents_group(self) -> Group:
        permission = Permission.objects.get(
            content_type__app_label="tickets",
            codename="can_manage_tickets",
        )
        group, _ = Group.objects.get_or_create(name="Agents")
        group.permissions.add(permission)
        return group

    def _ensure_user(
        self,
        username: str,
        email: str,
        agents_group: Group | None = None,
    ) -> User:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
            },
        )
        if created:
            user.set_password(DEFAULT_PASSWORD)
            user.save()
            self.stdout.write(f"Created user: {username}")
        else:
            self.stdout.write(f"User already exists: {username}")

        if agents_group is not None:
            user.groups.add(agents_group)
            user.user_permissions.add(
                Permission.objects.get(
                    content_type__app_label="tickets",
                    codename="can_manage_tickets",
                )
            )

        return user

    def _create_tickets(self, fake, customers, agents, count: int) -> list[Ticket]:
        tickets: list[Ticket] = []
        now = timezone.now()

        for index in range(count):
            customer = customers[index % len(customers)]
            status = choice(list(Ticket.Status))
            priority = choice(list(Ticket.Priority))
            assigned_agent = choice(agents) if randint(0, 1) else None
            created_at = now - timedelta(days=randint(1, 45), hours=randint(0, 23))

            ticket = Ticket(
                customer=customer,
                assigned_agent=assigned_agent,
                title=f"{SEED_TITLE_PREFIX} {fake.sentence(nb_words=6).rstrip('.')}",
                description=fake.paragraph(nb_sentences=3),
                status=status,
                priority=priority,
            )
            ticket.save()

            # auto_now_add / auto_now ignore manual values on create, so update timestamps
            update_fields = {
                "created_at": created_at,
                "updated_at": created_at + timedelta(hours=randint(1, 48)),
            }
            if status in (Ticket.Status.RESOLVED, Ticket.Status.CLOSED):
                update_fields["resolved_at"] = created_at + timedelta(
                    days=randint(1, 7),
                    hours=randint(1, 12),
                )
            Ticket.objects.filter(pk=ticket.pk).update(**update_fields)
            ticket.refresh_from_db()
            tickets.append(ticket)

        return tickets

    def _create_comments(self, fake, tickets, agents) -> None:
        for ticket in tickets:
            authors = [ticket.customer, *agents]
            for _ in range(randint(1, 3)):
                Comment.objects.create(
                    ticket=ticket,
                    author=choice(authors),
                    body=fake.paragraph(nb_sentences=2),
                )
