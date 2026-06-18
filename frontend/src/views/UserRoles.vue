<template>
    <div>
        <el-breadcrumb separator="/" style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px">
            <el-breadcrumb-item>系統管理後台</el-breadcrumb-item>
            <el-breadcrumb-item>成員與角色分配</el-breadcrumb-item>
        </el-breadcrumb>

        <el-row style="margin-bottom: 20px">
            <el-card class="box-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span style="font-weight: bold; font-size: 16px;"><i class="el-icon-user-solid"/> 用戶角色分配</span>
                </div>
                
                <el-row>
                    <el-col :span="22" :offset="1">
                        <el-table :data="userTableData" size="medium" style="width: 100%" v-loading="loading">
                            <el-table-column prop="username" label="用戶名" width="220">
                                <template slot-scope="scope">
                                    <div style="display: flex; align-items: center;">
                                        <el-avatar size="small" icon="el-icon-user" style="margin-right: 10px; background: #409eff;"/>
                                        <b>{{ scope.row.username }}</b>
                                    </div>
                                </template>
                            </el-table-column>
                            <el-table-column prop="email" label="郵箱" width="280">
                                <template slot-scope="scope">
                                    <span>{{ scope.row.email || '未設定' }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="分配系統角色">
                                <template slot-scope="scope">
                                    <el-select v-model="scope.row.role" placeholder="請選擇角色" style="width: 220px">
                                        <el-option label="管理員 (Admin)" value="admin"></el-option>
                                        <el-option label="運維員 (Operator)" value="operator"></el-option>
                                        <el-option label="審計員 (Auditor)" value="auditor"></el-option>
                                        <el-option label="訪客 (Visitor)" value="visitor"></el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" width="180" align="center">
                                <template slot-scope="scope">
                                    <el-button 
                                        type="primary" 
                                        size="small" 
                                        icon="el-icon-check"
                                        @click="saveUserRole(scope.row)">
                                        儲存變更
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-col>
                </el-row>
            </el-card>
        </el-row>
    </div>
</template>

<script>
    import {getDemoUserList, updateDemoUserRole} from '@/api/users'

    export default {
        data() {
            return {
                userTableData: [],
                loading: false
            }
        },
        methods: {
            getUserList() {
                this.loading = true
                getDemoUserList()
                    .then((response) => {
                        this.userTableData = response.data.results
                        this.loading = false
                    })
                    .catch((error) => {
                        this.loading = false
                        this.$notify.error({
                            title: '錯誤',
                            message: '獲取用戶列表失敗'
                        })
                    })
            },
            saveUserRole(row) {
                updateDemoUserRole(row.id, row.role)
                    .then((response) => {
                        this.$notify.success({
                            title: '成功',
                            message: `用戶 [${row.username}] 角色成功更新為 [${row.role}]！`
                        })
                    })
                    .catch((error) => {
                        this.$notify.error({
                            title: '錯誤',
                            message: '更新角色失敗'
                        })
                    })
            }
        },
        created() {
            this.getUserList()
        }
    }
</script>

<style scoped>
    .box-card {
        padding: 10px;
    }
</style>
