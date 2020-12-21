<template>

    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>業務資源</el-breadcrumb-item>
                <el-breadcrumb-item>虛擬機</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <el-row :gutter="20" style="margin-bottom: 20px">

            <el-col :span="24" style="text-align: right">

                <el-form :model="filterform">

                    <label style="margin-right: 20px;">名稱</label>

                    <el-input
                            v-model="filterform.name"
                            placeholder="请输入内容"
                            style="width:15%; margin-right: 20px;"
                            @change="handleFilterSubmit"
                    >
                    </el-input>


                    <label style="margin-left: 20px">狀態</label>
                    <el-select v-model="filterform.enabled"
                               style="margin-left: 20px;margin-right: 20px;"
                               placeholder="狀態"
                               @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""/>
                        <el-option label="啟用" key="True"
                                   value="True"
                        />
                        <el-option label="未啟用" key="False"
                                   value="False"
                        />

                    </el-select>

                    <label style="margin-left: 20px">業務線/分支</label>
                    <el-select v-model="filterform.node"
                               style="margin-left: 20px;margin-right: 20px;"
                               placeholder=""
                               filterable
                               @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""/>
                        <el-option
                                :key="item.id"
                                v-for="(item, index) in this.nodes"
                                :label="item.name"
                                :value="item.name"
                        />

                    </el-select>

                </el-form>
            </el-col>
        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index">
            </el-table-column>
            <el-table-column
                    label="名稱"
                    :width="300"
                    sortable
                    prop="name"
            >
                <template slot-scope="scope">
                    <router-link :to="{name:'HostDetail',params:{id:scope.row.id}}">
                        <el-link type="primary" :underline="false">{{ scope.row.name }}</el-link>
                    </router-link>
                </template>
            </el-table-column>


            <el-table-column label="類型">
                <template slot-scope="scope">
                    <span>{{scope.row.cate}}</span>
                </template>
            </el-table-column>

            <el-table-column label="IP">
                <template slot-scope="scope">
                    <span>{{scope.row.manage_ip}}</span>
                </template>
            </el-table-column>


            <el-table-column label="參數">
                <template slot-scope="scope">
                    <span>{{scope.row.total_cores}}Cores {{scope.row.total_disk}}GB {{scope.row.total_memory}}G</span>
                </template>
            </el-table-column>

            <el-table-column label="更新時間">
                <template slot-scope="scope">
                    <span>{{scope.row.latest_date}}</span>
                </template>
            </el-table-column>


            <el-table-column label="狀態">
                <template slot-scope="scope">
                    <span>{{scope.row.enabled}}</span>
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

    import {getHost, del} from '../../api/host'


    export default {
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                dialogTableVisible: false,
                dialogTableCreate: false,
                dialogFormVisible: false,
                form: {
                    name: '',
                },
                title: '',
                formLabelWidth: '120px',
                filterform: {
                    name: '',
                    enabled: '',
                    node: ''
                },
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
                            console.log(res)
                            this.dialogVisible = false
                            this.getInit(this.page, this.pageSize, this.filterform)
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
                this.getInit(this.page, this.pageSize, this.filterform)


            },
            handleSizeChange(size) {
                this.page = 1
                this.pageSize = size
                this.getInit(this.page, this.pageSize, this.filterform)


            },

            // 請求資產
            getInit(p, size, params) {
                if (p === '1') {
                    p = 0
                } else {
                    p = p - 1
                }
                const page = p * this.pageSize
                getHost(page, size, params)
                    .then((response) => {
                        console.log(response)
                        this.tableData = response.data.results
                        this.total = response.data.count
                        this.nodes = response.data.node
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


        }


    }
</script>