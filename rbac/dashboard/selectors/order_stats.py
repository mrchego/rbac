# rbac/dashboard/selectors/order_stats.py
from datetime import timedelta
from decimal import Decimal
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from rbac.orders.models import Order


def get_order_stats(*, company_id: str):
    qs = Order.objects.filter(company_id=company_id).prefetch_related("line_items")
    total = qs.count()

    # `total` isn't a DB field (it's derived from line_items), so Sum("total")
    # can't work — sum the computed property in Python instead.
    revenue = sum((order.total for order in qs), Decimal("0"))

    since = timezone.now() - timedelta(days=30)
    recent_orders = list(
        qs.filter(created_at__gte=since).annotate(day=TruncDate("created_at"))
    )

    daily_counts: dict = {}
    daily_revenue: dict = {}
    for order in recent_orders:
        daily_counts[order.day] = daily_counts.get(order.day, 0) + 1
        daily_revenue[order.day] = daily_revenue.get(order.day, Decimal("0")) + order.total

    days = sorted(daily_counts.keys())

    return {
        "total": total,
        "total_revenue": float(revenue),
        "orders_last_30_days": [
            {"date": d.isoformat(), "value": daily_counts[d]} for d in days
        ],
        "revenue_last_30_days": [
            {"date": d.isoformat(), "value": float(daily_revenue[d])} for d in days
        ],
    }