import pytest
from django.urls import reverse

from tickets.models import Comment, Ticket


@pytest.mark.django_db
def test_agent_can_access_all_tickets(
    client,
    agent,
    customer_ticket,
    other_customer_ticket,
):
    client.login(username="test_agent", password="password123")

    list_response = client.get(reverse("tickets:agent_tickets"))
    assert list_response.status_code == 200
    content = list_response.content.decode()
    assert customer_ticket.title in content
    assert other_customer_ticket.title in content

    detail_response = client.get(
        reverse(
            "tickets:agent_ticket_detail",
            kwargs={"pk": other_customer_ticket.pk},
        )
    )
    assert detail_response.status_code == 200


@pytest.mark.django_db
def test_customer_can_create_ticket(client, customer):
    client.login(username="test_customer", password="password123")

    response = client.post(
        reverse("tickets:ticket_create"),
        {
            "title": "Cannot log in",
            "description": "Login form returns an error",
        },
    )

    ticket = Ticket.objects.get(title="Cannot log in")
    assert ticket.customer == customer
    assert response.status_code == 302
    assert response["Location"] == reverse(
        "tickets:customer_ticket_detail",
        kwargs={"pk": ticket.pk},
    )


@pytest.mark.django_db
def test_customer_can_comment_on_own_ticket(client, customer, customer_ticket):
    client.login(username="test_customer", password="password123")

    response = client.post(
        reverse("tickets:add_comment", kwargs={"pk": customer_ticket.pk}),
        {"body": "Any update on this?"},
    )

    assert response.status_code == 302
    assert Comment.objects.filter(
        ticket=customer_ticket,
        author=customer,
        body="Any update on this?",
    ).exists()


@pytest.mark.django_db
def test_customer_cannot_comment_on_another_customers_ticket(
    client,
    customer,
    other_customer_ticket,
):
    client.login(username="test_customer", password="password123")

    response = client.post(
        reverse(
            "tickets:add_comment",
            kwargs={"pk": other_customer_ticket.pk},
        ),
        {"body": "Should not work"},
    )

    assert response.status_code == 404
    assert not Comment.objects.filter(body="Should not work").exists()


@pytest.mark.django_db
def test_agent_can_change_ticket_status(client, agent, customer_ticket):
    client.login(username="test_agent", password="password123")

    response = client.post(
        reverse(
            "tickets:agent_update_ticket",
            kwargs={"pk": customer_ticket.pk},
        ),
        {
            "status": Ticket.Status.RESOLVED,
            "priority": Ticket.Priority.MEDIUM,
            "assigned_agent": "",
        },
    )

    customer_ticket.refresh_from_db()
    assert response.status_code == 302
    assert customer_ticket.status == Ticket.Status.RESOLVED
    assert customer_ticket.resolved_at is not None


@pytest.mark.django_db
def test_agent_can_assign_ticket(client, agent, customer_ticket):
    client.login(username="test_agent", password="password123")

    response = client.post(
        reverse(
            "tickets:agent_update_ticket",
            kwargs={"pk": customer_ticket.pk},
        ),
        {
            "status": Ticket.Status.IN_PROGRESS,
            "priority": Ticket.Priority.HIGH,
            "assigned_agent": agent.pk,
        },
    )

    customer_ticket.refresh_from_db()
    assert response.status_code == 302
    assert customer_ticket.assigned_agent == agent
    assert customer_ticket.status == Ticket.Status.IN_PROGRESS
    assert customer_ticket.priority == Ticket.Priority.HIGH
