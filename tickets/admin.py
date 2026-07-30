from django.contrib import admin

from .models import Comment, Ticket


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "customer",
        "assigned_agent",
        "status",
        "priority",
        "created_at",
    )
    list_filter = ("status", "priority", "created_at")
    search_fields = ("title", "description", "customer__username")
    readonly_fields = ("created_at", "updated_at", "resolved_at")
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "author", "created_at")
    list_filter = ("created_at",)
    search_fields = ("body", "author__username", "ticket__title")
    readonly_fields = ("created_at",)
