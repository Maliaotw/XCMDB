<template>


    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>基礎資源</el-breadcrumb-item>
                <el-breadcrumb-item :to="{name:'Idrac'}">物理服務器</el-breadcrumb-item>
                <el-breadcrumb-item>{{this.form.name}}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>


        <el-row type="flex">
            <el-col :span="12">
                <template>
                    <el-tabs v-model="activeName">
                        <el-tab-pane label="資產詳情" name="hostinfo"/>
                        <el-tab-pane label="變更紀錄" name="changeinfo"/>
                    </el-tabs>
                </template>
            </el-col>

        </el-row>

        <el-row type="flex" v-show="activeName === 'hostinfo'">


            <el-col
                    :span="12"
            >
                <div>
                    <label><b>主機信息</b></label>
                    <el-form
                            label-position="left"
                            label-width="200px"
                            style="margin-left: 20px;"
                    >
                        <el-form-item label="主機名:" style="margin-bottom: 0px">
                            <label><b>{{this.form.name}}</b></label>
                        </el-form-item>

                        <el-form-item label="類型:" style="margin-bottom: 0px">
                            <label><b>{{this.form.cate}}</b></label>
                        </el-form-item>

                        <el-form-item label="IP:" style="margin-bottom: 0px">
                            <label><b>{{this.form.manage_ip}}</b></label>
                        </el-form-item>

                        <el-form-item label="製造商" style="margin-bottom: 0px">
                            <label><b>{{this.form.manufacturer}}</b></label>
                        </el-form-item>

                        <el-form-item label="型号:" style="margin-bottom: 0px">
                            <label><b>{{this.form.model}}</b></label>
                        </el-form-item>

                        <el-form-item label="系統平台:" style="margin-bottom: 0px">
                            <label><b>{{this.form.os_platform}}</b></label>
                        </el-form-item>

                        <el-form-item label="操作系統:" style="margin-bottom: 0px">
                            <label><b>{{this.form.os_distribution}}</b></label>
                        </el-form-item>

                        <el-form-item label="激活:" style="margin-bottom: 0px">
                            <label><b>{{ this.form.enabled }}</b></label>
                        </el-form-item>

                        <el-form-item label="序列號:" style="margin-bottom: 0px">
                            <label><b>{{ this.form.sn }}</b></label>
                        </el-form-item>

                        <el-form-item label="資產編號:" style="margin-bottom: 0px">
                            <label><b></b></label>
                        </el-form-item>

                        <el-form-item label="創建日期:" style="margin-bottom: 0px">
                            <label><b>{{ this.form.create_at }}</b></label>
                        </el-form-item>

                        <el-form-item label="最後更新日期:" style="margin-bottom: 0px">
                            <label><b>{{ this.form.latest_date }}</b></label>
                        </el-form-item>
                    </el-form>

                </div>


            </el-col>


            <el-col :span="12">
                <label><b>硬件信息</b></label>

                <el-collapse
                        style="margin-left: 20px;margin-top: 10px"
                >
                    <el-collapse-item title="CPU" name="1">
                        <el-form
                                label-width="200px"
                                label-position="left"
                                style="margin-left: 20px;"
                        >
                            <el-form-item
                                    v-for="cpu in form.cpu"
                                    :label="cpu.slot"
                                    style="margin-bottom: 0px"
                            >
                                <label><b>{{ cpu.cores}}Cores, {{ cpu.model }}</b></label>
                            </el-form-item>

                        </el-form>

                    </el-collapse-item>
                    <el-collapse-item title="Disk" name="2">
                        <el-form
                                label-position="left"
                                style="margin-left: 20px;"
                        >
                            <el-form-item
                                    v-for="disk in form.disk"
                                    :label="disk.slot"
                                    style="margin-bottom: 0px"
                            >
                                <label><b>{{ disk.manufacturer}}, {{ disk.capacity }}</b></label>
                            </el-form-item>

                        </el-form>
                    </el-collapse-item>
                    <el-collapse-item title="Nic" name="3">
                        <el-form
                                label-width="200px"
                                label-position="left"
                                style="margin-left: 20px;"
                        >
                            <el-form-item
                                    v-for="nic in form.nic"
                                    :label="nic.name"
                                    style="margin-bottom: 0px"
                            >
                                <label><b>{{ nic.ipaddress}}, {{ nic.macaddress }}</b></label>
                            </el-form-item>

                        </el-form>
                    </el-collapse-item>
                    <el-collapse-item title="memory" name="4">
                        <el-form
                                label-width="200px"
                                label-position="left"
                                style="margin-left: 20px;"
                        >
                            <el-form-item
                                    v-for="mem in form.memory"
                                    :label="mem.slot"
                                    style="margin-bottom: 0px"
                            >
                                <label><b>{{ mem.manufacturer}}, {{ mem.capacity }}GB</b></label>
                            </el-form-item>

                        </el-form>
                    </el-collapse-item>
                </el-collapse>

            </el-col>




        </el-row>

        <el-row type="flex" v-show="activeName === 'changeinfo'">
            <el-col :span="12">
                <el-table
                        :data="tableData"
                        size="small"
                >
                    <el-table-column
                            type="index"

                    >
                    </el-table-column>
                    <el-table-column
                            label="標題"
                    >

                        <template slot-scope="scope">
                            <span>{{scope.row.title}}</span>
                        </template>
                    </el-table-column>

                    <el-table-column
                            label="時間"
                    >
                        <template slot-scope="scope">
                            <span>{{scope.row.create_date}}</span>
                        </template>
                    </el-table-column>


                    <el-table-column
                            label="動作"
                    >
                        <template slot-scope="scope">
                            <el-button
                                    type="primary"
                                    @click="detask(scope.row)"
                                    style="margin-left: 10px"
                            >詳情
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
            </el-col>

            <el-col :span="12">
                <p>結果顯示在這裡</p>
                <pre style="background: #111111;min-height: 600px;color: white;padding: 15px;overflow: scroll;">{{result}}</pre>

            </el-col>

        </el-row>

        <el-dialog
                :visible.sync="dialogVisible"
                width="20%"
                :show-close="false"
        >
            <div style="text-align: center">
                <i class="el-icon-warning" style="font-size: 100px;color: gold"/>
                <h2 style="margin-bottom: 20px">你確定要刪除嗎</h2>

                <span slot="footer" class="dialog-footer">
                    <el-button type="info" @click="dialogVisible = false">取 消</el-button>
                    <el-button type="danger" @click="SubmitDelete(DeleteForm.id)">确 定</el-button>
                </span>
            </div>

        </el-dialog>



    </div>


</template>

<script>
    import {del, edit, getIdracObj} from "../../api/idrac"
    import {getHostRecord} from "../../api/host"


    export default {
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                msg: "",
                form: {},
                IDRACForm: {
                    idrac_ip: "",
                    port: "",
                    user: "",
                    passwd: ""
                },
                DeleteForm: {
                    name: '',
                    id: ''
                },
                dialogVisible: false,
                centerDialogVisible: false,
                activeName: 'hostinfo',
                ConnectLoading: false,
                ConnectError: false,
                filterform: {},
                result:''

            };
        },

        methods: {
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

            // 提交刪除
            SubmitDelete(id) {
                del(id)
                    .then((res) => {
                            this.dialogVisible = false
                            // this.$route.path({name:"Idrac"})
                        }
                    )
            },

            // 顯示刪除通知框
            DigDelete() {
                this.dialogVisible = true
                this.DeleteForm.id = this.$route.params.id

            },


            // 顯示刪除通知框
            detask(row) {
                // this.dialogVisible = true
                // this.Form.name = `${row.task_id}: ${row.task_name}`
                // this.Form.result = `${row.result}`
                // this.Form.id = row.id
                // this.result = `${row.summary}`
                // console.log(row)
                this.result = row.summary
            },


            // 提交更新
            UpdateSubmit() {
                edit(this.$route.params.id, this.IDRACForm)
                    .then(res => {
                        console.log(res);
                        this.$notify({
                            title: "成功",
                            message: "更新成功",
                            type: "success"
                        });
                    })
            },


            getInit(p, size, filterform) {
                if (p === '1') {
                    p = 0
                } else {
                    p = p - 1
                }
                const page = p * this.pageSize
                getHostRecord(page, size, filterform)
                    .then(res => {
                        console.log(res)
                        this.tableData = res.data.results
                        this.total = res.data.count

                    })

            },

        },
        created() {
            getIdracObj(this.$route.params.id)
                .then(res => {
                    console.log(res);
                    this.IDRACForm.idrac_ip = res.data.idrac_ip;
                    this.IDRACForm.port = res.data.port;
                    this.IDRACForm.user = res.data.user;
                    this.IDRACForm.passwd = res.data.passwd;

                    if (res.data.host) {
                        this.form = res.data.host;
                        this.filterform.host_obj = res.data.host.id
                        this.getInit(this.page, this.pageSize, this.filterform)

                    } else {
                        this.form = ""
                    }

                })


        }
    };
</script>


<style scoped>
    .el-row {
        margin-bottom: 20px;

    }


</style>


