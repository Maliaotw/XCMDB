<template>

    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>機房管理</el-breadcrumb-item>
                <el-breadcrumb-item>機房列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>


        <el-row type="flex" style="margin-bottom: 20px">

            <el-col :span="4">
                <router-link :to="{name:'IDCCreate'}">
                    <el-button type="primary">新增</el-button>
                </router-link>
            </el-col>

        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index">
            </el-table-column>
            <el-table-column
                    label="機房名稱"
                    :width="300"
            >
                <template slot-scope="scope">
                    <!--<span>{{scope.row.floor}}</span>-->
                    <span>{{scope.row.name}}</span>
                </template>
            </el-table-column>

            <el-table-column label="樓層">
                <template slot-scope="scope">
                    <span>{{scope.row.floor}}</span>
                </template>
            </el-table-column>

            <el-table-column label="機櫃數">
                <template slot-scope="scope">
                    <span>{{scope.row.rackunit}}</span>
                </template>
            </el-table-column>


            <el-table-column label="功能">
                <template slot-scope="scope">
                    <router-link :to="{name:'IDCUpdate',params:{id: scope.row.id}}">
                        <el-button>編輯</el-button>
                    </router-link>
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
                <i class="el-icon-warning" style="font-size: 100px;color: gold"/>
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

    import {getIDC, del} from '@/api/idc'


    export default {
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                title: '',
                formLabelWidth: '120px',
                CreateisShow: false,
                dialogVisible: false,
                DeleteForm: {
                    name: '',
                    id: ''
                },
            }
        },

        methods: {
            // 提交刪除
            SubmitDelete(id) {
                console.log(id)
                del(id)
                    .then((res) => {
                            this.dialogVisible = false
                            this.getInit(this.page, this.pageSize)

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
                this.getInit(this.page, this.pageSize, this.filterform)

            },

            // 分頁
            handleIndexChange(p) {
                this.page = p
                this.getInit(this.page, this.pageSize)

            },
            handleSizeChange(size) {
                this.page = 1
                this.pageSize = size
                this.getInit(this.page, this.pageSize)

            },

            // 請求資產
            getInit(p, size, params) {
                if (p === '1') {
                    p = 0
                } else {
                    p = p - 1
                }
                const page = p * this.pageSize
                getIDC(page, size, params)
                    .then((response) => {
                        this.tableData = response.data.results
                        this.total = response.data.count
                    })

                    .catch((error) => {
                        this.$notify.error({
                            title: '错误',
                            message: '这是一条错误的提示消息'
                        });
                    })
            },

        },
        created() {
            // get and set auth user
            this.getInit(this.page, this.pageSize)

        }


    }
</script>