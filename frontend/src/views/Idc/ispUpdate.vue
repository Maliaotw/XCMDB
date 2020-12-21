<template>

    <div>

        <el-page-header
                @back="gopack"
                content="ISP列表"
                style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px"
        />

        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>更新ISP</span>
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
                                        label="名稱"
                                        prop="name"
                                        :rules="{required: true, message: '名稱必填', trigger: 'blur'}"
                                >
                                    <el-input
                                            v-model="form.name"
                                    />
                                </el-form-item>
                            </el-col>

                            <el-col>

                                <el-form-item
                                        label="IP範圍"
                                        prop="ip_range"
                                        :rules="{required: true, message: 'IP範圍不能為空', trigger: 'blur'}">
                                    <el-input
                                            v-model="form.ip_range"
                                    >

                                    </el-input>
                                </el-form-item>

                            </el-col>


                            <el-col>

                                <el-form-item
                                        label="NETMASK"
                                        prop="netmask"
                                        :rules="{required: true, message: 'NETMASK不能為空', trigger: 'blur'}"
                                >
                                    <el-input
                                            v-model="form.netmask"
                                    />
                                </el-form-item>

                            </el-col>


                            <el-col>

                                <el-form-item
                                        label="GETEWAY"
                                        prop="geteway"
                                        :rules="{required: true, message: 'GETEWAY不能為空', trigger: 'blur'}"
                                >
                                    <el-input
                                            v-model="form.geteway"
                                    />
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

    import {getISPObj, edit} from '../../api/isp'

    export default {
        data() {
            return {
                form: {},
            }
        },

        methods: {
            getinit() {
                getISPObj(this.$route.params.id)
                    .then((res) => {
                        console.log(res)
                        this.form = res.data
                    })
                    .catch(
                        console.log('error')
                    )

            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        // console.log('submit')
                        // console.log(this.form)
                        edit(this.$route.params.id, this.form)
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
                this.$router.push({name: 'ISP'})
            }
        }

        ,
        created() {
            this.getinit()


        }


    }
</script>


<style scoped>


</style>