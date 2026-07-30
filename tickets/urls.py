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
        "agent/",
        views.agent_dashboard,
        name="agent_dashboard",
    ),
]