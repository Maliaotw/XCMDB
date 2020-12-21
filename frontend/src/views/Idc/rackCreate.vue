<template>

    <div>

        <el-page-header
                @back="gopack"
                content="機櫃列表"
                style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px"
        />

        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>新增機櫃</span>
            </div>

            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form
                            :model="form"
                            ref="form"
                            label-position="left"
                            label-width="120px"
                    >
                        <el-row>

                            <el-col :span="24">

                            </el-col>

                            <el-col>
                                <el-form-item
                                        label="IDC"
                                        prop="idc"
                                        :rules="{required: true, message: '機房必填', trigger: 'blur'}"
                                >

                                    <el-select
                                            v-model="form.idc"
                                            placeholder=""
                                    >
                                        <el-option
                                                v-for="item in idclist"
                                                :key="item.id"
                                                :label="item.name"
                                                :value="item.id">
                                        </el-option>
                                    </el-select>
                                </el-form-item>


                            </el-col>


                            <el-col>

                                <el-form-item
                                        label="機櫃號"
                                        prop="name"
                                        :rules="{required: true, message: '機櫃號不能為空', trigger: 'blur'}">
                                    <el-input
                                            v-model="form.name"
                                    >

                                    </el-input>
                                </el-form-item>

                            </el-col>


                            <el-col>

                                <el-form-item
                                        label="高度"
                                        prop="height"
                                        :rules="{required: true, message: '高度不能為空', trigger: 'blur'}">
                                    <el-input
                                            v-model="form.height"
                                            type="number"
                                    >

                                    </el-input>
                                </el-form-item>

                            </el-col>


                            <el-col>

                                <el-form-item
                                        label="最大功率(W)"
                                >
                                    <el-input
                                            v-model="form.max_power"
                                            type="number"
                                    >

                                    </el-input>
                                </el-form-item>

                            </el-col>

                            <el-col>
                                <el-form-item
                                        label="ISP"
                                        prop="isp"
                                        :rules="{required: true, message: '線路必填', trigger: 'blur'}"

                                >

                                    <el-select
                                            v-model="form.isp"
                                            multiple
                                            placeholder=""
                                    >
                                        <el-option
                                                v-for="item in isplist"
                                                :key="item.id"
                                                :label="item.name"
                                                :value="item.id">
                                        </el-option>
                                    </el-select>
                                </el-form-item>


                            </el-col>


                            <el-col>

                                <el-form-item
                                        label="備註"
                                >
                                    <el-input
                                            v-model="form.remark"
                                            type="textarea"
                                            rows="4"
                                    >
                                    </el-input>
                                </el-form-item>
                            </el-col>


                            <el-col style="text-align: center">
                                <el-button type="primary" @click="submitForm('form')">提交</el-button>
                            </el-col>
                        </el-row>

                    </el-form>
                </el-col>
            </el-row>


        </el-card>

    </div>

</template>


<script>

    import {add} from '../../api/rack'
    import {getISP} from '../../api/isp'
    import {getIDC} from '../../api/idc'

    export default {
        data() {
            return {
                form: {
                    name: '',
                    floor: ''
                },
                isplist:'',
                idclist:''
            }
        },

        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        // console.log('submit')
                        // console.log(this.form)
                        add(this.form)
                            .then((res) => {
                                this.$notify({
                                    title: '成功',
                                    message: '更新成功',
                                    type: 'success'
                                });
                            })

                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            gopack() {
                this.$router.push({name: 'Rack'})
            }
        }

        ,
        created() {

            getISP()
                .then((res)=>{
                    this.isplist = res.data
                })

            getIDC()
                .then((res)=>{
                    this.idclist = res.data
                })


        }


    }
</script>



<style scoped>
    .el-select {
        width: 100%;
    }
</style>