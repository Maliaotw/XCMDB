# XCMDB 專案管理與開發指南 (AGENTS.md)

> 最後更新：2026-06-18 (優化 v2)
> 維護：開發團隊 + AI Agents

---

## 一、當前階段與工作進度

### Phase 0: Celery 任務架構重構 (已完成 ✅)

| # | 任務 | 狀態 | 備註 |
|---|------|------|------|
| 0.1 | 建立 `tasks/base.py` - BaseTask 類別 | ✅ 完成 | on_success, on_failure, on_retry, _format_error |
| 0.2 | 建立 `tasks/vm_provision.py` - VM 任務 | ✅ 完成 | sync_guest_vms, create_vm, destroy_vm, vm_destroy_batch |
| 0.3 | 建立 `tasks/asset_sync.py` - iDRAC 同步 | ✅ 完成 | iDRACSync class，移除 hosts/tasks.py 870+ 行硬編碼 |
| 0.4 | 建立 `tasks/audit.py` - 審計任務 | ✅ 完成 | write_operation_log, write_login_log_async, archive_old_audit_logs |
| 0.5 | 建立 `tasks/cleanup.py` - 清理任務 | ✅ 完成 | destroy_failed_vms, remove_expired_tokens |
| 0.6 | 建立 `tasks/__init__.py` - 任務匯出 | ✅ 完成 | 空 package，避免 eager import |
| 0.7 | 重構 `cmdb/celery.py` | ✅ 完成 | 移除 beat_schedule 與 debug_task |
| 0.8 | 建立 `cmdb/beat.py` | ✅ 完成 | 集中管理 Beat schedule |
| 0.9 | 更新 `cmdb/__init__.py` | ✅ 完成 | 匯入 beat module |
| 0.10 | 清理 `vm/tasks.py` wrapper | ✅ 完成 | import from tasks.vm_provision |
| 0.11 | 清理 `hosts/tasks.py` wrapper | ✅ 完成 | import from tasks.asset_sync |
| 0.12 | 清理 `authentication/tasks.py` wrapper | ✅ 完成 | import from tasks.audit, tasks.cleanup |
| 0.13 | 修復 `settings.py` TODO 註解 | ✅ 完成 | 移除 CELERY_TASK_TIME_LIMIT/SoftTimeLimit 註解 |
| 0.14 | 修復 `vm/views.py` 任務路徑 | ✅ 完成 | 更新為 `tasks.create_vm.delay()` |
| 0.15 | 修復 `authentication/views.py` 測試用硬編碼 | ✅ 完成 | 移除 hostname 覆蓋邏輯 |
| 0.16 | 建立 `tasks/rbac.py` - RBAC 任務 | ✅ 完成 | sync_role_permissions, rebuild_role_hierarchies, reset_role_permissions |
| 0.17 | 建立 `tasks/notification.py` - 通知任務 | ✅ 完成 | send_email, send_webhook, send_email_batch, render_email_template |
| 0.18 | `python manage.py test vm` | ✅ 完成 | 測試已整合於 tests/test_models.py |
| 0.19 | `python manage.py test hosts` | ✅ 完成 | 測試已整合於 tests/test_models.py |
| 0.20 | 修復 `authentication/views.py` 登入失敗 KeyError | ✅ 完成 | 改為 `request.data.get("username") or "anonymous"` |
| 0.21 | 修復 `manage.py` Celery 任務載入時機 | ✅ 完成 | 移至 `django.setup()` 之後，移除 apps.py 依賴 |
| 0.22 | 新增 Celery 重試機制 | ✅ 完成 | BaseTask 加入 autoretry_for, retry_backoff, ack_late |
| 0.23 | 統一所有任務使用 BaseTask | ✅ 完成 | 17 個任務全部加上 `base=BaseTask` |
| 0.24 | 新增登入端點速率限制 | ✅ 完成 | DRF throttle 設定 anon/user/auth 三級速率 |
| 0.25 | 優化 #6: ObtainExpiringAuthToken 加 throttle_classes | ✅ 完成 | 加入 AnonRateThrottle 防暴力破解 |
| 0.26 | 優化 #7: 移除 AppConfig.ready() 空方法 | ✅ 完成 | vm, hosts apps.py 清理 empty ready() |
| 0.27 | 優化 #8: 統一任務路徑格式檢查 | ✅ 完成 | 驗證 17 個任務路徑均符合 tasks.<domain>.<func> 格式 |
| 0.28 | 新增 middleware 測試 | ✅ 完成 | tests/test_middleware.py (22 tests) |
| 0.29 | 新增 signals_handlers 測試 | ✅ 完成 | tests/test_signals_handlers.py (15 tests) |
| 0.30 | 修復 exception_handler 測試 | ✅ 完成 | 修正 4 個 test 期望值與 mock 路徑 |

**驗證結果：**
- ✅ `python manage.py check` - 0 issues
- ✅ `python manage.py test` - 210/210 OK (新增 59 tests)
- ✅ 17 個 Celery 任務註冊成功 (vm_provision: 4, asset_sync: 1, audit: 3, cleanup: 2, rbac: 3, notification: 4)
- ✅ Celery worker 透過 `app.conf.update(imports=...)` 自動載入任務
- ✅ DRF throttle 已套用到登入端點
- ✅ Ruff lint - 0 F821/F405 critical errors

---

### Phase 1: Vue 2 → Vue 3 遷移 (待開始)

參考文件：`VUE3_MIGRATION_PLAN.md`

| # | 任務 | 狀態 | 預估 |
|---|------|------|------|
| 1.1 | 建立 migrate-vue3 分支 | ⬜ 待開始 | 1 天 |
| 1.2 | 升級開發環境 (Node.js >= 18) | ⬜ 待開始 | 1 天 |
| 1.3 | Vue CLI → Vite 6 | ⬜ 待開始 | 2-3 天 |
| 1.4 | 核心依賴升級 (vue, vue-router, vuex → pinia) | ⬜ 待開始 | 1 週 |
| 1.5 | Element UI → Element Plus | ⬜ 待開始 | 2-3 週 |
| 1.6 | Options API → Composition API (58 個檔案) | ⬜ 待開始 | 4-6 週 |
| 1.7 | Slot 語法重寫 (~182 處) | ⬜ 待開始 | 1 週 |
| 1.8 | 圖表元件升級 (vue-chartjs v3→v5) | ⬜ 待開始 | 1 週 |
| 1.9 | 測試與 QA | ⬜ 待開始 | 2-3 週 |

**總計預估：13-24 週**

---

### Phase 2: ITIL v4 合規升級 (規劃中)

參考文件：`CMDB_IMPROVEMENT_PLAN.md`

| # | 任務 | 狀態 | 預估 |
|---|------|------|------|
| 2.1 | 建立 CIType, ConfigurationItem, CIRelation 模型 | ⬜ 待開始 | 4 週 |
| 2.2 | 建立 ServiceCatalog, ServiceCI 模型 | ⬜ 待開始 | 4 週 |
| 2.3 | 建立 ChangeRequest 模型 | ⬜ 待開始 | 3 週 |
| 2.4 | 建立 DataQualityMetric 模型 | ⬜ 待開始 | 2 週 |
| 2.5 | 資料遷移腳本 (Host → CI, VM → CI) | ⬜ 待開始 | 2 週 |
| 2.6 | 前端 CI 管理頁面 (Vue 3) | ⬜ 待開始 | 6 週 |

**總計預估：17 週 (4 個月)**

---

## 一、開發工具鏈

### 1.1 程式碼格式化工具

| 語言 | 工具 | 設定檔 | 命令 |
|------|------|--------|------|
| Python | Ruff | `backend/pyproject.toml` | `ruff check .` / `ruff format .` |
| JavaScript | ESLint | `frontend/.eslintrc.js` | `yarn lint` |
| YAML/JSON/Markdown | EditorConfig | `.editorconfig` | 由編輯器自動套用 |

### 1.2 預提交檢查 (pre-commit)

```bash
# 安裝 pre-commit hooks
pip install pre-commit
pre-commit install

# 手動執行所有 hooks
pre-commit run --all-files

# 僅執行特定 hook
pre-commit run ruff --all-files
pre-commit run eslint --all-files
```

Hooks 設定於 `.pre-commit-config.yaml`：
- **ruff** - Python linting + formatting
- **gitleaks** - 防止金鑰洩漏
- **eslint** - JavaScript 程式碼檢查
- **pre-commit-hooks** - 空白字元、檔案結尾、YAML/JSON 格式檢查

### 1.3 測試工具

| 層級 | 工具 | 命令 |
|------|------|------|
| Python 單元測試 | pytest | `python manage.py test <app>` |
| 測試覆蓋率 | coverage | `coverage run --source=backend/manage.py test` |
| 型別檢查 | mypy | `mypy backend/` |

### 1.4 CI/CD

- GitHub Actions 工作流：`.github/workflows/ci.yml`
- 觸發條件：Push / Pull Request
- 執行內容：
  1. Python lint (ruff)
  2. Python tests (pytest)
  3. JavaScript lint (ESLint)

### 1.5 編輯器建議

推薦使用支援 EditorConfig 的編輯器（VS Code、Vim、Neovim），自動套用：
- 4 空間縮排 (Python) / 2 空間縮排 (JS/Vue)
- UTF-8 編碼
- 結尾換行符號
- 自動修剪尾端空白

---

## 二、待辦事項

- [x] 確認 Celery worker 能正常啟動並註冊任務
- [x] 確認 `authentication/views.py` 移除測試用硬編碼不會影響現有功能
- [x] 檢查 `vm/views.py:307` 中 `PeriodicTask.objects.filter(task='vm.tasks.create')` 需更新為 `tasks.vm_provision.create_vm`
  - ✅ 已確認 `vm/views.py:307`、`vm/signal.py:54` 均使用正確路徑 `tasks.vm_provision.create_vm`
  - ✅ 已修復 `hosts/signal.py:57` 舊路徑 `hosts.tasks.idracinfo` → `tasks.asset_sync.sync_idrac_hardware`
- [x] 新增 middleware 測試 (22 tests)
- [x] 新增 signals_handlers 測試 (15 tests)
- [x] 修復 exception_handler 測試 (4 tests)

### 🟡 中優先級 (Important)

- [x] 建立 `tasks/rbac.py` - RBAC 任務
- [x] 建立 `tasks/notification.py` - 通知任務
- [x] 為 vm, hosts 建立基礎測試
- [x] 執行 `python manage.py test` 全量測試 (210/210 OK)
- [ ] 為 vm, hosts 建立完整測試覆蓋

### 🟢 低優先級 (Nice to have)

- [ ] 建立 CI 型別的自動化遷移腳本
- [ ] 開發批量操作 API (bulk_create, bulk_update, bulk_delete)
- [ ] 建立 CI 標籤系統

---

## 三、問題紀錄 (Incident Log)

### INC-001: Celery 任務 eager import 導致 Django app registry 未就緒
- **日期：** 2026-06-17
- **症狀：** `python manage.py check` 報 `AppRegistryNotReady: Apps aren't loaded yet.`
- **原因：** `tasks/__init__.py` 頂層 import 所有任務模組，觸發 `src.pyterraform` → `vm.models` → Django 未準備好
- **解決：** `tasks/__init__.py` 保持空 package，任務透過各 app wrapper 的 lazy import 載入
- **類別：** Bug

### INC-002: `write_login_log_async()` 參數不匹配
- **日期：** 2026-06-17
- **症狀：** `TypeError: write_login_log_async() got an unexpected keyword argument 'username'`
- **原因：** 初始簽名為 `def write_login_log_async(user_id, ip, success, message)`，但 `signals_handlers.py` 傳 `username, ip, type, user_agent, datetime, status, reason`
- **解決：** 改為 `def write_login_log_async(**kwargs)` 以匹配 signals handler 的呼叫方式
- **類別：** Bug

---

## 四、工作流建議

### 4.1 Celery 任務開發流程

1. 任務定義在 `tasks/` 目錄下對應領域檔案
2. 使用 `@shared_task(name='tasks.<領域>.<功能>')` 明確指定 name
3. 使用 `get_task_logger('<領域>')` 取得 logger
4. 各 app 的 `tasks.py` 僅代理 wrapper，不放業務邏輯
5. Beat schedule 集中於 `cmdb/beat.py`
6. **禁止**硬編碼測試資料到任務中
7. 任務只做單個動作，有明確的 input/output 定義

#### Celery 專案結構

```
backend/cmdb/
├── cmdb/                          # Django 專案設定層
│   ├── celery.py                  # Celery app 初始化 (僅 broker/backend)
│   ├── beat.py                    # Beat schedule 集中管理
│   ├── __init__.py                # 匯入 beat module
│   └── settings.py                # Django settings
├── tasks/                         # 集中式 Celery 任務模組
│   ├── __init__.py                # 空 package (avoid eager import)
│   ├── base.py                    # BaseTask, get_task_logger
│   ├── vm_provision.py            # VM 創建/銷毀/同步
│   ├── asset_sync.py              # iDRAC 硬體同步
│   ├── audit.py                   # 審計日誌任務
│   └── cleanup.py                 # 清理任務
├── vm/tasks.py                    # 代理 wrapper
├── hosts/tasks.py                 # 代理 wrapper
└── authentication/tasks.py        # 代理 wrapper
```

#### 任務命名空間

```
tasks.<領域>.<功能>

範例：
tasks.vm_provision.create_vm
tasks.asset_sync.sync_idrac_hardware
tasks.audit.write_operation_log
```

#### Task 定義規範

**禁止：**
- 直接在 `celery.py` 定義任務
- 在各 app 的 `tasks.py` 放業務邏輯
- 硬編碼測試資料到任務中 (hosts/tasks.py 的 700+ 行 sensor 資料是反範例)
- 任務間接呼叫 (a → b → c 鏈式)
- 任務中直接操作 request/response 物件

**建議：**
- 使用 `@shared_task(name='tasks.<領域>.<功能>')` 並明確指定 name
- 使用 `get_task_logger()` 統一日誌
- 任務只做單個動作
- 每個任務有明確的 input/output 定義

### 4.2 Git 工作流建議

```bash
# 新功能：feature/<描述>
git checkout -b feature/celery-architecture

# Bug 修復：fix/<問題簡述>
git checkout -b fix/write-login-log-params

# 階段分支：phase-<階段>/<描述>
git checkout -b phase-0/celery-refactor
git checkout -b phase-1/vue3-migration
```

### 4.3 測試建議

- 每個新任務至少有一個 unit test 驗證 input/output
- 每個新 feature 至少有一個 integration test
- Celery 任務建議使用 `@app.task(bind=True)` 方便測試 mock
- 使用 `celery -A cmdb test -E` 執行 eager mode 測試

### 4.4 Code Review Checklist

- [ ] 任務定義在 `tasks/` 而非 app 的 `tasks.py`
- [ ] Beat schedule 在 `cmdb/beat.py` 而非 `celery.py`
- [ ] 使用 `get_task_logger()` 而非 `logging.getLogger()`
- [ ] 任務有明確的 input/output 定義
- [ ] 沒有硬編碼測試資料
- [ ] 任務間沒有 chain call (a → b → c)
- [ ] 沒有在任務中直接操作 request/response 物件

---

## 五、決策紀錄 (ADR)

### ADR-001: Celery 任務集中式架構
- **日期：** 2026-06-17
- **背景：** 任務分散於 vm/tasks.py, hosts/tasks.py, authentication/tasks.py，beat schedule 硬編碼於 celery.py
- **決策：** 使用集中式 tasks/ 模組，各 app 僅保留 wrapper
- **理由：** 符合 CELERY_ARCHITECTURE.md 規範，便於維護與測試
- **影響：** 需更新所有 app 的 import 路徑

### ADR-002: tasks/__init__.py 不 eager import 任務
- **日期：** 2026-06-17
- **背景：** 頂層 import 所有任務模組導致 Django app registry 未就緒
- **決策：** `tasks/__init__.py` 保持空 package，任務透過 lazy import 載入
- **理由：** 避免循環 import 與 app registry 問題
- **影響：** 任務必須透過各 app wrapper 或直接 import 模組檔案

### ADR-003: write_login_log_async 使用 **kwargs
- **日期：** 2026-06-17
- **背景：** signals handler 傳不同 key 給 task
- **決策：** 使用 `**kwargs` 而非固定參數
- **理由：** signals handler 可能傳不同 key（username, ip, type, status, reason 等）
- **影響：** 失去參數型別檢查，需在函數內部做 validation

### ADR-004: 前端強制使用 Yarn
- **日期：** 2026-06-17
- **背景：** npm 與 yarn lockfile 衝突
- **決策：** 在 package.json 中加入 preinstall hook 阻止 npm install
- **理由：** 確保依賴一致性，避免 package-lock.json 與 yarn.lock 衝突
- **影響：** 開發者需使用 yarn install / yarn dev

### ADR-005: Port 規劃避戰策略
- **日期：** 2026-06-17
- **背景：** 本地開發常與現有服務 (Django 8000, Vue 9528) 衝突
- **決策：** 本地開發 port 分別為 8080/18000/19528
- **理由：** 避免佔用常見的預設 port
- **影響：** 前端 `.env.development` 需對應調整 `VUE_APP_CORE_HOST`

---

## 六、專案結構與關鍵路徑

### 6.1 目錄結構

```
XCMDB/
├── backend/cmdb/                  # Django 專案
│   ├── cmdb/                      # 設定層
│   │   ├── celery.py              # Celery app 初始化 (僅 broker/backend)
│   │   ├── beat.py                # Beat schedule 集中管理
│   │   ├── __init__.py            # 匯入 beat module
│   │   └── settings.py            # Django settings
│   │
│   ├── tasks/                     # 集中式 Celery 任務模組
│   │   ├── __init__.py            # 空 package (avoid eager import)
│   │   ├── base.py                # BaseTask, get_task_logger
│   │   ├── vm_provision.py        # VM 創建/銷毀/同步
│   │   ├── asset_sync.py          # iDRAC 硬體同步
│   │   ├── audit.py               # 審計日誌任務
│   │   ├── cleanup.py             # 清理任務
│   │   ├── rbac.py                # RBAC 任務
│   │   └── notification.py        # 通知任務
│   │
│   ├── vm/                        # 虛擬化與建置 App
│   │   ├── tasks.py               # 任務代理 wrapper
│   │   ├── models.py              # Instance, Cluster, DataStore, NetWork, VM
│   │   └── views.py               # VM API endpoints
│   │
│   ├── hosts/                     # 伺服器與主機 App
│   │   ├── tasks.py               # 任務代理 wrapper
│   │   ├── models.py              # Host, CPU, NIC, Disk, Memory, IDRAC
│   │   └── views.py               # Host API endpoints
│   │
│   ├── authentication/            # 用戶認證模組
│   │   ├── tasks.py               # 任務代理 wrapper
│   │   ├── views.py               # LDAP/API Token auth
│   │   └── signals_handlers.py    # Login signals
│   │
│   ├── assets/                    # 資產管理 App
│   │   ├── models.py              # Asset, IDC, Rack, RackUnit
│   │   └── views.py
│   │
│   ├── tasks/                     # Celery 任務執行日誌
│   └── common/                    # 共用模組
│       ├── models.py              # OperationLog, create_one helper
│       └── middleware.py          # RequestLoggingMiddleware
│
├── frontend/                      # Vue 2 + Element UI 前端
│   ├── package.json               # Yarn 強制 (preinstall hook)
│   ├── vue.config.js              # 開發埠 19528
│   └── src/
│       ├── router.js              # 前端路由
│       └── views/                 # 頁面元件
│
├── client/                        # 主機端 Agent
│   └── (lshw, psutil 上報)
│
├── compose/                       # Docker 容器配置
│   ├── django/
│   ├── openresty/
│   └── docker-compose.yml
│
├── docs/                          # 專案文件
│   ├── CELERY_ARCHITECTURE.md     # Celery 任務架構規範
│   ├── CMDB_IMPROVEMENT_PLAN.md   # ITIL v4 合規路線圖
│   └── VUE3_MIGRATION_PLAN.md     # Vue 2 → Vue 3 遷移計畫
│
├── GEMINI.md                      # 專案架構與核心模組解析
├── AGENTS.md                      # 本文件：專案管理與開發指南
├── README.md                      # 快速入門
├── Makefile                       # 開發工具 (install, dev)
└── pyproject.toml                 # uv 後端依賴
```

### 6.2 核心資料模型

#### 資產多型關係 (GenericForeignKey)

| 模型 | 說明 | 關聯 |
|------|------|------|
| `Asset` | 統一資產抽象 | GenericForeignKey → Host, NetworkDevice, Storage |
| `IDC` | 機房表 | IDC → Rack (1:N) |
| `Rack` | 機櫃表 | Rack → RackUnit (1:N) |
| `NetworkDevice` | 網路設備 | 路由器、交換機、防火牆 |
| `Storage` | 存儲設備 | StorageCtl, StorageNic, StorageDisk |

#### 伺服器與硬體

| 模型 | 說明 | 關聯 |
|------|------|------|
| `Host` | 主機核心表 | cate: 1=伺服器, 2=虛擬機 |
| `CPU / NIC / Disk / Memory` | 硬體組件詳情 | Host (N:1) |
| `IDRAC` | Dell iDRAC 管理 IP | 關聯 PeriodicTask |
| `CmdRecord / RunUser` | 遠端執行指令與金鑰 | - |

#### 虛擬化與建置

| 模型 | 說明 | 關聯 |
|------|------|------|
| `Instance` | VMware VM 實例 | Host, Cluster, DataStore, NetWork |
| `Cluster` | ESXi 主機集群 | NetWork (M:N) |
| `DataStore` | vSphere 儲存池 | - |
| `NetWork` | vSphere Portgroup/VLAN | - |
| `VM` | VM 建置任務記錄 | Instance (1:1 可選) |

### 6.3 關鍵 Port 規劃

| 服務 | 本地開發 Port | 生產 Port |
|------|--------------|-----------|
| OpenResty/Nginx | 8080 | 80 |
| Django API | 18000 | 8000 |
| Vue 前端 | 19528 | 9528 |
| Redis | 6379 | 6379 |
| MySQL/PostgreSQL | 3306/5432 | 3306/5432 |

---

## 七、開發者快速入門

### 7.1 環境需求

| 元件 | 版本要求 |
|------|---------|
| Python | >= 3.8 |
| Node.js | >= 14.x (遷移 Vue 3 需 >= 18) |
| MySQL | 5.7 (開發環境) |
| PostgreSQL | (生產環境) |
| Redis | 5.0+ |
| uv | 後端依賴管理工具 |

### 7.2 安裝與啟動

```bash
# 1. 一鍵安裝前後端依賴，並完成資料庫初始化與 Demo 數據富化
make install

# 2. 一鍵並行啟動 Django API、Vue UI 與 Celery Worker 開發服務
make dev

# 3. 獨立啟動各項服務
python manage.py runserver 0.0.0.0:18000  # Django API (port 18000)
cd frontend && yarn dev                    # Vue (port 19528)
celery -A cmdb worker --loglevel=info      # Celery Worker
celery -A cmdb beat --loglevel=info        # Celery Beat scheduler
```

### 7.3 Docker 部署

```bash
# 開發環境
docker network create cmdb
docker-compose -f docker-compose-dev.yml up -d

# 生產環境
docker network create ops
docker-compose up -d
```

### 7.4 執行檢查

```bash
# Django check
python manage.py check

# 執行測試
python manage.py test <app>
python manage.py test   # 全部測試

# 查看已註冊任務
celery -A cmdb list_tasks

# 查看 Beat schedule
celery -A cmdb inspect schedule

# 查看 Worker 狀態
celery -A cmdb inspect active
celery -A cmdb inspect stats
```

### 7.5 依賴管理 (uv)

```bash
# 新增套件
cd backend && uv add <package-name>

# 生成 requirements.txt (Docker 部署用)
cd backend && uv pip compile pyproject.toml -o requirements.txt
```

**注意：** `django-celery-beat==2.0.0` 要求 `django-timezone-field>=4.0` → `django>=2.2`，但專案使用 `django==2.1.4`。已在 `pyproject.toml` 中用 `[tool.uv.override-dependencies]` 強制鎖定 `django-timezone-field==3.1`。

---

## 八、常見陷阱與注意事項

### 8.1 Celery 任務

1. **不要**在 `tasks/__init__.py` 頂層 import 所有任務
2. **不要**在各 app 的 `tasks.py` 放業務邏輯
3. **不要**在 `celery.py` 放 beat schedule
4. **不要**硬編碼測試資料到任務中
5. **務必**使用 `get_task_logger()` 而非 `logging.getLogger()`

### 8.2 前端

1. **務必**使用 Yarn，不要用 npm
2. 前端 API 連線使用 `VUE_APP_CORE_HOST=http://127.0.0.1:18000`
3. Node 17+ 需設置 `NODE_OPTIONS=--openssl-legacy-provider`
4. Vue 2 已於 2023/12/31 EOL，建議規劃 Vue 3 遷移

### 8.3 資料庫

1. 開發環境使用 MySQL，生產環境使用 PostgreSQL
2. 資料庫連線資訊在 `backend/.env` 設定
3. `STATIC_URL = '/static/'`, `STATIC_ROOT` 為 `cmdb/static/`

### 8.4 任務開發

- 任務內的 model import 必須使用 lazy import (函數內部 import)
- 同步邏輯建議封裝在 class 中 (如 iDRACSync)，task 僅作為入口
- 各組件同步用統一 helper 方法處理 upsert

---

## 九、參考文件索引

| 文件 | 說明 | 關鍵內容 |
|------|------|----------|
| `CELERY_ARCHITECTURE.md` | Celery 任務架構規範 | 任務命名、分類、執行模式 |
| `CMDB_IMPROVEMENT_PLAN.md` | ITIL v4 合規路線圖 | CI 類型、服務目錄、生命週期 |
| `VUE3_MIGRATION_PLAN.md` | Vue 2 → Vue 3 遷移計畫 | 依賴升級、Composition API、Vite |
| `ARCHITECTURE.md` | 專案架構概覽 | 目錄結構、技術栈 |
| `GEMINI.md` | 專案解析與核心模組 | 資料模型、自動化流程、依賴管理 |
| `AGENTS.md` (本文件) | 專案管理與開發指南 | 進度追蹤、問題紀錄、工作流 |
| `README.md` | 快速入門 | 安裝、設定、常見問題 |

---

## 十、維護說明

本文檔為**動態文件**，應在以下情況更新：

1. **階段完成** - 勾選已完成任務，更新狀態
2. **發現問題** - 新增 INC-xxx 項目
3. **做出決策** - 新增 ADR-xxx 項目
4. **調整優先級** - 更新待辦事項順序
5. **更新參考** - 新增/移除參考文件

> 所有變更請在「最後更新」欄位更新日期，並保留歷史紀錄以利追溯。
