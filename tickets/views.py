from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    if request.user.groups.filter(name="Agents").exists():
        return redirect("tickets:agent_dashboard")

    return redirect("tickets:customer_tickets")