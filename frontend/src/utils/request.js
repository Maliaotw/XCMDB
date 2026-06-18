import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import Cookies from 'js-cookie'
import { useUserStore } from '@/stores/user'
import { removeAuthCookies } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_API ?? '', // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 60 * 1000 // request timeout
})

function beforeRequestAddToken(config) {
  const userStore = useUserStore()
  const accessToken = Cookies.get('x_access_token')
  if (accessToken) {
    config.headers['Authorization'] = `Bearer ${accessToken}`
    config.headers['X-CSRFToken'] = accessToken
  } else if (userStore.token) {
    config.headers['X-CSRFToken'] = userStore.token
    config.headers['Authorization'] = `Token ${userStore.token}`
  }
  if (userStore.currentOrg) {
    config.headers['X-JMS-ORG'] = userStore.currentOrg.id
  }
}

function beforeRequestAddTimezone(config) {
  try {
    config.headers['X-TZ'] = Intl.DateTimeFormat().resolvedOptions().timeZone
  } catch (e) {
    console.log('Current browser not support Intl tools')
  }
}

// request interceptor
service.interceptors.request.use(
  config => {
    beforeRequestAddToken(config)
    return config
  },
  error => {
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

function ifUnauthorized({ response, error }) {
  if (response.status === 401) {
    response.config.disableFlashErrorMsg = true
    Cookies.set('x_auth_token', '', { expires: -1 })
    Cookies.set('username', '', { expires: -1 })
    ElMessageBox.confirm('帳號已退出，請重新登錄', '提示', {
      confirmButtonText: '重新登錄',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      window.location = '/'
    }).catch(() => {})
  }
}

function ifBadRequest({ response, error }) {
  if (response.status === 400) {
    error.message = '請求錯誤，請檢查填寫內容'
  }
}

export function flashErrorMsg({ response, error }) {
  if (!response.config.disableFlashErrorMsg) {
    let msg = error.message
    const data = response.data
    // 優先使用統一錯誤格式的 message
    if (data && data.success === false && data.message) {
      msg = data.message
    } else if (data && (data.error || data.msg)) {
      msg = data.error || data.msg
    }
    ElMessage({
      message: msg,
      type: 'error',
      duration: 5 * 1000
    })
  }
}

let isRefreshing = false
let requestsQueue = []

// response interceptor
service.interceptors.response.use(
  response => {
    const res = response

    if (response.config.raw === 1) {
      return response
    }
    return res
  },
  error => {
    if (!error.response) {
      ElMessage({
        message: '網路連線異常，請檢查網路狀態',
        type: 'error',
        duration: 5 * 1000
      })
      return Promise.reject(error)
    }

    const response = error.response

    // 檢查是否為 401 且是 token已過期，若是，啟動無感自動刷新機制
    if (response.status === 401 && response.data && response.data.detail === 'token已過期') {
      const config = response.config
      const refreshToken = Cookies.get('x_refresh_token')

      if (refreshToken) {
        if (!isRefreshing) {
          isRefreshing = true
          // 發起刷新 Token 請求
          return axios.post((import.meta.env.VITE_APP_BASE_API ?? '') + '/api/v1/api-token-auth/', {
            refresh_token: refreshToken
          }).then(res => {
            const newAccessToken = res.data.access_token
            Cookies.set('x_access_token', newAccessToken, { expires: 14 })

            isRefreshing = false

            // 重新執行等待佇列中的請求
            requestsQueue.forEach(cb => cb(newAccessToken))
            requestsQueue = []

            // 重新執行當前失敗的請求
            config.headers['Authorization'] = `Bearer ${newAccessToken}`
            config.headers['X-CSRFToken'] = newAccessToken
            return service(config)
          }).catch(err => {
            isRefreshing = false
            requestsQueue = []
            // 刷新失敗，登出
            removeAuthCookies()
            window.location = '/'
            return Promise.reject(err)
          })
        } else {
          // 正在刷新中，將其回傳 Promise 暫存於佇列，待刷新完成後調用
          return new Promise((resolve) => {
            requestsQueue.push((newAccessToken) => {
              config.headers['Authorization'] = `Bearer ${newAccessToken}`
              config.headers['X-CSRFToken'] = newAccessToken
              resolve(service(config))
            })
          })
        }
      }
    }

    ifUnauthorized({ response, error })
    ifBadRequest({ response, error })
    flashErrorMsg({ response, error })
    return Promise.reject(error)
  }
)

export default service
