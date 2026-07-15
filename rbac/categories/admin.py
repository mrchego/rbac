from django.contrib import admin
from rbac.core.admin import BaseModelAdmin
from rbac.categories.models import Category


@admin.register(Category)
class CategoryAdmin(BaseModelAdmin):
    list_display = ["name", "parent", "company", "created_at"]
    list_filter = ["company"]
    search_fields = ["name"]