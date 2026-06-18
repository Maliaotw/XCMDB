"""VM 創建/銷毀/同步任務"""

import time

from celery import shared_task
from django.conf import settings
from pyvsphere import VcenterConfig, Vsphere
from src import create_one
from src.pyterraform import terraform

from vm import models as instance_models
from vm import models as vm_models

from .base import BaseTask, get_task_logger

logger = get_task_logger("vm_provision")


@shared_task(name="tasks.vm_provision.sync_guest_vms", base=BaseTask)
def sync_guest_vms():
    """同步 vCenter VM 資料"""
    if not all([settings.VCENTER_SERVER, settings.VCENTER_USER, settings.VCENTER_PASS]):
        return {"status": 200, "data": "VCENTER 資訊未輸入或不完全，無法同步。"}

    logger.info("vCenter VM 同步開始")
    start_time = time.strftime("%Y%m%d %H:%M:%S")

    vcenterconfig = VcenterConfig(
        hostname=settings.VCENTER_SERVER, username=settings.VCENTER_USER, password=settings.VCENTER_PASS
    )
    vsphere = Vsphere(vcenterconfig)
    vsphere.get()
    vsphere.clean()

    network_list = []
    for name, network in vsphere.network.items():
        obj = create_one(vm_models.NetWork, network, {"network": name})["obj"]
        network_list.append(name)
        if not obj.name:
            obj.remark = obj.network
            obj.save()

    cluster_list = []
    for name, cluster in vsphere.cluster.items():
        obj = create_one(vm_models.Cluster, cluster, {"name": name})["obj"]
        cluster_list.append(name)
        if not obj.remark:
            obj.remark = obj.name
            obj.save()
        obj.network.add(*[vm_models.NetWork.objects.get(network=n["network"]) for n in cluster["network"]])

    datastore_list = []
    for name, datastore in vsphere.datastores.items():
        datastore.update({"status": True})
        obj = create_one(vm_models.DataStore, datastore, {"name": name})["obj"]
        datastore_list.append(name)
        if not obj.remark:
            obj.remark = obj.name
            obj.save()

    host_list = []
    for name, host in vsphere.hosts.items():
        host_list.append(name)
        host["cluster"] = vm_models.Cluster.objects.get(name=host["cluster"])
        obj = create_one(vm_models.Host, host, {"name": name})["obj"]
        obj.network.add(*[vm_models.NetWork.objects.get(network=n["network"]) for n in host["network"]])
        obj.datastore.add(*[vm_models.DataStore.objects.get(name=d["name"]) for d in host["ansible_datastore"]])

    vm_list = []
    for name, vm in vsphere.include_vm.items():
        vm_list.append(vm)
        network_obj = vm_models.NetWork.objects.get(network=vm["network"])
        datastore_obj = vm_models.DataStore.objects.get(name=vm["datastore"]["name"])
        host_obj = vm_models.Host.objects.get(name=vm["host"]["name"])
        cluster_obj = host_obj.cluster
        vm.update({"host": host_obj, "cluster": cluster_obj, "datastore": datastore_obj, "network": network_obj})
        create_one(instance_models.Instance, vm, {"hw_name": name})

    ret = []
    ret.append(f"Cluster: {','.join(cluster_list)}")
    ret.append(f"Network: {','.join(network_list)}")
    ret.append(f"HOST: {','.join(host_list)}")
    ret.append(f"Datastore: {','.join(datastore_list)}")
    ret.append(f"VM: {','.join(vm_list)}")

    end_time = time.strftime("%Y%m%d %H:%M:%S")
    ret.append(f"執行結束時間 {end_time}")
    logger.info(f"vCenter VM 同步完成: {start_time} -> {end_time}")

    return {"status": 200, "data": "\n".join(ret)}


@shared_task(name="tasks.vm_provision.create_vm", base=BaseTask)
def create_vm(data):
    """創建 VM"""
    logger.info(f"創建 VM: {data.get('hostname', 'unknown')}")

    if not all([settings.VCENTER_SERVER, settings.VCENTER_USER, settings.VCENTER_PASS]):
        return {"status": 200, "data": "VCENTER 資訊未輸入或不完全，無法創建實例。"}

    name = data["hostname"]
    start_time = time.strftime("%Y%m%d %H:%M:%S")

    if data.get("gateway"):
        terraform.CustomIPCreate(**data)
    else:
        terraform.Create(**data)

    logger.info("創建完成")

    vcenterconfig = VcenterConfig(
        hostname=settings.VCENTER_SERVER, username=settings.VCENTER_USER, password=settings.VCENTER_PASS
    )
    vsphere = Vsphere(vcenterconfig)
    for vm in vsphere.vmware.vmware_vm_facts():
        if vm["guest_name"] == name:
            vsphere.get_datastores()
            vsphere.get_hosts()
            vsphere._vm[name] = vsphere.get_vm_datatil(vm)
            vsphere.clean_host_list()
            clean_data = vsphere.clean_vm(name)

            if clean_data:
                network_obj = vm_models.NetWork.objects.get(network=clean_data["network"])
                datastore_obj = vm_models.DataStore.objects.get(name=clean_data["datastore"]["name"])
                host_obj = vm_models.Host.objects.get(name=clean_data["host"]["name"])
                cluster_obj = host_obj.cluster
                clean_data.update(
                    {"host": host_obj, "cluster": cluster_obj, "datastore": datastore_obj, "network": network_obj}
                )
                create_one(instance_models.Instance, clean_data, {"hw_name": clean_data["hw_name"]})

    end_time = time.strftime("%Y%m%d %H:%M:%S")
    return {"status": 200, "data": f"執行開始時間 {start_time}\n{name} 創建完成\n執行結束時間 {end_time}"}


@shared_task(name="tasks.vm_provision.destroy_vm", base=BaseTask)
def destroy_vm(vm_id):
    """銷毀指定 VM"""
    try:
        vm = vm_models.VM.objects.get(id=vm_id)
        terraform.DeleteF(hostname=vm.name)
        vm.delete()
        logger.info(f"VM 銷毀完成: {vm.name}")
        return {"status": 200, "data": f"{vm.name} 銷毀完成"}
    except vm_models.VM.DoesNotExist:
        return {"status": 404, "data": f"VM #{vm_id} 不存在"}


@shared_task(name="tasks.vm_provision.vm_destroy_batch", base=BaseTask)
def vm_destroy_batch():
    """批次銷毀完成的 VM"""
    logger.info("vm_destroy_batch 開始執行")
    failed_vms = vm_models.VM.objects.filter(is_finish=True, status=5)
    _ret = []
    for vm in failed_vms:
        terraform.DeleteF(hostname=vm.name)
        vm.delete()
        logger.debug(f"{vm.name} 銷毀完成")
        _ret.append(f"{vm.name} 銷毀完成")

    return "\n".join(_ret) if _ret else "無待銷毀 VM"
