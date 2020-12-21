from django.db import models

# __all__ = ['VM', 'NetWork', 'Instance', 'Host', 'HostRunTime', 'RunTime', 'DataStore']


# Create your models here.

class VM(models.Model):
    '''
    用於建置
    '''
    name = models.CharField(max_length=255)
    status_choice = ((1, 'running'), (2, 'stop'), (3, 'restart'), (4, '正在初始化中'), (5, '構建失敗'))
    status = models.PositiveSmallIntegerField(choices=status_choice, default=4)
    check = models.CharField(max_length=64, default='')
    instance = models.OneToOneField('Instance', null=True, on_delete=models.CASCADE)
    task = models.CharField(max_length=64, default='')
    is_finish = models.BooleanField(default=False)
    manage_ip = models.GenericIPAddressField(blank=True, null=True)
    latest_date = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=255)
    cpu = models.PositiveIntegerField()
    memory = models.PositiveIntegerField()
    disk_size = models.PositiveIntegerField()

    def __str__(self):
        return "%s %s" % (self.name, self.manage_ip)


class Instance(models.Model):
    hw_name = models.CharField(max_length=255)
    hw_guest_full_name = models.CharField(max_length=255, blank=True)
    power_state_choice = (('poweredOn', '運行中'), ('poweredOff', '已停止'), ('building', '建置中'))
    hw_power_status = models.CharField(max_length=255, choices=power_state_choice)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=255, blank=True)
    instance_uuid = models.UUIDField(blank=True, null=True)
    host = models.ForeignKey("Host", on_delete=models.CASCADE, related_name='guests')
    hw_processor_count = models.PositiveIntegerField(verbose_name="CPU")
    hw_cores_per_socket = models.PositiveIntegerField(verbose_name="Cores", blank=True, null=True)
    hw_memtotal_mb = models.PositiveIntegerField(verbose_name="Memory")
    capacity = models.PositiveIntegerField(verbose_name="capacity")
    datastore = models.ForeignKey("DataStore", blank=True, null=True, on_delete=models.CASCADE)
    network = models.ForeignKey("NetWork", blank=True, null=True, on_delete=models.CASCADE)
    task = models.CharField(max_length=64, default='', blank=True, null=True)
    latest_date = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    hw_is_template = models.BooleanField()
    cluster = models.ForeignKey("Cluster", on_delete=models.CASCADE, related_name='instance')

    def __str__(self):
        return "%s" % self.hw_name

    class Meta:
        ordering = ['-create_at']


class Cluster(models.Model):
    name = models.CharField(max_length=255)
    remark = models.CharField(max_length=255, null=True, blank=True)
    network = models.ManyToManyField('NetWork')  # 跟著集群

    def __str__(self):
        return "%s" % self.name


class Host(models.Model):
    name = models.CharField(max_length=255)
    # cluster = models.CharField(max_length=255, null=True)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, related_name='host')
    datastore = models.ManyToManyField('DataStore')  # 跟著Host
    network = models.ManyToManyField('NetWork')  # 跟著集群
    last_date = models.DateTimeField(auto_now=True)

    # # overall_status = models.CharField(max_length=255)
    ansible_all_ipv4_addresses = models.GenericIPAddressField()
    ansible_processor = models.CharField(max_length=255)
    ansible_processor_cores = models.PositiveIntegerField()
    ansible_processor_count = models.PositiveIntegerField()
    ansible_processor_vcpus = models.PositiveIntegerField()
    ansible_memfree_mb = models.PositiveIntegerField()
    ansible_memtotal_mb = models.PositiveIntegerField()
    ansible_distribution = models.CharField(max_length=255)
    ansible_distribution_version = models.CharField(max_length=255)
    ansible_system_vendor = models.CharField(max_length=255)
    ansible_product_name = models.CharField(max_length=255)
    ansible_product_serial = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class HostRunTime(models.Model):
    Host = models.ForeignKey('Host', on_delete=models.CASCADE)
    RunTime = models.ForeignKey('RunTime', on_delete=models.CASCADE)
    last_date = models.DateTimeField(auto_now=True)


class RunTime(models.Model):
    cpu_allocation_expandable_reservation = models.BooleanField()
    cpu_allocation_limit = models.PositiveIntegerField()
    cpu_allocation_overhead_limit = models.CharField(max_length=255, blank=True)
    cpu_allocation_reservation = models.PositiveIntegerField()
    cpu_allocation_shares = models.PositiveIntegerField()
    cpu_allocation_shares_level = models.CharField(max_length=255)

    mem_allocation_expandable_reservation = models.BooleanField()
    mem_allocation_limit = models.PositiveIntegerField()
    mem_allocation_overhead_limit = models.CharField(max_length=255, blank=True)
    mem_allocation_reservation = models.PositiveIntegerField()
    mem_allocation_shares = models.PositiveIntegerField()
    mem_allocation_shares_level = models.CharField(max_length=255, blank=True)

    runtime_cpu_max_usage = models.PositiveIntegerField()
    runtime_cpu_overall_usage = models.PositiveIntegerField()
    runtime_cpu_reservation_used = models.PositiveIntegerField()
    runtime_cpu_reservation_used_vm = models.PositiveIntegerField()
    runtime_cpu_unreserved_for_pool = models.PositiveIntegerField()
    runtime_cpu_unreserved_for_vm = models.PositiveIntegerField()

    runtime_memory_max_usage = models.PositiveIntegerField()
    runtime_memory_overall_usage = models.PositiveIntegerField()
    runtime_memory_reservation_used = models.PositiveIntegerField()
    runtime_memory_reservation_used_vm = models.PositiveIntegerField()
    runtime_memory_unreserved_for_pool = models.PositiveIntegerField()
    runtime_memory_unreserved_for_vm = models.PositiveIntegerField()


class DataStore(models.Model):
    name = models.CharField(max_length=255, verbose_name="名稱")
    capacity = models.BigIntegerField(verbose_name="總容量")
    freeSpace = models.BigIntegerField(verbose_name="可用空間")
    provisioned = models.BigIntegerField(verbose_name="置備的空間", blank=True)
    type = models.CharField(max_length=255, verbose_name="文件系統", blank=True)
    status = models.BooleanField(default=True)
    remark = models.CharField(max_length=255, null=True, blank=True, verbose_name="別名")

    def __str__(self):
        return "%s" % self.name


class NetWork(models.Model):
    """
    ECS
    Vlan10
    13
    vSwitch0
    192.168.1.1/24
    192.168.1.1
    253
    0
    """
    name = models.CharField(max_length=255, null=True)
    network = models.CharField(max_length=255)  # portgroup = 'VLAN13'
    vlan_id = models.CharField(max_length=255)  # vlan_id = 13
    vswitch = models.CharField(max_length=255)  # vswitch = 'vSwitch0'
    status = models.BooleanField(default=True)
    remark = models.CharField(max_length=255, null=True, blank=True, verbose_name="別名")
    dhcp = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.network


class NetWorkStatic(models.Model):
    """
    網段關聯表
    """
    name = models.CharField(max_length=255, null=True,blank=True)
    lan = models.CharField(max_length=255) # 192.168.1.1/24
    gateway = models.CharField(max_length=255)
    template = models.OneToOneField("Instance",null=True,on_delete=models.CASCADE)
    remark = models.CharField(max_length=255, null=True, blank=True, verbose_name="別名")
    network = models.ForeignKey("NetWork", on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.name
