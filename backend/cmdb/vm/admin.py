from django.contrib import admin
from . import models
# Register your models here.



@admin.register(models.Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display =[i.attname for i in models.Instance._meta.fields]


@admin.register(models.DataStore)
class DataStoreAdmin(admin.ModelAdmin):
    list_display = [i.attname for i in models.DataStore._meta.fields]

@admin.register(models.Host)
class HostAdmin(admin.ModelAdmin):
    list_display = [i.attname for i in models.Host._meta.fields]

@admin.register(models.NetWork)
class NetWorkAdmin(admin.ModelAdmin):
    list_display = [i.attname for i in models.NetWork._meta.fields]

@admin.register(models.NetWorkStatic)
class NetWorkStaticAdmin(admin.ModelAdmin):
    list_display = [i.attname for i in models.NetWorkStatic._meta.fields]


@admin.register(models.Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'remark', 'net'
    ]

    def net(self, obj):
        return ", ".join([i.network for i in  obj.network.all()])
