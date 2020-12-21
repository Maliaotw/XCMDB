from .base import Terraform
import json
import os

class Update(Terraform):
    valid_text = "change"
    command = "terraform apply -no-color -auto-approve"

    def data(self, vars):
        js = os.path.join(self.path['host'], 'terraform.tfvars.json')
        with open(js, 'r') as f:
            data = json.load(f)
            data.update(vars)

        tfvars_json = open(os.path.join(self.path['host'], 'terraform.tfvars.json'), 'w')
        json.dump(data, tfvars_json)
        tfvars_json.close()


    def run(self):
        self.create_host_dir()
        self.data(self.vars)
        self._init()
        self._plan()
        self._main()


