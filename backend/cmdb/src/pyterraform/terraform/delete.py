from .base import Terraform
import subprocess
import logging


class Delete(Terraform):
    valid_text = "destroy"
    command = "terraform destroy -auto-approve"

    def run(self):
        self.create_host_dir()
        self._init()
        self._plan()
        self._main()

    def _plan(self):
        ret = subprocess.getoutput('terraform plan')
        if "No changes. Infrastructure is up-to-date." in ret:
            logging.info('%s plan ok' % self.hostname)
            return True
        else:
            logging.error('%s plan error %s' % (self.hostname,ret))
            raise Exception("%s plan錯誤 配置文件疑似修改過" % self.hostname)


class DeleteF(Delete):
    '''
    強制刪除
    '''

    def run(self):
        self.create_host_dir()
        self._init()
        self._main()

    def _main(self):
        ret = subprocess.getoutput(self.command)
        self.complete(ret)
        self.status = True

