<template>

    <div>

        <el-page-header
                @back="gopack"
                content="Network列表"
                style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px"
        />

        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>新增NetWork</span>
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
                                        label="名稱"
                                        prop="name"
                                >
                                    <el-input
                                            v-model="form.name"
                                    />
                                </el-form-item>
                            </el-col>

                            <el-col :span="24">
                                <el-form-item
                                        label="network"
                                        prop="network"
                                >
                                    <el-input
                                            v-model="form.network"
                                    />
                                </el-form-item>
                            </el-col>


                            <el-col :span="24">
                                <el-form-item
                                        label="IP範圍"
                                        prop="name"
                                >
                                    <el-input
                                            v-model="form.iprange"
                                    />
                                </el-form-item>
                            </el-col>

                            <el-col :span="24">
                                <el-form-item
                                        label="gateway"
                                        prop="name"
                                >
                                    <el-input
                                            v-model="form.gateway"
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

    import {AddNetwork, getNetworkAll} from '@/api/vm'

    export default {
        data() {
            return {
                form: {},
                data: {},
            }
        },

        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        AddNetwork("network", this.form)
                            .then((response) => {
                                this.$notify.success({
                                    title: '成功',
                                    message: '这是一条成功的提示消息'
                                });
                            })
                            .catch((error) => {
                                this.$notify.error({
                                    title: '错误',
                                    message: '这是一条错误的提示消息'
                                });
                            })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            gopack() {
                this.$router.push({name: 'Network'})
            },


        }
        ,
        created() {

        }


    }
</script>

<style scoped>
    .el-select {
        width: 100%;
    }

</style>
