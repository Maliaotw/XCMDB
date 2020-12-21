#!/bin/bash
#

function sync_instance() {
python3 ../cmdb/manage.py shell << EOF
from vm  import tasks
tasks.sync_guest()

print("OK")
EOF
}

sync_instance
