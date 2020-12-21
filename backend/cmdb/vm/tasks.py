import datetime
from celery import shared_task
import time
from django.core.cache import cache
from src.pyterraform import terraform
from . import models
from pyvsphere import Vsphere, VcenterConfig
from django.conf import settings
from src import create_one
import inspect
import logging

logger = logging.getLogger('__name__')




def except_handle(e):
    import sys
    import traceback
    error_class = e.__class__.__name__  # 取得錯誤類型
    detail = e.args[0]  # 取得詳細內容
    cl, exc, tb = sys.exc_info()  # 取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
    fileName = lastCallStack[0]  # 取得發生的檔案名稱
    lineNum = lastCallStack[1]  # 取得發生的行號
    funcName = lastCallStack[2]  # 取得發生的函數名稱
    errMsg = "-" * 100 + f"\n File \"{fileName}\",\n Line: {lineNum},\n In {funcName}: [{error_class}]\n {detail} \n" + "-" * 100
    return errMsg


@shared_task()
def hello(name='Maliao'):
    hello.app.startdate = datetime.datetime.now()
    hello.app.name = 'hello'
    for i in range(10):
        time.sleep(1)
        print(i)
        cache.set(name, i, 5)

    return "Hello {}".format(name)


@shared_task
def vm_destroy():
    # 銷毀VM
    _ret = []
    vm_obj = models.VM.objects.filter(is_finish=True, status=5)
    for vm in vm_obj:
        terraform.DeleteF(hostname=vm.name)
        vm.delete()
        logger.debug(f"{vm.name} 銷毀完成")
        _ret.append(f"{vm.name} 銷毀完成")

    return "\n".join(_ret)


@shared_task
def add(x, y):
    return x, y


@shared_task
def sync_guest():

    if not all([settings.VCENTER_SERVER,settings.VCENTER_USER,settings.VCENTER_PASS]):
        return {"status": 200, "data": "VCENTER資訊未輸入或不完全，無法同步。"}


    _status_list = []

    ret = []
    logger.debug("執行開始時間 %s" % time.strftime("%Y%m%d %H:%M:%S"))
    ret.append("執行開始時間 %s" % time.strftime("%Y%m%d %H:%M:%S"))




    vcenterconfig = VcenterConfig(hostname=settings.VCENTER_SERVER, username=settings.VCENTER_USER, password=settings.VCENTER_PASS)
    vsphere = Vsphere(vcenterconfig)
    vsphere.get()
    vsphere.clean()




    # NetWork
    network_list = []
    for name, network in vsphere.network.items():
        obj = create_one(models.NetWork, network, {'network': name})['obj']
        network_list.append(name)
        if not obj.name:
            obj.remark = obj.network
            obj.save()

    # Cluster
    cluster_list = []
    for name, cluster in vsphere.cluster.items():
        obj = create_one(models.Cluster, cluster, {'name': name})['obj']
        cluster_list.append(name)
        if not obj.remark:
            obj.remark = obj.name
            obj.save()
        obj.network.add(*[models.NetWork.objects.get(network=network['network']) for network in cluster['network']])

    # DataStore
    datastore_list = []
    for name, datastore in vsphere.datastores.items():
        datastore.update({'status': True})
        obj = create_one(models.DataStore, datastore, {'name': name})['obj']
        datastore_list.append(name)
        if not obj.remark:
            obj.remark = obj.name
            obj.save()

    # HOST
    host_list = []
    for name, host in vsphere.hosts.items():
        host_list.append(name)
        host['cluster'] = models.Cluster.objects.get(name=host['cluster'])
        obj = create_one(models.Host, host, {'name': name})['obj']
        obj.network.add(*[models.NetWork.objects.get(network=network['network']) for network in host['network']])
        obj.datastore.add(*[models.DataStore.objects.get(name=datastore['name']) for datastore in host['ansible_datastore']])

    # VM
    vm_list = []
    for name, vm in vsphere.include_vm.items():
        vm_list.append(vm)
        network_obj = models.NetWork.objects.get(network=vm['network'])
        datastore_obj = models.DataStore.objects.get(name=vm['datastore']['name'])
        host_obj = models.Host.objects.get(name=vm['host']['name'])
        cluster_obj = host_obj.cluster
        vm.update({'host': host_obj, 'cluster': cluster_obj, 'datastore': datastore_obj, 'network': network_obj})
        create_one(models.Instance, vm, {'hw_name': name})


    ret.append(f"Cluster: {','.join(cluster_list)}")
    ret.append(f"Network: {','.join(network_list)}")
    ret.append(f"HOST: {','.join(host_list)}")
    ret.append(f"Datastore: {','.join(datastore_list)}")
    ret.append(f"VM: {','.join(vm_list)}")

    ret.append("執行結束時間 %s" % time.strftime("%Y%m%d %H:%M:%S"))

    return {"status": 200, "data": "\n".join(ret)}


@shared_task
def create(data):
    logger.debug("%s %s" % (__name__, inspect.stack()[0][3]))

    if not all([settings.VCENTER_SERVER,settings.VCENTER_USER,settings.VCENTER_PASS]):
        return {"status": 200, "data": "VCENTER資訊未輸入或不完全，無法創建實例。"}


    name = data['hostname']
    _ret = []
    _ret.append("執行開始時間 %s" % time.strftime("%Y%m%d %H:%M:%S"))
    _ret.append("name: %s" % name)

    # 創建
    # 以data Key中的 "gateway" 當作 是否 是DHCP 還是 固定IP
    logging.info("選擇創建方式: DHCP 或 固定IP")

    # 固定IP
    if data.get("gateway"):
        terraform.CustomIPCreate(**data)
    # DHCP
    else:
        terraform.Create(**data)

    logging.info("創建完成")

    # 更新資訊
    vcenterconfig = VcenterConfig(hostname=settings.VCENTER_SERVER, username=settings.VCENTER_USER, password=settings.VCENTER_PASS)
    vsphere = Vsphere(vcenterconfig)
    for vm in vsphere.vmware.vmware_vm_facts():
        if vm['guest_name'] == name:
            vsphere.get_datastores()
            vsphere.get_hosts()
            vsphere._vm[name] = vsphere.get_vm_datatil(vm)
            vsphere.clean_host_list()
            data = vsphere.clean_vm(name)


    if data:
        network_obj = models.NetWork.objects.get(network=data['network'])
        datastore_obj = models.DataStore.objects.get(name=data['datastore']['name'])
        host_obj = models.Host.objects.get(name=data['host']['name'])
        cluster_obj = host_obj.cluster
        data.update({'host': host_obj, 'cluster': cluster_obj, 'datastore': datastore_obj, 'network': network_obj})
        create_one(models.Instance, data, {'hw_name': data['hw_name']})

    # _ret.append(str(clean_data))
    _ret.append("執行結束時間 %s" % time.strftime("%Y%m%d %H:%M:%S"))

    return {"status": 200, "data": "\n".join(_ret)}

