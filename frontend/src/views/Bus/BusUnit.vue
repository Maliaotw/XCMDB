<template>

    <div>



        <el-row :gutter="20" style="margin-bottom: 20px">

            <el-col :span="24" style="text-align: right">

            </el-col>
        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index">
            </el-table-column>
            <el-table-column
                    label="名稱"
                    :width="300"
            >
                <template slot-scope="scope">
                    <span>{{scope.row.name}}</span>
                </template>
            </el-table-column>

            <el-table-column label="英文">
                <template slot-scope="scope">
                    <span>{{scope.row.enname}}</span>
                </template>
            </el-table-column>


            <el-table-column label="資產">
                <template slot-scope="scope">
                    <span></span>
                </template>
            </el-table-column>



            <el-table-column label="功能">
                <template slot-scope="scope">
                    <el-button>編輯</el-button>
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

    </div>

</template>


<script>

    import {getBusunit} from '../../api/busunit'


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
                    device_status_id: '',
                    device_type_id: '',
                    name: '',
                    rack: '',
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
                const page = p * this.pageSize
                getBusunit(page, size, params)
                    .then((response) => {
                        this.tableData = response.data.results
                        this.total = response.data.count
                    })

                    .catch((error) => {

                    })
            },


        },
        created() {
            // get and set auth user
            this.getInit(this.page, this.pageSize)



        }


    }
</script>