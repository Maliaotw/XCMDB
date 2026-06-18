"""RBAC 相關任務 - 角色權限同步與層級重建"""

import json

from celery import shared_task

from .base import BaseTask, get_task_logger

logger = get_task_logger("rbac")

# 預設角色層級 (由高到低)
ROLE_HIERARCHY = ["admin", "operator", "auditor", "visitor"]

# 預設角色權限 (若資料庫不存在時自動建立)
DEFAULT_ROLE_PERMISSIONS = {
    "admin": {
        "menus": json.dumps(["Host", "VM", "Asset", "Network", "Dashboard", "Settings", "Audit", "Users", "Roles"]),
        "actions": json.dumps([
            "host:*", "vm:*", "asset:*", "network:*",
            "dashboard:read",
            "settings:read", "settings:update",
            "audit:read",
            "users:create", "users:read", "users:update", "users:delete",
            "roles:create", "roles:read", "roles:update", "roles:delete",
        ]),
    },
    "operator": {
        "menus": json.dumps(["Host", "VM", "Asset", "Network", "Dashboard", "Audit"]),
        "actions": json.dumps([
            "host:read", "host:create", "host:update", "host:delete",
            "vm:read", "vm:create", "vm:update", "vm:destroy",
            "asset:read",
            "network:read",
            "dashboard:read",
            "audit:read",
        ]),
    },
    "auditor": {
        "menus": json.dumps(["Host", "VM", "Asset", "Network", "Dashboard", "Audit"]),
        "actions": json.dumps([
            "host:read",
            "vm:read",
            "asset:read",
            "network:read",
            "dashboard:read",
            "audit:read",
        ]),
    },
    "visitor": {
        "menus": json.dumps(["Dashboard"]),
        "actions": json.dumps([
            "dashboard:read",
        ]),
    },
}


@shared_task(name="tasks.rbac.sync_role_permissions", base=BaseTask)
def sync_role_permissions(role_name, menus=None, actions=None):
    """同步指定角色的權限設定
    
    Args:
        role_name: 角色名稱
        menus: 菜單權限列表 (JSON string or list)
        actions: 動作權限列表 (JSON string or list)
    
    Returns:
        dict: 同步結果
    """
    from common.models import RolePermission

    try:
        if menus is not None and isinstance(menus, list):
            menus = json.dumps(menus)
        if actions is not None and isinstance(actions, list):
            actions = json.dumps(actions)

        if not menus and not actions:
            return {"status": 400, "data": "menus 或 actions 至少需要提供一項"}

        obj, created = RolePermission.objects.get_or_create(role=role_name)

        if menus is not None:
            obj.menus = menus
        if actions is not None:
            obj.actions = actions

        obj.save()
        status = "建立" if created else "更新"
        logger.info(f"{status} 角色權限: {role_name}")
        return {"status": 200, "data": f"{status}成功: {role_name}"}

    except Exception as e:
        logger.error(f"同步角色權限失敗: {role_name} - {e}")
        return {"status": 500, "data": f"同步失敗: {str(e)}"}


@shared_task(name="tasks.rbac.rebuild_role_hierarchies", base=BaseTask)
def rebuild_role_hierarchies(force=False):
    """重建角色層級與預設權限
    
    確保所有預設角色都存在且權限正確。
    
    Args:
        force: 是否強制覆蓋現有角色的預設權限 (預設 False)
    
    Returns:
        dict: 重建結果
    """
    from common.models import RolePermission

    created = []
    updated = []
    skipped = []

    for role_name in ROLE_HIERARCHY:
        perms = DEFAULT_ROLE_PERMISSIONS.get(role_name)
        if not perms:
            skipped.append(role_name)
            continue

        obj, created_flag = RolePermission.objects.get_or_create(role=role_name)

        if created_flag:
            obj.menus = perms["menus"]
            obj.actions = perms["actions"]
            obj.save()
            created.append(role_name)
            logger.info(f"建立預設角色: {role_name}")
        else:
            if force:
                old_menus = obj.menus
                old_actions = obj.actions
                obj.menus = perms["menus"]
                obj.actions = perms["actions"]
                obj.save()
                changed = (obj.menus != old_menus) or (obj.actions != old_actions)
                if changed:
                    updated.append(role_name)
                    logger.info(f"覆蓋角色權限: {role_name}")
                else:
                    skipped.append(role_name)
            else:
                skipped.append(role_name)

    result = {
        "status": 200,
        "data": {
            "created": created,
            "updated": updated,
            "skipped": skipped,
            "hierarchy": ROLE_HIERARCHY,
            "message": f"建立 {len(created)} 角色, 更新 {len(updated)} 角色, 跳過 {len(skipped)} 角色",
        },
    }

    logger.info(f"角色層級重建完成: created={created}, updated={updated}, skipped={skipped}")
    return result


@shared_task(name="tasks.rbac.reset_role_permissions", base=BaseTask)
def reset_role_permissions():
    """重置所有預設角色的權限為預設值"""
    return rebuild_role_hierarchies(force=True)
