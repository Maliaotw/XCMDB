from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from . import serializers
from django_celery_beat.models import PeriodicTask,CrontabSchedule
from django_celery_results import models as df_result_models
from django_filters import rest_framework as filters
from django_filters.rest_framework.backends import DjangoFilterBackend

# Create your views here.

class PeriodicTaskFilter(filters.FilterSet):

    name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = PeriodicTask
        fields = ('name',)


class PeriodicTaskListViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    PeriodicTaskListViewSet 序列化
    '''
    queryset = PeriodicTask.objects.all()
    serializer_class = serializers.PeriodicTaskListSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = PeriodicTaskFilter

    def get_serializer_class(self):
        # print(self.__class__.__name__,'get_serializer_class',self.action)
        if self.action == 'list':
            return serializers.PeriodicTaskListSerializer
        return serializers.PeriodicTaskSerializer

class TaskResultFilter(filters.FilterSet):

    datetime = filters.DateTimeFromToRangeFilter(label='datetime', method='filter_datetime')

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        # print(queryset)
        return queryset.filter(date_done__range=self.data.getlist('datetime[]'))

    class Meta:
        model = df_result_models.TaskResult
        fields = ('task_name', 'task_args','task_kwargs','status','datetime')


class CustomDjangoFilterBackend(DjangoFilterBackend):

    def get_filterset_kwargs(self, request, queryset, view):
        query_params = request.query_params.copy()

        if '[]' in request.query_params.get('task_args'):
            query_params['task_args'] = '()'

        if query_params.get('task_kwargs'):
            query_params['task_kwargs'] = query_params['task_kwargs'].replace('"',"'")

        return {
            'data': query_params,
            'queryset': queryset,
            'request': request,
        }


class TaskResultListViewSet(viewsets.ReadOnlyModelViewSet):
    '''
     序列化
    '''
    queryset = df_result_models.TaskResult.objects.all()
    serializer_class = serializers.TaskResultSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = TaskResultFilter
    filter_backends = [CustomDjangoFilterBackend,]

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        obj = super().get_queryset()
        return obj

    def get_serializer_class(self):
        # print(self.__class__.__name__,'get_serializer_class',self.action)

        if self.action == 'list':
            return serializers.TaskResultSerializer
        return serializers.TaskResultSerializer



