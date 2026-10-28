from taxi.models import AuditLog
from django.utils import timezone
import json

def log_action(user, action, object_type=None, object_id=None, description=None, extra_data=None, ip_address=None):
    AuditLog.objects.create(
        user=user,
        action=action,
        object_type=object_type,
        object_id=object_id,
        description=description,
        extra_data=json.dumps(extra_data) if extra_data else None,
        ip_address=ip_address,
    )


def get_order_urgency(order):
    if order.status not in ("Новый", "Назначен водитель"):
        return None

    minutes = (timezone.now() - order.created_at).total_seconds() / 60

    if minutes < 5:
        return "green"
    elif minutes < 15:
        return "yellow"
    else:
        return "red"