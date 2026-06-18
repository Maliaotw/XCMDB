<template>
  <div>
    <el-form :model="filterform">
      <label style="margin-right: 20px">名稱</label>

      <el-input
        v-model="filterform.hw_name"
        placeholder="請輸入內容"
        style="width: 10%; margin-right: 2px"
        @input="handleFilterSubmit"
      />

      <label style="margin-left: 20px; margin-right: 20px">IP</label>

      <el-input
        v-model="filterform.ip_address"
        placeholder=""
        style="width: 10%; margin-right: 2px"
        @input="handleFilterSubmit"
      />

      <label style="margin-left: 20px; margin-right: 20px">狀態</label>
      <el-select
        v-model="filterform.hw_power_status"
        style="margin-left: 2px; margin-right: 2px; width: 10%"
        placeholder="狀態"
        @change="handleFilterSubmit"
      >
        <el-option key="" label="----" value="" />
        <el-option label="運行中" key="poweredOn" value="poweredOn" />
        <el-option label="已停止" key="poweredOff" value="poweredOff" />
        <el-option label="建置中" key="building" value="building" />
      </el-select>

      <label style="margin-left: 20px; margin-right: 20px">主機</label>
      <el-select
        v-model="filterform.host"
        style="margin-left: 2px; margin-right: 2px; width: 10%"
        placeholder=""
        @change="handleFilterSubmit"
      >
        <el-option key="" label="----" value="" />
        <el-option v-for="item in hostList" :label="item.name" :key="item.id" :value="item.id" />
      </el-select>

      <label style="margin-left: 20px; margin-right: 20px">Network</label>
      <el-select
        v-model="filterform.network"
        style="margin-left: 2px; margin-right: 2px; width: 10%"
        placeholder=""
        @change="handleFilterSubmit"
      >
        <el-option key="" label="----" value="" />
        <el-option v-for="item in networkList" :label="item.network" :key="item.id" :value="item.id" />
      </el-select>

      <label style="margin-left: 20px; margin-right: 20px">DataStore</label>
      <el-select
        v-model="filterform.datastore"
        style="margin-left: 2px; margin-right: 2px"
        placeholder=""
        @change="handleFilterSubmit"
      >
        <el-option key="" label="----" value="" />
        <el-option v-for="item in dataList" :label="item.name" :key="item.id" :value="item.id" />
      </el-select>
    </el-form>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useInstanceStore } from '@/stores/instance'

const instanceStore = useInstanceStore()

const filterform = ref({})
const emit = defineEmits(['filter-change'])

const dataList = computed(() => instanceStore.datastore)
const networkList = computed(() => instanceStore.network)
const hostList = computed(() => instanceStore.host)

// Watch store filterform changes and keep local in sync
watch(
  () => instanceStore.filterform,
  (newVal) => {
    if (newVal && Object.keys(newVal).length > 0) {
      filterform.value = { ...newVal }
    }
  },
  { immediate: true }
)

function handleFilterSubmit() {
  // Emit filter changes to parent / store
  emit('filter-change', filterform.value)
}
</script>
