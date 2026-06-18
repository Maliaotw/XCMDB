import inspect
import logging

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

# from djcelery import models as djcelery_models
from django_celery_beat.models import PeriodicTask

from . import tasks
from .models import VM

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


@receiver(post_save, sender=VM)
def on_vm_save(sender, instance=None, created=True, **kwargs):
    """
    創建VM實例
    VM object

    :param sender: <django.db.models.signals.ModelSignal object at 0x10c49fda0>,
    :param instance: True
    :param kwargs: {
        'update_fields': ,
        'raw': False,
        'using': 'default'
    }
    :return:
    """
    logger.debug(f"VM signal triggered: {inspect.stack()[0][3]}")

    # print("接收信號")
    if created:
        data = cache.get(instance.name)
        logger.debug(f"data {data}")
        if not data:
            logger.debug(f"No data found in cache for VM {instance.name}, skipping signal tasks.")
            return
        data.pop("type")

        PeriodicTask.objects.get_or_create(
            name=f"創建VM資源: {instance.name}({instance.manage_ip})",
            task="tasks.vm_provision.create_vm",
            args=(data,),
            enabled=False,
        )

        # 異步任務 開始創建
        task = tasks.create_vm.delay(data)
        # task = tasks.init_vm.delay(**data)
        data.update({"time": "300"})
        data.update({"task": task.id})
        # print(task.id)
        cache.set(instance.name, data)
        # print(instance.name)
        instance.task = task.id
        instance.save()
