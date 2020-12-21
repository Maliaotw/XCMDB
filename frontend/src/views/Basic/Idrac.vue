<template>

    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>基礎資源</el-breadcrumb-item>
                <el-breadcrumb-item>物理服務器</el-breadcrumb-item>
            </el-breadcrumb>
        </div>


        <el-row :gutter="20" style="margin-bottom: 20px">

            <el-col :span="4">
                <router-link :to="{name:'IdracCreate'}">
                    <el-button type="primary">新增</el-button>
                </router-link>
            </el-col>


            <el-col :span="20" style="text-align: right">

                <el-form :model="filterform">

                    <label style="margin-right: 20px;">IP</label>

                    <el-input
                            v-model="filterform.idrac_ip"
                            placeholder=""
                            style="width:15%; margin-right: 20px;"
                            @change="handleFilterSubmit"
                    >

                    </el-input>


                    <label style="margin-left: 20px">狀態</label>
                    <el-select v-model="filterform.device_status_id"
                               style="margin-left: 20px;margin-right: 20px;"
                               placeholder="狀態"
                               @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""/>
                        <el-option v-for="item in this.statuslist" :label="item[1]" :key="item[0]"
                                   :value="item[0]"/>

                    </el-select>


                </el-form>
            </el-col>
        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index">
            </el-table-column>
            <el-table-column label="IP" :width="300">
                <template slot-scope="scope">
                    <router-link :to="{name:'IdracDetail',params:{id:scope.row.id}}">
                        <el-link type="primary" :underline="false">{{ scope.row.idrac_ip}}</el-link>
                    </router-link>
                </template>
            </el-table-column>

            <el-table-column label="參數">
                <template slot-scope="scope">
                    <span>{{ scope.row.info }}</span>
                </template>
            </el-table-column>


            <el-table-column label="狀態">
                <template slot-scope="scope">
                    <span>{{ status(scope.row.host) }}</span>
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

    import {getIdrac,del} from '../../api/idrac'


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
                CreateisShow: false,
                EditisShow: false,
                filterform: {
                    device_status_id: '',
                    device_type_id: '',
                    name: '',
                    rack: '',
                },
                statuslist: [
                    {0: '連接中'},
                    {1: '連接成功'}
                ],
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
                            this.getInit(this.page, this.pageSize,this.filterform)
                        }
                    )
            },


            // 顯示刪除通知框
            DigDelete(row) {
                this.dialogVisible = true
                this.DeleteForm.name = row.idrac_ip
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
                getIdrac(page, size, params)
                    .then((response) => {
                        console.log(response)
                        this.tableData = response.data.results
                        this.total = response.data.count
                    })

                    .catch((error) => {

                    })
            },
            status(val) {
                if (val) {
                    return '連接成功'
                } else {
                    return '連接中'
                }

            }

        },
        computed: {},
        created() {
            // get and set auth user
            this.getInit(this.page, this.pageSize, this.filterform)

        }


    }
</script>

