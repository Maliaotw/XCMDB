<template>
  <div>
    <div>
      <el-breadcrumb separator="/" style="padding-top: 0px; padding-bottom: 20px">
        <el-breadcrumb-item>VM</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ name: 'Instance' }">實例</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="4">
        <router-link :to="{ name: 'InsCreate' }">
          <el-button type="primary">新增</el-button>
        </router-link>
      </el-col>

      <el-col :span="20" style="text-align: right">
        <InstanceFilter ref="filterRef" @filter-change="onFilterChange" />
      </el-col>
    </el-row>

    <InstanceTable ref="tableRef" @table-ready="onTableReady" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import InstanceFilter from './InstanceFilter'
import InstanceTable from './InstanceTable'
import { useInstanceStore } from '@/stores/instance'

const instanceStore = useInstanceStore()

const filterRef = ref(null)
const tableRef = ref(null)

function onFilterChange(filterData) {
  instanceStore.setFilterform(filterData)
}

function onTableReady(tableInstance) {
  instanceStore.setTableRef(tableInstance)
}
</script>
