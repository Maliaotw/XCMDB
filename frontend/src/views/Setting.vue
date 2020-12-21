<template>

    <div>

        <el-breadcrumb separator="/" style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px">
            <el-breadcrumb-item >系統設置</el-breadcrumb-item>
            <el-breadcrumb-item>基本設置</el-breadcrumb-item>
        </el-breadcrumb>


        <el-row  style="margin-bottom: 20px">


            <el-tabs v-model="activeName" type="border-card" @tab-click="handleClick">
                <el-tab-pane label="iDRAC管理" name="idrac">

                        <el-row>
                            <el-col :span="14" :offset="6">
                                <el-form
                                         :model="form"
                                         ref="idrac"
                                         label-position="left"
                                         label-width="100px"
                                         class="demo-form-inline"
                                >


                                    <el-row type="flex" :gutter="20">

                                        <el-col>

                                            <el-form-item
                                                    label="User"
                                                    prop="IDRAC_USER"
                                                    :rules="{required: true, message: 'User不能為空', trigger: 'blur'}"
                                            >

                                                <el-input v-model="form.IDRAC_USER" placeholder=""></el-input>
                                            </el-form-item>

                                        </el-col>


                                    </el-row>


                                    <el-row type="flex" :gutter="20">

                                        <el-col>

                                            <el-form-item
                                                    label="Passwd"
                                                    prop="IDRAC_PASSWD"
                                                    :rules="{required: true, message: 'Passwd不能為空', trigger: 'blur'}"
                                            >

                                                <el-input v-model="form.IDRAC_PASSWD" placeholder="" show-password></el-input>
                                            </el-form-item>

                                        </el-col>

                                    </el-row>



                                    <el-row>
                                        <el-col style="text-align: center">
                                            <el-button @click="submitForm('idrac')" type="primary">提交</el-button>
                                        </el-col>
                                    </el-row>


                                </el-form>
                            </el-col>
                        </el-row>


                </el-tab-pane>

                <el-tab-pane label="Vcenter管理" name="vcenter">

                    <el-row>
                        <el-col :span="14" :offset="6">
                            <el-form
                                    :model="form"
                                    ref="vcenter"
                                    label-position="left"
                                    label-width="180px"
                                    class="demo-form-inline"
                            >

                                <el-row type="flex" :gutter="20">

                                    <el-col>

                                        <el-form-item
                                                label="VCENTER_SERVER"
                                                prop="VCENTER_SERVER"
                                                :rules="{required: true, message: '設備名稱不能為空', trigger: 'blur'}"
                                        >

                                            <el-input v-model="form.VCENTER_SERVER" placeholder=""></el-input>
                                        </el-form-item>

                                    </el-col>


                                </el-row>


                                <el-row type="flex" :gutter="20">

                                    <el-col>

                                        <el-form-item
                                                label="VCENTER_USER"
                                                prop="VCENTER_USER"
                                                :rules="{required: true, message: '設備名稱不能為空', trigger: 'blur'}"
                                        >

                                            <el-input v-model="form.VCENTER_USER" placeholder=""></el-input>
                                        </el-form-item>

                                    </el-col>

                                </el-row>

                                <el-row type="flex" :gutter="20">

                                    <el-col>

                                        <el-form-item
                                                label="VCENTER_PASS"
                                                prop="VCENTER_PASS"
                                                :rules="{required: true, message: '設備名稱不能為空', trigger: 'blur'}"
                                        >

                                            <el-input v-model="form.VCENTER_PASS" placeholder="" show-password></el-input>
                                        </el-form-item>

                                    </el-col>

                                </el-row>



                                <el-row>
                                    <el-col style="text-align: center">
                                        <el-button @click="submitForm('vcenter')" type="primary">提交</el-button>
                                    </el-col>
                                </el-row>


                            </el-form>
                        </el-col>
                    </el-row>



                </el-tab-pane>

                <el-tab-pane label="LDAP管理" name="ldap">

                    <el-row>
                        <el-col :span="14" :offset="6">
                            <el-form
                                    :model="form"
                                    ref="vcenter"
                                    label-position="left"
                                    label-width="180px"
                                    class="demo-form-inline"
                            >

                                <el-row type="flex" :gutter="20">

                                    <el-col>

                                        <el-form-item
                                                label="LDAP地址"
                                                prop="AUTH_LDAP_SERVER_URI"
                                                :rules="{required: true, message: 'LDAP地址不能為空', trigger: 'blur'}"
                                        >

                                            <el-input v-model="form.AUTH_LDAP_SERVER_URI" placeholder=""></el-input>
                                        </el-form-item>

                                    </el-col>


                                </el-row>


                                <el-row type="flex" :gutter="20">

                                    <el-col>

                                        <el-form-item
                                                label="綁定DN"
                                                prop="AUTH_LDAP_BIND_DN"
                                        >

                                            <el-input v-model="form.AUTH_LDAP_BIND_DN" placeholder=""></el-input>
                                        </el-form-item>

                                    </el-col>

                                </el-row>

                                <el-row type="flex" :gutter="20">

                                    <el-col>

                                        <el-form-item
                                                label="密碼"
                                                prop="AUTH_LDAP_BIND_PASSWORD"
                                        >

                                            <el-input v-model="form.AUTH_LDAP_BIND_PASSWORD" placeholder="" show-password></el-input>
                                        </el-form-item>

                                    </el-col>

                                </el-row>


                              <el-row type="flex" :gutter="20">

                                    <el-col>

                                        <el-form-item
                                                label="用戶OU"
                                                prop="AUTH_LDAP_SEARCH_OU"
                                        >

                                            <el-input v-model="form.AUTH_LDAP_SEARCH_OU" placeholder=""></el-input>
                                        </el-form-item>

                                    </el-col>

                                </el-row>


                                <el-row type="flex" :gutter="20">

                                    <el-col>

                                        <el-form-item
                                                label="用戶過濾器"
                                                prop="AUTH_LDAP_SEARCH_FILTER"
                                        >

                                            <el-input v-model="form.AUTH_LDAP_SEARCH_FILTER" placeholder=""></el-input>
                                        </el-form-item>

                                    </el-col>

                                </el-row>


                              <el-row type="flex" :gutter="20">

                                    <el-col>

                                        <el-form-item
                                                label="LDAP屬性映射"
                                                prop="AUTH_LDAP_USER_ATTR_MAP"
                                        >

                                            <el-input v-model="form.AUTH_LDAP_USER_ATTR_MAP" placeholder=""></el-input>
                                        </el-form-item>

                                    </el-col>

                              </el-row>

                              <el-row type="flex" :gutter="20">

                                    <el-col>

                                        <el-form-item
                                                label="啟用LDAP認證"
                                                prop="AUTH_LDAP"
                                        >

                                            <el-input v-model="form.AUTH_LDAP"  placeholder=""></el-input>
                                        </el-form-item>

                                    </el-col>

                              </el-row>


                              <el-row>
                                  <el-col style="text-align: center">
                                      <el-button @click="submitForm('vcenter')" type="primary">提交</el-button>
                                  </el-col>
                              </el-row>


                            </el-form>
                        </el-col>
                    </el-row>



                </el-tab-pane>
            </el-tabs>

        </el-row>




    </div>

</template>


<script>

    import {getSeeingsObj,UpdateSeeingsObj} from '@/api/settings'

    export default {
        data() {
            return {
                title: '',
                formLabelWidth: '120px',
                form: {},
                activeName: 'idrac'
            }
        },

        methods: {
            handleClick(tab, event) {
                // console.log(tab, event);
                // console.log(tab.paneName);
                this.getInit(tab.paneName)

            },
            getInit(name){
                getSeeingsObj(name)
                    .then((response) => {
                        this.form = response.data;
                    })
                    .catch((error) => {
                        this.$notify.error({
                            title: '错误',
                            message: '这是一条错误的提示消息'
                        });
                    })
            },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        console.log(formName)
                        console.log(this.$refs[formName])
                        UpdateSeeingsObj(formName,this.form)
                            .then((response) => {
                                this.$notify.success({
                                    title: '成功',
                                    message: '这是一条成功的提示消息'
                                });
                            })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },

        },
        created() {
            // get and set auth user
            this.getInit(this.activeName)
        }


    }
</script>
