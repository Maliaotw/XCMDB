<template>
  <el-row class="tac">
    <el-col :span="24" class="h100">
      <el-menu
        class="no-boarder el-menu-vertical-demo h100"
        router
        unique-opened
        @open="handleOpen"
        @close="handleClose"
        :background-color="isSystemAdminView ? '#2c3e50' : '#545c64'"
        text-color="#fff"
        :default-active="activeTag"
        :collapse="!isNavMenuOpen"
        active-text-color="#ffd04b"
        mode="vertical"
      >
        <el-menu-item align="center" style="font-weight: bold; font-size: 14px">
          <template v-if="!isNavMenuOpen">
            <i :class="isSystemAdminView ? 'el-icon-monitor' : 'el-icon-s-home'" />
          </template>
          <template v-else>
            <span v-if="isSystemAdminView" style="color: #e6a23c">
              <i class="el-icon-monitor" /> XCMDB 管理後台
            </span>
            <span v-else style="color: #409eff">
              <i class="el-icon-s-home" /> XCMDB 資源管理
            </span>
          </template>
        </el-menu-item>

        <el-menu-item v-if="!isSystemAdminView" index="/Home">
          <i class="el-icon-view" />
          <span>&nbsp;&nbsp;&nbsp;儀表盤</span>
        </el-menu-item>

        <el-submenu v-for="item in filteredMenu" :index="item.name" :key="item.name" class="no-boarder">
          <template #title>
            <i :class="item.meta.icon" />&nbsp;
            <span v-text="item.meta.title" />
          </template>
          <el-menu-item-group class="over-hide" v-for="sub in item.sub" :key="sub.name">
            <el-menu-item :index="sub.meta.index" v-text="sub.meta.title"></el-menu-item>
          </el-menu-item-group>
        </el-submenu>
      </el-menu>
    </el-col>
  </el-row>
</template>

<style scoped>
.h100 {
  height: 100%;
}

.tac {
  position: fixed;
  top: 0px;
  bottom: 0px;
  z-index: 999;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 201px;
}
</style>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import menu from '../config/menu-config'
import Cookies from 'js-cookie'

const route = useRoute()
const userStore = useUserStore()

const activeTag = ref('')

// Sync active tag from route meta on mount
function syncActiveTag() {
  activeTag.value = route.meta.index || ''
}

const isNavMenuOpen = computed(() => userStore.isNavMenuOpen)

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

function parseCookieJson(name) {
  try {
    const value = Cookies.get(name)
    return value ? JSON.parse(value) : []
  } catch {
    return []
  }
}

const filteredMenu = computed(() => {
  if (isSystemAdminView.value) {
    // 後台管理視圖：精美分類為三大板塊
    return [
      {
        name: 'iam_control',
        meta: {
          title: '成員與權限控制',
          icon: 'el-icon-user'
        },
        sub: [
          {
            name: 'Users',
            meta: {
              index: '/Home/Users',
              title: '帳戶與用戶管理'
            }
          },
          {
            name: 'UserRoles',
            meta: {
              index: '/Home/UserRoles',
              title: '用戶角色分配'
            }
          },
          {
            name: 'RolePermissions',
            meta: {
              index: '/Home/RolePermissions',
              title: '角色權限配置'
            }
          }
        ]
      },
      {
        name: 'system_control',
        meta: {
          title: '系統連線配置',
          icon: 'el-icon-setting'
        },
        sub: [
          {
            name: 'Setting',
            meta: {
              index: '/Home/Setting',
              title: '基礎參數配置'
            }
          }
        ]
      },
      {
        name: 'audit_control',
        meta: {
          title: '安全審計日誌',
          icon: 'el-icon-document'
        },
        sub: [
          {
            name: 'LoginLog',
            meta: {
              index: '/Home/LoginLog',
              title: '登入歷史日誌'
            }
          }
        ]
      }
    ]
  } else {
    // 前台資源視圖
    const userMenus = parseCookieJson('x_user_menus')
    const roles = parseCookieJson('x_user_roles')
    const isAdmin = roles.includes('admin')

    return menu
      .map((item) => {
        const filteredSub = item.sub.filter((sub) => {
          // Setting (系統設置) 只能在管理後台看到，前台直接排除
          if (sub.name === 'Setting') return false

          // 如果是登入歷史，管理員因為可以在後台看，前台就隱藏；普通用戶若有權限則在前台顯示
          if (sub.name === 'LoginLog' || sub.name === '登入歷史') {
            if (isAdmin) return false
            return userMenus.includes('LoginLog') || userMenus.includes('登入歷史')
          }

          // 其它菜單，如果是管理員全可見，否則依照角色擁有的菜單權限過濾
          return isAdmin || userMenus.includes(sub.name)
        })
        return {
          ...item,
          sub: filteredSub
        }
      })
      .filter((item) => item.sub.length > 0)
  }
})

function handleOpen(key, keyPath) {
  // 選單展開
}

function handleClose(key, keyPath) {
  // 選單收起
}
</script>
