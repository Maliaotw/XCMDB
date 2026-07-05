<template>

    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>基礎資源</el-breadcrumb-item>
                <el-breadcrumb-item>資產列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <el-row :gutter="20" style="margin-bottom: 20px">

            <el-col :span="24" style="text-align: right">

                <el-form :model="filterform">

                    <label style="margin-right: 20px;">名稱</label>

                    <el-input
                            v-model="filterform.name"
                            placeholder="請輸入內容"
                            style="width:15%; margin-right: 20px;"
                            @change="handleFilterSubmit"
                    >

                    </el-input>

                    <label style="margin-right: 20px;">類型</label>
                    <el-select
                            v-model="filterform.device_type_id"
                            placeholder="類型"
                            @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""/>
                        <el-option label="服務器" key="1" value="1"/>
                        <el-option label="網路設備" key="2" value="2"/>
                        <el-option label="存儲設備" key="3" value="3"/>
                    </el-select>

                    <label style="margin-left: 20px">狀態</label>
                    <el-select v-model="filterform.device_status_id"
                               style="margin-left: 20px;margin-right: 20px;"
                               placeholder="狀態"
                               @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""/>
                        <el-option label="上架" key="1" value="1"/>
                        <el-option label="線上" key="2" value="2"/>
                        <el-option label="離線" key="3" value="3"/>
                        <el-option label="下架" key="4" value="4"/>

                    </el-select>

                    <label style="margin-left: 20px">機櫃</label>
                    <el-select v-model="filterform.rack"
                               style="margin-left: 20px;margin-right: 20px;"
                               placeholder="機櫃"
                               @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""/>
                        <el-option v-for="item in racklist" :label="item.name" :key="item.id"
                                   :value="item.id"/>

                    </el-select>


                </el-form>
            </el-col>
        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index">
            </el-table-column>
            <el-table-column
                    label="資產名稱"
            >
                <template #default="scope">

                    <router-link :to="{name:'AssetDetail',params:{id:scope.row.id}}">
                        <el-link type="primary" :underline="false">{{ scope.row.name }}</el-link>
                    </router-link>
                </template>
            </el-table-column>

            <el-table-column label="類型">
                <template #default="scope">
                    <span>{{scope.row.device_type_id}}</span>
                </template>
            </el-table-column>


            <el-table-column label="狀態">
                <template #default="scope">
                    <span>{{scope.row.device_status_id}}</span>
                </template>
            </el-table-column>

            <el-table-column label="標籤">
                <template #default="scope">
                    <span>{{scope.row.tag}}</span>
                </template>
            </el-table-column>


            <el-table-column label="機櫃">
                <template #default="scope">
                    <span>{{scope.row.rack}}</span>
                </template>
            </el-table-column>

            <el-table-column label="產編">
                <template #default="scope">
                    <span>{{scope.row.number}}</span>
                </template>
            </el-table-column>

            <el-table-column label="操作" v-permission="'asset:assign'">
                <template #default="scope">
                    <el-button type="text" size="small" @click="handleAssign(scope.row)">分配</el-button>
                </template>
            </el-table-column>

        </el-table>
        <el-pagination
                :page-sizes="[5,10,20,50,100]"
                :page-size="pageSize"
                :pager-count="7"
                layout="total,sizes,prev, pager, next"
                :total="total"
                @current-change="handleIndexChange"
                @size-change="handleSizeChange"
                style="float: right;margin-top: 20px"
        >
        </el-pagination>

    </div>

</template>


<script setup>
import { ref, onMounted } from 'vue'
import { getAsset } from '../../api/asset'

const total = ref(0)
const pageSize = ref(10)
const page = ref(1)
const tableData = ref([])
const form = ref({
  name: '',
})
const title = ref('')
const formLabelWidth = ref('120px')
const filterform = ref({})
const typelist = ref('')
const statuslist = ref('')
const racklist = ref('')

// 提交搜索
function handleFilterSubmit() {
  getAssets(page.value, pageSize.value, filterform.value)

}

// 分頁
function handleIndexChange(p) {
  page.value = p
  getAssets(page.value, pageSize.value, filterform.value)

}
function handleSizeChange(size) {
  page.value = 1
  pageSize.value = size
  getAssets(page.value, pageSize.value, filterform.value)

}

// 請求資產
function getAssets(p, size, params) {
  if (p === '1') {
    p = 0
  } else {
    p = p - 1
  }
  const pageValue = p * pageSize.value


  getAsset(pageValue, size, params)
    .then((response) => {
      console.log(response)
      tableData.value = response.data.results
      racklist.value = response.data.rack
      total.value = response.data.count
    })

    .catch((error) => {
    })
}

function handleAssign(row) {
  // router.push is already handled in the template so we just need to import router
  window.location.hash = `#/AssetUpdate/${row.id}`
}

onMounted(() => {
  // get and set auth user
  getAssets(page.value, pageSize.value)
})
</script>