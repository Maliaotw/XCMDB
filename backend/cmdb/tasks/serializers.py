from rest_framework import serializers
from django_celery_beat.models import PeriodicTask
import inspect
import logging
from django_celery_results import models as djcelery_results_models
from celery.result import AsyncResult
import json

class TaskResultSerializer(serializers.ModelSerializer):
    '''
    TaskResult
    '''
    date_done = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    result = serializers.SerializerMethodField()

    def get_result(self, obj):
        logging.debug("%s %s" % (self.__class__.__name__, inspect.stack()[0][3]))

        if obj.status == 'SUCCESS':

            async_result = AsyncResult(obj.task_id).get(timeout=1)
            # async_result = obj.result
            # print(async_result)
            # print(type(async_result))
            if isinstance(async_result,dict):
                print(async_result)
                return async_result['data']
            else:
                return async_result
        else:

            error_msg = json.loads(obj.result)['exc_message']
            # print(obj.task_id)
            # print(obj.traceback)
            return "%s\n%s" % (error_msg, obj.traceback)

    class Meta:
        model = djcelery_results_models.TaskResult
        fields = '__all__'


class PeriodicTaskListSerializer(serializers.ModelSerializer):
    """PeriodicTask
    """
    crontab = serializers.SerializerMethodField()
    total_success_count = serializers.SerializerMethodField()
    total_run_count = serializers.SerializerMethodField()
    total_failure_count = serializers.SerializerMethodField()
    last_status = serializers.SerializerMethodField()
    last_run_at = serializers.SerializerMethodField()

    def to_representation(self, instance):
        """Convert `username` to lowercase."""

        self.task_result_obj = djcelery_results_models.TaskResult.objects.filter(
            task_name=instance.task,
            task_kwargs=json.loads(instance.kwargs),
            task_args='()' if instance.args in '[]' else instance.args
        )
        ret = super().to_representation(instance)
        return ret

    def get_crontab(self, obj):
        return str(obj.crontab).replace(" (m/h/d/dM/MY)", "")

    def get_last_run_at(self, obj):
        if self.task_result_obj.first():

            datetime = self.task_result_obj.first().date_done
            serserializer = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
            return serserializer.to_representation(datetime)
        else:
            return ''

    def get_last_status(self, obj):
        logging.debug("%s %s" % (self.__class__.__name__, inspect.stack()[0][3]))
        obj = self.task_result_obj.last()
        # 交給前端判斷 'SUCCESS' 'FAILURE' ''
        if obj:
            return obj.status
        else:
            return ''

    def get_total_success_count(self, obj):
        # logging.debug("%s %s" % (self.__class__.__name__, inspect.stack()[0][3]))
        # task_args = '()'
        return self.task_result_obj.filter(status='SUCCESS').count()

    def get_total_failure_count(self, obj):
        # logging.debug("%s %s" % (self.__class__.__name__, inspect.stack()[0][3]))
        return self.task_result_obj.filter(status='FAILURE').count()

    def get_total_run_count(self, obj):
        # logging.debug("%s %s" % (self.__class__.__name__, inspect.stack()[0][3]))
        return self.task_result_obj.count()

    class Meta:
        model = PeriodicTask
        fields = ['id', 'total_success_count', 'total_failure_count', 'last_run_at', 'last_status', 'name',
                  'total_run_count', 'crontab']


class PeriodicTaskSerializer(serializers.ModelSerializer):
    '''
    PeriodicTask
    '''

    class Meta:
        model = PeriodicTask
        fields = '__all__'

