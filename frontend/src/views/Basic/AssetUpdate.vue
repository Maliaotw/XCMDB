<template>


    <div>

        <el-row type="flex">

            <el-col :span="12">
                <template>
                    <el-tabs @tab-click="handleClick">
                        <el-tab-pane label="資產詳情" name="first"></el-tab-pane>
                        <el-tab-pane label="變更紀錄" name="second"></el-tab-pane>
                    </el-tabs>
                </template>
            </el-col>

            <el-col :span="12" style="text-align: right">
                <el-button type="success" icon="el-icon-upload2" @click="UpdateSubmit">更新</el-button>
            </el-col>

        </el-row>

        <el-row type="flex">
            <el-col :span="14">
                <label><b>網路設備信息</b></label>
                <el-form label-position="left" label-width="200px" style="margin-left: 20px;">

                    <el-form-item label="名稱:" style="margin-bottom: 0px">
                        <label><b>{{this.form.name}}</b></label>
                    </el-form-item>

                    <el-form-item label="類型:" style="margin-bottom: 0px">
                        <label><b>{{this.form.device_type_id}}</b></label>
                    </el-form-item>

                    <el-form-item label="管理IP:" style="margin-bottom: 0px">
                        <label><b>{{this.form.content_object.manage_ip}}</b></label>
                    </el-form-item>

                    <el-form-item label="內網IP:" style="margin-bottom: 0px">
                        <label><b>{{this.form.content_object.intranet_ip}}</b></label>
                    </el-form-item>

                    <el-form-item label="型号:" style="margin-bottom: 0px">
                        <label><b>{{this.form.content_object.model}}</b></label>
                    </el-form-item>

                    <el-form-item label="端口個數:" style="margin-bottom: 0px">
                        <label><b>{{this.form.content_object.port_num}}</b></label>
                    </el-form-item>

                    <el-form-item label="製造商:" style="margin-bottom: 0px">
                        <label><b>{{this.form.content_object.manufactory}}</b></label>
                    </el-form-item>

                    <el-form-item label="SN號:" style="margin-bottom: 0px">
                        <label><b>{{this.form.content_object.sn}}</b></label>
                    </el-form-item>

                    <el-form-item label="備註:" style="margin-bottom: 0px">
                        <label><b>{{this.form.content_object.detail}}</b></label>
                    </el-form-item>

                    <el-form-item label="创建日期:" style="margin-bottom: 0px">
                        <label><b>{{this.form.content_object.create_date}}</b></label>
                    </el-form-item>

                    <el-form-item label="最後更新日期:" style="margin-bottom: 0px">
                        <label><b>{{this.form.content_object.latest_date}}</b></label>
                    </el-form-item>


                </el-form>


            </el-col>

            <el-col :span="10">
                <div class="grid-content bg-purple-light commit">

                    <el-card class="box-card">
                        <div slot="header" class="clearfix">
                            <span><i class="el-icon-info"></i> 快速修改</span>
                        </div>
                        <el-form :model="AssetForm" label-position="left" label-width="100px"
                                 style="margin-left: 20px;">

                            <el-form-item label="資產編號" style="margin-bottom: 20px">
                                <el-input v-model="AssetForm.number"></el-input>
                            </el-form-item>

                            <el-form-item label="狀態" style="margin-bottom: 20px">
                                <el-select v-model="AssetForm.device_status_id" placeholder="" style="width: 100%">
                                    <el-option
                                            v-for="item in this.statuslist"
                                            :key="item[0]"
                                            :label="item[1]"
                                            :value="item[0]"
                                    >
                                    </el-option>
                                </el-select>
                            </el-form-item>

                            <el-form-item label="標籤" style="margin-bottom: 20px">
                                <el-select v-model="AssetForm.tag" placeholder="" style="width: 100%">
                                    <el-option
                                            v-for="item in this.taglist"
                                            :key="item.id"
                                            :label="item.name"
                                            :value="item.id"
                                    >
                                    </el-option>
                                </el-select>
                            </el-form-item>

                            <el-form-item label="機櫃大小(U)" style="margin-bottom: 20px">
                                <el-input v-model="AssetForm.size" type="number"></el-input>
                            </el-form-item>

                        </el-form>
                    </el-card>

                </div>

                <div class="grid-content bg-purple-light rack" style="margin-top: 20px">

                    <el-card class="box-card">
                        <div slot="header" class="clearfix">
                            <span><i class="el-icon-info"></i> 快速修改</span>
                        </div>

                        <el-form :model="AssetForm" label-position="left" label-width="100px"
                                 style="margin-left: 20px;">

                            <el-form-item label="機房" style="margin-bottom: 20px">
                                <el-select
                                        v-model="idc"
                                        placeholder=""
                                        style="width: 100%"
                                        @change="selidc"
                                        @blur="selchk"
                                >
                                    <el-option
                                            v-for="item in this.idclist"
                                            :key="item.id"
                                            :label="item.name"
                                            :value="item.id"

                                    >
                                    </el-option>
                                </el-select>
                            </el-form-item>

                            <el-form-item label="機櫃" style="margin-bottom: 20px">
                                <el-select v-model="AssetForm.rack" placeholder="" style="width: 100%">
                                    <el-option
                                            v-for="item in this.racklist"
                                            :key="item.id"
                                            :label="item.name"
                                            :value="item.id"
                                    >
                                    </el-option>
                                </el-select>
                            </el-form-item>

                        </el-form>


                    </el-card>
                </div>

            </el-col>

        </el-row>


    </div>

</template>


<script>
    import http from '../../services/http'
    import {getStatus, getType, add, edit} from '../../api/asset'
    import {getTag} from '../../api/tag'
    import {getRackAll} from '../../api/rack'
    import {getIDCAll} from '../../api/idc'

    export default {
        data() {
            return {
                msg: '',
                form: {},
                AssetForm: {
                    number: '',
                    device_status_id: '',
                    tag: '',
                    rack: '',
                    size:''
                },
                idc: '',
                idclist: '',
                racklist:'',


            }
        },

        methods: {

            // 提交更新
            UpdateSubmit() {
                edit(this.$route.params.id, this.AssetForm)
                    .then((res) => {
                        console.log(res)
                        this.$notify({
                            title: '成功',
                            message: '更新成功',
                            type: 'success'
                        });
                    })
                    .catch({

                    })
            },

            myid() {
                console.log(this.$route.params.id)
                this.msg = this.$route.params.id
            },
            getAssetObj() {
                http({
                    url: `/assets/${this.$route.params.id}/`,
                    method: "get",
                }).then((res) => {
                    console.log(res)
                    this.form = res.data
                    this.AssetForm.number = res.data.number
                    this.AssetForm.device_status_id = res.data.device_status_id
                    this.AssetForm.tag = res.data.tag
                    this.AssetForm.size = res.data.size
                    this.AssetForm.object_id = res.data.object_id
                    this.AssetForm.rack = res.data.rack
                    this.AssetForm.name = res.data.name
                    this.idc = res.data.idc
                })

            },
            selidc(val) {
                console.log('selidc')
                // console.log(val)
                getRackAll({idc: val})
                    .then((res) => {
                        // console.log(res)
                        this.racklist = res.data
                        this.AssetForm.rack = ''

                    })
            },
            selchk() {
                console.log('selchk')

            }

        },
        created() {
            this.myid()
            this.getAssetObj()
            getStatus()
                .then((res) => {
                    console.log(res)
                    this.statuslist = res.data
                })

            getTag()
                .then((res) => {
                    console.log(res)
                    this.taglist = res.data
                })

            getIDCAll()
                .then((res) => {
                    console.log(`getIDCAllres`)
                    console.log(res)
                    this.idclist = res.data
                })

            getRackAll()
                .then((res) => {
                    console.log(res)
                    this.racklist = res.data
                })

        }


    }
</script>


<style scoped>
    .el-row {
        margin-bottom: 20px;

    &
    :last-child {
        margin-bottom: 0;
    }

    }
    .el-col {
        border-radius: 4px;
    }

    .bg-purple-dark {
        background: #99a9bf;
    }

    .bg-purple {
        background: #d3dce6;
    }

    .bg-purple-light {
        background: #e5e9f2;
    }

    .grid-content {
        border-radius: 4px;
        min-height: 36px;
    }

    .row-bg {
        padding: 10px 0;
        background-color: #f9fafc;
    }

    .text {
        font-size: 14px;
    }

    .item {
        margin-bottom: 18px;
    }

    .clearfix:before,
    .clearfix:after {
        display: table;
        content: "";
    }

    .clearfix:after {
        clear: both
    }

    .box-card {
        width: 480px;
    }

    .el-card {
        width: 100%;
    }

    .rack .el-card__header {
        color: white;
        background: #f6c23e;
    }

    .commit .el-card__header {
        color: white;
        background: #4e73df;
    }

</style>
