<template>

    <div>

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


                    <label style="margin-right: 20px;">業務線</label>
                    <el-select
                            v-model="filterform.busline"
                            placeholder="類型"
                            @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""></el-option>
                        <el-option label="棋牌" key="dsg" value="dsg"></el-option>
                        <el-option label="融合" key="fusion" value="fusion"></el-option>

                    </el-select>

                    <label style="margin-left: 20px;margin-right:20px">付費方式</label>
                    <el-select
                            v-model="filterform.paytype"
                            placeholder="類型"
                            @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""></el-option>
                        <el-option label="按量付費" key="Postpaid" value="Postpaid"></el-option>
                        <el-option label="包年包月" key="Prepaid" value="Prepaid"></el-option>

                    </el-select>


                </el-form>
            </el-col>
        </el-row>


        <el-table :data="tableData" size="small">
            <el-table-column type="index">
            </el-table-column>
            <el-table-column
                    label="name"
                    align="center"
                    prop="name"
                    width="230px"
                    sortable
            >
                <template slot-scope="scope">
                    <p>{{scope.row.instanceid}}</p>
                    <p>{{scope.row.name}}</p>
                </template>
            </el-table-column>


            <el-table-column
                    label="資料庫類型"
                    align="center"
                    width="100px"
            >
                <template slot-scope="scope">
                    <p>{{scope.row.engine }} {{scope.row.version}}</p>
                </template>
            </el-table-column>


            <el-table-column
                    label="狀態"
                    align="center"
                    width="90px"
            >
                <template slot-scope="scope">
                    <p>{{scope.row.status}}</p>
                </template>
            </el-table-column>


            <el-table-column
                    label="規格"
                    align="center"
            >
                <template slot-scope="scope">
                    <p>{{scope.row.info}}</p>
                </template>
            </el-table-column>

            <el-table-column
                    label="地區"
                    align="center"
                    width="90px"
            >
                <template slot-scope="scope">
                    <p>{{scope.row.region}}</p>
                </template>
            </el-table-column>

            <el-table-column
                    label="網路類型"
                    align="center"
                    width="220px"
                    prop="vpc_id"
            >
                <template slot-scope="scope">
                    <p>專有網路</p>
                    <p>{{scope.row.vpc_id}}</p>
                </template>
            </el-table-column>





            <el-table-column
                    label="業務線"
                    align="center"
                    prop="busline"
                    sortable
            >
                <template slot-scope="scope">
                    <p>{{scope.row.busline}}</p>
                </template>
            </el-table-column>

            <el-table-column
                    label="磁盤使用量"
                    align="center"
                    prop="disk_percentage"
                    sortable
            >
                <template slot-scope="scope">
                    <p>{{scope.row.disk_usaged}}G / {{scope.row.disk}}G</p>
                    <el-progress :text-inside="true" :stroke-width="26" :percentage="scope.row.disk_percentage" :status=percentage(scope.row)></el-progress>
                </template>
            </el-table-column>


            <el-table-column
                    label="付費方式"
                    align="center"
                    prop="last_day"
                    sortable
            >
                <template slot-scope="scope">
                    <div v-if="scope.row.expired_time">
                        <p>{{scope.row.paytype}} <span style="color: red">{{scope.row.last_day}}</span>天後到期<p>
                        <p>{{scope.row.expired_time}} 到期</p>

                    </div>
                    <div v-else>
                        <p>{{scope.row.paytype}}<p>
                        <p>{{scope.row.create_date}} 創建</p>
                    </div>


                </template>
            </el-table-column>




        </el-table>
        <el-pagination
                :page-sizes="[5,10,20,50,100,total]"
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

    import {getRDS} from '../../api/rds'


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
                filterform: {
                    name: '',
                    ip: '',
                    busline: '',
                    paytype: '',
                },
            }
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
                const page = p * this.pageSize;
                getRDS(page, size, params)
                    .then((response) => {
                        this.tableData = response.data.results;
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

        },
        computed: {
            percentage: function () {
                return function (row) {
                    if (row.disk_percentage < 50){
                        return "success"
                    }else if (row.disk_percentage < 75){
                        return "warning"
                    }else {
                        return "exception"
                    }

                }
            },

        }


    }
</script>

<style scoped>
    .cell p {
        margin: 0px
    }


</style>