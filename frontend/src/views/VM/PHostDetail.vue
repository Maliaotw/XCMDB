<template>


    <div>


        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>VM</el-breadcrumb-item>
                <el-breadcrumb-item :to="{name:'PHost'}">主機</el-breadcrumb-item>
                <el-breadcrumb-item>{{this.form.name}}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>


        <el-row type="flex">

            <el-col :span="12">
                <template>
                    <el-tabs v-model="activeName">
                        <el-tab-pane label="主機詳情" name="info"/>
                        <el-tab-pane label="Datastore" name="Datastore"/>
                    </el-tabs>
                </template>
            </el-col>

            <el-col :span="12" style="text-align: right">
                <label>最近更新日期： {{ this.form.last_date }}</label>
            </el-col>

        </el-row>

        <el-row type="flex">
            <el-col :span="24">
                <div v-show="activeName === 'info'">

                    <label><b>主機信息</b></label>
                    <el-form
                            label-position="left"
                            label-width="200px"
                            style="margin-left: 20px;"
                    >
                        <el-form-item label="主機名:" style="margin-bottom: 0px">
                            <label><b>{{this.form.name}}</b></label>
                        </el-form-item>


                    </el-form>

                </div>

                <div v-show="activeName === 'Datastore'">


                    <DatastoreTable v-bind:id="this.$route.params.id"/>


                </div>


            </el-col>


        </el-row>


    </div>

</template>


<script>
    import DatastoreTable from './DatastoreTable'
    import {getHostobj, putDataStoreobj} from '@/api/vm'

    export default {
        components: {DatastoreTable},
        data() {
            return {
                form: {},
                activeName: 'info'
            }
        },

        methods: {
            datastore_push(row) {
                // console.log(row)
                // console.log(row.id)

                const data = row
                const id = row.id
                delete data['id']

                putDataStoreobj(id, data)
                    .then((res) => {
                        console.log('ok')
                        console.log(res)

                        if (res) {
                            this.$notify.success({
                                title: '成功',
                                message: '这是一条成功的提示消息'
                            });
                        } else {
                            this.$notify.error({
                                title: '失敗',
                                message: '这是一条失敗的提示消息'
                            });
                        }


                    })

            }


        },
        created() {
            getHostobj(this.$route.params.id)
                .then((res) => {
                    this.form = res.data
                })

            console.log('PHostDetail')


        }


    }
</script>


<style>
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

    .demo-table-expand {
        font-size: 0;
    }

    .demo-table-expand label {
        width: 90px;
        color: #99a9bf;
    }

    .demo-table-expand .el-form-item {
        margin-right: 0;
        margin-bottom: 0;
        width: 50%;
    }


</style>
