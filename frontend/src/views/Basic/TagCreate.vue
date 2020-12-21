<template>

    <div>

        <el-page-header
                @back="gopack"
                content="標籤列表"
                style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px"
        />


        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>新增標籤</span>
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
                                        label="標籤名稱"
                                        prop="name"
                                        :rules="{required: true, message: '設備類型不能為空', trigger: 'blur'}">
                                    <el-input
                                            v-model="form.name"
                                    >

                                    </el-input>
                                </el-form-item>
                            </el-col>

                            <el-col>

                                <el-form-item
                                        label="備註"
                                >
                                    <el-input
                                            v-model="form.remark"
                                            type="textarea"
                                            :rows="4"
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

    import {add} from '../../api/tag'

    export default {
        data() {
            return {
                form: {
                    name: '',
                    remark: ''

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
                this.$router.push({name: 'Tag'})
            }
        }

        ,
        created() {

        }


    }
</script>

