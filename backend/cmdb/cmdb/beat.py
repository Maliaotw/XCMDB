"""Beat 排程集中管理 - 所有 cron schedule 在此定義"""

from celery.schedules import crontab

from .celery import app

app.conf.beat_schedule = {
    "定期同步VM Guest": {
        "task": "tasks.vm_provision.sync_guest_vms",
        "schedule": crontab(minute="*/10"),  # 每 10 分鐘
    },
    "vm-destroy-batch": {
        "task": "tasks.vm_provision.vm_destroy_batch",
        "schedule": crontab(minute="*/5"),  # 每 5 分鐘
    },
    "定期重建角色權限": {
        "task": "tasks.rbac.rebuild_role_hierarchies",
        "schedule": crontab(hour="*/4"),  # 每 4 小時
    },
}

app.conf.timezone = "Asia/Taipei"
