from django.contrib import admin
from rbac.core.admin import BaseModelAdmin
from rbac.orders.models import Order, OrderLineItem


class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem
    extra = 0


@admin.register(Order)
class OrderAdmin(BaseModelAdmin):
    list_display = ["reference", "status", "company", "created_by", "created_at"]
    list_filter = ["status", "company"]
    search_fields = ["reference"]
    inlines = [OrderLineItemInline]