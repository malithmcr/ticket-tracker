from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "tickets/",
        views.customer_tickets,
        name="customer_tickets",
    ),

    path(
        "tickets/create/",
        views.ticket_create,
        name="ticket_create",
    ),

    path(
        "tickets/<int:pk>/",
        views.customer_ticket_detail,
        name="customer_ticket_detail",
    ),

    path(
        "tickets/<int:pk>/comment/",
        views.add_comment,
        name="add_comment",
    ),

    path(
        "agent/",
        views.agent_dashboard,
        name="agent_dashboard",
    ),
    path(
        "agent/tickets/",
        views.agent_tickets,
        name="agent_tickets",
    ),
    path(
        "agent/tickets/<int:pk>/",
        views.agent_ticket_detail,
        name="agent_ticket_detail",
    ),
    path(
        "agent/tickets/<int:pk>/update/",
        views.agent_update_ticket,
        name="agent_update_ticket",
    ),
    path(
        "agent/tickets/<int:pk>/comment/",
        views.agent_add_comment,
        name="agent_add_comment",
    ),
]