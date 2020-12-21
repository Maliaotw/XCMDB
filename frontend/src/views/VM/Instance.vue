<template>

    <div>


        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>VM</el-breadcrumb-item>
                <el-breadcrumb-item :to="{name:'Instance'}">實例</el-breadcrumb-item>
            </el-breadcrumb>
        </div>


        <el-row :gutter="20" style="margin-bottom: 20px">


            <el-col :span="4">
                <router-link :to="{name:'InsCreate'}">
                    <el-button type="primary">新增</el-button>
                </router-link>
            </el-col>


            <el-col :span="20" style="text-align: right">
                <InstanceFilter ref="filter"/>
            </el-col>
        </el-row>

        <InstanceTable ref="table"/>
    </div>

</template>


<script>

    import InstanceFilter from './InstanceFilter'
    import InstanceTable from './InstanceTable'
    import app from '../../main'

    export default {
        components: {InstanceTable, InstanceFilter},
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
            }
        },
        created() {
          // console.log(InstanceTable.created())
          // console.log(InstanceFilter.created())
          // console.log(InstanceTable.data['tableData'])


        },
        methods: {


        },
        mounted: function () {
            app.$emit('filter',this.$refs.filter);
            app.$emit('table',this.$refs.table);
        }


    }
</script>