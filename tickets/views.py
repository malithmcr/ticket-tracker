from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from .models import Ticket

@login_required
def home(request):
    if request.user.groups.filter(name="Agents").exists():
        return redirect("tickets:agent_dashboard")

    return redirect("tickets:customer_tickets")

@login_required
def customer_tickets(request):
    tickets = (
        Ticket.objects
        .filter(customer=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "tickets/customer/ticket_list.html",
        {"tickets": tickets},
    )


@login_required
@permission_required(
    "tickets.can_manage_tickets",
    raise_exception=True,
)
def agent_dashboard(request):
    total_tickets = Ticket.objects.count()


    return render(
        request,
        "tickets/agent/agent_dashboard.html",
        {
            "total_tickets": total_tickets,
        },
    )

