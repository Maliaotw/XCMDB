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
                <template slot-scope="scope">

                    <router-link :to="{name:'StorageDetail',params:{id:scope.row.id}}">
                        <el-link type="primary" :underline="false">{{ scope.row.name }}</el-link>
                    </router-link>

                </template>
            </el-table-column>

            <el-table-column label="插槽數量">
                <template slot-scope="scope">
                    <span>{{scope.row.slotnum}}</span>
                </template>
            </el-table-column>

            <el-table-column label="創建日期">
                <template slot-scope="scope">
                    <span>{{scope.row.create_at}}</span>
                </template>
            </el-table-column>


            <el-table-column label="功能">
                <template slot-scope="scope">
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
                :visible.sync="dialogVisible"
                width="20%"
                :show-close="false"
        >
            <div style="text-align: center">
                <i class="el-icon-warning" style="font-size: 100px;color: gold"></i>
                <h2 style="margin-bottom: 20px">你確定要刪除嗎</h2>
                <p>[{{DeleteForm.name}}]</p>

                <span slot="footer" class="dialog-footer">
                    <el-button type="info" @click="dialogVisible = false">取 消</el-button>
                    <el-button type="danger" @click="SubmitDelete(DeleteForm.id)">确 定</el-button>
                </span>
            </div>

        </el-dialog>

    </div>

</template>


<script>

    import {getStorageAll, del} from '../../api/storage'


    export default {
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                form: {
                    name: '',
                },
                filterform: {
                    name: '',
                    sub_asset_type: '',
                    manage_ip: '',
                    port_num: '',
                },
                DeleteForm: {
                    name: '',
                    id: ''
                },
                dialogVisible: false
            }
        },

        methods: {
            // 提交刪除
            SubmitDelete(id) {
                console.log(id)
                del(id)
                    .then((res) => {
                            console.log(res)
                            this.dialogVisible = false
                            this.getinit(this.page, this.pageSize)
                        }
                    )
            },

            // 顯示刪除通知框
            DigDelete(row) {
                this.dialogVisible = true
                this.DeleteForm.name = row.name
                this.DeleteForm.id = row.id

            },

            // 提交搜索
            handleFilterSubmit() {
                this.getinit(this.page, this.pageSize, this.filterform)

            },

            // 分頁
            handleIndexChange(p) {
                this.page = p
                this.getinit(this.page, this.pageSize)

            },
            handleSizeChange(size) {
                this.page = 1
                this.pageSize = size
                this.getinit(this.page, this.pageSize)

            },

            getinit(p, size, params) {
                if (p === '1') {
                    p = 0
                } else {
                    p = p - 1
                }
                const page = p * this.pageSize
                getStorageAll(page, size, params)
                    .then((response) => {
                        console.log(response)
                        this.tableData = response.data.results
                        this.total = response.data.count
                    })

                    .catch((error) => {

                    })
            },


        },
        created() {
            // 請求網路設備
            this.getinit(this.page, this.pageSize)

        }


    }
</script>