from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from rbac.products.models import Product


def get_product_stats(*, company_id: str):
    qs = Product.objects.filter(company_id=company_id)
    total = qs.count()
    active = qs.filter(is_active=True).count()
    since = timezone.now() - timedelta(days=30)

    daily = (
        qs.filter(created_at__gte=since)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    return {
        "total": total,
        "active": active,
        "inactive": total - active,
        "created_last_30_days": [
            {"date": d["day"].isoformat(), "value": d["count"]} for d in daily
        ],
    }