<template>


    <div>
        <!--  ESXI List -->
        <el-table
                :data="tableData"
                size="small"
                style="width: 100%"
        >
            <el-table-column type="index"/>

            <el-table-column
                    prop="network"
                    label="network"
                    sortable
            >
                <template slot-scope="scope">
                    {{scope.row.network}}
                    <el-input v-model="scope.row.remark" @change="network_push(scope.row)"/>
                </template>

            </el-table-column>


            <el-table-column
                    prop="vlan_id"
                    label="vlan_id"
            >
            </el-table-column>


            <el-table-column
                    prop="vswitch"
                    label="vswitch"
            >
            </el-table-column>


            <el-table-column
                    label="Status"
            >
                <template slot-scope="scope">
                    <el-switch
                            v-model="scope.row.status"
                            active-color="#13ce66"
                            inactive-color="#ff4949"
                            @change="network_push(scope.row)"
                    >
                    </el-switch>

                </template>
            </el-table-column>

            <el-table-column
                    label="自動分配"
            >
                <template slot-scope="scope">
                    <el-switch
                            v-model="scope.row.dhcp"
                            active-color="#13ce66"
                            inactive-color="#ff4949"
                            @change="network_push(scope.row)"
                    >
                    </el-switch>

                </template>
            </el-table-column>

            <el-table-column
                    label="功能"
            >
                <template slot-scope="scope">
                    <el-button @click="foo(scope.row)">選擇</el-button>
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

    import {getNetwork, putNetworkobj} from '@/api/vm'
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
                filterform: {},
            }
        },
        watch: {
            id: {
                immediate: true,
                handler(value) {
                    console.log('watch')
                    console.log(this.id)
                    if (this.id === 0) {
                        this.tableData = []
                    } else {
                        // 根據集群調出底下的instance
                        // console.log(this.ins)
                        this.filterform['cluster'] = this.id
                        this.getInit(this.page, this.pageSize, this.filterform)
                    }
                }
            }
        },
        methods: {

            foo(row) {
                console.log('foo')
                console.log(row.id)
                this.cluster.setnet(row.id)

            },

            network_push(row) {
                // console.log(row)
                // console.log(row.id)
                const data = row;
                const id = row.id;
                // delete data['id'];

                putNetworkobj(id, data)
                    .then((res) => {
                        console.log('ok')
                        console.log(res)

                        if (res) {
                            this.$notify.success({
                                title: '成功',
                                message: '这是一条成功的提示消息'
                            });
                        } else {
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
                getNetwork(page, size, params)
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

            app.$on('cluster', (data) => {
                // console.log(data)
                vm.cluster = data
            })
        }

    }
</script>
