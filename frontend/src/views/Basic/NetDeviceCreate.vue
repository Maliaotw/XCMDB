<template>

    <div>

        <el-page-header @back="gopack" content="網路設備"
                        style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px">
        </el-page-header>


        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>新增設備</span>
            </div>
            <el-row>
                <el-col :span="14" :offset="6">
                    <el-form :inline="true" :model="form" ref="form" label-position="left" label-width="100px"
                             class="demo-form-inline">


                        <el-row type="flex" :gutter="20">
                            <el-col>
                                <el-form-item
                                        label="設備類型"
                                        prop="sub_asset_type"
                                        :rules="{required: true, message: '設備類型不能為空', trigger: 'blur'}">
                                    <el-select v-model="form.sub_asset_type" placeholder="">
                                        <el-option
                                                v-for="item in this.types"
                                                :key="item[0]"
                                                :label="item[1]"
                                                :value="item[0]">
                                        </el-option>
                                    </el-select>

                                </el-form-item>

                            </el-col>

                            <el-col>

                                <el-form-item
                                        label="設備名稱"
                                        prop="name"
                                        :rules="{required: true, message: '設備名稱不能為空', trigger: 'blur'}">

                                    <el-input v-model="form.name" placeholder=""></el-input>
                                </el-form-item>

                            </el-col>

                        </el-row>
                        <el-row type="flex" :gutter="20">
                            <el-col>

                                <el-form-item label="管理IP" style="text-align: left">
                                    <el-input v-model="form.manage_ip" placeholder=""></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col>
                                <el-form-item label="內部IP" style="text-align: right">
                                    <el-input v-model="form.intranet_ip" placeholder=""></el-input>
                                </el-form-item>

                            </el-col>

                        </el-row>

                        <el-row type="flex" :gutter="20">


                            <el-col>
                                <el-form-item label="製造商">
                                    <el-input
                                            v-model="form.manufactory"
                                            placeholder="">

                                    </el-input>
                                </el-form-item>

                            </el-col>
                            <el-col>
                                <el-form-item label="型號">
                                    <el-input v-model="form.model" placeholder=""></el-input>
                                </el-form-item>

                            </el-col>

                        </el-row>
                        <el-row type="flex" :gutter="20">
                            <el-col>
                                <el-form-item
                                        label="端口個數"
                                        prop="port_num"
                                        :rules="{required: true, message: '端口個數 不能為空', trigger: 'blur'}"
                                >
                                    <el-input v-model="form.port_num" port_num=""></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col>
                                <el-form-item
                                        label="保固日期"
                                        prop="warranty_date"
                                        :rules="{required: true, message: '保固日期 不能為空', trigger: 'blur'}"
                                >
                                    <el-date-picker
                                            v-model="form.warranty_date"
                                            type="date"
                                            placeholder=""
                                            value-format="yyyy-MM-dd"
                                    >
                                    </el-date-picker>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-row>
                            <el-col :span="24">
                                <el-form-item
                                        label="SN號"
                                        prop="sn"
                                        :rules="{required: true, message: 'SN 不能為空', trigger: 'blur'}">
                                    <el-input v-model="form.sn" placeholder=""></el-input>
                                </el-form-item>

                            </el-col>
                        </el-row>

                        <el-row type="flex" :gutter="20">

                            <el-col>
                                <el-form-item label="備註" style="width: 100%">
                                    <el-input v-model="form.detail"
                                              :rows="4"
                                              type="textarea"
                                              placeholder=""
                                    ></el-input>
                                </el-form-item>

                            </el-col>
                        </el-row>

                        <el-row>
                            <el-col style="text-align: center">
                                <el-button @click="submitForm('form')" type="primary">提交</el-button>
                            </el-col>
                        </el-row>



                    </el-form>
                </el-col>
            </el-row>
        </el-card>

    </div>

</template>


<script>

    import {add,getType} from '@/api/netdrive'

    export default {
        data() {
            return {
                mag: this.$route.params.id,
                form: {
                    sub_asset_type: '',
                    name: '',
                    manage_ip: '',
                    intranet_ip: '',
                    sn: '',
                    manufactory: '',
                    model: '',
                    port_num: '',
                    detail: '',
                    warranty_date: ''
                },
                types: ''
            }
        },

        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        console.log('submit')
                        console.log(this.form)
                        add(this.form)
                            .then((res) => {
                                this.$notify({
                                    title: '成功',
                                    message: '新增成功',
                                    type: 'success'
                                });
                            })

                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            gopack(){
                this.$router.push({name: 'NetDevice'})
            }
        }

        ,
        created() {
            getType()
                .then((res)=>{
                    this.types = res.data
                })
        }


    }
</script>

<style>



</style>