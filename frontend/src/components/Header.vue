<template>
  <el-row>
    <el-col :span="2" class="header-wrap">
      <!-- 折疊menu  -->
      <el-button class="no-b" :icon="iconName" @click="toggleMenuOpen" />
    </el-col>

    <el-col :span="2" class="header-wrap text-r" style="float: right; margin-right: 5px">
      <el-dropdown>
        <el-button class="no-b">
          {{ username }}
          <i class="fa fa-user-circle" aria-hidden="true" />
          <i class="el-icon-arrow-down el-icon--right" />
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>
              <i class="fa fa-address-card-o" />
              查看個人信息
            </el-dropdown-item>
            <el-dropdown-item @click="logout">
              <i class="fa fa-power-off" />
              登出
            </el-dropdown-item>
            <el-dropdown-item>
              <i class="fa fa-wrench" />
              修改密碼
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-col>

    <el-col
      v-if="hasAdminRole"
      :span="4"
      class="header-wrap text-r"
      style="
        float: right;
        margin-right: 15px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-top: 6px;
      "
    >
      <el-button
        v-if="!isSystemAdminView"
        type="warning"
        size="mini"
        @click="switchToAdminView"
      >
        進入管理後台
      </el-button>
      <el-button v-else type="success" size="mini" @click="switchToResourceView">
        返回資源視圖
      </el-button>
    </el-col>
  </el-row>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Cookies from 'js-cookie'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const username = computed(() => userStore.username)
const isNavMenuOpen = computed(() => userStore.isNavMenuOpen)

const hasAdminRole = computed(() => {
  try {
    const rolesStr = Cookies.get('x_user_roles')
    const roles = rolesStr ? JSON.parse(rolesStr) : []
    return roles.includes('admin')
  } catch {
    return false
  }
})

const isSystemAdminView = computed(() => {
  const path = route.path
  return (
    path.startsWith('/Home/Setting') ||
    path.startsWith('/Home/LoginLog') ||
    path.startsWith('/Home/UserRoles') ||
    path.startsWith('/Home/RolePermissions') ||
    path.startsWith('/Home/Users')
  )
})

const iconName = computed(() => (isNavMenuOpen.value ? 'fa fa-outdent' : 'fa fa-indent'))

function toggleMenuOpen() {
  userStore.toggleMenuOpen()
}

async function logout() {
  try {
    await userStore.logout()
    router.push({ name: 'Login' })
  } catch (e) {
    console.error('Logout API failed, forcing local logout:', e)
    userStore.resetState()
    router.push({ name: 'Login' })
  }
}

function switchToAdminView() {
  router.push('/Home/Setting')
}

function switchToResourceView() {
  router.push('/Home')
}
</script>

<style scoped>
.no-b {
  border: none !important;
}

.text-r {
  text-align: right;
}

.head-wrap {
  height: 40px;
  border-bottom: 1px solid #eee;
}
</style>
