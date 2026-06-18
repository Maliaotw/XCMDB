"""資產同步任務 - iDRAC / SNMP / 硬體 inventory"""

from celery import shared_task
from pyesxi import dellemc_get_system_inventory
from src import create_one

from hosts import models as host_models
from settings.models import Setting
from settings.models import settings as django_settings

from .base import BaseTask, get_task_logger

logger = get_task_logger("asset_sync")


class iDRACSync:
    """iDRAC 硬體同步 - 以 class 組織邏輯"""

    def __init__(self, ip, port="443"):
        self.idrac_ip = ip
        self.idrac_port = port
        self.result = []
        self.status_list = []
        self.idrac_data = self._get_idrac_data()

    def _get_idrac_data(self):
        config = {}
        setting_objs = Setting.objects.filter(name__contains="IDRAC")
        if setting_objs.exists():
            for s in setting_objs:
                config[s.name.lower()] = s.cleaned_value
        else:
            config.update(
                {
                    "idrac_user": django_settings.IDRAC_USER,
                    "idrac_passwd": django_settings.IDRAC_PASSWD,
                }
            )

        return dellemc_get_system_inventory(
            idrac_ip=self.idrac_ip,
            idrac_port=self.idrac_port,
            idrac_user=config.get("idrac_user"),
            idrac_passwd=config.get("idrac_passwd"),
        )

    def _create_or_update(self, model_class, data, filter_data):
        result = create_one(model_class, data, filter_data)
        self.result.append(f"{model_class.__name__}: {result['message']}")
        self.status_list.append(result["code"])
        return result["obj"]

    def run(self):
        logger.info(f"開始同步 iDRAC: {self.idrac_ip}")

        for category, model_map in [
            ("BIOS", host_models.BIOS),
            ("CPU", host_models.CPU),
            ("Controller", host_models.Controller),
            ("ControllerBattery", host_models.ControllerBattery),
            ("ControllerSensor", host_models.ControllerSensor),
            ("Enclosure", host_models.Enclosure),
            ("EnclosureSensor", host_models.EnclosureSensor),
            ("Fan", host_models.Fan),
            ("License", host_models.License),
            ("Memory", host_models.Memory),
            ("NIC", host_models.NIC),
            ("PCIDevice", host_models.PCIDevice),
            ("PhysicalDisk", host_models.PhysicalDisk),
        ]:
            for item in self.idrac_data.get(category, []):
                self._create_or_update(model_map, item, {"Key": item.get("Key", "")})

        logger.info(f"iDRAC {self.idrac_ip} 同步完成")
        return {
            "status": 200,
            "result": "\n".join(self.result),
            "errors": [s for s in self.status_list if s != 200],
        }


@shared_task(name="tasks.asset_sync.sync_idrac_hardware", base=BaseTask)
def sync_idrac_hardware(idrac_id):
    """iDRAC 硬體同步入口 (供 view 呼叫)"""
    from hosts.models import IDRAC

    try:
        idrac = IDRAC.objects.get(id=idrac_id)
        syncer = iDRACSync(idrac.idrac_ip, idrac.port)
        return syncer.run()
    except IDRAC.DoesNotExist:
        return {"status": 404, "result": f"iDRAC #{idrac_id} 不存在"}
