<template>

    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>機房管理</el-breadcrumb-item>
                <el-breadcrumb-item>ISP列表</el-breadcrumb-item>
            </el-breadcrumb>
        </div>


        <el-row :gutter="20" style="margin-bottom: 20px">

            <el-col :span="4">
                <router-link :to="{name:'IspCreate'}">
                    <el-button type="primary">新增</el-button>
                </router-link>
            </el-col>

            <el-col :span="24" style="text-align: right">

            </el-col>
        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index">
            </el-table-column>
            <el-table-column
                    label="名稱"
            >
                <template slot-scope="scope">
                    <span>{{scope.row.name}}</span>

                </template>
            </el-table-column>

            <el-table-column label="IP範圍">
                <template slot-scope="scope">
                    <span>{{scope.row.ip_range}}</span>
                </template>
            </el-table-column>


            <el-table-column label="NETMASK">
                <template slot-scope="scope">
                    <span>{{scope.row.netmask}}</span>
                </template>
            </el-table-column>

            <el-table-column label="GETEWAY">
                <template slot-scope="scope">
                    <span>{{scope.row.geteway}}</span>
                </template>
            </el-table-column>


            <el-table-column label="備註">
                <template slot-scope="scope">
                    <span>{{scope.row.remark}}</span>
                </template>
            </el-table-column>

            <el-table-column label="功能">
                <template slot-scope="scope">
                    <router-link :to="{name:'ISPUpdate',params:{id:scope.row.id}}">
                        <el-button>編輯</el-button>
                    </router-link>
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

    import {getISP} from '../../api/isp'


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
                EditisShow: false,
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
                getISP(page, size, params)
                    .then((response) => {
                        console.log(response)
                        this.tableData = response.data.results
                        this.total = response.data.count
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