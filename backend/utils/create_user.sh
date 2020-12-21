#!/bin/bash

function sync_instance() {
python3 ../cmdb/manage.py shell << EOF
from common import models

models.UserProfile.objects.all().delete()

user = models.UserProfile()
user.username = "admin"
user.set_password("admin")
user.is_staff = True
user.is_superuser = True
user.save()

EOF
}

sync_instance
