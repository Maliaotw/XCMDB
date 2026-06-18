<template>
  <div class="not-found-container">
    <div class="content-wrapper">
      <!-- 科技資產風 SVG 插圖 -->
      <div class="illustration">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" class="svg-img">
          <!-- 背景裝飾圈圈 -->
          <circle cx="400" cy="300" r="180" fill="#f0f5ff" />
          <circle cx="400" cy="300" r="140" fill="none" stroke="#e6f0ff" stroke-width="4" stroke-dasharray="8 8" />
          
          <!-- 服務器機架 -->
          <rect x="290" y="220" width="220" height="180" rx="12" fill="#fff" stroke="#409eff" stroke-width="6" />
          
          <!-- 服務器層板 1 -->
          <rect x="310" y="250" width="180" height="24" rx="4" fill="#f5f7fa" stroke="#dcdfe6" stroke-width="3" />
          <circle cx="330" cy="262" r="4" fill="#67c23a" />
          <circle cx="345" cy="262" r="4" fill="#909399" />
          <line x1="370" y1="262" x2="470" y2="262" stroke="#dcdfe6" stroke-width="4" stroke-linecap="round" />

          <!-- 服務器層板 2 (警報燈) -->
          <rect x="310" y="290" width="180" height="24" rx="4" fill="#f5f7fa" stroke="#409eff" stroke-width="3" />
          <circle cx="330" cy="302" r="4" fill="#f56c6c" class="pulse-red" />
          <circle cx="345" cy="302" r="4" fill="#409eff" />
          <line x1="370" y1="302" x2="450" y2="302" stroke="#409eff" stroke-width="4" stroke-linecap="round" />

          <!-- 服務器層板 3 -->
          <rect x="310" y="330" width="180" height="24" rx="4" fill="#f5f7fa" stroke="#dcdfe6" stroke-width="3" />
          <circle cx="330" cy="342" r="4" fill="#e6a23c" />
          <circle cx="345" cy="342" r="4" fill="#909399" />
          <line x1="370" y1="342" x2="460" y2="342" stroke="#dcdfe6" stroke-width="4" stroke-linecap="round" />

          <!-- 底座 -->
          <path d="M 350 400 L 320 440 L 480 440 L 450 400 Z" fill="#e6f0ff" stroke="#409eff" stroke-width="6" stroke-linejoin="round" />
          <line x1="300" y1="440" x2="500" y2="440" stroke="#409eff" stroke-width="6" stroke-linecap="round" />
          
          <!-- 漂浮的小雲朵/網絡節點裝飾 -->
          <g class="float-element-1">
            <circle cx="240" cy="180" r="15" fill="#e6f0ff" />
            <circle cx="260" cy="180" r="20" fill="#e6f0ff" />
            <circle cx="280" cy="180" r="15" fill="#e6f0ff" />
            <rect x="240" y="180" width="40" height="15" fill="#e6f0ff" />
          </g>
          
          <g class="float-element-2">
            <circle cx="530" cy="200" r="3" fill="#409eff" />
            <circle cx="560" cy="180" r="6" fill="#ffd04b" />
            <circle cx="580" cy="230" r="4" fill="#67c23a" />
          </g>

          <!-- 404 大字 -->
          <text x="400" y="150" font-size="90" font-weight="900" fill="#303133" text-anchor="middle" font-family="Arial, sans-serif" letter-spacing="2">404</text>
        </svg>
      </div>

      <!-- 錯誤文字提示 -->
      <h2 class="title">抱歉，您訪問的資產頁面不存在</h2>
      <p class="description">
        可能該設備已被移除、下架，或者您輸入的 URL 網址有誤。
      </p>

      <!-- 操作按鈕 -->
      <div class="actions">
        <el-button type="primary" class="btn-home" @click="goHome">
          返回首頁
        </el-button>
        <el-button class="btn-prev" @click="goBack">
          返回上一步
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "notFound",
  methods: {
    goHome() {
      this.$router.push({ name: 'Home' });
    },
    goBack() {
      this.$router.go(-1);
    }
  }
}
</script>

<style scoped>
.not-found-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  padding: 20px;
}

.content-wrapper {
  max-width: 550px;
  width: 100%;
  background: #ffffff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  text-align: center;
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.illustration {
  width: 100%;
  max-width: 320px;
  margin: 0 auto 20px;
}

.svg-img {
  width: 100%;
  height: auto;
}

.title {
  font-size: 22px;
  color: #303133;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 12px;
}

.description {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-top: 0;
  margin-bottom: 30px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.btn-home {
  background-color: #409eff !important;
  border-color: #409eff !important;
  color: #ffffff !important;
  font-weight: 500;
  padding: 10px 24px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.btn-home:hover {
  background-color: #66b1ff !important;
  border-color: #66b1ff !important;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(64, 159, 255, 0.3);
}

.btn-prev {
  background-color: #ffffff !important;
  border: 1px solid #dcdfe6 !important;
  color: #606266 !important;
  font-weight: 500;
  padding: 10px 24px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.btn-prev:hover {
  color: #409eff !important;
  border-color: #c6e2ff !important;
  background-color: #ecf5ff !important;
  transform: translateY(-1px);
}

/* 輕微動畫 */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 紅燈閃爍 */
.pulse-red {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { fill: #f56c6c; opacity: 1; }
  50% { fill: #ff9f9f; opacity: 0.4; }
  100% { fill: #f56c6c; opacity: 1; }
}

/* 漂浮雲朵 */
.float-element-1 {
  animation: float1 6s ease-in-out infinite;
}

@keyframes float1 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(-10px, -5px); }
}

/* 漂浮點綴點 */
.float-element-2 {
  animation: float2 5s ease-in-out infinite;
}

@keyframes float2 {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(5px, -10px); }
}
</style>