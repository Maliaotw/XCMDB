"""VM app 任務入口 - 僅作為代理"""

from tasks.vm_provision import create_vm, destroy_vm, sync_guest_vms, vm_destroy_batch

__all__ = ["create_vm", "destroy_vm", "sync_guest_vms", "vm_destroy_batch"]
