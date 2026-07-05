<template>
    <div>
        <el-breadcrumb separator="/" style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px">
            <el-breadcrumb-item>系統管理後台</el-breadcrumb-item>
            <el-breadcrumb-item>系統用戶帳戶管理</el-breadcrumb-item>
        </el-breadcrumb>

        <el-row style="margin-bottom: 20px">
            <el-card class="box-card" shadow="hover">
                <div slot="header" class="clearfix" style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; font-size: 16px;"><i class="el-icon-user"/> 用戶帳戶清單</span>
                    <el-button type="primary" size="small" icon="el-icon-plus" @click="openCreateDialog">新增用戶</el-button>
                </div>
                
                <el-row>
                    <el-col :span="22" :offset="1">
                        <el-table :data="userTableData" size="medium" style="width: 100%" v-loading="loading">
                            <el-table-column prop="username" label="用戶名" width="180">
                                <template slot-scope="scope">
                                    <div style="display: flex; align-items: center;">
                                        <el-avatar size="small" icon="el-icon-user" style="margin-right: 10px; background: #409eff;"/>
                                        <b>{{ scope.row.username }}</b>
                                    </div>
                                </template>
                            </el-table-column>
                            <el-table-column prop="email" label="電子郵箱" width="250">
                                <template slot-scope="scope">
                                    <span>{{ scope.row.email || '—' }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="role" label="所屬角色" width="180">
                                <template slot-scope="scope">
                                    <el-tag :type="getRoleTagType(scope.row.role)" size="small">
                                        {{ scope.row.role }}
                                    </el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column prop="is_superuser" label="超級管理員" width="150" align="center">
                                <template slot-scope="scope">
                                    <el-tag :type="scope.row.is_superuser ? 'danger' : 'info'" size="small" effect="dark">
                                        {{ scope.row.is_superuser ? '是' : '否' }}
                                    </el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column label="帳戶操作" align="center">
                                <template slot-scope="scope">
                                    <el-button 
                                        type="warning" 
                                        size="small" 
                                        icon="el-icon-edit"
                                        @click="openEditDialog(scope.row)">
                                        編輯
                                    </el-button>
                                    <el-button 
                                        type="danger" 
                                        size="small" 
                                        icon="el-icon-delete"
                                        @click="handleDelete(scope.row)"
                                        :disabled="scope.row.username === 'admin'">
                                        刪除
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-col>
                </el-row>
            </el-card>
        </el-row>

        <!-- 新增/編輯用戶 Dialog -->
        <el-dialog
                :title="isEdit ? '編輯用戶帳戶' : '新增用戶帳戶'"
                :visible.sync="dialogVisible"
                width="40%"
                @close="resetForm"
        >
            <el-form :model="form" :rules="rules" ref="userForm" label-position="left" label-width="120px">
                <el-form-item label="用戶名" prop="username">
                    <el-input v-model="form.username" placeholder="請輸入用戶名" :disabled="isEdit"></el-input>
                </el-form-item>
                
                <el-form-item label="電子郵箱" prop="email">
                    <el-input v-model="form.email" placeholder="請輸入 Email 地址"></el-input>
                </el-form-item>
                
                <el-form-item :label="isEdit ? '重設密碼' : '初始密碼'" prop="password">
                    <el-input 
                        v-model="form.password" 
                        show-password 
                        :placeholder="isEdit ? '若不變更請留空' : '請輸入初始密碼'">
                    </el-input>
                </el-form-item>

                <el-form-item label="系統角色" prop="role">
                    <el-select v-model="form.role" placeholder="請選擇角色" style="width: 100%">
                        <el-option label="管理員 (Admin)" value="admin"></el-option>
                        <el-option label="運維員 (Operator)" value="operator"></el-option>
                        <el-option label="審計員 (Auditor)" value="auditor"></el-option>
                        <el-option label="訪客 (Visitor)" value="visitor"></el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="超級管理員" prop="is_superuser">
                    <el-switch v-model="form.is_superuser"></el-switch>
                    <span style="margin-left: 10px; color: #909399; font-size: 13px;">(賦予 Django 後台 Superuser 權限)</span>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="submitForm" :loading="submitLoading">確 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import {getDemoUserList, createDemoUser, updateDemoUser, deleteDemoUser} from '@/api/users'

    export default {
        data() {
            return {
                userTableData: [],
                loading: false,
                submitLoading: false,
                dialogVisible: false,
                isEdit: false,
                form: {
                    id: null,
                    username: '',
                    email: '',
                    password: '',
                    role: 'visitor',
                    is_superuser: false
                },
                rules: {
                    username: [
                        { required: true, message: '用戶名不能為空', trigger: 'blur' },
                        { min: 3, max: 20, message: '長度在 3 到 20 個字元', trigger: 'blur' }
                    ],
                    email: [
                        { type: 'email', message: '請輸入正確的電子郵箱格式', trigger: 'blur' }
                    ],
                    role: [
                        { required: true, message: '請選擇一個系統角色', trigger: 'change' }
                    ],
                    password: [
                        { validator: (rule, value, callback) => {
                            if (!this.isEdit && !value) {
                                callback(new Error('新增用戶時初始密碼為必填項'))
                            } else if (value && value.length < 5) {
                                callback(new Error('密碼長度不能小於 5 位'))
                            } else {
                                callback()
                            }
                        }, trigger: 'blur' }
                    ]
                }
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
                    .catch(() => {
                        this.loading = false
                        this.$notify.error({
                            title: '錯誤',
                            message: '獲取用戶列表失敗'
                        })
                    })
            },
            getRoleTagType(role) {
                const map = {
                    'admin': 'danger',
                    'operator': 'primary',
                    'auditor': 'success',
                    'visitor': 'info'
                }
                return map[role] || 'info'
            },
            openCreateDialog() {
                this.isEdit = false
                this.form = {
                    id: null,
                    username: '',
                    email: '',
                    password: '',
                    role: 'visitor',
                    is_superuser: false
                }
                this.dialogVisible = true
            },
            openEditDialog(row) {
                this.isEdit = true
                this.form = {
                    id: row.id,
                    username: row.username,
                    email: row.email,
                    password: '',
                    role: row.role,
                    is_superuser: row.is_superuser
                }
                this.dialogVisible = true
            },
            resetForm() {
                this.$refs.userForm && this.$refs.userForm.resetFields()
            },
            submitForm() {
                this.$refs.userForm.validate((valid) => {
                    if (valid) {
                        this.submitLoading = true
                        const payload = { ...this.form }
                        if (this.isEdit && !payload.password) {
                            delete payload.password // 如果是編輯且密碼為空，不發送該欄位以防止清空密碼
                        }
                        
                        if (this.isEdit) {
                            updateDemoUser(payload.id, payload)
                                .then(() => {
                                    this.submitLoading = false
                                    this.dialogVisible = false
                                    this.$notify.success({
                                        title: '成功',
                                        message: `用戶 [${payload.username}] 資料更新成功！`
                                    })
                                    this.getUserList()
                                })
                                .catch(() => {
                                    this.submitLoading = false
                                    this.$notify.error({
                                        title: '錯誤',
                                        message: '更新用戶失敗'
                                    })
                                })
                        } else {
                            createDemoUser(payload)
                                .then(() => {
                                    this.submitLoading = false
                                    this.dialogVisible = false
                                    this.$notify.success({
                                        title: '成功',
                                        message: `用戶 [${payload.username}] 新建成功！`
                                    })
                                    this.getUserList()
                                })
                                .catch(() => {
                                    this.submitLoading = false
                                    this.$notify.error({
                                        title: '錯誤',
                                        message: '新建用戶失敗'
                                    })
                                })
                        }
                    }
                })
            },
            handleDelete(row) {
                this.$confirm(`確定要刪除系統用戶 [${row.username}] 嗎？此操作將永久移除其所有登入權限。`, '警告', {
                    confirmButtonText: '確定刪除',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    deleteDemoUser(row.id)
                        .then(() => {
                            this.$notify.success({
                                title: '成功',
                                message: `用戶 [${row.username}] 已被成功刪除。`
                            })
                            this.getUserList()
                        })
                        .catch(() => {
                            this.$notify.error({
                                title: '錯誤',
                                message: '刪除用戶失敗'
                            })
                        })
                }).catch(() => {})
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
