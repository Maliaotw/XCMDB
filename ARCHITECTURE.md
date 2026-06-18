# XCMDB Architecture

XCMDB is an IT asset management platform built on Django with Celery for async tasks.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.x |
| Database | PostgreSQL |
| Cache / Queue | Redis |
| Tasks | Celery |
| Frontend | Vue.js |

## Directory Structure

```
XCMDB/
├── backend/cmdb/                  # Django project
│   ├── cmdb/                      # Settings & config
│   │   ├── celery.py              # Celery app initialization
│   │   ├── beat.py                # Task schedule definitions
│   │   └── __init__.py            # Celery app loader
│   │
│   ├── apps/                      # Business logic
│   │   ├── tasks/                 # All async task definitions
│   │   │   ├── base.py            # Base task class (logging, retry)
│   │   │   ├── asset_sync.py      # iDRAC/SNMP hardware sync
│   │   │   ├── vm_provision.py    # VM create/destroy/sync
│   │   │   ├── audit.py           # Operation log writing
│   │   │   ├── rbac.py            # Role/permission sync
│   │   │   └── cleanup.py         # Expired token/log cleanup
│   │   └── common/                # Shared utilities
│   │
│   ├── hosts/                     # Host management (iDRAC)
│   ├── vm/                        # VM management (ESXi/vSphere)
│   ├── authentication/            # Auth & login logging
│   └── roles/                     # RBAC
│
├── frontend/                      # Vue.js frontend
└── docs/                          # Architecture & conventions
```

## Celery Architecture

### Flow

```
HTTP Request
    │
    ├── Synchronous: Direct view response
    │
    └── Asynchronous: Celery Task
         ├── View → apps.tasks.<category>.<func>
         ├── Redis queue
         └── Worker executes → writes to DB
```

### Key Rules

1. **No business logic in views** - delegate to celery tasks
2. **Centralize tasks** - all tasks in `apps/tasks/`, one per business domain
3. **Centralize schedule** - all cron in `cmdb_project/beat.py`
4. **Standard logging** - use `get_task_logger()` from `apps.tasks.base`
5. **Never hardcode test data** - sync from actual APIs (iDRAC, vCenter)

### Task Categories

| Category | Category | Trigger |
|----------|----------|---------|
| `sync_idrac_hardware` | `sync_role_permissions` | HTTP request |
| `create_vm` | `write_operation_log` | HTTP request |
| `destroy_vm` | `send_email` | HTTP request |
| `sync_guest_vms` (cron 10m) | `archive_audit_logs` (cron daily) | Beat scheduler |

### Execution Modes

- **Eager (development)**: Tasks run inline, useful for testing
- **Async (production)**: Tasks go through Redis broker to workers

```bash
# Start worker
celery -A cmdb_project worker -l info

# Start scheduler
celery -A cmdb_project beat -l info

# Start both
celery -A cmdb_project worker -l info -B
```

## Data Model

### Core Entities

- **Host**: Physical servers managed via iDRAC
- **VM (Instance)**: Virtual machines managed via vCenter
- **NetWork / Cluster / DataStore**: VM infrastructure
- **Role / Permission / RolePermission**: RBAC
- **OperationLog**: Audit trail for all changes

## Integration Points

- **Dell iDRAC**: Hardware inventory sync (CPU, Memory, Disk, NIC, RAID)
- **VMware vSphere**: VM inventory & lifecycle management
- **Terraform**: VM provisioning
- **Redis**: Message broker & cache
- **PostgreSQL**: Primary database
