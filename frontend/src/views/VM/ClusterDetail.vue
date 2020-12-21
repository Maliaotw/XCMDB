<template>


    <div>


        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>VM</el-breadcrumb-item>
                <el-breadcrumb-item :to="{name:'Cluster'}">集群</el-breadcrumb-item>
                <el-breadcrumb-item>{{this.form.remark}} {{this.form.name}}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>


        <el-row type="flex">

            <el-col :span="12">
                <template>
                    <el-tabs v-model="activeName">
                        <el-tab-pane label="集群詳情" name="info"/>
                        <el-tab-pane label="Network" name="Network"/>
                        <el-tab-pane label="ESXI" name="ESXI"/>
                        <el-tab-pane label="Instance" name="Instance"/>
                    </el-tabs>
                </template>
            </el-col>

            <el-col :span="12" style="text-align: right">
            </el-col>

        </el-row>

        <el-row type="flex">
            <el-col :span="24">
                <div v-show="activeName === 'info'">

                    <el-col
                            :span="18"
                    >
                        <div>
                            <span>監控負載</span>
                        </div>


                    </el-col>


                    <el-col :span="6">
                        <span>基礎信息</span>

                    </el-col>

                </div>

                <div v-show="activeName === 'Network'">


                    <el-col
                            :span="12"
                    >
                        <div>
                            <!--  Network List -->
                            <span>列表</span>
                            <NetworkTable :id="this.$route.params.id" ref="net" />

                        </div>


                    </el-col>

                    <el-col
                            :span="10"
                            style="margin-left: 40px">
                        <div>
                            <!--  NetStaticTable -->
                            <span>網段關聯表</span>
                            <NetStaticTable :id="this.net" ref="netstatic" />
                        </div>


                    </el-col>



                </div>

                <div v-show="activeName === 'ESXI'">

                    <el-col
                            :span="14"
                    >
                        <div>
                            <!--  ESXI List -->
                            <span>列表</span>
                            <PHostTable :id="this.$route.params.id" ref="esxi"/>

                        </div>


                    </el-col>

                    <el-col
                            :span="8"
                            style="margin-left: 40px">
                        <div>
                            <!--  ESXI DataStore -->
                            <span>儲存區</span>
                            <DatastoreTable ref="datastore" :id="this.host"/>

                        </div>


                    </el-col>


                </div>


                <div v-show="activeName === 'Instance'">
                    <!--  Instance -->
                    <InstanceTable :id="this.$route.params.id"/>
                </div>


            </el-col>


        </el-row>


    </div>

</template>


<script>
    import {getClusterobj} from '../../api/vm'
    import PHostTable from './PHostTable'
    import InstanceTable from './InstanceTable'
    import DatastoreTable from './DatastoreTable'
    import NetworkTable from './NetworkTable'
    import NetStaticTable from './NetStaticTable'
    import app from "../../main";

    export default {
        components: {
            PHostTable,
            InstanceTable,
            DatastoreTable,
            NetworkTable,
            NetStaticTable
        },
        data() {
            return {
                form: {},
                activeName: 'info',
                host: 0,
                net:0

            }
        },

        methods: {
            sethost(val){
                this.host = val
            },
            setnet(val){
                this.net = val
            }

        },
        created() {
            getClusterobj(this.$route.params.id)
                .then((res) => {
                    this.form = res.data

                })

            // console.log('ClusterDetail')
            // console.log(this.$route.params.id)


        },
        mounted: function () {

            // console.log(this.$refs.esxi)
            console.log(this.$refs.datastore)
            const vm = this
            app.$emit('cluster',vm);
            // app.$emit('datastoreobj',vm.$refs.datastore);
        }


    }
</script>


<style>


</style>
