import { createRouter, createWebHistory } from 'vue-router'
import Layout from './views/Layout'
import { getTokenFromCookie } from '@/utils/auth'
import { ElMessage } from 'element-plus'

const constantRoutes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('./views/Login')
  },
  {
    path: '/Home',
    name: 'Home',
    component: Layout,
    children: [
      {
        path: '/Home',
        name: 'HomeDashboard',
        meta: {
          index: '/Home',
          title: '儀表盤',
          type: 'menu',
          active: false,
          notCache: true
        },
        component: () => import('./views/DashBoard')
      },
      {
        path: 'Asset',
        name: 'Asset',
        meta: {
          index: '/Home/Asset',
          title: '資產',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Basic/Asset')
      },
      {
        path: 'AssetDetail/:id',
        name: 'AssetDetail',
        meta: {
          index: '/Home/Asset',
          title: '資產詳細',
          type: 'page',
          active: false
        },
        component: () => import('./views/Basic/AssetDetail')
      },
      {
        path: 'Asset/:id/Update',
        name: 'AssetUpdate',
        meta: {
          index: '/Home/Asset',
          title: '分配資產',
          type: 'page',
          active: false
        },
        component: () => import('./views/Basic/AssetUpdate')
      },
      {
        path: 'idrac',
        name: 'Idrac',
        meta: {
          index: '/Home/Idrac',
          title: '物理服務器',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Basic/Idrac')
      },
      {
        path: 'idrac/Create',
        name: 'IdracCreate',
        meta: {
          index: '/Home/Idrac',
          title: '創建物理服務器',
          type: 'page',
          active: false
        },
        component: () => import('./views/Basic/IdracCreate')
      },
      {
        path: 'idrac/:id/Detail',
        name: 'IdracDetail',
        meta: {
          index: '/Home/Idrac',
          title: '物理服務器詳細',
          type: 'page',
          active: false
        },
        component: () => import('./views/Basic/IdracDetail')
      },
      {
        path: 'NetDevice',
        name: 'NetDevice',
        meta: {
          index: '/Home/NetDevice',
          title: '網路設備',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Basic/NetDevice')
      },
      {
        path: 'NetDevice/Create',
        name: 'NetDeviceCreate',
        meta: {
          index: '/Home/NetDevice',
          title: '新增網路設備',
          type: 'page',
          active: false
        },
        component: () => import('./views/Basic/NetDeviceCreate')
      },
      {
        path: 'NetDevice/:id',
        name: 'NetDeviceUpdate',
        meta: {
          index: '/Home/NetDevice',
          title: '更新網路設備',
          type: 'page',
          active: false
        },
        component: () => import('./views/Basic/NetDeviceUpdate')
      },
      {
        path: 'Storage',
        name: 'Storage',
        meta: {
          index: '/Home/Storage',
          title: '存儲設備列表',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Basic/Storage')
      },
      {
        path: 'StorageDetail/:id',
        name: 'StorageDetail',
        meta: {
          index: '/Home/Storage',
          title: '存儲設備詳細',
          type: 'page',
          active: false
        },
        component: () => import('./views/Basic/StorageDetail')
      },
      {
        path: 'Tag',
        name: 'Tag',
        meta: {
          index: '/Home/Tag',
          title: '標籤列表',
          type: 'page',
          active: false
        },
        component: () => import('./views/Basic/Tag')
      },
      {
        path: 'Tag/Create',
        name: 'TagCreate',
        meta: {
          index: '/Home/Tag',
          title: '新增標籤',
          type: 'page',
          active: false
        },
        component: () => import('./views/Basic/TagCreate')
      },
      {
        path: 'Tag/:id',
        name: 'TagUpdate',
        meta: {
          index: '/Home/Tag',
          title: '更新標籤',
          type: 'page',
          active: false
        },
        component: () => import('./views/Basic/TagUpdate')
      },
      {
        path: 'Host',
        name: 'Host',
        meta: {
          index: '/Home/Host',
          title: '虛擬機',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Bus/Host')
      },
      {
        path: 'HostDetail/:id',
        name: 'HostDetail',
        meta: {
          index: '/Home/Host',
          title: '虛擬機詳細',
          type: 'page',
          active: false
        },
        component: () => import('./views/Bus/HostDetail')
      },
      {
        path: 'BusUnit',
        name: 'BusUnit',
        meta: {
          index: '/Home/BusUnit',
          title: '業務線 / 分支',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Bus/BusUnit')
      },
      {
        path: 'Category',
        name: 'Category',
        meta: {
          index: '/Home/Category',
          title: '分類 / 術語',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Bus/Category')
      },
      {
        path: 'Instance',
        name: 'Instance',
        meta: {
          index: '/Home/Instance',
          title: 'Instance',
          type: 'menu',
          active: false
        },
        component: () => import('./views/VM/Instance')
      },
      {
        path: 'Cluster',
        name: 'Cluster',
        meta: {
          index: '/Home/Cluster',
          title: 'Cluster',
          type: 'menu',
          active: false
        },
        component: () => import('./views/VM/Cluster')
      },
      {
        path: 'Cluster/:id',
        name: 'ClusterDetail',
        meta: {
          index: '/Home/Cluster',
          title: 'Cluster詳細',
          type: 'page',
          active: false
        },
        component: () => import('./views/VM/ClusterDetail')
      },
      {
        path: 'PHost',
        name: 'PHost',
        meta: {
          index: '/Home/PHost',
          title: 'PHost',
          type: 'menu',
          active: false
        },
        component: () => import('./views/VM/PHost')
      },
      {
        path: 'PHost/:id',
        name: 'PHostDetail',
        meta: {
          index: '/Home/PHost',
          title: 'PHost詳細',
          type: 'page',
          active: false
        },
        component: () => import('./views/VM/PHostDetail')
      },
      {
        path: 'Instance/Create',
        name: 'InsCreate',
        meta: {
          index: '/Home/Instance',
          title: '新增Instance',
          type: 'page',
          active: false
        },
        component: () => import('./views/VM/InsCreate')
      },
      {
        path: 'IDC',
        name: 'IDC',
        meta: {
          index: '/Home/IDC',
          title: 'IDC',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Idc/idc')
      },
      {
        path: 'IDC/Create',
        name: 'IDCCreate',
        meta: {
          index: '/Home/IDC',
          title: '新增IDC',
          type: 'page',
          active: false
        },
        component: () => import('./views/Idc/idcCreate')
      },
      {
        path: 'IDC/:id',
        name: 'IDCUpdate',
        meta: {
          index: '/Home/IDC',
          title: '更新標籤',
          type: 'page',
          active: false
        },
        component: () => import('./views/Idc/idcUpdate')
      },
      {
        path: 'Rack',
        name: 'Rack',
        meta: {
          index: '/Home/Rack',
          title: 'Rack',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Idc/rack')
      },
      {
        path: 'Rack/Create',
        name: 'RackCreate',
        meta: {
          index: '/Home/Rack',
          title: '新增機櫃',
          type: 'page',
          active: false
        },
        component: () => import('./views/Idc/rackCreate')
      },
      {
        path: 'Rack/:id',
        name: 'RackUpdate',
        meta: {
          index: '/Home/Rack',
          title: '更新機櫃',
          type: 'page',
          active: false
        },
        component: () => import('./views/Idc/rackUpdate')
      },
      {
        path: 'RackUnit/:id',
        name: 'RackUnit',
        meta: {
          index: '/Home/RackUnit',
          title: '機櫃使用表',
          type: 'page',
          active: false
        },
        component: () => import('./views/Idc/rackunit')
      },
      {
        path: 'ISP',
        name: 'ISP',
        meta: {
          index: '/Home/ISP',
          title: 'ISP',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Idc/isp')
      },
      {
        path: 'ISP/:id',
        name: 'ISPUpdate',
        meta: {
          index: '/Home/ISP',
          title: '更新ISP',
          type: 'page',
          active: false
        },
        component: () => import('./views/Idc/ispUpdate')
      },
      {
        path: 'pt',
        name: 'pt',
        meta: {
          index: '/Home/pt',
          title: '任務列表',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Task/pt')
      },
      {
        path: 'pt/:id',
        name: 'PtDetail',
        meta: {
          index: '/Home/pt',
          title: 'Pt詳細',
          type: 'page',
          active: false
        },
        component: () => import('./views/Task/PtDetail')
      },
      {
        path: 'LoginLog',
        name: 'LoginLog',
        meta: {
          index: '/Home/LoginLog',
          title: '登入歷史',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Audit/loginlog')
      },
      {
        path: 'Setting/',
        name: 'Setting',
        meta: {
          index: '/Home/Setting',
          title: 'Setting',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Setting')
      },
      {
        path: 'Users/',
        name: 'Users',
        meta: {
          index: '/Home/Users',
          title: '帳戶與用戶管理',
          type: 'menu',
          active: false
        },
        component: () => import('./views/Users')
      },
      {
        path: 'UserRoles/',
        name: 'UserRoles',
        meta: {
          index: '/Home/UserRoles',
          title: '用戶角色分配',
          type: 'menu',
          active: false
        },
        component: () => import('./views/UserRoles')
      },
      {
        path: 'RolePermissions/',
        name: 'RolePermissions',
        meta: {
          index: '/Home/RolePermissions',
          title: '角色權限分配',
          type: 'menu',
          active: false
        },
        component: () => import('./views/RolePermissions')
      }
    ]
  },
  {
    name: '404',
    path: '/404',
    component: () => import('./views/notFound.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes: constantRoutes
})

const whiteList = ['/login', '/404']

// Helper to parse cookie value
function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
  return match ? match[2] : null
}

// Helper to parse JSON from cookie
function parseCookieJson(name) {
  try {
    const value = getCookie(name)
    return value ? JSON.parse(value) : []
  } catch {
    return []
  }
}

router.beforeEach((to, from, next) => {
  const hasToken = getTokenFromCookie()

  if (hasToken) {
    if (to.path === '/login' || to.path === '/') {
      next({ path: '/Home' })
    } else {
      // 路由角色權限阻擋 (針對系統設置頁面)
      if (to.path === '/Home/Setting' || to.path === '/Home/Setting/') {
        const roles = parseCookieJson('x_user_roles')
        if (!roles.includes('admin')) {
          ElMessage.error('權限不足，無法存取該頁面！')
          next({ path: '/Home' })
          return
        }
      }

      // 路由動作權限阻擋 (針對資產分配頁面)
      if (to.name === 'AssetUpdate') {
        const actions = parseCookieJson('x_user_actions')
        const roles = parseCookieJson('x_user_roles')
        if (!actions.includes('asset:assign') && !roles.includes('admin')) {
          ElMessage.error('權限不足，無法進行資產分配！')
          next({ path: '/Home' })
          return
        }
      }

      next()
    }
  } else {
    /* has no token*/
    if (whiteList.includes(to.path)) {
      next()
    } else {
      next('/login')
    }
  }
})

export function resetRouter() {
  const newRouter = createRouter({
    history: createWebHistory(),
    routes: constantRoutes
  })
  router.matcher = newRouter.matcher
}

export default router
