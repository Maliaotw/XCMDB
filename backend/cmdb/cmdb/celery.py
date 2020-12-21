from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

from celery.utils.log import get_task_logger
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmdb.settings')

app = Celery('cmdb')
# platforms.C_FORCE_ROOT = True

app.config_from_object('django.conf:settings',namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    # 自動測試
    'add': {
        'task': 'vm.tasks.add',
        'args': (3, 4,),
        'schedule': crontab(minute='*/1'),
    },
    # '定期銷毀失敗VM': {
    #     'task': 'vm.tasks.vm_destroy',
    #     'schedule': crontab(minute='*/1'),
    # },
    # 自動排程清理構建失敗的VM
    '定期同步VM Guest': {
        'task': 'vm.tasks.sync_guest',
        'schedule': crontab(minute='*/10'),
    },
    # #
    # # 自動排程清理構建失敗的VM
    # 'hello': {
    #     'task': 'vm.tasks.hello',
    #     'schedule': crontab(minute='*/1'),
    # },

}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


