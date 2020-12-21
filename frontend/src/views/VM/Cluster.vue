<template>

    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>VM</el-breadcrumb-item>
                <el-breadcrumb-item :to="{name:'Server'}">集群</el-breadcrumb-item>
            </el-breadcrumb>
        </div>


        <el-row :gutter="20" style="margin-bottom: 20px">

            <el-col :span="4">
            </el-col>

        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index"/>


            <el-table-column
                    label="Name"
            >
                <template slot-scope="scope">
                    <router-link :to="{name:'ClusterDetail',params:{id:scope.row.id}}">
                        <el-link type="primary" :underline="false">{{ scope.row.name }}</el-link>

                    </router-link>
                    <el-input v-model="scope.row.remark" @change="cluster_push(scope.row)"/>
                </template>
            </el-table-column>

            <el-table-column
                    label="Esxi"
            >
                <template slot-scope="scope">
                    <span>{{scope.row.esxi_num}} (台)</span>
                </template>
            </el-table-column>

            <el-table-column
                    label="虛擬機"
            >
                <template slot-scope="scope">
                    <span>{{scope.row.vm_num}} (台)</span>
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

    import {getCluster, putClusterobj} from '@/api/vm'


    export default {
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                form: {},
            }
        },
        destroyed() {

        },
        methods: {
            // 分頁
            cluster_push(row) {
                // console.log(row)
                // console.log(row.id)

                const data = row
                const id = row.id
                delete data['id']

                putClusterobj(id, data)
                    .then((res) => {
                        console.log('ok')
                        console.log(res)

                        if (res){
                            this.$notify.success({
                                title: '成功',
                                message: '这是一条成功的提示消息'
                            });
                        }else{
                            this.$notify.error({
                                title: '失敗',
                                message: '这是一条失敗的提示消息'
                            });
                        }



                    })

            },

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
                getCluster(page, size, params)
                    .then((response) => {
                        this.tableData = response.data.data.results
                        this.total = response.data.data.count
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


    }
</script>
