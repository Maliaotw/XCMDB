from django.db.models.signals import post_save
from django.core.cache import cache
from . import tasks
from . import models
from django.dispatch import receiver
import logging
import inspect
import ipaddress
from assets import models as asset_model
import json

# from djcelery import models as djcelery_models
from django_celery_beat.models import PeriodicTask,CrontabSchedule

'''
pre_init                    # django的modal执行其构造方法前，自动触发
post_init                   # django的modal执行其构造方法后，自动触发
pre_save                    # django的modal对象保存前，自动触发
post_save                   # django的modal对象保存后，自动触发
pre_delete                  # django的modal对象删除前，自动触发
post_delete                 # django的modal对象删除后，自动触发
m2m_changed                 # django的modal中使用m2m字段操作第三张表（add,remove,clear）前后，自动触发
class_prepared              # 程序启动时，检测已注册的app中modal类，对于每一个类，自动触发

'''


@receiver(post_save, sender=models.IDRAC)
def on_idrac_save(sender, instance=None, created=True, **kwargs):
    '''
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
    '''
    # logging.debug("%s %s" % (__name__, inspect.stack()[0][3]))

    # print("接收信號")
    if created:
        data = {'id': instance.id, 'idrac_ip': instance.idrac_ip}
        logging.debug("data %s" % (data))

        cron_5min_obj = CrontabSchedule.objects.get_or_create(
            minute='*/5', hour='*', day_of_week='*', day_of_month='*', month_of_year='*'
        )[0]

        name = "創建iDRAC: {}".format(instance.idrac_ip)
        periodictask_obj = PeriodicTask.objects.filter(name=name)
        if periodictask_obj:
            periodictask_obj.first().delete()

        task_obj = PeriodicTask.objects.get_or_create(
            name=name,
            task='hosts.tasks.idracinfo',
            crontab=cron_5min_obj,
            kwargs=json.dumps(data),
            enabled=True
        )

        instance.task = task_obj[0]
        tasks.idracinfo.apply_async(kwargs=data, countdown=10)
        # task = tasks.idracinfo.apply_async(kwargs=data, countdown=10)
        # task = tasks.init_vm.delay(**data)
        instance.save()


