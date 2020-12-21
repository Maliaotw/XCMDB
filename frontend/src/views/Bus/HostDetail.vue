<template>


    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>業務資源</el-breadcrumb-item>
                <el-breadcrumb-item :to="{name:'Host'}">虛擬機</el-breadcrumb-item>
                <el-breadcrumb-item>{{this.form.name}}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>


        <el-row type="flex">

            <el-col :span="12">
                <template>
                    <el-tabs v-model="activeName" @tab-click="handleClick">
                        <el-tab-pane label="資產詳情" name="info"></el-tab-pane>
                        <el-tab-pane label="端口信息" name="port"></el-tab-pane>
                        <el-tab-pane label="進程信息" name="process"></el-tab-pane>
                        <el-tab-pane label="變更紀錄" name="change"></el-tab-pane>
                    </el-tabs>
                </template>
            </el-col>

            <el-col :span="12" style="text-align: right">
                <label>最近更新日期： {{ this.form.latest_date }}</label>
            </el-col>

        </el-row>

        <el-row type="flex">
            <el-col :span="14">
                <div v-show="activeName === 'info'">

                    <label><b>主機信息</b></label>
                    <el-form
                            label-position="left"
                            label-width="200px"
                            style="margin-left: 20px;"
                    >
                        <el-form-item label="主機名:" style="margin-bottom: 0px">
                            <label><b>{{this.form.name}}</b></label>
                        </el-form-item>

                        <el-form-item label="類型:" style="margin-bottom: 0px">
                            <label><b>{{this.form.cate}}</b></label>
                        </el-form-item>

                        <el-form-item label="IP:" style="margin-bottom: 0px">
                            <label><b>{{this.form.manage_ip}}</b></label>
                        </el-form-item>

                        <el-form-item label="製造商" style="margin-bottom: 0px">
                            <label><b>{{this.form.manufacturer}}</b></label>
                        </el-form-item>

                        <el-form-item label="型号:" style="margin-bottom: 0px">
                            <label><b>{{this.form.model}}</b></label>
                        </el-form-item>

                        <el-form-item label="系統平台:" style="margin-bottom: 0px">
                            <label><b>{{this.form.os_platform}}</b></label>
                        </el-form-item>

                        <el-form-item label="操作系統:" style="margin-bottom: 0px">
                            <label><b>{{this.form.os_distribution}}</b></label>
                        </el-form-item>

                        <el-form-item label="激活:" style="margin-bottom: 0px">
                            <label><b>{{ this.form.enabled }}</b></label>
                        </el-form-item>

                        <el-form-item label="序列號:" style="margin-bottom: 0px">
                            <label><b>{{ this.form.sn }}</b></label>
                        </el-form-item>

                        <el-form-item label="資產編號:" style="margin-bottom: 0px">
                            <label><b></b></label>
                        </el-form-item>

                        <el-form-item label="創建日期:" style="margin-bottom: 0px">
                            <label><b>{{ this.form.create_at }}</b></label>
                        </el-form-item>

                        <el-form-item label="最後更新日期:" style="margin-bottom: 0px">
                            <label><b>{{ this.form.latest_date }}</b></label>
                        </el-form-item>
                    </el-form>

                    <el-col>
                        <el-collapse v-model="activeNames" @change="handleChange">
                            <el-collapse-item title="CPU" name="1">
                                <el-form
                                        label-width="200px"
                                        label-position="left"
                                        style="margin-left: 20px;"
                                >
                                    <el-form-item
                                            v-for="cpu in form.cpu"
                                            :label="cpu.slot"
                                            style="margin-bottom: 0px"
                                    >
                                        <label><b>{{ cpu.cores}}Cores, {{ cpu.model }}</b></label>
                                    </el-form-item>

                                </el-form>

                            </el-collapse-item>
                            <el-collapse-item title="Disk" name="2">
                                <el-form
                                        label-width="200px"
                                        label-position="left"
                                        style="margin-left: 20px;"
                                >
                                    <el-form-item
                                            v-for="disk in form.disk"
                                            :label="disk.slot"
                                            style="margin-bottom: 0px"
                                    >
                                        <label><b>{{ disk.capacity}}, {{ disk.iface_type }}</b></label>
                                    </el-form-item>

                                </el-form>
                            </el-collapse-item>
                            <el-collapse-item title="Nic" name="3">
                                <el-form
                                        label-width="200px"
                                        label-position="left"
                                        style="margin-left: 20px;"
                                >
                                    <el-form-item
                                            v-for="nic in form.nic"
                                            :label="nic.name"
                                            style="margin-bottom: 0px"
                                    >
                                        <label><b>{{ nic.ipaddress}}, {{ nic.macaddress }}</b></label>
                                    </el-form-item>

                                </el-form>
                            </el-collapse-item>
                            <el-collapse-item title="memory" name="4">
                                <el-form
                                        label-width="200px"
                                        label-position="left"
                                        style="margin-left: 20px;"
                                >
                                    <el-form-item
                                            v-for="mem in form.memory"
                                            :label="mem.slot"
                                            style="margin-bottom: 0px"
                                    >
                                        <label><b>{{ mem.capacity}}G</b></label>
                                    </el-form-item>

                                </el-form>
                            </el-collapse-item>
                        </el-collapse>

                    </el-col>
                </div>

                <div v-show="activeName === 'port'">


                    <template>
                        <el-table
                                :data="form.hostnet"
                                style="width: 95%"
                        >
                            <el-table-column
                                    prop="proto"
                                    label="協定"
                                    sortable
                            >
                            </el-table-column>
                            <el-table-column
                                    prop="port"
                                    label="port"
                                    sortable
                            >
                            </el-table-column>
                            <el-table-column
                                    prop="pid"
                                    label="pid"
                                    sortable
                            >
                            </el-table-column>
                            <el-table-column
                                    prop="name"
                                    label="name"
                                    sortable
                            >
                            </el-table-column>
                        </el-table>
                    </template>


                </div>

                <div v-show="activeName === 'process'">


                    <template>
                        <el-table
                                :data="form.hostproc"
                                border=""
                                style="width: 95%"
                        >
                            <el-table-column
                                    prop="pid"
                                    label="pid"
                                    sortable
                            >
                            </el-table-column>

                            <el-table-column
                                    prop="username"
                                    label="username"
                                    sortable
                            >
                            </el-table-column>

                            <el-table-column
                                    prop="name"
                                    label="進程名稱"
                                    sortable
                            >
                            </el-table-column>


                            <el-table-column
                                    prop="cmdline"
                                    label="cmdline"
                                    sortable
                            >
                                <template slot-scope="scope">
                                    <el-tooltip class="item" effect="dark" :content="scope.row.cmdline" placement="bottom">
                                        <span>{{scope.row.cmdline.slice(0,15)}}..</span>
                                    </el-tooltip>
                                </template>
                            </el-table-column>
                            <el-table-column
                                    prop="create_time"
                                    label="create_time"
                                    sortable
                            >
                            </el-table-column>
                        </el-table>
                    </template>


                </div>

                <div v-show="activeName === 'change'">

                    <template>
                        <el-table
                                :data="form.hostrecord"
                                border=""
                                style="width: 95%"
                        >
                            <el-table-column type="expand">
                                <template slot-scope="props">
                                    <el-form label-position="left" inline class="demo-table-expand">
                                        <el-form-item label="summary">
                                            <span>{{ props.row.summary }}</span>
                                        </el-form-item>
                                    </el-form>
                                </template>
                            </el-table-column>
                            <el-table-column
                                    prop="title"
                                    label="title"
                                    sortable
                            >
                            </el-table-column>
                            <el-table-column
                                    prop="summary"
                                    label="summary"
                                    sortable
                            >
                                <template slot-scope="scope">
                                    <span>{{scope.row.summary.slice(0,10)}}..</span>
                                </template>
                            </el-table-column>
                            <el-table-column
                                    prop="create_date"
                                    label="create_date"
                                    sortable
                            >
                            </el-table-column>

                        </el-table>
                    </template>


                </div>


            </el-col>

            <el-col :span="10">
                <div class="grid-content bg-purple-light commit">

                    <el-card class="box-card" style="min-height: 260px">
                        <div slot="header" class="clearfix">
                            <span><i class="el-icon-info"/> Zabbix接入</span>
                        </div>
                    </el-card>

                </div>

            </el-col>

        </el-row>


    </div>

</template>


<script>
    import {getHostObj} from '../../api/host'

    export default {
        data() {
            return {
                form: {},
                activeName: 'info'
            }
        },

        methods: {


        },
        created() {
            getHostObj(this.$route.params.id)
                .then((res) => {
                    this.form = res.data


                })


        }


    }
</script>

<style scoped>
    .el-row {
        margin-bottom: 20px;

    }

</style>
