<template>

    <div>
        <el-page-header
                @back="gopack"
                :content=name
                style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px"
        />

        <el-row type="flex" style="margin-bottom: 20px">

            <el-col :span="4">
            </el-col>

            <el-col :span="24" style="text-align: right">
                <el-form :model="filterform">


                    <label style="margin-left: 20px">狀態</label>
                    <el-select v-model="filterform.status"
                               style="margin-left: 20px;margin-right: 20px;"
                               placeholder="狀態"
                               @change="handleFilterSubmit"
                    >
                        <el-option key="" label="----" value=""/>
                        <el-option label="SUCCESS" key="SUCCESS" value="SUCCESS"/>
                        <el-option label="FAILURE" key="FAILURE" value="FAILURE"/>

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



        <el-row type="flex" style="margin-bottom: 20px">

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
                            label="ID"
                            width="320"
                    >

                        <template slot-scope="scope">
                            <span>{{scope.row.task_id}}</span>
                        </template>
                    </el-table-column>

                    <el-table-column
                            label="開始日期"
                            width="170"
                    >
                        <template slot-scope="scope">
                            <span>{{scope.row.date_done}}</span>
                        </template>
                    </el-table-column>


                    <el-table-column
                            label="狀態"
                            width="150"
                    >
                        <template slot-scope="scope">
                            <span>{{scope.row.status}}</span>
                        </template>
                    </el-table-column>


                    <el-table-column
                            label="動作"
                            width="100"
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


                <el-dialog
                        :visible.sync="dialogVisible"
                        width="40%"
                        :show-close="false"
                >
                    <div>
                        <h2 style="margin-bottom: 20px">{{Form.name}}</h2>
                        <p>結果返回: </p>
                        <pre style="min-height:300px;padding: 0.5em;background:#F0F0F0;white-space: pre-wrap;">{{Form.result}}</pre>
                    </div>

                    <div style="text-align: center">
                 <span slot="footer" class="dialog-footer">
                    <el-button type="info" @click="dialogVisible = false">確定</el-button>
                </span>

                    </div>

                </el-dialog>

            </el-col>


            <el-col :span="12">
                <p>結果顯示在這裡</p>
                <pre style="background: #111111;min-height: 600px;color: white;padding: 15px;overflow: scroll;">{{result}}</pre>

            </el-col>

        </el-row>


    </div>

</template>


<script>

    import {getPtObj} from '../../api/pt'
    import {getTd} from '../../api/td'
    import LineChart from '../../Chart/LineChart'
    import PieChart from '../../Chart/PieChart'



    export default {
        components: {
            LineChart,
            PieChart
        },
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
                Form: {
                    name: '',
                    result: '',
                    id: ''
                },
                filterform: {
                    datetime:''
                },
                name: '',
                result: ''
            }
        },

        methods: {

            // 提交搜索
            handleFilterSubmit() {
                this.getInit(this.page, this.pageSize, this.filterform)
            },

            gopack() {
                this.$router.push({name: 'pt'})
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

            // 顯示刪除通知框
            detask(row) {
                // this.dialogVisible = true
                // this.Form.name = `${row.task_id}: ${row.task_name}`
                // this.Form.result = `${row.result}`
                // this.Form.id = row.id
                this.result = `${row.result}`
            },


            getInit(p, size, params) {
                if (p === '1') {
                    p = 0
                } else {
                    p = p - 1
                }
                const page = p * this.pageSize
                getPtObj(this.$route.params.id)
                    .then((response) => {
                        // console.log(response)
                        const data = response.data;
                        this.name = data.name;

                        this.filterform.task_name = data.task
                        this.filterform.task_args = data.args
                        this.filterform.task_kwargs = data.kwargs

                        getTd(page, size, this.filterform)
                            .then((response) => {
                                this.tableData = response.data.results
                                this.total = response.data.count
                            })

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
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
            this.filterform.datetime = [start, end]

            // get and set auth user
            this.getInit(this.page, this.pageSize)

        }


    }
</script>