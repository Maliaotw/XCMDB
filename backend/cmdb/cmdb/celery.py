"""Celery app 設定 - 僅保留初始化與 broker/backend config"""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmdb.settings")

app = Celery("cmdb")
# platforms.C_FORCE_ROOT = True

app.config_from_object("django.conf:settings", namespace="CELERY")

# Celery worker 啟動時自動匯入任務模組
app.conf.update(imports=("tasks.vm_provision", "tasks.asset_sync", "tasks.audit", "tasks.cleanup", "tasks.rbac", "tasks.notification"))


def setup_tasks():
    """在 Django setup 完成後載入任務模組"""
    import authentication.tasks  # noqa: F401
    import hosts.tasks  # noqa: F401
    import vm.tasks  # noqa: F401
