<template>

    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>基礎資源</el-breadcrumb-item>
                <el-breadcrumb-item>網路設備</el-breadcrumb-item>
            </el-breadcrumb>
        </div>


        <el-row type="flex" style="margin-bottom: 20px">

            <el-col :span="4">
                <router-link :to="{name:'NetDeviceCreate'}">
                    <el-button type="primary">新增設備</el-button>
                </router-link>
            </el-col>

            <el-col :span="20" style="text-align: right">

                <el-form :model="filterform">

                    <label style="margin-right: 20px;">名稱</label>

                    <el-input
                            v-model="filterform.name"
                            placeholder=""
                            style="width:15%; margin-right: 20px;"
                            @change="handleFilterSubmit"
                    />

                    <label style="margin-right: 20px;">類型</label>
                    <el-select
                            v-model="filterform.sub_asset_type"
                            placeholder="類型"
                            @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""/>
                        <el-option label="路由器" key="1" value="1"/>
                        <el-option label="交換機" key="2" value="2"/>
                        <el-option label="防火牆" key="3" value="3"/>


                    </el-select>

                    <label style="margin-left: 20px;margin-right: 20px;">管理IP</label>
                    <el-input
                            v-model="filterform.manage_ip"
                            placeholder=""
                            style="width:15%; margin-right: 20px;"
                            @change="handleFilterSubmit"
                    />

                    <label style="margin-left: 20px;margin-right: 20px;">端口個數</label>

                    <el-input
                            v-model="filterform.port_num"
                            placeholder=""
                            style="width:15%; margin-right: 20px;"
                            @change="handleFilterSubmit"
                    />


                </el-form>
            </el-col>
        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index">
            </el-table-column>
            <el-table-column label="名稱" :width="300">
                <template slot-scope="scope">
                    <span>{{ scope.row.name }}</span>
                </template>
            </el-table-column>

            <el-table-column label="類型">
                <template slot-scope="scope">
                    <span>{{scope.row.sub_asset_type}}</span>
                </template>
            </el-table-column>


            <el-table-column label="管理IP">
                <template slot-scope="scope">
                    <span>{{scope.row.manage_ip}}</span>
                </template>
            </el-table-column>

            <el-table-column label="端口個數">
                <template slot-scope="scope">
                    <span>{{scope.row.port_num}}</span>
                </template>
            </el-table-column>


            <el-table-column label="保固日期">
                <template slot-scope="scope">
                    <span>{{scope.row.warranty_date}}</span>
                </template>
            </el-table-column>

            <el-table-column label="功能">
                <template slot-scope="scope">
                    <router-link :to="{name:'NetDeviceUpdate',params:{id:scope.row.id}}">
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
                <h2 class="mb-2">你確定要刪除嗎</h2>
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

    import {getNetDeviceAll, del} from '@/api/netdrive'


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
                            this.getNets(this.page, this.pageSize)
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
                this.getNets(this.page, this.pageSize, this.filterform)

            },

            // 分頁
            handleIndexChange(p) {
                this.page = p
                this.getNets(this.page, this.pageSize, this.filterform)

            },
            handleSizeChange(size) {
                this.page = 1
                this.pageSize = size
                this.getNets(this.page, this.pageSize, this.filterform)

            },

            // 請求網路設備
            getNets(p, size, params) {
                if (p === '1') {
                    p = 0
                } else {
                    p = p - 1
                }
                const page = p * this.pageSize
                getNetDeviceAll(page, size, params)
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
            this.getNets(this.page, this.pageSize)

        }


    }
</script>
