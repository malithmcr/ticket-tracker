from django import forms
from django.contrib.auth import get_user_model

from .models import Comment, Ticket

User = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full border-slate-200 bg-white",
                    "placeholder": "Short summary of the issue",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full min-h-32 border-slate-200 bg-white",
                    "placeholder": "Describe the problem in detail",
                    "rows": 5,
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "body",
        ]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full border-slate-200 bg-white",
                    "placeholder": "Write a comment…",
                    "rows": 3,
                }
            ),
        }
        labels = {
            "body": "",
        }


class AgentTicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "status",
            "priority",
            "assigned_agent",
        ]
        widgets = {
            "status": forms.Select(
                attrs={"class": "select select-bordered w-full border-slate-200 bg-white"}
            ),
            "priority": forms.Select(
                attrs={"class": "select select-bordered w-full border-slate-200 bg-white"}
            ),
            "assigned_agent": forms.Select(
                attrs={"class": "select select-bordered w-full border-slate-200 bg-white"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_agent"].queryset = (
            User.objects
            .filter(groups__name="Agents", is_active=True)
            .order_by("username")
        )
        self.fields["assigned_agent"].required = False
        self.fields["assigned_agent"].empty_label = "Unassigned"
