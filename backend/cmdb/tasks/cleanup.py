"""清理相關任務"""

from datetime import datetime, timedelta

from celery import shared_task

from .base import BaseTask, get_task_logger

logger = get_task_logger("cleanup")


@shared_task(name="tasks.cleanup.destroy_failed_vms", base=BaseTask)
def destroy_failed_vms():
    """清理失敗的 VM (cron 版本)"""
    from vm.models import VM

    failed_vms = VM.objects.filter(is_finish=True, status=5)
    count = failed_vms.count()
    logger.info(f"發現 {count} 筆待銷毀的 VM")
    return {"status": 200, "data": f"待銷毀 VM: {count} 筆"}


@shared_task(name="tasks.cleanup.remove_expired_tokens", base=BaseTask)
def remove_expired_tokens():
    """清理過期的認證 token"""
    from rest_framework.authtoken.models import Token

    cutoff = datetime.now() - timedelta(days=30)
    expired = Token.objects.filter(created__lt=cutoff)
    count = expired.count()
    expired.delete()
    logger.info(f"已清理 {count} 筆過期 token")
    return {"status": 200, "data": f"清理 {count} 筆過期 token"}
