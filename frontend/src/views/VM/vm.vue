<template>

    <div>

        <el-row :gutter="20" style="margin-bottom: 20px">

            <el-col :span="4">
                <router-link :to="{name:'InsCreate'}">
                    <el-button type="primary">新增Ins</el-button>
                </router-link>
            </el-col>

        </el-row>

        <el-table :data="tableData" size="small">
            <el-table-column type="index"></el-table-column>
            <el-table-column
                    label="Name"
                    width="150px"
            >
                <template slot-scope="scope">
                    <span>{{scope.row.name}}</span>
                </template>
            </el-table-column>


            <el-table-column
                    label="類型"
                    width="80px"
            >
                <template slot-scope="scope">
                    <span>{{scope.row.type}}</span>
                </template>
            </el-table-column>


            <el-table-column
                    label="實例ID"
                    width="320px"
            >
                <template slot-scope="scope">
                    <span>{{scope.row.task}}</span>
                </template>
            </el-table-column>


            <el-table-column label="狀態">
                <template slot-scope="scope">
                    <span v-html="status(scope.row)"></span>
                </template>
            </el-table-column>

            <el-table-column label="狀態檢查">
                <template slot-scope="scope">
                    <span v-html="check(scope.row)"></span>
                </template>
            </el-table-column>


            <el-table-column label="管理IP">
                <template slot-scope="scope">
                    <span>{{scope.row.manage_ip}}</span>
                </template>
            </el-table-column>

            <el-table-column label="功能">
                <template slot-scope="scope">

                    <div v-if="scope.row.is_finish">
                        <el-button
                                type="primary"
                                style="margin-left: 10px"
                        >
                            <span>更新</span>
                        </el-button>
                    </div>

                    <div v-else>
                        <el-button
                                style="margin-left: 10px"
                                type="info" plain
                                disabled
                                :ref="scope.row.name"
                        >
                            <span>{{ time(scope.row) }}</span>
                        </el-button>
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

    import {getInstance} from '../../api/instance'


    export default {
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                form: {},
                websock: null,
                names: [],
            }
        },
        destroyed() {
            this.websock.close() //离开路由之后断开websocket连接
            window.clearInterval(this.interval);
        },
        methods: {
            time: function (row) {
                // return function (row) {

                // 計算出剩餘秒數 由300秒開始計算
                // const now = Date.parse(new Date(d))
                const end = Date.parse(new Date(row.create_at)) + 300000
                const now = Date.parse(new Date())
                const msec = end - now
                const ret = msec / 1000

                // 將name推到列表
                // console.log(row.name)
                if (this.names.includes(row.name)) {
                } else {
                    this.names.push(row.name)
                }
                return ret


                // }
            },
            send: function () {
                this.interval = window.setInterval(() => {
                    console.log(this.names)
                    this.names.forEach((v) => {
                        let val = this.$refs[v].$el.innerText
                        if (val > 0) {
                            --this.$refs[v].$el.innerText
                        } else if (typeof val === 'number') {
                            // this.$refs[v].$el.innerText = "應該快了...";
                        } else {
                            this.$refs[v].$el.innerText = "應該快了...";
                            this.tableData = []
                            this.names = []
                            this.getInit(this.page, this.pageSize)
                        }
                    })
                }, 1000);
            },

            initWebSocket() { //初始化weosocket
                const wsuri = "ws://192.168.10.81:8000/api/vm/echo_once";
                // const wsuri = "ws://192.168.10.81:8080/ws/echo_once";
                this.websock = new WebSocket(wsuri);
                this.websock.onmessage = this.websocketonmessage;
                this.websock.onerror = this.websocketonerror;
                this.websock.onclose = this.websocketclose;
            },
            websocketonerror() {//连接建立失败重连
                this.initWebSocket();
            },
            websocketonmessage(e) { //数据接收
                const redata = JSON.parse(e.data);
                // console.log(redata)
                this.foo(redata)
            },
            websocketclose(e) {  //关闭
                console.log('断开连接', e);
            },

            // 提交搜索
            handleFilterSubmit() {
                this.getInit(this.page, this.pageSize, this.filterform)
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
            foo(data) {
                console.log(data)
                console.log(this.tableData)
                console.log(`this.names ${this.names}`)

                const namelist = []

                this.tableData.forEach((v) => {
                    namelist.push(v.name)
                });
                console.log(`namelist ${namelist}`)

                if (namelist.includes(data.hostname)){

                }else {
                    this.tableData = []
                    this.getInit(this.page, this.pageSize)
                }

                let col = this.tableData.find((item) => {
                        return item.name === data.hostname
                })
                if (data.is_finish) {
                    col.is_finish = data.is_finish
                    this.tableData = []
                    this.names = []
                    this.getInit(this.page, this.pageSize)
                }
                if (col) {
                    col.name = data.hostname
                    // col.status = data.status
                    col.check = data.check
                    // col.time = data.time
                    // console.log(data.time)
                }
            },


            // 請求資產
            getInit(p, size, params) {
                if (p === '1') {
                    p = 0
                } else {
                    p = p - 1
                }
                const page = p * this.pageSize
                getInstance(page, size, params)
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
            this.getInit(this.page, this.pageSize)
            this.initWebSocket();
            this.send()


        },
        computed: {
            status: function () {
                return function (row) {
                    if (row.status === "running") {
                        return '<i class="el-icon-video-play" style="color: green"></i> Running'
                    } else if (row.status === "構建失敗") {
                        return '<i class="el-icon-warning" style="color: red"></i> 構建失敗'
                    } else if (row.status === "正在初始化中") {
                        return '<i class="el-icon-time"></i> 開始初始化中'
                    }
                }
            },

            check: function (row) {
                return function (row) {
                    if (row.check === "即將銷毀") {
                        return `${row.check}...`
                    } else if (row.check.includes("check pass")) {
                        return `<i class="el-icon-success" style="color: green"></i>${row.check}`
                    } else {
                        return `${row.check}`
                    }
                }
            }


        }


    }
</script>