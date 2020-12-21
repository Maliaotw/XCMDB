<template>

    <div>

        <div>
            <el-breadcrumb separator="/" style="padding-top: 0px;padding-bottom: 20px">
                <el-breadcrumb-item>VM</el-breadcrumb-item>
                <el-breadcrumb-item :to="{name:'Server'}">主機</el-breadcrumb-item>
            </el-breadcrumb>
        </div>


        <el-row :gutter="20" style="margin-bottom: 20px">

            <el-col :span="4">
            </el-col>

            <el-col :span="20" style="text-align: right">
                <PHostFilter ref="filter"/>
            </el-col>


        </el-row>
        <PHostTable ref="table"/>

    </div>

</template>


<script>


    import PHostTable from './PHostTable'
    import PHostFilter from './PHostFilter'
    import app from "../../main";


    export default {
        components: {PHostTable, PHostFilter},
        data() {
            return {
                total: 0,
                pageSize: 10,
                page: 1,
                tableData: [],
                form: {},
            }
        },
        destroyed() {

        },
        methods: {

        },
        created() {


        },
        mounted: function () {
            app.$emit('filter',this.$refs.filter);
            app.$emit('table',this.$refs.table);
        }


    }
</script>