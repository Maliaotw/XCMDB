<template>
    <div>
        <el-breadcrumb separator="/" style="background: white;padding-top: 20px;padding-bottom: 20px;margin-bottom: 20px">
            <el-breadcrumb-item>系統管理後台</el-breadcrumb-item>
            <el-breadcrumb-item>角色權限配置 (RBAC)</el-breadcrumb-item>
        </el-breadcrumb>

        <el-row style="margin-bottom: 20px">
            <el-card class="box-card" shadow="hover">
                <div slot="header" class="clearfix">
                    <span style="font-weight: bold; font-size: 16px;"><i class="el-icon-lock"/> 角色選單與動作權限分配</span>
                </div>
                
                <el-row>
                    <el-col :span="22" :offset="1">
                        <el-table :data="rolePermTableData" size="medium" style="width: 100%" v-loading="loading">
                            <el-table-column prop="role" label="系統角色識別碼" width="200">
                                <template slot-scope="scope">
                                    <el-tag :type="getRoleTagType(scope.row.role)" effect="dark" size="small" style="font-weight: bold; font-size: 13px; padding: 2px 10px;">
                                        {{ scope.row.role.toUpperCase() }}
                                    </el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column label="可存取選單 (Menus)">
                                <template slot-scope="scope">
                                    <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                                        <el-tag v-for="menuName in parseJSON(scope.row.menus)" :key="menuName" type="info" size="small" effect="plain">
                                            {{ getMenuTitle(menuName) }}
                                        </el-tag>
                                        <span v-if="parseJSON(scope.row.menus).length === 0" style="color: #c0c4cc; font-style: italic; font-size: 13px;">未配置任何選單</span>
                                    </div>
                                </template>
                            </el-table-column>
                            <el-table-column label="可執行敏感操作 (Actions)" width="280">
                                <template slot-scope="scope">
                                    <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                                        <el-tag v-for="actionName in parseJSON(scope.row.actions)" :key="actionName" type="warning" size="small" effect="plain">
                                            {{ actionName }}
                                        </el-tag>
                                        <span v-if="parseJSON(scope.row.actions).length === 0" style="color: #c0c4cc; font-style: italic; font-size: 13px;">僅唯讀 (無寫入操作)</span>
                                    </div>
                                </template>
                            </el-table-column>
                            <el-table-column label="權限操作" width="180" align="center">
                                <template slot-scope="scope">
                                    <el-button 
                                        type="warning" 
                                        size="small" 
                                        icon="el-icon-edit"
                                        @click="editRolePerm(scope.row)">
                                        配置權限
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-col>
                </el-row>
            </el-card>
        </el-row>

        <!-- 配置角色權限 Dialog -->
        <el-dialog
                title="配置系統角色之選單與操作動作"
                :visible.sync="permDialogVisible"
                width="55%"
        >
            <el-form label-position="top">
                <el-form-item label="當前編輯角色" style="margin-bottom: 25px;">
                    <el-tag type="primary" size="medium" effect="dark" style="font-weight: bold; font-size: 14px; padding: 2px 12px;">
                        {{ currentEditRole.role ? currentEditRole.role.toUpperCase() : '' }}
                    </el-tag>
                </el-form-item>
                
                <el-form-item label="配置前台可見選單 (Menus)" style="border-top: 1px solid #f2f6fc; padding-top: 15px; margin-bottom: 25px;">
                    <el-checkbox-group v-model="selectedMenus">
                        <el-row>
                            <el-col :span="6" v-for="m in allMenus" :key="m.value" style="margin-bottom: 12px;">
                                <el-checkbox :label="m.value"><b>{{ m.label }}</b></el-checkbox>
                            </el-col>
                        </el-row>
                    </el-checkbox-group>
                </el-form-item>

                <el-form-item label="配置後端與按鈕動作權限 (Actions)" style="border-top: 1px solid #f2f6fc; padding-top: 15px;">
                    <el-checkbox-group v-model="selectedActions">
                        <el-row>
                            <el-col :span="8" v-for="act in allActions" :key="act.value" style="margin-bottom: 12px;">
                                <el-checkbox :label="act.value">
                                    <span>{{ act.label }}</span>
                                </el-checkbox>
                            </el-col>
                        </el-row>
                    </el-checkbox-group>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="permDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveRolePerm" icon="el-icon-check">確認變更</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import {getRolePermissions, updateRolePermission} from '@/api/settings'

    export default {
        data() {
            return {
                rolePermTableData: [],
                loading: false,
                permDialogVisible: false,
                currentEditRole: {},
                selectedMenus: [],
                selectedActions: [],
                allMenus: [
                    { label: '資產列表', value: 'Asset' },
                    { label: '物理服務器', value: 'Idrac' },
                    { label: '網路設備', value: 'NetDevice' },
                    { label: '標籤列表', value: 'Tag' },
                    { label: '虛擬機', value: 'Host' },
                    { label: 'Cluster', value: 'Cluster' },
                    { label: 'ESXI', value: 'PHost' },
                    { label: 'Instance', value: 'Instance' },
                    { label: '機房列表', value: 'IDC' },
                    { label: '機櫃列表', value: 'Rack' },
                    { label: 'ISP資訊', value: 'ISP' },
                    { label: '任務列表', value: 'pt' },
                    { label: '登入歷史', value: 'LoginLog' }
                ],
                allActions: [
                    { label: '資產編輯 (asset:edit)', value: 'asset:edit' },
                    { label: '資產分配 (asset:assign)', value: 'asset:assign' },
                    { label: '新增網設 (netdevice:add)', value: 'netdevice:add' },
                    { label: '編輯網設 (netdevice:edit)', value: 'netdevice:edit' },
                    { label: '刪除網設 (netdevice:delete)', value: 'netdevice:delete' },
                    { label: '新增標籤 (tag:add)', value: 'tag:add' },
                    { label: '編輯標籤 (tag:edit)', value: 'tag:edit' },
                    { label: '刪除標籤 (tag:delete)', value: 'tag:delete' },
                    { label: '編輯業務 (busunit:edit)', value: 'busunit:edit' },
                    { label: '刪除業務 (busunit:delete)', value: 'busunit:delete' },
                    { label: '編輯機房 (idc:edit)', value: 'idc:edit' },
                    { label: '編輯ISP (isp:edit)', value: 'isp:edit' },
                    { label: '編輯機櫃 (rack:edit)', value: 'rack:edit' },
                    { label: '編輯網路 (network:edit)', value: 'network:edit' }
                ]
            }
        },
        methods: {
            getRolePerms() {
                this.loading = true
                getRolePermissions()
                    .then((response) => {
                        this.rolePermTableData = response.data.results
                        this.loading = false
                    })
                    .catch((error) => {
                        this.loading = false
                        this.$notify.error({
                            title: '錯誤',
                            message: '獲取角色權限列表失敗'
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
            parseJSON(val) {
                try {
                    return val ? JSON.parse(val) : []
                } catch(e) {
                    return []
                }
            },
            getMenuTitle(val) {
                const map = {
                    'Asset': '資產列表',
                    'Idrac': '物理服務器',
                    'NetDevice': '網路設備',
                    'Tag': '標籤列表',
                    'Host': '虛擬機',
                    'Cluster': 'Cluster',
                    'PHost': 'ESXI',
                    'Instance': 'Instance',
                    'IDC': '機房列表',
                    'Rack': '機櫃列表',
                    'ISP': 'ISP資訊',
                    'pt': '任務列表',
                    'LoginLog': '登入歷史'
                }
                return map[val] || val
            },
            editRolePerm(row) {
                this.currentEditRole = row
                this.selectedMenus = this.parseJSON(row.menus)
                this.selectedActions = this.parseJSON(row.actions)
                this.permDialogVisible = true
            },
            saveRolePerm() {
                const id = this.currentEditRole.id
                const payload = {
                    menus: JSON.stringify(this.selectedMenus),
                    actions: JSON.stringify(this.selectedActions)
                }
                updateRolePermission(id, payload)
                    .then((res) => {
                        this.permDialogVisible = false
                        this.$notify.success({
                            title: '成功',
                            message: `角色 [${this.currentEditRole.role}] 權限配置更新成功！`
                        })
                        this.getRolePerms()
                    })
                    .catch((err) => {
                        this.$notify.error({
                            title: '錯誤',
                            message: '配置權限失敗'
                        })
                    })
            }
        },
        created() {
            this.getRolePerms()
        }
    }
</script>

<style scoped>
    .box-card {
        padding: 10px;
    }
</style>
