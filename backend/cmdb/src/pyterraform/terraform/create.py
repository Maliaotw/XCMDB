from .base import Terraform
from shutil import copyfile
import os
import json


class Create(Terraform):
    valid_text = "add"
    command = "terraform apply -no-color -auto-approve"

    def run(self):
        self.create_host_dir()
        self.data(self.vars)
        self.copyfile()
        self._init()
        self._plan()
        self._main()

    def data(self, vars):
        js = os.path.join(self.path['conf'], 'terraform_example.tfvars.json')
        data = json.load(open(js, 'r'))

        data.update(vars)

        # data['hostname'] = self.hostname
        # data['ipaddress'] = self.ipaddress
        tfvars_json = open(os.path.join(self.path['host'], 'terraform.tfvars.json'), 'w')
        json.dump(data, tfvars_json)
        tfvars_json.close()

    def copyfile(self):
        for file in ['main.tf', 'variables.tf']:
            copyfile(os.path.join(self.path['conf'], file), os.path.join(self.path['host'], file))


class CustomIPCreate(Create):
    dhcp = False