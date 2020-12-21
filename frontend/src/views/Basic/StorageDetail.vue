<template>
    <div>
        <el-row type="flex">
            <el-col :span="24">
                <template>
                    <el-tabs v-model="activeName" @tab-click="handleClick">
                        <el-tab-pane label="基本資訊" name="basic"></el-tab-pane>
                        <el-tab-pane label="硬盤資訊" name="disk"></el-tab-pane>
                        <el-tab-pane label="控制器" name="ctl"></el-tab-pane>
                    </el-tabs>
                </template>
            </el-col>

        </el-row>

        <el-row type="flex">
            <el-col
                    :span="tabcontainer"
            >

                <div v-show="activeName === 'basic'">
                    <el-card
                            class="box-card"
                    >
                        <div slot="header" class="clearfix">
                            <span>基本資訊</span>
                        </div>

                        <el-row>
                            <el-col :span="12" :offset="6">
                                <el-form
                                        :model="form"
                                        ref="form"
                                        label-position="left"
                                        label-width="160px"
                                >
                                    <el-row>

                                        <el-col :span="24">

                                        </el-col>

                                        <el-col>
                                            <el-form-item
                                                    label="名稱"
                                            >
                                                <span>{{tableData.name}}</span>
                                            </el-form-item>
                                        </el-col>

                                        <el-col>
                                            <el-form-item label="控制器數量">
                                                <span>{{tableData.storagectl.length}}</span>
                                            </el-form-item>
                                        </el-col>

                                        <el-col>
                                            <el-form-item label="硬盤插槽數量">
                                                {{tableData.storagedisk.length}} / <span style="color: red">{{tableData.slotnum}}</span>
                                            </el-form-item>
                                        </el-col>

                                        <el-col>
                                            <el-form-item label="創建日期">
                                                <span>{{tableData.create_at}}</span>
                                            </el-form-item>
                                        </el-col>

                                        <el-col>
                                            <el-form-item label="最近更新日期">
                                                <span>{{tableData.latest_date}}</span>
                                            </el-form-item>
                                        </el-col>

                                    </el-row>

                                </el-form>
                            </el-col>
                        </el-row>


                    </el-card>

                </div>


                <div v-show="activeName === 'disk'">
                    <p class="text-center">硬盤清單</p>
                    <el-table
                            :data="tableData.storagedisk"
                            style="width: 100%">
                        <el-table-column
                                prop="slot"
                                label="插槽"
                        >
                        </el-table-column>
                        <el-table-column
                                prop="model"
                                label="型號"
                        >
                        </el-table-column>
                        <el-table-column
                                prop="capacity"
                                label="容量"
                        >
                        </el-table-column>
                    </el-table>

                </div>


                <div v-show="activeName === 'ctl'">
                    <p class="text-center">控制器</p>
                    <el-table
                            :data="tableData.storagectl"
                            style="width: 100%">
                        <el-table-column
                                prop="name"
                                label="名稱"
                        >
                        </el-table-column>
                        <el-table-column
                                prop="slot"
                                label="插槽"
                        >
                        </el-table-column>
                        <el-table-column
                                prop="manage_ip"
                                label="管理IP"
                        >
                        </el-table-column>
                    </el-table>
                </div>


            </el-col>


        </el-row>


    </div>


</template>

<script>
    import {getStorageObj} from "../../api/storage"

    export default {
        data() {
            return {
                form: {},
                activeName: 'basic',
                tabcontainer: 24,
                tableData: [],
            };
        },

        methods: {


            handleClick(tab, event) {
                // console.log(tab, event);
                if (tab.paneName === 'change') {
                    this.tabcontainer = 12
                } else {
                    this.tabcontainer = 24
                }

            },

            SubmitChange(row) {

                // this.form.id = row.id
                this.form.position = row.position
                this.form.num = row.num
                edit(row.id, this.form).then(
                    (res) => {
                        console.log(res)
                        this.$notify.success(
                            {message: '更改成功'}
                        )
                        this.getinit()
                    }
                )

            },

            getinit() {
                getStorageObj(this.$route.params.id)
                    .then(res => {
                        // console.log(res);
                        this.tableData = res.data
                        // this.form = res.data
                        // this.height = res.data.height
                        // this.posrange = res.data.posrange
                        // this.size = res.data.size
                        // this.isplist = res.data.isp
                    })

            },
        },
        created() {

            // this.activeTag = '/Home/Host'
            // this.$attrs.activeTag = "/Home/Host"
            this.getinit()
            console.log(this.$store.state.jwt)
            console.log(this.$store.state)
            this.$store.state.users.navTags = [{
                active: true,
                index: "/Home/Storage",
                title: "存儲設備列表"
            },]

            // this.size()
        }
    };
</script>

<style scoped>



</style>
