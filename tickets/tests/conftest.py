import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from tickets.models import Ticket

User = get_user_model()
PASSWORD = "password123"


@pytest.fixture
def customer(db):
    return User.objects.create_user("test_customer", password=PASSWORD)


@pytest.fixture
def other_customer(db):
    return User.objects.create_user("other_customer", password=PASSWORD)


@pytest.fixture
def agent(db):
    user = User.objects.create_user("test_agent", password=PASSWORD)
    group, _ = Group.objects.get_or_create(name="Agents")
    perm = Permission.objects.get(codename="can_manage_tickets")
    group.permissions.add(perm)
    user.groups.add(group)
    user.user_permissions.add(perm)
    return user


@pytest.fixture
def customer_ticket(customer):
    return Ticket.objects.create(
        customer=customer,
        title="My ticket",
        description="Something broke",
    )


@pytest.fixture
def other_customer_ticket(other_customer):
    return Ticket.objects.create(
        customer=other_customer,
        title="Someone else ticket",
        description="Not yours",
    )