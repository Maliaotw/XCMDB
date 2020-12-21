<template>
    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>機房管理</el-breadcrumb-item>
                <el-breadcrumb-item :to="{name:'Rack'}">機櫃列表</el-breadcrumb-item>
                <el-breadcrumb-item>{{form.name}}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>



        <el-row type="flex">
            <el-col :span="24">
                <template>
                    <el-tabs v-model="activeName" @tab-click="handleClick">
                        <el-tab-pane label="基本資訊" name="basic"/>
                        <el-tab-pane label="設備調整" name="change"/>
                        <el-tab-pane label="ISP接入" name="isp"/>
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
                                                    label="IDC"
                                            >
                                                <span>{{form.idc.name}}</span>
                                            </el-form-item>
                                        </el-col>

                                        <el-col>
                                            <el-form-item
                                                    label="地址"
                                            >
                                                <span>#</span>
                                            </el-form-item>
                                        </el-col>

                                        <el-col>
                                            <el-form-item
                                                    label="廠商"
                                            >
                                                <span>#</span>
                                            </el-form-item>
                                        </el-col>

                                        <el-col>
                                            <el-form-item
                                                    label="聯繫人"
                                            >
                                                <span>#</span>
                                            </el-form-item>
                                        </el-col>

                                        <el-col>
                                            <el-form-item
                                                    label="機櫃號"
                                            >
                                                <span>{{form.name}}</span>
                                            </el-form-item>
                                        </el-col>

                                        <el-col>
                                            <el-form-item
                                                    label="最大功率"
                                            >
                                                <span>{{form.max_power}} (W)</span>
                                            </el-form-item>
                                        </el-col>


                                        <el-col>
                                            <el-form-item
                                                    label="高度"
                                            >
                                                <span>{{form.height}}U</span>
                                            </el-form-item>
                                        </el-col>


                                        <el-col>
                                            <el-form-item
                                                    label="備註"
                                            >
                                                <span>{{form.remark}}</span>
                                            </el-form-item>
                                        </el-col>


                                    </el-row>

                                </el-form>
                            </el-col>
                        </el-row>


                    </el-card>

                </div>


                <div v-show="activeName === 'change'">
                    <p class="text-center">設備清單</p>

                    <el-table
                            :data="tableData"
                            style="width: 100%"
                    >

                        <el-table-column type="index">
                        </el-table-column>

                        <el-table-column
                                label="名稱"
                                width="200px"
                        >
                            <template slot-scope="scope">
                                <router-link :to="{name:'AssetDetail',params:{id:scope.row.asset.id}}">
                                    <el-link type="primary" :underline="false">{{ scope.row.asset.name }}</el-link>
                                </router-link>

                            </template>

                        </el-table-column>


                        <el-table-column
                                prop="address"
                                label="機型大小"
                                width="100px"

                        >
                            <template slot-scope="scope">
                                <span>{{scope.row.asset.size}}</span>
                            </template>


                        </el-table-column>

                        <el-table-column
                                prop="address"
                                label="位置"
                        >
                            <template slot-scope="scope">
                                <el-select
                                        v-model="scope.row.position"
                                        placeholder=""
                                        class="text-center"
                                        @change="SubmitChange(scope.row)"
                                >
                                    <el-option
                                            v-for="item in positionlist"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value"
                                    >

                                    </el-option>

                                </el-select>

                            </template>
                        </el-table-column>


                        <el-table-column
                                prop="address"
                                label="層數"
                        >
                            <template slot-scope="scope">

                                <el-select
                                        v-model="scope.row.num"
                                        placeholder=""
                                        class="text-center"
                                        @change="SubmitChange(scope.row)"
                                >

                                    <el-option
                                            v-for="item in size"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value"
                                            :disabled="item.disabled"
                                    >

                                    </el-option>
                                </el-select>
                            </template>

                        </el-table-column>


                    </el-table>


                </div>


                <div v-show="activeName === 'isp'">

                    <el-table
                            :data="isplist"
                            style="width: 100%">
                        <el-table-column
                                label="名稱"
                        >
                            <template slot-scope="scope">
                                {{ scope.row.name }}
                            </template>
                        </el-table-column>
                        <el-table-column
                                label="IP範圍"
                        >
                            <template slot-scope="scope">
                                {{ scope.row.ip_range }}
                            </template>
                        </el-table-column>
                        <el-table-column
                                label="NETMASK"
                        >
                            <template slot-scope="scope">
                                {{ scope.row.netmask }}
                            </template>
                        </el-table-column>

                        <el-table-column
                                label="GETEWAY"
                        >
                            <template slot-scope="scope">
                                {{ scope.row.geteway }}
                            </template>
                        </el-table-column>

                        <el-table-column
                                label="備註"
                        >
                            <template slot-scope="scope">
                                {{ scope.row.remark }}
                            </template>
                        </el-table-column>

                    </el-table>

                </div>


            </el-col>


            <el-col :span="12" v-show="activeName === 'change'">
                <p class="text-center">機櫃</p>


                <el-col
                        :span="12"
                >
                    <p class="text-center">Front</p>

                    <el-table
                            class="table"
                            :data="posrange"
                            style="width: 95%;margin-left: 10px"
                            :show-header=false
                            :span-method="objectSpanMethod"
                    >


                        <el-table-column
                                width="40"
                                class-name="tdl"
                        >
                            <template slot-scope="scope">
                                <p class="text-center">
                                    {{scope.row.num}}
                                </p>
                            </template>
                        </el-table-column>

                        <el-table-column
                                class-name="tdr"


                        >
                            <template slot-scope="scope">
                                <div v-if="scope.row.position === 'Front'"
                                     class="text-center  font-black"
                                >
                                    <p>
                                        {{scope.row.name}}
                                    </p>
                                    <p>
                                        {{scope.row.manage_ip}}
                                    </p>
                                </div>
                                <div v-else class="text-center font-grey">
                                    <p>
                                        {{scope.row.name}}
                                    </p>
                                    <p>
                                        {{scope.row.manage_ip}}
                                    </p>
                                </div>
                            </template>
                        </el-table-column>

                    </el-table>

                </el-col>

                <el-col :span="12">
                    <p class="text-center">Back</p>

                    <el-table
                            class="table"
                            :data="posrange"
                            style="width: 95%;margin-left: 10px"
                            :show-header=false
                            :span-method="objectSpanMethod"
                    >


                        <el-table-column
                                label=""
                                width="40px"
                                class-name="tdl"

                        >
                            <template slot-scope="scope">
                                <p class="text-center">
                                    {{scope.row.num}}
                                </p>
                            </template>
                        </el-table-column>

                        <el-table-column
                                label=""
                                class-name="tdr"

                        >
                            <template slot-scope="scope">
                                <div v-if="scope.row.position === 'Back'"
                                     class="text-center font-black"
                                >
                                    <p>
                                        {{scope.row.name}}
                                    </p>
                                    <p>
                                        {{scope.row.manage_ip}}
                                    </p>
                                </div>
                                <div v-else class="text-center font-grey">
                                    <p>
                                        {{scope.row.name}}
                                    </p>
                                    <p>
                                        {{scope.row.manage_ip}}
                                    </p>
                                </div>
                            </template>
                        </el-table-column>

                    </el-table>

                </el-col>
            </el-col>
        </el-row>


    </div>


</template>

<script>
    import {getRackDetailObj} from "../../api/rack"
    import {edit} from "../../api/rackunit"

    export default {
        data() {
            return {
                form: {},
                // activeName: 'basic',
                tabcontainer: 12,
                activeName: 'change',
                tableData: [],
                positionlist: [
                    {'value': 1, 'label': 'Front'},
                    {'value': 2, 'label': 'Back'},
                ],
                height: 42,
                posrange: []
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
                getRackDetailObj(this.$route.params.id)
                    .then(res => {
                        // console.log(res);
                        this.tableData = res.data.rackunit
                        this.form = res.data
                        this.height = res.data.height
                        this.posrange = res.data.posrange
                        this.size = res.data.size
                        this.isplist = res.data.isp
                    })

            },
            objectSpanMethod({row, column, rowIndex, columnIndex}) {
                // console.log(row)
                // console.log('第' + rowIndex + '行', '第' + columnIndex + '列', 'rowspan:' + row, 'colspan:' + column)
                if (columnIndex === 1) {
                    if (row.size > 1) {
                        return {
                            rowspan: row.size,
                            colspan: 1
                        };
                    } else if (row.disabled === 'true') {
                        return {
                            rowspan: 0,
                            colspan: 0
                        };
                    }
                }
            }
        },
        created() {
            this.getinit();
            // this.size()
        }
    };
</script>

<style scoped>

    .el-row {
        margin-bottom: 20px;
    }



</style>
