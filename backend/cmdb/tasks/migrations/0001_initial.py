# Generated by Django 2.1.4 on 2020-11-19 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_results', '0004_auto_20190516_0412'),
        ('django_celery_beat', '0011_auto_20190508_0153'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(blank=True, max_length=255)),
                ('arg', models.CharField(blank=True, max_length=64)),
                ('create_date', models.DateTimeField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.PeriodicTask')),
                ('taskid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='django_celery_results.TaskResult')),
            ],
        ),
        migrations.CreateModel(
            name='TaskManualRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('app', models.CharField(max_length=64)),
                ('arg', models.CharField(blank=True, max_length=64)),
                ('remark', models.TextField(blank=True)),
                ('create_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
