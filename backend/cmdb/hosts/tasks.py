"""Hosts app 任務入口 - 僅作為代理"""

from tasks.asset_sync import sync_idrac_hardware

__all__ = ["sync_idrac_hardware"]
