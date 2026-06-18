# XCMDB Vue 2 → Vue 3 遷移計畫

> 產生日期：2026-06-17
> 當前版本：Vue 2.6.4 / Element UI 2.13.2 / Vue CLI 3.x

---

## 一、現況盤點

### 1.1 套件版本

| 套件 | 當前版本 | Vue 3 對應版本 | 相容性 |
|---|---|---|---|
| `vue` | ^2.6.4 | ^3.5.x | 需升級 |
| `vue-router` | ^3.0.1 | ^4.x | 需升級 |
| `vuex` | ^3.0.1 | ^4.x | 需升級 |
| `element-ui` | ^2.13.2 | `element-plus` ^1.x/2.x | **需全量替換** |
| `vue-chartjs` | ^3.5.0 | ^5.x | 需升級 |
| `vue-echarts` | ^5.0.0-beta.0 | ^7.x | 需升級 |
| `vue-progressbar` | ^0.7.5 | 無直接替代 | 需替換 |
| `vue-top-progress` | ^0.7.0 | 無直接替代 | 需替換 |
| `vue-cookie` | ^1.1.4 | 需改用 `js-cookie` 或 `unplugin-cookie-banner` | 需替換 |
| `@vue/cli-service` | ^3.4.0 | ^5.x | 需升級 |

### 1.2 程式碼規模

- `.vue` 檔案：**58 個**
- 全部使用 **Options API**，無 Composition API
- Mixin 使用：`PieChart.js`、`LineChart.js`（chartjs mixin）

### 1.3 不兼容模式盤點

| 模式 | 出現次數 | 嚴重度 | Vue 3 對應寫法 |
|---|---|---|---|
| `slot-scope="..."` | ~144 處 | 高 | `v-slot="{ ... }"` |
| `slot="..."`（元素屬性） | ~38 處 | 高 | `v-slot:slotname` |
| `:visible.sync` / `.sync` 修飾符 | ~12 處 | 高 | `v-model:visible` |
| `.native` 修飾符 | 2 處 | 高 | 移除 |
| `>>>` 深度選擇器 | 3 處 | 中 | `:deep(.el-class)` |
| `destroyed()` 生命週期 | 3 處 | 中 | `unmounted()` |
| 物件 Options API | 全部 | 高 | 遷移為 Composition API（建議） |

---

## 二、遷移步驟

### Phase 0：準備工作（1-2 週）

#### 0.1 建立 Git 分支
```bash
git checkout -b migrate-vue3
```

#### 0.2 升級開發環境
```bash
# 確保 Node.js >= 18.x
node -v

# 移除舊的 node_modules 和 package-lock.json
rm -rf node_modules package-lock.json

# 改用新的 Vue CLI（或直接使用 Vite）
npm i -D @vue/cli-service@latest  # 或遷移到 Vite
```

#### 0.3 建立兼容性檢查工具
- 使用 [vue-migration-helper](https://v3-migration.vuejs.org/migration-wizard.html) 自動化掃描
- 使用 `vitest` 建立基礎測試覆蓋

### Phase 1：基礎依賴升級（2-3 週）

#### 1.1 升級核心框架
```json
{
  "dependencies": {
    "vue": "^3.5.x",
    "vue-router": "^4.x",
    "vuex": "^4.x",
    "axios": "^1.x",
    "echarts": "^5.x",
    "element-plus": "^2.x",
    "vue-echarts": "^7.x"
  },
  "devDependencies": {
    "vite": "^6.x",
    "@vitejs/plugin-vue": "^5.x",
    "vitest": "^3.x",
    "@vue/test-utils": "^2.x"
  }
}
```

#### 1.2 選擇 Vite 替代 Vue CLI（建議）
```
Vue CLI 3.x → Vite 6.x

理由：
- Vue CLI 已進入維護模式，不再積極開發
- Vite 開發體驗更好（HMR 更快、ESBuild 編譯更快）
- Vue 3 官方首選工具鏈
- 原生支援 Vite 生態系
```

`vite.config.js`:
```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    port: 19528
  }
})
```

### Phase 2：主要遷移（4-6 週）

#### 2.1 `main.js` 入口遷移
```js
// === 遷移前 (Vue 2) ===
import Vue from 'vue'
import ElementUI from 'element-ui'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.use(ElementUI)
Vue.use(progressBar)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

// === 遷移後 (Vue 3) ===
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import store from './store'
import { createPinia } from 'pinia'  // 建議改用 Pinia

const app = createApp(App)

app.use(ElementPlus)
app.use(router)
app.use(createPinia())  // 替代 Vuex
app.mount('#app')
```

#### 2.2 Options API → Composition API（全部 58 個檔案）
```vue
<!-- === 遷移前 (Options API) === -->
<template>
  <div>
    <el-button @click="handleClick">按鈕</el-button>
    <span>{{ count }}</span>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'MyComponent',
  props: {
    userId: { type: Number, required: true }
  },
  data() {
    return {
      count: 0,
      loading: false
    }
  },
  computed: {
    ...mapState(['userName']),
    displayName() {
      return `${this.userName} - #${this.count}`
    }
  },
  methods: {
    handleClick() {
      this.loading = true
      this.$api.getUser(this.userId).then(res => {
        this.count = res.data
      })
    }
  },
  created() {
    this.handleClick()
  },
  destroyed() {
    // cleanup
  }
}
</script>

<style scoped>
>>> .el-button { border-radius: 0; }
</style>

<!-- === 遷移後 (Composition API) === -->
<template>
  <div>
    <el-button @click="handleClick">按鈕</el-button>
    <span>{{ count }}</span>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useStore } from 'vuex'

const props = defineProps({
  userId: { type: Number, required: true }
})

const store = useStore()
const count = ref(0)
const loading = ref(false)

const displayName = computed(() => {
  return `${store.state.userName} - #${count.value}`
})

const handleClick = async () => {
  loading.value = true
  const res = await $api.getUser(props.userId)
  count.value = res.data
}

onMounted(() => {
  handleClick()
})

onUnmounted(() => {
  // cleanup
})
</script>

<style scoped>
:deep(.el-button) { border-radius: 0; }
</style>
```

#### 2.3 Slot 語法重寫（~182 處）
```html
<!-- 遷移前 -->
<el-table-column>
  <template slot-scope="{ row }">
    <span>{{ row.name }}</span>
  </template>
</el-table-column>
<parent :visible.sync="show">
  <div slot="header">標題</div>
</parent>

<!-- 遷移後 -->
<el-table-column>
  <template #default="{ row }">
    <span>{{ row.name }}</span>
  </template>
</el-table-column>
<parent v-model:visible="show">
  <template #header>標題</template>
</parent>
```

**工具建議**：使用 VS Code 擴充或 `jscodeshift` 自動轉換 slot 語法。

#### 2.4 `.sync` → `v-model` 修飾符
```html
<!-- 遷移前 -->
<el-dialog :visible.sync="show">

<!-- 遷移後 -->
<el-dialog v-model="show">
```

#### 2.5 `.native` 修飾符移除
```html
<!-- 遷移前 -->
<Header @click.native="logout" />

<!-- 遷移後（直接監聽事件） -->
<Header @click="logout" />
<!-- 或在 Header 中使用 defineEmits -->
```

#### 2.6 生命週期重命名
| Vue 2 | Vue 3 |
|---|---|
| `created()` | `onMounted()` / `onBeforeMount()` |
| `mounted()` | `onMounted()` |
| `updated()` | `onUpdated()` |
| `destroyed()` | `onUnmounted()` |
| `beforeDestroy()` | `onBeforeUnmount()` |

### Phase 3：狀態管理遷移（2-3 週）

#### 3.1 Vuex 4 → Pinia（強烈建議）
```js
// === 遷移前 (Vuex 3) ===
// store/index.js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    loading: false
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    setLoading(state, value) {
      state.loading = value
    }
  },
  actions: {
    async fetchUser({ commit }, id) {
      commit('setLoading', true)
      const res = await api.getUser(id)
      commit('SET_USER', res.data)
      commit('setLoading', false)
    }
  },
  modules: {
    vm: vmModule,
    hosts: hostsModule
  }
})

// === 遷移後 (Pinia) ===
// stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    loading: false
  }),
  getters: {
    isLoggedIn: (state) => !!state.user
  },
  actions: {
    async fetchUser(id) {
      this.loading = true
      const res = await api.getUser(id)
      this.user = res.data
      this.loading = false
    }
  }
})

// stores/index.js
import { createPinia } from 'pinia'
export default createPinia()
```

### Phase 4：路由遷移（1 週）

```js
// === 遷移前 (Vue Router 3) ===
import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/vm',
    component: () => import('@/views/VM/vm.vue'),
    children: [
      { path: '', component: () => import('@/views/VM/vm.vue') }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router

// === 遷移後 (Vue Router 4) ===
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/vm',
    component: () => import('@/views/VM/vm.vue'),
    children: [
      { path: '', component: () => import('@/views/VM/vm.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),  // 注意：不再是 mode: 'history'
  routes
})

export default router
```

### Phase 5：圖表元件升級（1 週）

```js
// === 遷移前 (vue-chartjs v3.5.0) ===
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Arc } from 'chart.js/auto'

ChartJS.register(Title, Tooltip, Arc)

export default Pie.extendOptions({
  // 或直接用 extends
  props: ['data', 'options'],
  mounted () {
    this.renderChart(this.data, this.options)
  }
})

// === 遷移後 (vue-chartjs v5.x + chart.js v4) ===
import { defineComponent } from 'vue'
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, ArcElement)

export default defineComponent({
  extends: Pie,
  props: ['data', 'options'],
  setup(props) {
    // Chart.js v4 API 變更
  }
})
```

> `echarts` 本身不受 Vue 版本影響，`vue-echarts` 需升級至 v7.x。

### Phase 6：測試與 QA（2-3 週）

#### 6.1 單元測試
```bash
npm i -D vitest @vue/test-utils jsdom
```

#### 6.2 手動測試清單

| 頁面 | 功能 | 風險級別 |
|---|---|---|
| `Login.vue` | 登入表單、驗證 | 高（CSS 選擇器、.native） |
| `VM/vm.vue` | VM 管理、WebSocket | 高（生命週期、插槽） |
| `VM/PHost.vue` | 物理機管理 | 高（destroyed 生命週期） |
| `VM/Cluster.vue` | 叢集管理 | 高（destroyed 生命週期） |
| `assets/` 系列 | IDC/Rack/機櫃管理 | 高（大量 Element UI 表格/表單） |
| `hosts/` 系列 | 主機管理 | 中 |
| Dashboard | 圖表/ECharts | 中（chartjs 升級） |

---

## 三、風險與影響評估

### 3.1 高風險項目

| 風險 | 影響 | 緩解策略 |
|---|---|---|
| **Element UI → Element Plus** | 所有 58 個元件全部影響 | 逐頁面重寫 + 自動化測試 |
| **Slot 語法 ~182 處** | 渲染錯誤、功能失效 | 使用自動化工具批量轉換 + 人工審查 |
| **Options API 全部重寫** | 邏輯錯誤、狀態管理混亂 | 逐步遷移，先從簡單頁面開始 |
| **CSS 選擇器破壞** | 頁面樣式跑版 | 使用 `:deep()` 替換 `>>>`，逐頁面檢查 |
| **Pinia/Vuex 遷移** | 狀態不一致、SSO 失效 | 保留 Vuex 4 相容模式，逐步過渡 |

### 3.2 中風險項目

| 風險 | 影響 | 緩解策略 |
|---|---|---|
| **WebSocket 實時通訊** | VM 構建進度不更新 | 單獨測試 `vm.vue` 的 WebSocket |
| **圖表渲染** | 儀表板數據顯示錯誤 | 升級 chart.js v4 需檢查 API 變更 |
| **Vue CLI → Vite 工具鏈** | 開發/建構流程變化 | 額外 2-3 天適應期 |
| **第三方套件相容性** | `vue-progressbar` 等無 Vue 3 版本 | 尋找替代套件 |

### 3.3 低風險項目

| 風險 | 影響 | 緩解策略 |
|---|---|---|
| **`.native` 修飾符 (2 處)** | 事件監聽失效 | 手動移除 |
| **`>>>` 選擇器 (3 處)** | 樣式失效 | 替換為 `:deep()` |
| **`destroyed()` (3 處)** | 清理邏輯失效 | 替換為 `onUnmounted()` |

### 3.4 時間估算

| 階段 | 預估時間 |
|---|---|
| Phase 0: 準備 | 1-2 週 |
| Phase 1: 基礎依賴 | 2-3 週 |
| Phase 2: 主要遷移 | 4-6 週 |
| Phase 3: 狀態管理 | 2-3 週 |
| Phase 4: 路由遷移 | 1 週 |
| Phase 5: 圖表升級 | 1 週 |
| Phase 6: 測試 QA | 2-3 週 |
| **總計** | **13-24 週** |

---

## 四、遷移好處

### 4.1 效能提升

| 項目 | Vue 2 | Vue 3 | 提升 |
|---|---|---|---|
| 記憶體使用量 | 基準 | -54% | 大幅降低 |
| 初始載入速度 | 基準 | +53% | 更快 |
| 虛擬 DOM 重新渲染 | 基準 | +33% | 更流暢 |
| SSR 速度 | 基準 | +200-300% | 數倍提升 |

### 4.2 開發體驗

- **Composition API**：更好的程式碼組織與邏輯複用，解決 Options API 中大型元件邏輯分散問題
- **TypeScript 第一方支援**：Vue 3 原生支援 TS，提供更好的 IDE 體驗與型別檢查
- **Vite**：HMR 熱更新從秒級縮短到毫秒級，大幅加速開發流程
- **更小的 Bundle 大小**：Tree-shaking 支援更完善

### 4.3 生態與長期支援

- **Vue 2 已於 2023/12/31 EOL**，不再獲得安全更新
- 所有新套件和生態系項目都優先支援 Vue 3
- 現有 `vue-chartjs`、`vue-progressbar` 等已停止維護 Vue 2 版本
- 團隊招聘時 Vue 3 已成為市場主流技能要求

### 4.4 程式碼品質

- **Composition API** 改善邏輯複用（替代 Mixin 的問題）
- **更好的 TS 支援** 減少執行時錯誤
- **Vite 工具鏈** 提供更好的開發體驗和更快的建構

---

## 五、建議策略

### 策略 A：大爆炸式遷移（推薦）
一次性完成所有遷移，優點是無相容期、無雙重維護成本，風險在於開發時間長（13-24 週）。

### 策略 B：漸進式遷移
使用 [Vue 3 相容層](https://v3-migration.vuejs.org/migration-build.html) 並行 Vue 2 與 Vue 3，適用於有持續新功能需求的專案，但需承擔雙重維護成本。

### 建議路線
```
1. 先建立自動化測試覆蓋度（確保遷移不破壞功能）
2. 使用 vue-migration-wizard 掃描所有不兼容項目
3. 優先遷移：main.js → Vuex/Pinia → 路由 → 簡單頁面 → 複雜頁面
4. Element UI → Element Plus 是最關鍵路徑
5. 每個頁面遷移後立即測試
6. 最後統一處理圖表、進度條等第三方套件
```

---

## 六、替代方案考量

### 6.1 維持 Vue 2
- 短期（3-6 個月）內功能不變動可考慮
- 但 Vue 2 已 EOL，安全風險持續累積
- 第三方套件支援逐漸消失

### 6.2 遷移到 React / Svelte
- 成本遠高於 Vue 2→3 遷移
- 不建議因版本升級而跨框架遷移

### 6.3 結論
**直接執行 Vue 2 → Vue 3 遷移是最具成本效益的方案。**
