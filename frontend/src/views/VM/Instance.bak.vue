<template>

    <div>


        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>VM</el-breadcrumb-item>
                <el-breadcrumb-item :to="{name:'Instance'}">實例</el-breadcrumb-item>
            </el-breadcrumb>
        </div>



        <el-row :gutter="20" style="margin-bottom: 20px">


            <el-col :span="4">
                <router-link :to="{name:'InsCreate'}">
                    <el-button type="primary">新增</el-button>
                </router-link>
            </el-col>


            <el-col :span="20" style="text-align: right">

                <el-form :model="filterform">

                    <label style="margin-right: 20px;">名稱</label>

                    <el-input
                            v-model="filterform.hw_name"
                            placeholder="请输入内容"
                            style="width:10%; margin-right: 2px;"
                            @change="handleFilterSubmit"
                    >

                    </el-input>

                    <label style="margin-left: 20px;margin-right: 20px;">IP</label>

                    <el-input
                            v-model="filterform.ip_address"
                            placeholder=""
                            style="width:10%; margin-right: 2px;"
                            @change="handleFilterSubmit"
                    >

                    </el-input>




                    <label style="margin-left: 20px;margin-right: 20px;">狀態</label>
                    <el-select v-model="filterform.hw_power_status"
                               style="margin-left: 2px;margin-right: 2px;width:10%"
                               placeholder="狀態"
                               @change="handleFilterSubmit"

                    >
                        <el-option key="" label="----" value=""/>
                        <el-option label="運行中" key="poweredOn" value="poweredOn"/>
                        <el-option label="已停止" key="poweredOff" value="poweredOff"/>
                        <el-option label="建置中" key="building" value="poweredOff"/>


                    </el-select>

                    <label style="margin-left: 20px;margin-right: 20px;">主機</label>
                    <el-select
                            v-model="filterform.host"
                            style="margin-left: 2px;margin-right: 2px;width:10%"
                            placeholder=""
                            @change="handleFilterSubmit"

                    >
                        <el-option key="" label="----" value=""/>
                        <el-option v-for="item in this.host" :label="item.name" :key="item.id"
                                   :value="item.id"/>

                    </el-select>


                    <label style="margin-left: 20px;margin-right: 20px;">Network</label>
                    <el-select v-model="filterform.network"
                               style="margin-left: 2px;margin-right: 2px;width:10%"
                               placeholder=""
                               @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""/>
                        <el-option v-for="item in this.network" :label="item.network" :key="item.id"
                                   :value="item.id"/>

                    </el-select>

                    <label style="margin-left: 20px;margin-right: 20px;">DataSrotre</label>
                    <el-select v-model="filterform.datastore"
                               style="margin-left: 2px;margin-right: 2px;"
                               placeholder=""
                               @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""/>
                        <el-option v-for="item in this.datastore" :label="item.name" :key="item.id"
                                   :value="item.id"/>

                    </el-select>


                </el-form>
            </el-col>
        </el-row>


        <el-table :data="tableData" style="width: 100%"  >
            <el-table-column type="index"/>
            <el-table-column
                    label="Name"
                    width="300"
                    prop="hw_name"
                    sortable
            >
                <template slot-scope="scope">
                    <span>{{scope.row.hw_name}}</span>
                </template>
            </el-table-column>

            <el-table-column
                    label="實例ID"
                    width="320px"
            >
                <template slot-scope="scope">
                    <span>{{scope.row.instance_uuid}}</span>
                </template>
            </el-table-column>


            <el-table-column
                    label="狀態"
                    prop="hw_power_status"
                    sortable
            >
                <template slot-scope="scope">
                    <span>{{scope.row.hw_power_status}}</span>
                </template>
            </el-table-column>


            <el-table-column label="規格">
                <template slot-scope="scope">
                    <span>
                        {{scope.row.info }}
                    </span>
                </template>
            </el-table-column>


            <el-table-column
                    label="管理IP"
                    prop="ip_address"
                    sortable
            >
                <template slot-scope="scope">
                    <span>{{scope.row.ip_address}}</span>
                </template>
            </el-table-column>

            <el-table-column
                    label="主機"
            >
                <template
                        slot-scope="scope"

                >
                    <span>{{scope.row.host}}</span>
                </template>
            </el-table-column>

            <el-table-column label="Network">
                <template slot-scope="scope">
                    <span>{{scope.row.network.network}}</span>
                </template>
            </el-table-column>

            <el-table-column label="DataStore">
                <template slot-scope="scope">
                    <span>{{scope.row.datastore.name}}</span>
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


<script>

    import {getInstance} from '@/api/instance'


    export default {
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                form: {},
                filterform: {

                },
                host:'',
                network:'',
                datastore:''
            }
        },
        destroyed() {

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

            // 請求資產
            getInit(p, size, params) {
                if (p === '1') {
                    p = 0
                } else {
                    p = p - 1
                }
                const page = p * this.pageSize
                getInstance(page, size, params)
                    .then((response) => {
                        // console.log(response)
                        this.tableData = response.data.results
                        this.total = response.data.count
                        this.host = response.data.host
                        this.network = response.data.network
                        this.datastore = response.data.datastore
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


        },
        computed: {}


    }
</script>
