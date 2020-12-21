<template>


    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>基礎資源</el-breadcrumb-item>
                <el-breadcrumb-item :to="{name:'Asset'}">資產列表</el-breadcrumb-item>
                <el-breadcrumb-item>{{this.form.name}}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <el-row type="flex">

            <el-col :span="12">
                <template>
                    <el-tabs v-model="activeName">

                        <el-tab-pane
                                :key="item.name"
                                v-for="(item, index) in editableTabs"
                                :label="item.title"
                                :name="item.name"
                        />

                    </el-tabs>
                </template>
            </el-col>

            <el-col :span="12" style="text-align: right">
                <el-button type="success" icon="el-icon-upload2" @click="UpdateSubmit">更新</el-button>
            </el-col>

        </el-row>

        <el-row type="flex">
            <el-col :span="14">
                <div v-show="activeName === 'first'">

                    <el-form label-position="left" label-width="200px" style="margin-left: 20px;">


                        <el-form-item label="名稱:" style="margin-bottom: 0px">
                            <label><b>{{this.form.name}}</b></label>
                        </el-form-item>

                        <el-form-item label="類型:" style="margin-bottom: 0px">
                            <label><b>{{this.form.device_type_id}}</b></label>
                        </el-form-item>


                        <div v-show="this.form.device_type_id === '網路設備'">

                            <el-form-item label="管理IP:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.manage_ip}}</b></label>
                            </el-form-item>

                            <el-form-item label="內網IP:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.intranet_ip}}</b></label>
                            </el-form-item>

                            <el-form-item label="型号:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.model}}</b></label>
                            </el-form-item>

                            <el-form-item label="端口個數:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.port_num}}</b></label>
                            </el-form-item>

                            <el-form-item label="製造商:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.manufactory}}</b></label>
                            </el-form-item>

                            <el-form-item label="SN號:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.sn}}</b></label>
                            </el-form-item>

                            <el-form-item label="備註:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.detail}}</b></label>
                            </el-form-item>


                        </div>


                        <div v-show="this.form.device_type_id === '服務器'">

                            <el-form-item label="管理IP:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.manage_ip}}</b></label>
                            </el-form-item>

                            <el-form-item label="製造商:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.manufacturer}}</b></label>
                            </el-form-item>

                            <el-form-item label="型号:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.model}}</b></label>
                            </el-form-item>


                            <el-form-item label="系統:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.os_platform}}</b></label>
                            </el-form-item>



                            <el-form-item label="SN號:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.sn}}</b></label>
                            </el-form-item>

                            <el-form-item label="規格:" style="margin-bottom: 0px">
                                <label><b>{{this.content_object.total_cores}}Cores {{this.content_object.total_disk}}GB  {{this.content_object.total_memory}}GB</b></label>
                            </el-form-item>



                        </div>

                        <el-form-item label="创建日期:" style="margin-bottom: 0px">
                            <label><b>{{this.form.create_at}}</b></label>
                        </el-form-item>

                        <el-form-item label="最後更新日期:" style="margin-bottom: 0px">
                            <label><b>{{this.form.latest_date}}</b></label>
                        </el-form-item>


                    </el-form>

                </div>


            </el-col>

            <el-col :span="10">
                <div class="grid-content bg-purple-light commit">

                    <el-card class="box-card">
                        <div slot="header" class="clearfix">
                            <span><i class="el-icon-info"/> 快速修改</span>
                        </div>
                        <el-form
                                :model="AssetForm"
                                label-position="left"
                                label-width="100px"
                                class="ml-2"
                        >

                            <el-form-item label="資產編號" class="mb-2">
                                <el-input v-model="AssetForm.number"/>
                            </el-form-item>

                            <el-form-item label="狀態" class="mb-2">
                                <el-select v-model="AssetForm.device_status_id" placeholder="" style="width: 100%">
                                    <el-option key="" label="----" value=""/>
                                    <el-option label="上架" key="1" value="1"/>
                                    <el-option label="線上" key="2" value="2"/>
                                    <el-option label="離線" key="3" value="3"/>
                                    <el-option label="下架" key="4" value="4"/>
                                </el-select>
                            </el-form-item>

                            <el-form-item label="標籤" class="mb-2">
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

                            <el-form-item label="機櫃大小(U)" class="mb-2">
                                <el-input v-model="AssetForm.size" type="number"/>
                            </el-form-item>

                        </el-form>
                    </el-card>

                </div>

                <div class="grid-content bg-purple-light rack mt-3">

                    <el-card class="box-card">
                        <div slot="header" class="clearfix">
                            <span><i class="el-icon-info"/> 機櫃調整</span>
                        </div>

                        <el-form
                                :model="AssetForm"
                                label-position="left"
                                label-width="100px"
                                class="ml-2"
                        >

                            <el-form-item label="機房" class="mb-2">
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

                                    />
                                </el-select>
                            </el-form-item>

                            <el-form-item label="機櫃" class="mb-2">
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
    import {edit, getAssetObj} from '@/api/asset'
    import {getRackAll} from '@/api/rack'

    export default {
        data() {
            return {
                msg: '',
                form: {},
                content_object: {},
                AssetForm: {
                    number: '',
                    device_status_id: 1,
                    tag: '',
                    rack: '',
                    size: ''
                },
                idc: '',
                idclist: '',
                racklist: '',
                taglist: '',
                activeName: 'first',
                editableTabs: [{
                    title: '資產詳情',
                    name: 'first',
                }]

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
                            message: '这是一条成功的提示消息',
                            type: 'success'
                        });
                    })
                    .catch({})
            },

            getInit() {
                getAssetObj(this.$route.params.id)
                    .then((res) => {
                        console.log(res)
                        this.form = res.data
                        this.content_object = res.data.content_object
                        this.AssetForm.number = res.data.number
                        this.AssetForm.device_status_id = `${res.data.device_status_id}`
                        this.AssetForm.tag = res.data.tag
                        this.AssetForm.size = res.data.size
                        this.AssetForm.object_id = res.data.object_id
                        this.AssetForm.rack = res.data.rack
                        this.AssetForm.name = res.data.name
                        this.idc = res.data.idc

                        this.taglist = res.data.tag_list
                        this.idclist = res.data.idc_list
                        this.racklist = res.data.rack_list

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
            this.tab_hostrecord = true
            this.getInit()

        }


    }
</script>


<style scoped>
    .el-row {
        margin-bottom: 20px;

    }


</style>
