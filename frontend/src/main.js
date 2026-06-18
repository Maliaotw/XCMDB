import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'normalize.css'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import service from '@/utils/request'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

import '@/styles/index.scss' // global css

const app = createApp(App)

// Register axios on app instance
app.config.globalProperties.$axios = service

app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn })

// Global permission directive
app.directive('permission', {
  mounted(el, binding) {
    const { value } = binding
    let roles = []
    let actions = []
    
    try {
      roles = JSON.parse(document.cookie.split('x_user_roles=')[1]?.split(';')[0] || '[]')
      actions = JSON.parse(document.cookie.split('x_user_actions=')[1]?.split(';')[0] || '[]')
    } catch (e) {
      roles = []
      actions = []
    }

    // 管理員 (admin) 擁有全部權限，直接放行
    if (roles.includes('admin')) {
      return
    }

    if (typeof value === 'string') {
      // 如果是字串，代表是動作權限識別碼
      const hasAction = actions.includes(value)
      if (!hasAction) {
        el.parentNode && el.parentNode.removeChild(el)
      }
    } else if (value && Array.isArray(value) && value.length > 0) {
      // 如果是陣列，相容舊的的角色匹配
      const hasPermission = roles.some(role => value.includes(role))
      if (!hasPermission) {
        el.parentNode && el.parentNode.removeChild(el)
      }
    } else {
      throw new Error(`need string or array! Like v-permission="'asset:delete'" or v-permission="['admin', 'operator']"`)
    }
  }
})

app.mount('#app')

export default app
