<template>

    <div>
        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>機房管理</el-breadcrumb-item>
                <el-breadcrumb-item>機櫃列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>




        <el-row :gutter="20" style="margin-bottom: 20px">


            <el-col :span="4">
                <router-link :to="{name:'RackCreate'}">
                    <el-button type="primary">新增</el-button>
                </router-link>
            </el-col>
        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index">
            </el-table-column>
            <el-table-column
                    label="機櫃號"
            >
                <template slot-scope="scope">
                    <router-link :to="{name:'RackUnit',params:{id:scope.row.id}}">
                        <el-link type="primary" :underline="false">{{ scope.row.name }}</el-link>
                    </router-link>

                </template>
            </el-table-column>

            <el-table-column label="機房">
                <template slot-scope="scope">
                    <span>{{scope.row.idc}}</span>
                </template>
            </el-table-column>


            <el-table-column label="高度">
                <template slot-scope="scope">
                    <span>{{scope.row.height}}</span>
                </template>
            </el-table-column>

            <el-table-column label="資產">
                <template slot-scope="scope">
                    <span>{{scope.row.asset}}</span>
                </template>
            </el-table-column>


            <el-table-column label="使用率">
                <template slot-scope="scope">
                    <el-progress :text-inside="true" :stroke-width="26" :percentage="scope.row.used" status="success"></el-progress>
                </template>
            </el-table-column>


            <el-table-column label="ISP接入">
                <template slot-scope="scope">
                    <p v-for="isp in scope.row.isp">
                        <el-tag type="info">{{isp.name}}</el-tag>
                    </p>
                </template>
            </el-table-column>


            <el-table-column label="功能" width="200">
                <template slot-scope="scope">
                    <router-link :to="{name:'RackUpdate',params:{id:scope.row.id}}">
                        <el-button>編輯</el-button>
                    </router-link>
                    <el-button
                            type="danger"
                            @click="DigDelete(scope.row)"
                            class="ml-1"
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
                class="mt-2 pull-right"
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

    import {getRack, del} from '../../api/rack'


    export default {
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                dialogVisible: false,
                form: {
                    name: '',
                },
                title: '',
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
                getRack(page, size, params)
                    .then((response) => {
                        console.log(response)
                        this.tableData = response.data.results
                        this.total = response.data.count
                    })

                    .catch((error) => {
                        console.log(error);
                        console.debug(error);
                        console.dir(error);
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

            getISP()
                .then((res) => {
                    this.isplist = res.data
                })

        }


    }
</script>

<style>


</style>