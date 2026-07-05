<template>

    <div>

        <el-row type="flex" style="margin-bottom: 20px">

            <el-col :span="4">
                <router-link :to="{name:''}">
                    <el-button type="primary">新增設備</el-button>
                </router-link>
            </el-col>

            <el-col :span="20" style="text-align: right">

            </el-col>
        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index">
            </el-table-column>
            <el-table-column label="名稱" :width="300">
                <template #default="scope">

                    <router-link :to="{name:'StorageDetail',params:{id:scope.row.id}}">
                        <el-link type="primary" :underline="false">{{ scope.row.name }}</el-link>
                    </router-link>

                </template>
            </el-table-column>

            <el-table-column label="插槽數量">
                <template #default="scope">
                    <span>{{scope.row.slotnum}}</span>
                </template>
            </el-table-column>

            <el-table-column label="創建日期">
                <template #default="scope">
                    <span>{{scope.row.create_at}}</span>
                </template>
            </el-table-column>


            <el-table-column label="功能">
                <template #default="scope">
                    <el-button
                            type="danger"
                            @click="DigDelete(scope.row)"
                            style="margin-left: 10px"
                    >刪除
                    </el-button>
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


        <el-dialog
                v-model="dialogVisible"
                width="20%"
                show-close="false"
                @close="dialogVisible = false"
        >
            <div style="text-align: center">
                <i class="el-icon-warning" style="font-size: 100px;color: gold"></i>
                <h2 style="margin-bottom: 20px">你確定要刪除嗎</h2>
                <p>[{{DeleteForm.name}}]</p>

                <span class="dialog-footer">
                    <el-button type="info" @click="dialogVisible = false">取 消</el-button>
                    <el-button type="danger" @click="SubmitDelete(DeleteForm.id)">確 定</el-button>
                </span>
            </div>

        </el-dialog>

    </div>

</template>


<script setup>
import { ref, onMounted } from 'vue'
import { getStorageAll, del } from '../../api/storage'

const total = ref(0)
const pageSize = ref(10)
const page = ref(1)
const tableData = ref([])
const form = ref({
  name: '',
})
const filterform = ref({
  name: '',
  sub_asset_type: '',
  manage_ip: '',
  port_num: '',
})
const DeleteForm = ref({
  name: '',
  id: ''
})
const dialogVisible = ref(false)

// 提交刪除
function SubmitDelete(id) {
  console.log(id)
  del(id)
    .then((res) => {
      console.log(res)
      dialogVisible.value = false
      getinit(page.value, pageSize.value)
    })
}

// 顯示刪除通知框
function DigDelete(row) {
  dialogVisible.value = true
  DeleteForm.value.name = row.name
  DeleteForm.value.id = row.id

}

// 提交搜索
function handleFilterSubmit() {
  getinit(page.value, pageSize.value, filterform.value)

}

// 分頁
function handleIndexChange(p) {
  page.value = p
  getinit(page.value, pageSize.value)

}
function handleSizeChange(size) {
  page.value = 1
  pageSize.value = size
  getinit(page.value, pageSize.value)

}

function getinit(p, size, params) {
  if (p === '1') {
    p = 0
  } else {
    p = p - 1
  }
  const pageValue = p * pageSize.value
  getStorageAll(pageValue, size, params)
    .then((response) => {
      console.log(response)
      tableData.value = response.data.results
      total.value = response.data.count
    })

    .catch((error) => {

    })
}

// 請求網路設備
onMounted(() => {
  getinit(page.value, pageSize.value)
})
</script>