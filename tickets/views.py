from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import AgentTicketUpdateForm, TicketForm
from .models import Ticket

TICKETS_PER_PAGE = 20



def _format_avg_resolution(avg_delta):
    if avg_delta is None:
        return "—", "No resolved tickets yet"

    total_seconds = int(avg_delta.total_seconds())
    if total_seconds < 0:
        return "—", "No resolved tickets yet"

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes = remainder // 60

    if days:
        display = f"{days}d {hours}h"
    elif hours:
        display = f"{hours}h {minutes}m"
    else:
        display = f"{minutes}m"

    return display, "Across tickets with a resolution timestamp"



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
def customer_ticket_detail(request, pk):
    ticket = get_object_or_404(
        Ticket.objects.prefetch_related("comments__author"),
        pk=pk,
        customer=request.user,
    )

    return render(
        request,
        "tickets/customer/ticket_detail.html",
        {
            "ticket": ticket,
        },
    )


@login_required
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.customer = request.user
            ticket.save()

            return redirect(
                "tickets:customer_ticket_detail",
                pk=ticket.pk,
            )
    else:
        form = TicketForm()

    return render(
        request,
        "tickets/customer/ticket_form.html",
        {"form": form},
    )


@login_required
@permission_required(
    "tickets.can_manage_tickets",
    raise_exception=True,
)
def agent_dashboard(request):
    total_tickets = Ticket.objects.count()

    status_raw = {
        row["status"]: row["count"]
        for row in Ticket.objects.values("status").annotate(count=Count("id"))
    }
    status_counts = [
        {
            "label": label,
            "count": status_raw.get(value, 0),
        }
        for value, label in Ticket.Status.choices
    ]

    priority_raw = {
        row["priority"]: row["count"]
        for row in Ticket.objects.values("priority").annotate(count=Count("id"))
    }
    priority_counts = [
        {
            "label": label,
            "count": priority_raw.get(value, 0),
        }
        for value, label in Ticket.Priority.choices
    ]

    resolved_qs = Ticket.objects.filter(resolved_at__isnull=False)
    resolved_count = resolved_qs.count()
    avg_delta = resolved_qs.aggregate(
        avg=Avg(
            ExpressionWrapper(
                F("resolved_at") - F("created_at"),
                output_field=DurationField(),
            )
        )
    )["avg"]
    avg_resolution_display, avg_resolution_hint = _format_avg_resolution(avg_delta)

    return render(
        request,
        "tickets/agent/agent_dashboard.html",
        {
            "total_tickets": total_tickets,
            "status_counts": status_counts,
            "priority_counts": priority_counts,
            "resolved_count": resolved_count,
            "avg_resolution_display": avg_resolution_display,
            "avg_resolution_hint": avg_resolution_hint,
        },
    )


@login_required
@permission_required(
    "tickets.can_manage_tickets",
    raise_exception=True,
)
def agent_tickets(request):
    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()
    priority_filter = request.GET.get("priority", "").strip()

    tickets = (
        Ticket.objects
        .select_related("customer", "assigned_agent")
        .order_by("-created_at")
    )

    if search_query:
        tickets = tickets.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(customer__username__icontains=search_query)
        )

    if status_filter in Ticket.Status.values:
        tickets = tickets.filter(status=status_filter)
    else:
        status_filter = ""

    if priority_filter in Ticket.Priority.values:
        tickets = tickets.filter(priority=priority_filter)
    else:
        priority_filter = ""

    paginator = Paginator(tickets, TICKETS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    query_params = request.GET.copy()
    query_params.pop("page", None)
    query_string = query_params.urlencode()

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "status_choices": Ticket.Status.choices,
        "priority_choices": Ticket.Priority.choices,
        "query_string": query_string,
    }

    if request.htmx:
        return render(
            request,
            "tickets/partials/agent_ticket_list.html",
            context,
        )

    return render(
        request,
        "tickets/agent/ticket_list.html",
        context,
    )


@login_required
@permission_required(
    "tickets.can_manage_tickets",
    raise_exception=True,
)
def agent_ticket_detail(request, pk):
    ticket = get_object_or_404(
        Ticket.objects
        .select_related("customer", "assigned_agent")
        .prefetch_related("comments__author"),
        pk=pk,
    )

    return render(
        request,
        "tickets/agent/ticket_detail.html",
        {
            "ticket": ticket,
            "update_form": AgentTicketUpdateForm(instance=ticket),
        },
    )


@login_required
@permission_required(
    "tickets.can_manage_tickets",
    raise_exception=True,
)
@require_POST
def agent_update_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    form = AgentTicketUpdateForm(request.POST, instance=ticket)

    if form.is_valid():
        ticket = form.save(commit=False)
        if ticket.status in (Ticket.Status.RESOLVED, Ticket.Status.CLOSED):
            if ticket.resolved_at is None:
                ticket.resolved_at = timezone.now()
        else:
            ticket.resolved_at = None
        ticket.save()

    return redirect("tickets:agent_ticket_detail", pk=ticket.pk)

