from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from rbac.accounts.models import User
from rbac.staff.models import Invitation


def get_user_stats(*, company_id: str):
    qs = User.objects.filter(company_id=company_id)
    total = qs.count()
    active = qs.filter(is_active=True).count()
    locked = sum(1 for u in qs.filter(locked_until__isnull=False) if u.is_locked)
    pending_invitations = Invitation.objects.filter(
        company_id=company_id, used=False
    ).count()

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
        "locked": locked,
        "pending_invitations": pending_invitations,
        "signups_last_30_days": [
            {"date": d["day"].isoformat(), "value": d["count"]} for d in daily
        ],
    }