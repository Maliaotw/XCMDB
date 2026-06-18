"""審計相關任務 - OperationLog 寫入"""

from datetime import datetime, timedelta

from celery import shared_task

from .base import BaseTask, get_task_logger

logger = get_task_logger("audit")


@shared_task(name="tasks.audit.write_operation_log", base=BaseTask)
def write_operation_log(
    actor_id,
    action,
    resource_type,
    resource_id,
    resource_name="",
    old_values=None,
    new_values=None,
    reason="",
    ip="",
    user_agent="",
):
    """寫入操作審計日誌 (异步)"""
    from common.models import OperationLog

    OperationLog.objects.create(
        actor_id=actor_id,
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id),
        resource_name=resource_name,
        old_values=old_values or {},
        new_values=new_values or {},
        reason=reason,
        ip=ip,
        user_agent=user_agent,
    )

    return {"status": 200, "data": f"操作日誌已記錄: {action} {resource_type}#{resource_id}"}


@shared_task(name="tasks.audit.write_login_log_async", base=BaseTask)
def write_login_log_async(**kwargs):
    """异步寫入登入日誌"""
    from authentication.utils import write_login_log

    write_login_log(**kwargs)
    return {"status": 200}


@shared_task(name="tasks.cleanup.archive_old_audit_logs", base=BaseTask)
def archive_old_audit_logs(days=365):
    """歸檔/清理舊審計日誌"""
    from common.models import OperationLog

    cutoff = datetime.now() - timedelta(days=days)
    old_logs = OperationLog.objects.filter(created_at__lt=cutoff)
    count = old_logs.count()
    old_logs.delete()
    logger.info(f"已清理 {count} 筆超過 {days} 天的操作日誌")
    return {"status": 200, "data": f"清理 {count} 筆舊日誌"}
