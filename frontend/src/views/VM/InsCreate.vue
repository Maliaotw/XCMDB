<template>

    <div>

        <el-page-header
                @back="gopack"
                content="Instance列表"
                style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px"
        />


        <el-row>
            <el-col :span="14">
                <el-card class="box-card">
                    <div slot="header" class="clearfix">
                        <span>參數選擇</span>
                    </div>

                    <el-row>
                        <el-col :span="20" :offset="1">
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
                                                prop="hw_name"
                                                :rules="rules.hostname"
                                        >
                                            <el-input
                                                    v-model="form.hw_name"
                                            />
                                        </el-form-item>
                                    </el-col>

                                    <el-col>
                                        <el-form-item
                                                label="集群"
                                                :rules="{required: true, message: '主機不能為空', trigger: 'blur'}"
                                        >
                                            <el-radio-group v-model="form.cluster" size="medium"
                                                            @change="selcluster">
                                                <el-radio-button v-for="item in data.cluster" :label="item.id">
                                                    {{item.remark}}
                                                </el-radio-button>
                                            </el-radio-group>
                                        </el-form-item>

                                    </el-col>

                                    <el-col>
                                        <el-form-item
                                                label="ESXI"
                                                :rules="{required: true, message: '主機不能為空', trigger: 'blur'}"
                                        >
                                            <el-radio-group v-model="form.host" size="medium"
                                                            @change="selhost">
                                                <el-radio-button v-for="item in data.host" :label="item.id">
                                                    {{item.name}}
                                                </el-radio-button>
                                            </el-radio-group>
                                        </el-form-item>

                                    </el-col>

                                    <el-col>
                                        <el-form-item
                                                label="Network"
                                                :rules="{required: true, message: 'Network不能為空', trigger: 'blur'}"

                                        >
                                            <el-radio-group v-model="form.network" size="medium">
                                                <el-radio-button v-for="item in data.network" :label="item.id">
                                                    {{item.remark}}
                                                </el-radio-button>
                                            </el-radio-group>
                                        </el-form-item>
                                    </el-col>

                                    <el-col>
                                        <el-form-item
                                                label="Datasote"
                                                :rules="{required: true, message: 'Datasote不能為空', trigger: 'blur'}"
                                        >
                                            <el-radio-group v-model="form.datastore" size="medium">
                                                <el-radio-button v-for="item in data.datastore" :label="item.id">
                                                    {{item.name}} (剩{{item.freeSpace}})
                                                </el-radio-button>
                                            </el-radio-group>
                                        </el-form-item>

                                    </el-col>


                                    <el-col>

                                        <el-form-item
                                                label="CPU"
                                                prop="hw_processor_count"
                                                :rules="{required: true, message: 'CPU不能為空', trigger: 'blur'}">
                                            <el-select v-model="form.hw_processor_count" placeholder="">
                                                <el-option
                                                        v-for="item in data.cpu"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>

                                    </el-col>

                                    <el-col>
                                        <el-form-item
                                                label="內存"
                                                prop="hw_memtotal_mb"
                                                :rules="{required: true, message: '內存不能為空', trigger: 'blur'}">
                                            <el-select v-model="form.hw_memtotal_mb" placeholder="">
                                                <el-option
                                                        v-for="item in data.mem"
                                                        :key="item.value"
                                                        :label="item.label"
                                                        :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                    </el-col>


                                    <el-col>


                                        <el-form-item
                                                label="硬盤"
                                                prop="capacity"
                                                :rules="{required: true, message: '硬盤不能為空', trigger: 'blur'}">

                                            <div class="block">
                                                <el-slider
                                                        v-model="form.capacity"
                                                        show-input
                                                        :min=100
                                                        :max=500
                                                >
                                                </el-slider>
                                            </div>
                                        </el-form-item>


                                    </el-col>

                                    <el-col>

                                        <el-form-item
                                                label="Template"
                                                prop="type"
                                        >
                                            <el-radio-group v-model="form.template" size="medium">
                                                <el-radio-button v-for="item in data.template" :label="item.hw_name">
                                                    {{item.hw_name}}
                                                </el-radio-button>
                                            </el-radio-group>

                                        </el-form-item>

                                    </el-col>


                                </el-row>

                            </el-form>
                        </el-col>
                    </el-row>

                </el-card>
            </el-col>

            <el-col
                    :span="10"
                    style="padding-left: 20px"

            >

                <el-card class="box-card now">
                    <div slot="header" class="clearfix">
                        <span><i class="fa fa-info-circle"/> 當前配置</span>
                    </div>

                    <el-row>
                        <el-col :span="20" :offset="1">
                            <el-form
                                    label-position="left"
                                    label-width="100px"
                            >
                                <el-row>

                                    <el-col>
                                        <el-form-item label="名稱">{{form.hw_name}}</el-form-item>
                                    </el-col>

                                    <el-col>
                                        <el-form-item label="集群">{{conf.cluster}}</el-form-item>
                                    </el-col>

                                    <el-col>
                                        <el-form-item label="主機">{{conf.hw_name}}</el-form-item>
                                    </el-col>

                                    <el-col>
                                        <el-form-item label="網路">{{conf.network}}</el-form-item>
                                    </el-col>

                                    <el-col>
                                        <el-form-item label="儲存區">{{conf.datastore}}</el-form-item>

                                    </el-col>

                                    <el-col>
                                        <el-form-item label="配置">
                                            {{form.hw_processor_count}}Cores {{form.hw_memtotal_mb}}GB
                                            {{form.capacity}}GB
                                        </el-form-item>

                                    </el-col>

                                    <el-col>
                                        <el-form-item label="Template">{{form.template}}</el-form-item>

                                    </el-col>


                                    <el-col style="text-align: center">
                                        <el-button type="primary" @click="submitForm('form')">提交</el-button>
                                    </el-col>
                                </el-row>

                            </el-form>
                        </el-col>
                    </el-row>

                </el-card>


            </el-col>
        </el-row>
    </div>

</template>


<script>

    import {add, get} from '../../api/instance'
    import {getClusterAll} from '../../api/vm'

    export default {
        data() {

            var validateHostname = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('名稱不得為空'));
                } else {
                    get(this.form.hw_name)
                        .then((response) => {
                            console.log('chkname');
                            if (response.data.length !== 0) {
                                console.log(`response.data ${response.data}`);
                                callback(new Error('名稱不得重複'));
                            } else {
                                callback()
                            }
                        })

                }
            };
            return {

                form: {
                    hw_name: '',
                    hw_processor_count: '',
                    hw_memtotal_mb: '',
                    host: '',
                    template: '',
                    cluster:'',
                    network:''

                },
                conf: {
                    hw_name: '',
                    hw_processor_count: '',
                    hw_memtotal_mb: '',
                    network: '',
                    datastore: '',
                    cluster: ''

                },
                rules: {
                    hostname: [
                        {validator: validateHostname, trigger: 'blur'}
                    ],
                },
                data: {
                    cpu: [
                        {
                            value: '1',
                            label: '1'
                        },
                        {
                            value: '2',
                            label: '2'
                        },
                        {
                            value: '4',
                            label: '4'
                        },
                        {
                            value: '8',
                            label: '8'
                        }
                    ],
                    mem: [
                        {
                            value: '1024',
                            label: '1G'
                        },
                        {
                            value: '2048',
                            label: '2G'
                        },
                        {
                            value: '4096',
                            label: '4G'
                        },
                        {
                            value: '8192',
                            label: '8G'
                        },
                        {
                            value: '16384',
                            label: '16G'
                        },
                        {
                            value: '32768',
                            label: '32G'
                        },

                    ],
                    disk: [
                        {
                            value: '100',
                            label: '100G'
                        },
                        {
                            value: '500',
                            label: '500G'
                        },
                        {
                            value: '1000',
                            label: '1T'
                        },
                        {
                            value: '2000',
                            label: '2T'
                        },
                    ],
                    host: [],
                    datastore: [],
                    network: [],
                    cluster: []
                },

            }
        },
        watch: {
            'conf.cluster': function (value) {
                const self = this

                self.conf['hw_name'] = ''
                self.conf['network'] = ''
                self.conf['datastore'] = ''


                self.form['host'] = ''
                self.form['template'] = ''
                self.form['network'] = ''

            },
            'form.network': function (value) {
                const self = this

                this.data.network.map(function (v, i) {

                    if (v.id === value) {
                        // console.log(v)
                        self.conf.network = v['network']
                    }
                })
            },
            'form.datastore': function (value) {
                const self = this

                this.data.datastore.map(function (v, i) {

                    if (v.id === value) {
                        // console.log(v)
                        self.conf.datastore = v['name']
                    }
                })
            }
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        console.log(this.form)
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
                this.$router.push({name: 'Instance'})
            },
            selcluster(val) {
                const self = this

                this.data.cluster.map(function (v, i) {
                    // console.log(v)
                    // console.log(val)

                    if (v.id === val) {
                        // self.conf.hw_name=v['name']
                        // self.conf.cluster=v['name']

                        // console.log(`v['name'] == val ${val}`)
                        self.data.host = v.host
                        self.data.network = v.network
                        console.log(self)
                        self.data.datastore = []
                        // self.data.template = v.template
                        // self.data.datastore = v.datastore
                        // self.data.template = v.template

                        // self.conf = {}
                        self.conf.cluster = v['name']
                        // self.conf.network=''
                        // self.conf.datastore=''
                        // self.form.network = ''

                    }
                })
            },
            selhost(val) {
                const self = this

                this.data.host.map(function (v, i) {
                    // console.log(v)
                    // console.log(val)

                    if (v.id === val) {
                        self.conf.hw_name = v['name']
                        // console.log(`v['name'] == val ${val}`)
                        // self.data.network = v.network
                        self.data.datastore = v.datastore
                        // self.data.template = v.template
                    }
                })
            },


            // 請求資產
            getInit() {
                getClusterAll()
                    .then((response) => {
                        console.log(response.data)
                        // this.data.host = response.data.host
                        this.data.cluster = response.data.data
                        this.data.template = response.data.template
                        // this.data.network = response.data.network
                        // this.data.datastore = response.data.datastore
                    })
                    .catch((error) => {
                        this.$notify.error({
                            title: '错误',
                            message: '这是一条错误的提示消息'
                        });
                    })

            },
        },
        created() {
            // get and set auth user
            this.getInit()
        }


    }
</script>

<style scoped>
    .el-select {
        width: 100%;
    }


</style>


<style>


    .now .el-card__header {
        background: #4e73df;
        color: #fff;
    }
</style>