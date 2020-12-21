from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings
# from djcelery.models import PeriodicTask, CrontabSchedule
from django_celery_beat.models import PeriodicTask,CrontabSchedule
# from django.contrib.auth.models import User
from common.models import UserProfile
import os
import stat
from assets import models as asset_model
__all__ = [
    "Host", "CPU", "NIC", "Disk", "Memory", "Node", "HostRecord", 'IDRAC', 'CmdRecord', 'RunUser', 'Process',
    "HostProc", "BusinessUnit"
]


class IDRAC(models.Model):
    '''
    iDRAC
    '''

    idrac_ip = models.GenericIPAddressField(verbose_name='IDRAC IP')
    port = models.PositiveSmallIntegerField(verbose_name='端口', default=443)
    host = models.OneToOneField("Host", verbose_name='Host', blank=True, null=True, on_delete=models.CASCADE)
    task = models.ForeignKey("django_celery_beat.PeriodicTask", verbose_name="任務", blank=True, null=True,
                             on_delete=models.CASCADE)

    @property
    def get_taskdetail(self):
        return self.task.taskdetail_set.order_by('-create_date').all()[:10]

    def __str__(self):
        return "%s" % self.idrac_ip

    class Mata:
        verbose_name_plural = "iDRAC表"
        verbose_name = '服務器'

class BusinessUnit(models.Model):
    """
    業務線
    """
    name = models.CharField('業務線', max_length=64, unique=True)
    enname = models.CharField('英文', max_length=64)
    remark = models.TextField('備註', blank=True)

    class Meta:
        verbose_name_plural = "業務線表"

    def __str__(self):
        return self.name


class Host(models.Model):
    '''
    服務器表
    '''

    cate_choice = (
        (1, '服務器'),
        (2, '虛擬機'),
    )

    cate = models.SmallIntegerField(verbose_name="類型", choices=cate_choice, default=1)
    name = models.CharField(verbose_name="主機名稱", max_length=64)
    sn = models.CharField('SN序號', max_length=64)

    manufacturer = models.CharField(verbose_name='製造商', max_length=64, blank=True)
    model = models.CharField('型號', max_length=64, null=True, blank=True)

    manage_ip = models.GenericIPAddressField('IP', null=True, blank=True)

    os_distribution = models.CharField('發行版本', max_length=64, blank=True)
    os_platform = models.CharField('系統', max_length=64, blank=True)
    os_version = models.CharField('系統版本', max_length=64, blank=True)

    latest_date = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    enabled_choice = ((True, '啟用'), (False, '未啟用'),)
    enabled = models.BooleanField("啟用狀態", default=False, choices=enabled_choice)

    node = models.ForeignKey(
        "Node",
        verbose_name='分支',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    bus_unit = models.ForeignKey(
        'BusinessUnit', verbose_name='業務線', null=True, blank=True, on_delete=models.CASCADE
    )

    total_cores = models.PositiveIntegerField(null=True, blank=True)
    total_disk = models.PositiveIntegerField(null=True, blank=True)
    total_memory = models.PositiveIntegerField(null=True, blank=True)

    # 只關聯不會生成字段 # 服務器入資產 # 虛擬機不入
    asset = GenericRelation(to='assets.Asset')

    manage_ssh = models.CharField('sshd', max_length=16, default='22')

    #
    # def get_info(self):
    #     data = {'cpu': '', 'disk': '', 'mem': ''}
    #     if self.cpu.all().count() > 1:
    #         data['cpu'] = "%sCores" % sum([i.cores for i in self.cpu.all()])
    #     else:
    #         data['cpu'] = "%sCores" % self.cpu.all().first().cores
    #
    #     data['disk'] = "%s GB" % sum([i.capacity for i in self.disk.all()])
    #     data['mem'] = "%s GB" % sum([i.capacity for i in self.memory.all()])
    #     return "{cpu} {disk} {mem}".format(**data)

    def get_info(self):
        return "{}Cores {}GB {}G".format(self.total_cores, self.total_disk, self.total_memory)

    def __str__(self):
        return "%s %s" % (self.name, self.manage_ip)


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)

        # print(self.asset.all())
        if self.cate == 1:

            if not self.asset.all():
                asset_model.Asset.objects.create(content_object=self, name=self.name, device_type_id=1)

    class Meta:
        verbose_name = '服務器'
        verbose_name_plural = "服務器表"
        ordering = ['-latest_date']


class HostProc(models.Model):
    host = models.ForeignKey("Host", on_delete=models.CASCADE, related_name='HostProc')
    proc = models.ManyToManyField("Process")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.host.name, self.create_at)

    class Meta:
        verbose_name_plural = '服務器進程表'
        verbose_name = '服務器進程表'


class Process(models.Model):
    '''
    {'exe': '/usr/lib/systemd/systemd-journald',
    'status': 'sleeping',
    'username': 'root',
    'create_time': 1568100982.13,
    'pid': 543,
    'cmdline': ['/usr/lib/systemd/systemd-journald']}
    '''

    name = models.CharField(max_length=255, verbose_name='進程名稱')
    status = models.CharField(max_length=255, verbose_name='狀態')
    username = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    pid = models.IntegerField()
    cmdline = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name_plural = '進程表'
        verbose_name = '進程表'


class HostNet(models.Model):
    host = models.ForeignKey("Host", on_delete=models.CASCADE, related_name='HostNet')
    net = models.ManyToManyField("Net")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.host.name, self.create_at)

    class Meta:
        verbose_name_plural = '服務器網路端口表'
        verbose_name = '服務器網路端口表'


class Net(models.Model):
    proto = models.CharField(max_length=64)
    port = models.CharField(max_length=64)
    pid = models.CharField(max_length=64)
    name = models.CharField(max_length=64)


class CPU(models.Model):
    '''
    CPU表
    '''
    slot = models.CharField("插槽位置", max_length=64)
    manufacturer = models.CharField(verbose_name='製造商', max_length=64, blank=True)
    model = models.CharField('型號', max_length=255, null=True, blank=True)
    cores = models.SmallIntegerField('cores', blank=True)
    threads = models.SmallIntegerField('threads', blank=True, null=True)
    host_obj = models.ForeignKey("Host", related_name='cpu', on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.slot, self.model)

    class Meta:
        verbose_name_plural = "CPU表"


class NIC(models.Model):
    '''
    網卡表
    '''
    name = models.CharField('網卡名稱', max_length=255, null=True, blank=True)
    ipaddress = models.GenericIPAddressField('IP', blank=True, null=True)
    model = models.CharField('型號', max_length=255, null=True, blank=True)
    macaddress = models.CharField('MAC', max_length=255, null=True, blank=True)
    netmask = models.CharField('Netmask', max_length=255, null=True, blank=True)
    host_obj = models.ForeignKey("Host", related_name='nic', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "網卡表"

    def __str__(self):
        return "%s %s" % (self.name, self.macaddress)


class Disk(models.Model):
    """
    硬盤信息表
    """
    slot = models.CharField('插槽位置', max_length=64)
    model = models.CharField('硬盤型號', max_length=64, null=True, blank=True)
    capacity = models.FloatField('硬盤容量', null=True, blank=True)
    host_obj = models.ForeignKey("Host", related_name='disk', on_delete=models.CASCADE)
    sn = models.CharField("硬碟序號", max_length=128, null=True, blank=True)
    manufacturer = models.CharField('製造商', max_length=32, null=True, blank=True)
    iface_type = models.CharField('接口類型', max_length=64, null=True, blank=True)

    class Meta:
        verbose_name_plural = "硬盤表"

    def __str__(self):
        return "%s %s" % (self.slot, self.sn)


class Memory(models.Model):
    """
    内存信息表
    """
    slot = models.CharField('插槽位置', max_length=64)
    manufacturer = models.CharField('製造商', max_length=32, null=True, blank=True)
    model = models.CharField('型號', max_length=64)
    capacity = models.FloatField('內存容量', null=True, blank=True)
    sn = models.CharField('內存SN號', max_length=64, null=True, blank=True)
    host_obj = models.ForeignKey("Host", related_name='memory', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "内存表"

    def __str__(self):
        return "%s %s" % (self.slot, self.sn)


class HostRecord(models.Model):
    """,
    主機變更紀錄表
    """
    host_obj = models.ForeignKey('Host', on_delete=models.CASCADE, related_name='hostrecord')
    title = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)

    create_date = models.DateTimeField(auto_now_add=True, verbose_name='創建日期')

    class Meta:
        verbose_name_plural = "主機紀錄表"
        ordering = ['-create_date']

    def __str__(self):
        return "%s" % (self.host_obj)


class Node(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class CmdRecord(models.Model):
    host = models.ManyToManyField('Host', verbose_name='主機')
    user = models.ForeignKey(UserProfile, verbose_name='用戶', on_delete=models.CASCADE)
    run_as = models.CharField(verbose_name='運行用戶', default='root', max_length=64)
    command = models.TextField(verbose_name="Command")
    _result = models.TextField(blank=True, null=True, verbose_name='Result')
    is_finished = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(null=True)
    date_finished = models.DateTimeField(null=True)

    def __str__(self):
        return "%s" % self.command[:20]

    class Meta:
        ordering = ['-date_created']


def content_file_name(instance, filename):
    return '/'.join(['rununser', str(instance.username), filename])


class RunUser(models.Model):
    name = models.CharField(verbose_name='名稱', max_length=255)
    username = models.CharField(verbose_name='用戶名', max_length=255, blank=True, null=True)
    password = models.CharField(verbose_name='密鑰', max_length=255, blank=True, null=True)
    private_key = models.FileField(blank=True, null=True, verbose_name="私鑰", upload_to=content_file_name)
    comment = models.TextField(blank=True, verbose_name="備註")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="創建日期")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="更新日期")
    created_by = models.CharField(max_length=128, null=True, verbose_name="Created by")

    def __str__(self):
        return "%s" % self.username

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using,update_fields=update_fields)

        if self.private_key:
            # print(self.private_key.file)
            os.chmod("%s" % self.private_key.file, stat.S_IRUSR)

    class Meta:
        verbose_name = '執行用戶'
        verbose_name_plural = '執行用戶'
