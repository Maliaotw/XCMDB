<template>
  <div>
    <el-table :data="tableData" style="width: 100%">
      <el-table-column type="index" />
      <el-table-column label="Name" prop="hw_name" sortable>
        <template #default="scope">
          <span>{{ scope.row.hw_name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="狀態" prop="hw_power_status" sortable>
        <template #default="scope">
          <span>{{ scope.row.hw_power_status }}</span>
        </template>
      </el-table-column>

      <el-table-column label="規格">
        <template #default="scope">
          <span>{{ scope.row.info }}</span>
        </template>
      </el-table-column>

      <el-table-column label="管理IP" prop="ip_address" sortable>
        <template #default="scope">
          <span>{{ scope.row.ip_address }}</span>
        </template>
      </el-table-column>

      <el-table-column label="主機">
        <template #default="scope">
          <span>{{ scope.row.host }}</span>
        </template>
      </el-table-column>

      <el-table-column label="Network">
        <template #default="scope">
          <span>{{ scope.row.network.network }}</span>
        </template>
      </el-table-column>

      <el-table-column label="DataStore">
        <template #default="scope">
          <span>{{ scope.row.datastore.name }}</span>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      :page-sizes="[5, 10, 20, 50, 100]"
      :page-size="pageSize"
      :pager-count="7"
      layout="total, sizes, prev, pager, next"
      :total="total"
      @current-change="handleIndexChange"
      @size-change="handleSizeChange"
      style="float: right; margin-top: 20px"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { getInstance } from '@/api/instance'
import { useInstanceStore } from '@/stores/instance'

const instanceStore = useInstanceStore()

const props = defineProps({
  id: {
    type: [String, Number],
    default: 0
  }
})

const emit = defineEmits(['table-ready'])

const total = ref(0)
const pageSize = ref(10)
const page = ref(1)
const tableData = ref([])
const filterform = ref({})
const ins = ref(props.id || 0)

async function getInit(p, size, params = {}) {
  try {
    const offset = p === 1 ? 0 : (p - 1) * size
    const response = await getInstance(offset, size, params)
    tableData.value = response.data.results
    total.value = response.data.count

    // Emit updated datasets to filter via store
    if (response.data.datastore || response.data.network || response.data.host) {
      instanceStore.setDatasets(response.data)
    }
  } catch (error) {
    ElMessage.error('載入資料時發生錯誤，請重試')
    console.error('Failed to fetch instance data:', error)
  }
}

function handleIndexChange(p) {
  page.value = p
  getInit(page.value, pageSize.value, filterform.value)
}

function handleSizeChange(size) {
  page.value = 1
  pageSize.value = size
  getInit(page.value, pageSize.value, filterform.value)
}

// Watch store filterform and auto-refresh data
watch(
  () => instanceStore.filterform,
  (newVal) => {
    if (newVal && Object.keys(newVal).length > 0) {
      filterform.value = { ...newVal }
      getInit(page.value, pageSize.value, filterform.value)
    }
  },
  { deep: true }
)

// Expose methods for parent / store to call
defineExpose({
  getInit,
  page,
  pageSize
})

onMounted(() => {
  emit('table-ready', { getInit, page, pageSize })

  if (ins.value === 0) {
    getInit(page.value, pageSize.value)
  } else {
    filterform.value['cluster'] = ins.value
    getInit(page.value, pageSize.value, filterform.value)
  }
})
</script>
