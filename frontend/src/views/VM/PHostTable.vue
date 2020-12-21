<template>

    <div>

    <el-table :data="tableData" size="small">
        <el-table-column type="index"/>
        <el-table-column
                label="Name"
        >
            <template slot-scope="scope">
                <router-link :to="{name:'PHostDetail',params:{id:scope.row.id}}">
                    <el-link type="primary" :underline="false">{{ scope.row.name }}</el-link>
                </router-link>
            </template>
        </el-table-column>

        <el-table-column
                label="機型"
        >
            <template slot-scope="scope">
                <span>{{scope.row.ansible_product_name}}</span>
            </template>
        </el-table-column>


        <el-table-column
                label="系統"
        >
            <template slot-scope="scope">
                <span>{{scope.row.ansible_distribution}}</span>
            </template>
        </el-table-column>

        <el-table-column
                label="邏輯處理器"
        >
            <template slot-scope="scope">
                <span>{{scope.row.ansible_processor_vcpus}}</span>
            </template>
        </el-table-column>

        <el-table-column
                label="內存使用率"
        >
            <template slot-scope="scope">
                <span>{{scope.row.ansible_memfree_gb}}GB / {{scope.row.ansible_memtotal_gb}}GB</span>
            </template>
        </el-table-column>


        <el-table-column
                label="IP"
        >
            <template slot-scope="scope">
                <span>{{scope.row.ansible_all_ipv4_addresses}}</span>
            </template>
        </el-table-column>


        <el-table-column
                label="cluster"
        >
            <template slot-scope="scope">
                <span>{{scope.row.cluster}}</span>
            </template>
        </el-table-column>


        <el-table-column label="更新時間">
            <template slot-scope="scope">
                <span>{{scope.row.last_date}}</span>
            </template>
        </el-table-column>

        <el-table-column
                label="功能"
        >
            <template slot-scope="scope">
                <el-button  @click="foo(scope.row)">選擇</el-button>

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

    import {getHost} from '@/api/vm'
    import app from "../../main";


    export default {
        props: ['id'],
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                ins:this.id ||  0,
                filterform:{},
                host:''
            }
        },
        methods: {
            // 分頁
            foo(row){
                // this.datastore.ins = e.id
                console.log(this.cluster)
                console.log(this.cluster.host)
                this.cluster.sethost(row.id)
                // this.datastore.getInit(this.datastore.page,this.datastore.pageSize, this.datastore.filterform)
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
                getHost(page, size, params)
                    .then((response) => {
                        // console.log(response)
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
            // app.$on('datastoreobj', (data) => {
            //     // console.log(data)
            //     vm.datastore = data
            // })
            app.$on('cluster', (data) => {
                // console.log(data)
                vm.cluster = data
            })

        }

    }
</script>
