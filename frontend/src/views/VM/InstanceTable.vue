<template>

    <div>


        <el-table :data="tableData" style="width: 100%"  >
            <el-table-column type="index"/>
            <el-table-column
                    label="Name"
                    prop="hw_name"
                    sortable
            >
                <template slot-scope="scope">
                    <span>{{scope.row.hw_name}}</span>
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
    import app from '../../main'

    export default {
        name: "InstanceTable",  // using EXACTLY this name is essential,
        props: ['id'],
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                ins:this.id ||  0,
                filterform:{}
            }
        },
        methods: {


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
            getInit(p, size) {


                if (p === '1') {
                    p = 0
                } else {
                    p = p - 1
                }
                const page = p * this.pageSize
                getInstance(page, size, this.filterform)
                    .then((response) => {
                        // console.log(response)
                        this.tableData = response.data.results
                        this.total = response.data.count
                        // this.host = response.data.host
                        // this.network = response.data.network
                        // this.datastore = response.data.datastore
                        app.$emit('datastore',response.data.datastore);
                        app.$emit('network',response.data.network);
                        app.$emit('host',response.data.host)

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

            if (this.ins === 0){
                this.getInit(this.page, this.pageSize)
            }else {
                // 根據集群調出底下的instance
                // console.log(this.ins)
                this.filterform['cluster'] = this.ins
                this.getInit(this.page, this.pageSize,this.filterform)
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
