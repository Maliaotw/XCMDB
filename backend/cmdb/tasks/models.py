from django.db import models

# Create your models here.

class TaskDetail(models.Model):
    name = models.ForeignKey('django_celery_beat.PeriodicTask',on_delete=models.CASCADE)
    taskid = models.OneToOneField('django_celery_results.TaskResult',on_delete=models.CASCADE)
    remark = models.CharField(max_length=255, blank=True)
    arg = models.CharField(max_length=64, blank=True)
    create_date = models.DateTimeField()

    class Mata:
        verbose_name_plural = "任務詳細表"
        ordering =['-create_date']



class TaskManualRecord(models.Model):
    name = models.CharField(max_length=255)
    app = models.CharField(max_length=64)
    arg = models.CharField(max_length=64, blank=True)
    remark = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now=True)

