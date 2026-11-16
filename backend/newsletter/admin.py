from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
