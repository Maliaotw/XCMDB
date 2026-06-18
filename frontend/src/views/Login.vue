<template>
  <div class="login-container">
    <!-- 科技拓撲背景 -->
    <div class="topology-bg">
      <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(64, 158, 255, 0.08)" stroke-width="1" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- 背景裝飾科技線條與節點 -->
        <g stroke="rgba(64, 158, 255, 0.15)" stroke-width="1.5" fill="none">
          <path d="M-100,200 Q200,100 500,400 T1100,200" />
          <path d="M100,500 Q400,200 800,600 T1400,400" />
        </g>
        <!-- 緩慢漂浮與閃爍的網絡節點 -->
        <circle cx="200" cy="150" r="5" fill="rgba(64, 158, 255, 0.6)" class="blink-node" />
        <circle cx="500" cy="400" r="6" fill="rgba(103, 194, 58, 0.6)" class="blink-node" style="animation-delay: 1.5s" />
        <circle cx="800" cy="250" r="5" fill="rgba(230, 162, 60, 0.6)" class="blink-node" style="animation-delay: 3s" />
      </svg>
    </div>

    <!-- 登入卡片容器 -->
    <div class="login-card-wrapper">
      <!-- 左側品牌宣傳區域 (大螢幕顯示) -->
      <div class="brand-panel">
        <div class="brand-header">
          <span class="brand-logo"><i class="el-icon-monitor" /></span>
          <span class="brand-name">XCMDB</span>
        </div>
        <div class="brand-content">
          <h3>智能 IT 資產與虛擬化自動部署</h3>
          <p>整合 VMware vSphere 與實體 Dell iDRAC 設備採集，實現高效、精準、自動化的資產生命週期管理。</p>
        </div>
        <div class="brand-footer">
          <span>Version 1.0.0</span>
        </div>
      </div>

      <!-- 右側登入表單區域 -->
      <div class="form-panel">
        <div class="form-header">
          <h2>歡迎登入</h2>
          <p>請輸入您的管理員帳號密碼</p>
        </div>

        <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="login">
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="請輸入郵箱或用戶名"
              prefix-icon="el-icon-user"
              clearable
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              placeholder="請輸入密碼"
              type="password"
              prefix-icon="el-icon-lock"
              show-password
            />
          </el-form-item>

          <!-- Demo 角色快速切換 -->
          <div class="demo-accounts-wrapper">
            <span class="demo-title">快速體驗 Demo 角色：</span>
            <div class="demo-buttons">
              <span class="demo-btn admin-btn" @click="quickFill('admin', 'admin')">管理員 (Admin)</span>
              <span class="demo-btn operator-btn" @click="quickFill('operator', 'operator')">運維員 (Operator)</span>
              <span class="demo-btn auditor-btn" @click="quickFill('auditor', 'auditor')">審計員 (Auditor)</span>
              <span class="demo-btn visitor-btn" @click="quickFill('visitor', 'visitor')">訪客 (Visitor)</span>
            </div>
          </div>

          <el-form-item class="submit-item">
            <el-button type="primary" class="btn-submit" :loading="loading" native-type="submit">
              立即登入
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)

const form = ref({
  username: 'admin',
  password: ''
})

const loading = ref(false)

const rules = {
  username: [{ required: true, message: '請輸入用戶名', trigger: 'blur' }],
  password: [{ required: true, message: '請輸入密碼', trigger: 'blur' }]
}

function reloadPage() {
  window.location.reload()
}

function quickFill(username, password) {
  form.value.username = username
  form.value.password = password
}

function login() {
  formRef.value.validate((valid) => {
    if (valid) {
      loading.value = true
      const payload = {
        username: form.value.username,
        password: form.value.password
      }

      userStore
        .login(payload)
        .then(() => {
          ElMessage.success('登入成功！')
          reloadPage()
        })
        .catch((error) => {
          loading.value = false
          const msg =
            error.response && error.response.data && error.response.data.non_field_errors
              ? error.response.data.non_field_errors[0]
              : '登入失敗，請檢查帳號密碼'
          ElMessage.error(msg)
        })
    }
  })
}

onMounted(() => {
  if (userStore.token !== '') {
    router.push({ name: 'Home' })
  }
})
</script>

<style scoped>
.login-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    sans-serif;
  padding: 20px;
}

/* 背景拓撲格線 */
.topology-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* 節點閃爍動畫 */
.blink-node {
  animation: blink 3s ease-in-out infinite;
}
@keyframes blink {
  0%,
  100% {
    opacity: 0.2;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.3);
  }
}

/* 登入主卡片 */
.login-card-wrapper {
  position: relative;
  z-index: 10;
  display: flex;
  width: 850px;
  min-height: 480px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.6);
  overflow: hidden;
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 左側品牌面板 */
.brand-panel {
  flex: 1.1;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: #ffffff;
  position: relative;
}

/* 加上裝飾性發光圓形 */
.brand-panel::before {
  content: '';
  position: absolute;
  top: -50px;
  left: -50px;
  width: 200px;
  height: 200px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.brand-header {
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 2;
}

.brand-logo {
  font-size: 24px;
}

.brand-name {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 1px;
}

.brand-content {
  z-index: 2;
}

.brand-content h3 {
  font-size: 22px;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 15px;
  line-height: 1.3;
}

.brand-content p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.85);
  line-height: 1.6;
  margin: 0;
}

.brand-footer {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  z-index: 2;
}

/* 右側表單面板 */
.form-panel {
  flex: 1;
  padding: 50px 45px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-header {
  margin-bottom: 35px;
}

.form-header h2 {
  font-size: 24px;
  color: #303133;
  margin-top: 0;
  margin-bottom: 8px;
  font-weight: 600;
}

.form-header p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

/* 修正 Element-UI 輸入框樣式 */
:deep(.el-input__inner) {
  height: 44px !important;
  line-height: 44px !important;
  border-radius: 6px !important;
  border-color: #dcdfe6 !important;
  transition: all 0.2s ease;
  font-size: 14px;
}

:deep(.el-input__inner:focus) {
  border-color: #409eff !important;
  box-shadow: 0 0 6px rgba(64, 158, 255, 0.2) !important;
}

:deep(.el-input__icon) {
  line-height: 44px !important;
  font-size: 16px;
}

.submit-item {
  margin-top: 30px;
  margin-bottom: 0;
}

.btn-submit {
  width: 100% !important;
  height: 44px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  border-radius: 6px !important;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(30, 60, 114, 0.3) !important;
  transition: all 0.2s ease !important;
  color: #ffffff !important;
}

.btn-submit:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(30, 60, 114, 0.5) !important;
}

.btn-submit:active {
  transform: translateY(1px);
}

/* 響應式處理 */
@media (max-width: 850px) {
  .login-card-wrapper {
    width: 420px;
    flex-direction: column;
  }
  .brand-panel {
    display: none;
  }
  .form-panel {
    padding: 40px 30px;
  }
}

/* Demo 帳號快速切換樣式 */
.demo-accounts-wrapper {
  margin-top: 15px;
  margin-bottom: 5px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.demo-title {
  font-size: 13px;
  color: #909399;
  font-weight: 500;
}

.demo-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.demo-btn {
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  user-select: none;
  font-weight: 500;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.admin-btn {
  background-color: rgba(245, 108, 108, 0.1);
  color: #f56c6c;
  border-color: rgba(245, 108, 108, 0.2);
}
.admin-btn:hover {
  background-color: #f56c6c;
  color: #ffffff;
}

.operator-btn {
  background-color: rgba(64, 158, 255, 0.1);
  color: #409eff;
  border-color: rgba(64, 158, 255, 0.2);
}
.operator-btn:hover {
  background-color: #409eff;
  color: #ffffff;
}

.auditor-btn {
  background-color: rgba(230, 162, 60, 0.1);
  color: #e6a23c;
  border-color: rgba(230, 162, 60, 0.2);
}
.auditor-btn:hover {
  background-color: #e6a23c;
  color: #ffffff;
}

.visitor-btn {
  background-color: rgba(144, 147, 153, 0.1);
  color: #909399;
  border-color: rgba(144, 147, 153, 0.2);
}
.visitor-btn:hover {
  background-color: #909399;
  color: #ffffff;
}
</style>
