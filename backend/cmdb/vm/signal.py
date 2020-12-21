from django.db.models.signals import post_save
from django.core.cache import cache
from . import tasks
from .models import VM
from django.dispatch import receiver
import logging
import inspect
import ipaddress
import json
# from djcelery import models as djcelery_models
from django_celery_beat.models import PeriodicTask

"""
pre_init                    # django的modal执行其构造方法前，自动触发
post_init                   # django的modal执行其构造方法后，自动触发
pre_save                    # django的modal对象保存前，自动触发
post_save                   # django的modal对象保存后，自动触发
pre_delete                  # django的modal对象删除前，自动触发
post_delete                 # django的modal对象删除后，自动触发
m2m_changed                 # django的modal中使用m2m字段操作第三张表（add,remove,clear）前后，自动触发
class_prepared              # 程序启动时，检测已注册的app中modal类，对于每一个类，自动触发
"""


@receiver(post_save, sender=VM)
def on_vm_save(sender, instance=None, created=True, **kwargs):
    '''
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
    '''
    logging.debug("%s %s" % (__name__, inspect.stack()[0][3]))

    # print("接收信號")
    if created:
        data = cache.get(instance.name)
        logging.debug("data %s" % (data))
        # print("instance.name",instance.name)
        # print(data)
        data.pop('type')

        PeriodicTask.objects.get_or_create(
            name="創建VM資源: {}({})".format(instance.name,instance.manage_ip),
            task='vm.tasks.create',
            kwargs=data,
            enabled=False

        )

        # 異步任務 開始創建
        task = tasks.create.apply_async(kwargs=data,countdown=10)
        # task = tasks.init_vm.delay(**data)
        data.update({'time': "300"})
        data.update({'task':task.id})
        # print(task.id)
        cache.set(instance.name,data)
        # print(instance.name)
        instance.task = task.id
        instance.save()
