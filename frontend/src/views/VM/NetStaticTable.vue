<template>


    <div>
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
                    <el-input v-model="scope.row.lan" size="small"/>
                </template>

            </el-table-column>


            <el-table-column
                    prop="gateway"
                    label="gateway"
            >
                <template slot-scope="scope">
                    <el-input v-model="scope.row.gateway" size="small"/>
                </template>

            </el-table-column>


            <el-table-column
                    prop="template"
                    label="template"
            >
                <template slot-scope="scope">
                    <el-select v-model="scope.row.template" placeholder="">
                        <el-option
                                v-for="item in template"
                                :key="item.id"
                                :label="item.hw_name"
                                :value="item.id">
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>


            <el-table-column
                    label="功能"
            >
                <template slot-scope="scope">
                    <!--                    <div v-html=option(scope.row)></div>-->
                    <div v-if="scope.row.id">
                        <el-button type="primary" @click="change(scope.row)" size="small">修改</el-button>
                        <el-button type="danger" @click="del(scope.row)" size="small">刪除</el-button>
                    </div>
                    <div v-else>
                        <el-button type="primary" @click="add(scope.row)" size="small">新增</el-button>
                    </div>

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

    import {getNetStatic, PutNetStatic, AddNetStatic,DelNetStatic} from '../../api/vm'
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
                value: "",
                options: [],
                template: []
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
                        this.filterform['network'] = this.id
                        this.getInit(this.page, this.pageSize, this.filterform)
                    }
                }
            }
        },
        computed: {},
        methods: {

            // 修改 網段關聯表
            change(row) {
                console.log("修改 網段關聯表")
                console.log(row)

                PutNetStatic(row.id, row)
                    .then((res) => {
                        console.log(res)
                        this.$notify.success({
                            title: '成功',
                            message: '这是一条成功的提示消息'
                        });
                    })
                    .catch((error) => {
                        this.$notify.error({
                            title: '错误',
                            message: '这是一条错误的提示消息'
                        });
                    })
            },

            // 新增 網段關聯表
            add(row) {
                console.log("新增 網段關聯表")
                console.log(row)

                AddNetStatic(row)
                    .then((res) => {
                        console.log(res)
                        this.$notify.success({
                            title: '成功',
                            message: '这是一条成功的提示消息'
                        });
                        this.getInit(this.page, this.pageSize, this.filterform)

                    })
                    .catch((error) => {
                        this.$notify.error({
                            title: '错误',
                            message: '这是一条错误的提示消息'
                        });
                    })

            },

            del(row){
                console.log("刪除 網段關聯表")
                DelNetStatic(row.id)
                    .then((res) => {
                        console.log(res)
                        this.$notify.success({
                            title: '成功',
                            message: '这是一条成功的提示消息'
                        });
                        this.getInit(this.page, this.pageSize, this.filterform)

                    })
                    .catch((error) => {
                        this.$notify.error({
                            title: '错误',
                            message: '这是一条错误的提示消息'
                        });
                    })
            },


            // 分頁
            handleIndexChange(p) {
                this.page = p;
                this.getInit(this.page, this.pageSize)

            },
            handleSizeChange(size) {
                this.page = 1;
                this.pageSize = size;
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
                getNetStatic(page, size, params)
                    .then((response) => {
                        console.log(response);
                        this.template = response.data.template;
                        this.tableData = response.data.results;
                        this.tableData.push({
                            "name": "",
                            "lan": "",
                            "gateway": "",
                            "remark": "",
                            "network": this.id,
                            "template": []
                        });

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
                // this.filterform['host'] = this.ins
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