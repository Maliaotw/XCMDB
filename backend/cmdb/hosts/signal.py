import json
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

# from djcelery import models as djcelery_models
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from . import models, tasks

logger = logging.getLogger(__name__)

"""
pre_init                    # django的modal執行其構造方法前，自動觸發
post_init                   # django的modal執行其構造方法後，自動觸發
pre_save                    # django的modal對象保存前，自動觸發
post_save                   # django的modal對象保存後，自動觸發
pre_delete                  # django的modal對象刪除前，自動觸發
post_delete                 # django的modal對象刪除後，自動觸發
m2m_changed                 # django的modal中使用m2m欄位操作第三張表（add,remove,clear）前後，自動觸發
class_prepared              # 程序啟動時，檢測已註冊的app中modal類，對於每一個類，自動觸發

"""


@receiver(post_save, sender=models.IDRAC)
def on_idrac_save(sender, instance=None, created=True, **kwargs):
    """
    創建Idrac
    Idrac object

    :param sender: <django.db.models.signals.ModelSignal object at 0x10c49fda0>,
    :param instance: True
    :param kwargs: {
        'update_fields': ,
        'raw': False,
        'using': 'default'
    }
    :return:
    """
    if created:
        logger.info(f"IDRAC created: {instance.idrac_ip}")

        cron_5min_obj = CrontabSchedule.objects.get_or_create(
            minute="*/5", hour="*", day_of_week="*", day_of_month="*", month_of_year="*"
        )[0]

        name = f"創建iDRAC: {instance.idrac_ip}"
        periodictask_obj = PeriodicTask.objects.filter(name=name)
        if periodictask_obj:
            periodictask_obj.first().delete()

        task_obj = PeriodicTask.objects.get_or_create(
            name=name, task="tasks.asset_sync.sync_idrac_hardware", crontab=cron_5min_obj, kwargs=json.dumps({"idrac_id": instance.id}), enabled=True
        )

        instance.task = task_obj[0]
        tasks.sync_idrac_hardware.delay(idrac_id=instance.id)
        instance.save()
