import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_customer_cannot_access_another_customers_ticket(
    client,
    customer,
    other_customer_ticket,
):
    client.login(username="test_customer", password="password123")

    response = client.get(
        reverse(
            "tickets:customer_ticket_detail",
            kwargs={"pk": other_customer_ticket.pk},
        )
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_customer_cannot_access_agent_pages(client, customer, customer_ticket):
    client.login(username="test_customer", password="password123")

    agent_urls = [
        reverse("tickets:agent_dashboard"),
        reverse("tickets:agent_tickets"),
        reverse(
            "tickets:agent_ticket_detail",
            kwargs={"pk": customer_ticket.pk},
        ),
    ]

    for url in agent_urls:
        response = client.get(url)
        assert response.status_code == 403
