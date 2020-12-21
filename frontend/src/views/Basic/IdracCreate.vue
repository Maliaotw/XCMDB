<template>

    <div>

        <el-page-header
                @back="gopack"
                content="IDRAC列表"
                style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px"
        />


        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>新增服務器</span>
            </div>

            <el-row>
                <el-col :span="12" :offset="6">
                    <el-form
                            :model="form"
                            ref="form"
                            label-position="left"
                            label-width="100px"
                    >
                        <el-row>
                            <el-col :span="24">
                                <el-form-item
                                        label="IDRAC IP"
                                        prop="idrac_ip"
                                        :rules="{required: true, message: '設備類型不能為空', trigger: 'blur'}">
                                    <el-input
                                            v-model="form.idrac_ip"
                                    >
                                    </el-input>
                                </el-form-item>
                            </el-col>

                            <el-col>

                                <el-form-item
                                        label="端口"
                                        prop="port"
                                        :rules="{required: true, message: '端口不能為空', trigger: 'blur'}">
                                    <el-input
                                            v-model="form.port"
                                            type="number"
                                    />
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

    import {add} from '../../api/idrac'

    export default {
        data() {
            return {
                form: {
                    idrac_ip: '',
                    port: '443',
                },
            }
        },

        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
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
                this.$router.push({name: 'Idrac'})
            }
        }

        ,
        created() {

        }


    }
</script>

