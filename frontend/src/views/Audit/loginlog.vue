<template>

    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>日誌審計</el-breadcrumb-item>
                <el-breadcrumb-item>登入歷史</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <el-row type="flex" style="margin-bottom: 20px">

            <el-col :span="24" style="text-align: right">

                <el-form :model="filterform">

                    <label style="margin-right: 20px;">名稱</label>

                    <el-input
                            v-model="filterform.username"
                            placeholder="请输入内容"
                            style="width:15%; margin-right: 20px;"
                            @change="handleFilterSubmit"
                    >

                    </el-input>


                    <label style="margin-left: 20px">狀態</label>
                    <el-select v-model="filterform.status"
                               style="margin-left: 20px;margin-right: 20px;"
                               placeholder="狀態"
                               @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""/>
                        <el-option label="成功" key="True" value="True"/>
                        <el-option label="失敗" key="False" value="False"/>

                    </el-select>


                    <label style="margin-left: 20px">日期</label>
                    <el-date-picker
                            v-model="filterform.datetime"
                            style="margin-left: 20px;margin-right: 20px;"
                            type="datetimerange"
                            start-placeholder="开始日期"
                            end-placeholder="结束日期"
                            @change="handleFilterSubmit"
                    >
                    </el-date-picker>


                </el-form>
            </el-col>

        </el-row>

        <el-table
                :data="tableData"
                size="small"
        >
            <el-table-column type="index">
            </el-table-column>
            <el-table-column label="用戶名">
                <template slot-scope="scope">
                    <span>{{scope.row.username}}</span>
                </template>
            </el-table-column>

            <el-table-column label="類型">
                <template slot-scope="scope">
                    <span>{{scope.row.type}}</span>
                </template>
            </el-table-column>

            <el-table-column label="Agent">
                <template slot-scope="scope">
                    <span>{{scope.row.user_agent.slice(0,20)}}</span>
                </template>
            </el-table-column>

            <el-table-column label="IP">
                <template slot-scope="scope">
                    <span>{{scope.row.ip}}</span>
                </template>
            </el-table-column>

            <el-table-column label="城市">
                <template slot-scope="scope">
                    <span>{{scope.row.city}}</span>
                </template>
            </el-table-column>

            <el-table-column label="原因">
                <template slot-scope="scope">
                    <span>{{scope.row.reason}}</span>
                </template>
            </el-table-column>

            <el-table-column label="狀態">
                <template slot-scope="scope">
                    <span>{{scope.row.status}}</span>
                </template>
            </el-table-column>

            <el-table-column label="日期">
                <template slot-scope="scope">
                    <span>{{scope.row.datetime}}</span>
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

    import {getAll} from '../../api/loginlog'


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
                filterform: {
                    datetime:''
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
                const page = p * this.pageSize;

                getAll(page, size, this.filterform)
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
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
            this.filterform.datetime = [start, end]

            this.getInit(this.page, this.pageSize)



        }


    }
</script>