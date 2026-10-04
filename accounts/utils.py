from .models import ActivityLog


def log_action(actor, action, target_type, target_id=""):
    ActivityLog.objects.create(
        actor=actor,
        action=action,
        target_type=target_type,
        target_id=str(target_id),
    )