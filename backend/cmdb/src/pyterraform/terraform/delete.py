import logging
import subprocess

from .base import Terraform


class Delete(Terraform):
    valid_text = "destroy"
    command = "terraform destroy -auto-approve"

    def run(self):
        self.create_host_dir()
        self._init()
        self._plan()
        self._main()

    def _plan(self):
        ret = subprocess.getoutput("terraform plan")
        if "No changes. Infrastructure is up-to-date." in ret:
            logging.info(f"{self.hostname} plan ok")
            return True
        else:
            logging.error(f"{self.hostname} plan error {ret}")
            raise Exception(f"{self.hostname} plan錯誤 配置文件疑似修改過")


class DeleteF(Delete):
    """
    強制刪除
    """

    def run(self):
        self.create_host_dir()
        self._init()
        self._main()

    def _main(self):
        ret = subprocess.getoutput(self.command)
        self.complete(ret)
        self.status = True
