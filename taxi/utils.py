from taxi.models import AuditLog
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