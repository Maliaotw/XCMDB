<template>

    <div>



    </div>

</template>


<script>
    import app from '../../main'

    export default {
        name: "PHostFilter",  // using EXACTLY this name is essential,
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
                // console.log(this.table)
                // this.table.getInit(this.table.page, this.table.pageSize)
                // this.table.table.getInit(this.table.page, this.table.pageSize, this.filterform)
                // this.getInit(this.page, this.pageSize, this.filterform)

            },
        },
        mounted: function () {


        }

    }
</script>