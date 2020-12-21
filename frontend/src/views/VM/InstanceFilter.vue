<template>

    <div>

        <el-form :model="filterform">

            <label style="margin-right: 20px;">名稱</label>

            <el-input
                    v-model="filterform.hw_name"
                    placeholder="请输入内容"
                    style="width:10%; margin-right: 2px;"
                    @change="handleFilterSubmit"
            >

            </el-input>

            <label style="margin-left: 20px;margin-right: 20px;">IP</label>

            <el-input
                    v-model="filterform.ip_address"
                    placeholder=""
                    style="width:10%; margin-right: 2px;"
                    @change="handleFilterSubmit"
            >

            </el-input>


            <label style="margin-left: 20px;margin-right: 20px;">狀態</label>
            <el-select v-model="filterform.hw_power_status"
                       style="margin-left: 2px;margin-right: 2px;width:10%"
                       placeholder="狀態"
                       @change="handleFilterSubmit"

            >
                <el-option key="" label="----" value=""/>
                <el-option label="運行中" key="poweredOn" value="poweredOn"/>
                <el-option label="已停止" key="poweredOff" value="poweredOff"/>
                <el-option label="建置中" key="building" value="building"/>


            </el-select>

            <label style="margin-left: 20px;margin-right: 20px;">主機</label>
            <el-select
                    v-model="filterform.host"
                    style="margin-left: 2px;margin-right: 2px;width:10%"
                    placeholder=""
                    @change="handleFilterSubmit"

            >
                <el-option key="" label="----" value=""/>
                <el-option v-for="item in this.host" :label="item.name" :key="item.id"
                           :value="item.id"/>

            </el-select>


            <label style="margin-left: 20px;margin-right: 20px;">Network</label>
            <el-select v-model="filterform.network"
                       style="margin-left: 2px;margin-right: 2px;width:10%"
                       placeholder=""
                       @change="handleFilterSubmit"
            >
                <el-option key="" label="----" value=""/>
                <el-option v-for="item in this.network" :label="item.network" :key="item.id"
                           :value="item.id"/>

            </el-select>

            <label style="margin-left: 20px;margin-right: 20px;">DataSrotre</label>
            <el-select v-model="filterform.datastore"
                       style="margin-left: 2px;margin-right: 2px;"
                       placeholder=""
                       @change="handleFilterSubmit"
            >
                <el-option key="" label="----" value=""/>
                <el-option v-for="item in this.datastore" :label="item.name" :key="item.id"
                           :value="item.id"/>

            </el-select>



        </el-form>


    </div>

</template>


<script>
    import app from '../../main'

    export default {
        name: "InstanceFilter",  // using EXACTLY this name is essential,

        data() {
            return {
                filterform: {},
                datastore: {},
                network: {},
                host: {},
            }
        },
        methods: {
            // 提交搜索
            handleFilterSubmit() {
                // console.log(this.$refs)
                console.log(this.table)
                this.table.getInit(this.table.page, this.table.pageSize)
                // this.table.table.getInit(this.table.page, this.table.pageSize, this.filterform)
                // this.getInit(this.page, this.pageSize, this.filterform)

            },
        },
        mounted: function () {
            var vm = this;
            // app.$emit('filter',this.$refs.filter);
            app.$on('datastore', (data) => {
                // console.log(data)
                vm.datastore = data
            })
            app.$on('network', (data) => {
                // console.log(data)
                vm.network = data
            })
            app.$on('host', (data) => {
                // console.log(data)
                vm.host = data
            })
            app.$on('init', (data) => {
                // console.log(data)
                vm.init = data
            })
            app.$on('table', (data) => {
                // console.log(data)
                vm.table = data
                // console.log(data)
                // vm.datastore = data
            })

        }

    }
</script>