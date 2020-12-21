<template>

    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>作業中心</el-breadcrumb-item>
                <el-breadcrumb-item>任務列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <el-row type="flex" style="margin-bottom: 20px">

            <el-col :span="4">
            </el-col>

            <el-col :span="20" style="text-align: right">

                <el-form :model="filterform">

                    <label style="margin-right: 20px;">名稱</label>

                    <el-input
                            v-model="filterform.name"
                            placeholder="请输入内容"
                            style="width:20%; margin-right: 2px;"
                            @change="handleFilterSubmit"
                    >

                    </el-input>





                </el-form>
            </el-col>


        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index">
            </el-table-column>
            <el-table-column
                    label="name"
                    width="300px"
            >
                <template slot-scope="scope">
                    <!--<span>{{scope.row.floor}}</span>-->
                    <router-link :to="{name:'PtDetail',params:{id:scope.row.id}}">
                        <el-link type="primary" :underline="false">{{ scope.row.name }}: {{scope.row.crontab}}</el-link>
                    </router-link>

                </template>
            </el-table-column>

            <el-table-column label="執行次數">
                <template slot-scope="scope">
                    <p>
                        <span style="color: red">{{scope.row.total_failure_count}}/</span>
                        <span style="color:#1ab394;">{{scope.row.total_success_count}}/</span>
                        <span>{{scope.row.total_run_count}}</span>
                    </p>
                </template>
            </el-table-column>

            <el-table-column label="成功">
                <template slot-scope="scope">
                    <span v-html="status(scope.row)"/>
                </template>
            </el-table-column>

            <el-table-column label="日期">
                <template slot-scope="scope">

                    <span>{{scope.row.last_run_at}}</span>
                </template>
            </el-table-column>


            <el-table-column label="功能">
                <template slot-scope="scope">

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

    import {getPT} from '../../api/pt'


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
                filterform:{}
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
                getPT(page, size, params)
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

        },
        computed: {
            status: function () {
                return function (row) {
                    const status = row.last_status;
                    if (status === "SUCCESS") {
                        return '<i class="el-icon-check" style="color: green"></i>'
                    } else if (status === "FAILURE") {
                        return '<i class="el-icon-close" style="color: red"></i>'
                    }
                }
            },


        }

    }
</script>