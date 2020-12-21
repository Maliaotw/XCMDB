<template>

    <div>

        <el-table
                :data="tableData"
                size="small"
                style="width: 100%"

        >

            <el-table-column
                    prop="name"
                    label="name"
            >
                <template slot-scope="scope">
                    {{scope.row.name}}
                    <el-input v-model="scope.row.remark" @change="datastore_push(scope.row)"/>
                </template>

            </el-table-column>

            <el-table-column
                    prop="capacity"
                    label="總容量"
            >
            </el-table-column>


            <el-table-column
                    prop="freeSpace"
                    label="可用空間"
            >
            </el-table-column>

            <el-table-column
                    prop="provisioned"
                    label="置備空間"
            >
            </el-table-column>

            <el-table-column
                    label="status"
            >
                <template slot-scope="scope">
                    <el-switch
                            v-model="scope.row.status"
                            active-color="#13ce66"
                            inactive-color="#ff4949"
                            @change="datastore_push(scope.row)"
                    >
                    </el-switch>

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

    import {getDatastore, putDataStoreobj} from '../../api/vm'
    import app from "../../main";


    export default {
        props: ['id'],
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                ins: this.id || 0,
                filterform: {}
            }
        },
        watch: {
            id:{
                immediate: true,
                handler(value) {
                    console.log('watch')
                    console.log(this.id)
                    if (this.id === 0) {
                        this.tableData = []
                    } else {
                        // 根據集群調出底下的instance
                        // console.log(this.ins)
                        this.filterform['host'] = this.id
                        this.getInit(this.page, this.pageSize, this.filterform)
                    }
                }
            }
        },
        methods: {


            datastore_push(row) {
                // console.log(row)
                // console.log(row.id)
                const data = row;
                const id = row.id;
                // delete data['id'];

                putDataStoreobj(id, data)
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
                getDatastore(page, size, params)
                    .then((response) => {
                        console.log(response)
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
            if (this.ins === 0) {
                // this.getInit(this.page, this.pageSize)
                this.tableData = []
            } else {
                // 根據集群調出底下的instance
                // console.log(this.ins)
                this.filterform['host'] = this.ins
                this.getInit(this.page, this.pageSize, this.filterform)
            }
        },
        mounted: function () {
            // app.$emit('init',this.getInit)
            // app.$emit('table',this)
            const vm = this
            app.$on('filter', (data) => {
                console.log(data)
                vm.filterform = data.filterform
            })


        }

    }
</script>