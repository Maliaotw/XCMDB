# CMDB 改進計劃 (ITIL v4 合規路線圖)

> 基於 XCMDB 現有架構 (Django 2.1.4 / Vue 2.6.4) 的 ITIL v4 & ISO 20000 合規升級方案

---

## 一、差距分析 (Gap Analysis)

| 類別 | ITIL v4 要求 | 現狀 | 嚴重程度 |
|------|-------------|------|----------|
| CI 類型架構 | 支援多種 CI 類型與擴充欄位 | Host/Instance/NetworkDevice 為獨立模型，無法擴充 | 🔴 Critical |
| CI 關係 | 需支援雙向依賴關係 (A depends on B) | 無 CI 間關係定義 | 🔴 Critical |
| 服務目錄 | Service Catalog 是 CMDB 核心 | 不存在 Service Catalog | 🔴 Critical |
| 生命週期管理 | CI 需有標準狀態機 (Create → Active → Retired) | 無狀態追蹤 | 🟡 High |
| 審計日誌 | 所有 CI 變更需有不可變審計紀錄 | Host 有 `update_history` 但非標準化 | 🟡 High |
| 資料品質 | 需有自動資料品質指標 (Completeness, Freshness) | 無 | 🟡 High |
| 服務拓撲 | 服務 → CI 映射、拓撲圖 | 完全缺失 | 🟡 High |
| 變更管理整合 | Change Request 觸發 CI 狀態變更 | 完全缺失 | 🟡 High |
| 標籤與分組 | 支援動態分組與自訂標籤 | 僅有基本關聯 | 🟢 Medium |
| 批量操作 | 支援 CI 的批量建立/更新/刪除 | 需前端自行實現 | 🟢 Medium |

---

## 二、核心模型設計

### 2.1 ConfigurationItem (CI)

所有硬體、VM、網路設備統一使用此抽象模型：

```python
# backend/cmdb/models.py

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CIType(models.Model):
    """CI 類型定義 - 類似資料庫表結構"""
    name = models.CharField("名稱", max_length=128, unique=True)
    code = models.SlugField("代碼", unique=True)  # host, vm, router, etc.
    description = models.TextField("描述", blank=True)

    # 動態欄位定義 (JSON Schema 格式)
    schema_fields = models.JSONField("欄位定義", default=list, blank=True)
    # 範例: [{"name": "os_version", "type": "string", "required": false}]

    # 繼承關係 (CIType 可層級化)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE,
        related_name="child_types"
    )

    # 列表顯示與表單欄位
    list_display = models.JSONField("列表欄位", default=list)
    filter_fields = models.JSONField("過濾欄位", default=list)
    create_form_fields = models.JSONField("建立表單欄位", default=list)

    is_active = models.BooleanField("啟用", default=True)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        verbose_name = "CI 類型"
        verbose_name_plural = "CI 類型"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class ConfigurationItem(models.Model):
    """通用 CI 實例"""
    LIFE_CYCLE_STATUS = [
        ("draft", "草稿"),
        ("active", "使用中"),
        ("maintenance", "維護中"),
        ("retired", "已停用"),
        ("archive", "已封存"),
    ]

    name = models.CharField("名稱", max_length=255)
    serial_number = models.CharField("序列號", max_length=128, blank=True)
    ip_address = models.GenericIPAddressField("IP 位址", blank=True, null=True)

    # 關聯的 CI 類型
    ci_type = models.ForeignKey(
        CIType, on_delete=models.PROTECT, related_name="instances"
    )

    # 通用 JSON 欄位 - 儲存各 CI 類型的特有資料
    attributes = models.JSONField("屬性資料", default=dict, blank=True)

    # 生命週期狀態
    status = models.CharField("狀態", max_length=20, choices=LIFE_CYCLE_STATUS, default="draft")

    # 通用位置資訊 (可被各 CI 類型擴充)
    location = models.CharField("位置", max_length=255, blank=True)

    # 擁有者
    owner = models.CharField("擁有者", max_length=128, blank=True)
    department = models.CharField("部門", max_length=128, blank=True)

    is_active = models.BooleanField("啟用", default=True)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        verbose_name = "配置項目"
        verbose_name_plural = "配置項目"
        indexes = [
            models.Index(fields=["ci_type", "status"]),
            models.Index(fields=["serial_number"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ci_type}: {self.name}"


class CIRelation(models.Model):
    """CI 之間關係 - 支援有向邊"""
    RELATION_TYPE = [
        # 硬體依賴
        ("depends_on", "依賴於"),
        ("powers", "供電"),
        ("connects_to", "連接到"),
        # 虛擬化
        ("runs_on", "運行於"),
        ("migrates_to", "遷移至"),
        # 服務層級
        ("provides", "提供"),
        ("consumes", "消費"),
        ("relies_on", "依賴"),
        # 邏輯關係
        ("belongs_to", "屬於"),
        ("maps_to", "對應到"),
    ]

    parent_ci = models.ForeignKey(
        ConfigurationItem, on_delete=models.CASCADE,
        related_name="parent_relations"
    )
    child_ci = models.ForeignKey(
        ConfigurationItem, on_delete=models.CASCADE,
        related_name="child_relations"
    )
    relation_type = models.CharField("關係類型", max_length=32, choices=RELATION_TYPE)
    description = models.TextField("描述", blank=True)

    # 拓撲圖繪製資訊 (可選)
    graph_position_x = models.FloatField("圖位置 X", default=0)
    graph_position_y = models.FloatField("圖位置 Y", default=0)

    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        verbose_name = "CI 關係"
        verbose_name_plural = "CI 關係"
        constraints = [
            models.UniqueConstraint(
                fields=["parent_ci", "child_ci", "relation_type"],
                name="unique_ci_relation"
            ),
        ]
        indexes = [
            models.Index(fields=["parent_ci", "relation_type"]),
            models.Index(fields=["child_ci", "relation_type"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.parent_ci} --[{self.relation_type}]--> {self.child_ci}"

    def get_reverse_relation(self):
        """取得反向關係 (A→B 的反向是 B→A)"""
        try:
            return CIRelation.objects.get(
                parent_ci=self.child_ci,
                child_ci=self.parent_ci,
                relation_type=self.relation_type.replace("_on", "_from").replace("_to", "_from")
            )
        except CIRelation.DoesNotExist:
            return None


class ConfigurationItemHistory(models.Model):
    """CI 不可變審計紀錄"""
    ci = models.ForeignKey(ConfigurationItem, on_delete=models.CASCADE, related_name="audit_log")
    action = models.CharField("操作類型", max_length=32)
    # create, update, delete, status_change, relation_change
    old_values = models.JSONField("舊值", default=dict, blank=True)
    new_values = models.JSONField("新值", default=dict, blank=True)
    actor = models.CharField("操作者", max_length=128)
    reason = models.TextField("原因", blank=True)

    created_at = models.DateTimeField("建立時間", auto_now_add=True)

    class Meta:
        verbose_name = "CI 審計紀錄"
        verbose_name_plural = "CI 審計紀錄"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["ci", "action"]),
            models.Index(fields=["created_at"]),
        ]
```

### 2.2 Service Catalog (服務目錄)

```python
# backend/cmdb/models.py (續)


class ServiceCatalog(models.Model):
    """服務目錄 - ITIL Service Catalog 核心"""
    SERVICE_TYPE = [
        ("application", "應用程式"),
        ("infrastructure", "基礎設施"),
        ("database", "資料庫"),
        ("network", "網路服務"),
        ("security", "安全服務"),
        ("other", "其他"),
    ]

    name = models.CharField("服務名稱", max_length=255)
    code = models.SlugField("服務代碼", unique=True)
    description = models.TextField("描述", blank=True)
    service_type = models.CharField("服務類型", max_length=32, choices=SERVICE_TYPE)

    # 服務生命週期
    status = models.CharField("狀態", max_length=20, default="draft",
                              choices=ConfigurationItem.LIFE_CYCLE_STATUS)

    # 服務擁有者
    owner = models.CharField("負責人", max_length=128)
    department = models.CharField("部門", max_length=128, blank=True)

    # SLA 相關
    sla_uptime = models.FloatField("目標可用性 (%)", default=99.9)
    sla_response_time = models.IntegerField("回應時間 (分鐘)", default=15)

    is_active = models.BooleanField("啟用", default=True)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        verbose_name = "服務目錄"
        verbose_name_plural = "服務目錄"
        ordering = ["name"]

    def __str__(self):
        return f"[{self.service_type}] {self.name}"


class ServiceCI(models.Model):
    """服務與 CI 的關聯 - 建立服務拓撲"""
    service = models.ForeignKey(
        ServiceCatalog, on_delete=models.CASCADE, related_name="supported_cis"
    )
    ci = models.ForeignKey(
        ConfigurationItem, on_delete=models.CASCADE, related_name="supports_services"
    )

    # 關聯角色 - 該 CI 在服務中扮演什麼角色
    role = models.CharField("角色", max_length=128, blank=True)
    # 例如: "Web Server", "Load Balancer", "Database Instance"

    is_primary = models.BooleanField("主要 CI", default=False)
    priority = models.IntegerField("優先級", default=1)

    created_at = models.DateTimeField("建立時間", auto_now_add=True)

    class Meta:
        verbose_name = "服務-CI 關聯"
        verbose_name_plural = "服務-CI 關聯"
        constraints = [
            models.UniqueConstraint(
                fields=["service", "ci"],
                name="unique_service_ci"
            ),
        ]
        indexes = [
            models.Index(fields=["service", "is_primary"]),
            models.Index(fields=["ci"]),
        ]

    def __str__(self):
        return f"{self.service}: {self.ci}"
```

### 2.3 Change Management Integration (變更管理整合)

```python
# backend/cmdb/models.py (續)


class ChangeRequest(models.Model):
    """變更請求 - 與 CMDB 整合"""
    PRIORITY = [
        ("low", "低"),
        ("medium", "中"),
        ("high", "高"),
        ("critical", "緊急"),
    ]

    REQUEST_TYPE = [
        ("standard", "標準變更"),
        ("normal", "一般變更"),
        ("emergency", "緊急變更"),
    ]

    title = models.CharField("變更標題", max_length=255)
    description = models.TextField("描述")
    priority = models.CharField("優先級", max_length=20, choices=PRIORITY)
    request_type = models.CharField("變更類型", max_length=20, choices=REQUEST_TYPE)

    # 生命週期狀態
    STATUS_CHOICES = [
        ("requested", "已請求"),
        ("review", "審核中"),
        ("approved", "已核准"),
        ("implemented", "已執行"),
        ("closed", "已關閉"),
        ("rejected", "已拒絕"),
    ]
    status = models.CharField("狀態", max_length=20, choices=STATUS_CHOICES, default="requested")

    requested_by = models.CharField("申請者", max_length=128)
    approved_by = models.CharField("核准者", max_length=128, blank=True)

    # 影響範圍
    affected_cis = models.ManyToManyField(
        ConfigurationItem, blank=True, related_name="change_requests"
    )

    # 執行時間窗口
    start_time = models.DateTimeField("開始時間", blank=True, null=True)
    end_time = models.DateTimeField("結束時間", blank=True, null=True)

    # 後評
    post_implement_review = models.TextField("執行後評估", blank=True)
    success = models.BooleanField("是否成功", null=True)

    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        verbose_name = "變更請求"
        verbose_name_plural = "變更請求"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.status}] {self.title}"
```

### 2.4 Data Quality & Metrics (資料品質與指標)

```python
# backend/cmdb/models.py (續)


class DataQualityMetric(models.Model):
    """CMDB 資料品質指標"""
    METRIC_TYPE = [
        ("completeness", "完整性"),
        ("accuracy", "準確性"),
        ("freshness", "新鮮度"),
        ("consistency", "一致性"),
    ]

    ci_type = models.ForeignKey(CIType, on_delete=models.CASCADE, related_name="quality_metrics")
    metric_type = models.CharField("指標類型", max_length=32, choices=METRIC_TYPE)
    metric_name = models.CharField("指標名稱", max_length=128)
    score = models.FloatField("分數 (0-100)")
    total_count = models.IntegerField("總數")
    valid_count = models.IntegerField("有效數")

    last_calculated = models.DateTimeField("最後計算時間")
    created_at = models.DateTimeField("建立時間", auto_now_add=True)

    class Meta:
        verbose_name = "資料品質指標"
        verbose_name_plural = "資料品質指標"
        ordering = ["-last_calculated"]

    def __str__(self):
        return f"{self.ci_type}: {self.metric_name} = {self.score}%"
```

---

## 三、資料遷移策略

### Phase 1: 現有模型 → CIType/ConfigurationItem

```
┌─────────────────────┐       ┌──────────────────────┐
│  現有模型 (Host, VM) │       │   新模型 (CI 架構)    │
├─────────────────────┤       ├──────────────────────┤
│ Host                │       │ CIType(code='host')  │
│ ├ cpu, memory, ...  │ ──►   │   └ schema_fields    │
│ ├ nic, disk, ...    │       │                      │
│ └ idrac_info        │       │ ConfigurationItem    │
│                     │       │ ├ ci_type → CIType   │
│ Instance            │       │ ├ attributes (JSON)  │
│ ├ vsphere_ref       │       │ └ status, owner, ... │
│ └ vm_attributes     │ ──►   │                      │
│                     │       │ CIRelation           │
│ NetworkDevice       │       │ ├ parent_ci          │
│ ├ snmp_info         │       │ ├ child_ci           │
│ └ config_file       │ ──►   │ └ relation_type      │
└─────────────────────┘       └──────────────────────┘
```

**遷移步驟：**

1. **建立新模型**：`CIType`, `ConfigurationItem`, `CIRelation` 等。
2. **建立遷移腳本** (`migrate_existing_to_ci`)：
   - 讀取所有 `Host` 記錄 → 建立 `CIType(code='host')`
   - 將 `Host` 資料映射到 `ConfigurationItem(attributes={...})`
   - 讀取所有 `Instance` 記錄 → 建立 `CIType(code='vm')`
   - 將 `Instance` 資料映射到 `ConfigurationItem(attributes={...})`
3. **建立雙寫層** (雙向同步，可選)：
   - 使用 Django signal 在 `Host.save()` 時自動同步到 `ConfigurationItem`
4. **切換前端路由**：將 `/hosts/` 和 `/instances/` 轉向新的 `/cis/` 頁面
5. **確認無誤後停用**：將 `Host` 和 `Instance` 標記為 `is_active=False`
6. **清理舊模型** (Phase 3)：`Host`, `Instance`, `NetworkDevice` 模型

### Phase 2: 服務目錄與拓撲

- 建立 `ServiceCatalog` 與 `ServiceCI` 關聯表
- 開發服務拓撲圖頁面 (基於 ECharts Graph)
- 開發服務→CI 下鑽功能

### Phase 3: 清理與優化

- 刪除已停用的 `Host`, `Instance` 模型
- 統一 `CIListView`、`CIViewSet` 作為唯一入口
- 開發批量操作 API (bulk_create, bulk_update, bulk_delete)
- 開發標籤系統 (`CITag`, `CITagMapping`)

---

## 四、前端改動

### 4.1 頁面改動

| 現有頁面 | 新頁面 | 備註 |
|---------|--------|------|
| `/hosts/` | `/cis/?type=host` | 統一 CI 列表，依 type 過濾 |
| `/instances/` | `/cis/?type=vm` | 統一 CI 列表，依 type 過濾 |
| `/assets/` | 保留但整合進 CI 瀏覽 | Assets 可視為 CI 的子集 |
| (新增) | `/services/` | 服務目錄管理 |
| (新增) | `/services/:id/topology` | 服務拓撲圖 |
| (新增) | `/cis/:id/history` | CI 審計紀錄 |
| (新增) | `/changes/` | 變更請求管理 |

### 4.2 通用 CI 頁面設計

```vue
<!-- frontend/src/views/ci/CIMaster.vue -->
<template>
  <div class="ci-master">
    <div class="ci-header">
      <el-breadcrumb>
        <el-breadcrumb-item :to="{ path: '/cis' }">CI 清單</el-breadcrumb-item>
        <el-breadcrumb-item>{{ ciType.name }}</el-breadcrumb-item>
        <el-breadcrumb-item>{{ ci.name }}</el-breadcrumb-item>
      </el-breadcrumb>

      <el-button-group>
        <el-button @click="editMode = true">編輯</el-button>
        <el-button type="danger" @click="changeStatus('retired')">停用</el-button>
        <el-button @click="viewHistory">審計紀錄</el-button>
      </el-button-group>
    </div>

    <!-- 動態表單 - 依 CIType 渲染不同欄位 -->
    <el-form :model="ciData" v-if="editMode">
      <el-form-item v-for="field in ciType.schema_fields" :key="field.name">
        <component
          :is="getFieldComponent(field)"
          v-model="ciData[field.name]"
          :field="field"
        />
      </el-form-item>
    </el-form>

    <!-- 關聯關係 -->
    <div class="ci-relations">
      <h3>關聯 CI</h3>
      <ci-relation-tree :ci-id="ci.id" />
    </div>

    <!-- 關聯服務 -->
    <div class="ci-services">
      <h3>關聯服務</h3>
      <el-table :data="ci.services">
        <el-table-column prop="service.name" label="服務名稱" />
        <el-table-column prop="role" label="角色" />
      </el-table>
    </div>

    <!-- 生命週期狀態 -->
    <div class="ci-lifecycle">
      <h3>生命週期</h3>
      <el-timeline>
        <el-timeline-item
          v-for="log in auditLogs"
          :key="log.id"
          :timestamp="log.created_at"
        >
          {{ log.action }} - {{ log.reason }}
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>
```

---

## 五、API 設計

### 5.1 CI 核心 API

```
GET    /api/ci/types/                  # 取得所有 CI 類型
GET    /api/ci/types/:id/              # 取得 CI 類型詳情 (含 schema)
POST   /api/ci/types/                  # 建立 CI 類型
PUT    /api/ci/types/:id/              # 更新 CI 類型
DELETE /api/ci/types/:id/              # 停用 CI 類型

GET    /api/cis/                       # CI 列表 (支援 type/status/tag 過濾)
POST   /api/cis/                       # 建立 CI
GET    /api/cis/:id/                   # CI 詳情
PUT    /api/cis/:id/                   # 更新 CI
DELETE /api/cis/:id/                   # 停用 CI
PATCH  /api/cis/:id/status/            # 變更 CI 狀態

POST   /api/cis/:id/relations/         # 建立 CI 關係
DELETE /api/cis/:id/relations/:rid/    # 移除 CI 關係
GET    /api/cis/:id/relations/         # 取得 CI 所有關係
GET    /api/cis/:id/topology/          # 取得 CI 拓撲子圖

POST   /api/cis/:id/history/           # 取得 CI 審計紀錄
POST   /api/cis/bulk/                  # 批量建立/更新
```

### 5.2 服務目錄 API

```
GET    /api/services/                  # 服務目錄清單
POST   /api/services/                  # 建立服務
GET    /api/services/:id/              # 服務詳情
GET    /api/services/:id/topology/     # 服務拓撲 (所有關聯 CI + 關係)
PUT    /api/services/:id/              # 更新服務
```

### 5.3 資料品質 API

```
GET    /api/quality/                   # 整體資料品質報告
GET    /api/quality/:ci_type/          # 指定 CI 類型的品質指標
POST   /api/quality/calculate/         # 觸發重新計算
```

---

## 六、執行時間表

### Phase 0: 準備 (2 週)
- [ ] 建立新模型檔案
- [ ] 開發基礎 CRUD API
- [ ] 設定 CI 類型管理頁面 (後台)

### Phase 1: 核心 CMDB 模型 (4 週)
- [ ] CIType + schema_fields 動態欄位系統
- [ ] ConfigurationItem 統一模型
- [ ] CIRelation 關係模型 (支援拓撲)
- [ ] 資料遷移腳本 (Host → CI, VM → CI)
- [ ] 通用 CI 管理頁面

### Phase 2: 服務目錄與拓撲 (4 週)
- [ ] ServiceCatalog 模型 + API
- [ ] ServiceCI 關聯表
- [ ] 服務拓撲圖頁面 (ECharts Graph)
- [ ] CI→Service 下鑽功能

### Phase 3: 生命週期與審計 (3 週)
- [ ] ConfigurationItemHistory 不可變審計紀錄
- [ ] 狀態機 (Draft → Active → Retired)
- [ ] CI 生命週期管理頁面
- [ ] 審計日誌頁面

### Phase 4: 變更管理整合 (3 週)
- [ ] ChangeRequest 模型 + API
- [ ] Change ↔ CI 關聯
- [ ] 變更執行時自動更新 CI 狀態
- [ ] 變更請求管理頁面

### Phase 5: 資料品質 (2 週)
- [ ] DataQualityMetric 計算
- [ ] 完整性/準確性/新鮮度 儀表板
- [ ] 自動提醒 (低於閾值時通知)

### Phase 6: 清理與優化 (3 週)
- [ ] 停用舊模型 (Host, Instance)
- [ ] 統一前端路由 (/cis/)
- [ ] 批量操作 API
- [ ] 標籤系統
- [ ] 效能優化與測試

**總計：約 17 週 (4 個月) **

---

## 七、風險分析

| 風險 | 影響 | 機率 | 緩解措施 |
|------|------|------|----------|
| 資料遷移遺失 | 🔴 高 | 中 | 遷移前後自動比對總數與欄位完整性 |
| 舊功能不兼容 | 🟡 中 | 中 | 雙寫層確保過渡期資料同步 |
| 前端大量改動 | 🔴 高 | 高 | 分階段切換：先 API 後 UI |
| CIType schema 性能 | 🟡 中 | 低 | JSON 欄位加索引 (MySQL 5.7+ JSON functions) |
| 服務拓撲圖效能 | 🟢 低 | 中 | 分頁 + 懶載入拓撲子圖 |
| 團隊學習曲線 | 🟡 中 | 高 | 先建立 PoC 再全面推行 |

---

## 八、預期效益

| 指標 | 目前 | 目標 |
|------|------|------|
| CI 類型數量 | 3 (Host, VM, NetDev) | 無上限 (可動態新增) |
| CI 關聯查詢 | 無法關聯 | 支援 N 層拓撲查詢 |
| 新增 CI 類型 | 需修改 code | 後台新增，零程式碼 |
| 服務視角 | 無 | 完整服務→CI 映射 |
| 審計紀錄 | Host 個別紀錄 | 所有 CI 標準化審計 |
| ITIL v4 合規 | 0% | ~70% (基礎合規) |

---

## 九、與 Vue 3 Migration 協同

| 階段 | Vue 3 Migration | CMDB Improvement |
|------|----------------|------------------|
| Week 1-13 | Phase 0-3 | Phase 0 (準備) |
| Week 13-24 | Phase 4-6 | Phase 1-2 (核心模型 + 服務) |
| Week 24+ | 維護期 | Phase 3-6 (生命週期 + 品質) |

> **建議**：Vue 3 Migration 優先於 CMDB 改進，因為新的通用 CI 頁面需要使用 Vue 3 Composition API 才能有效處理動態表單。
