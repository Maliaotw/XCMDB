<template>
  <div>
    <NavMenu />
    <div class="v3-main" :style="{ 'margin-left': isNavMenuOpen ? '200px' : '64px' }">
      <div class="v3-header">
        <Header />
      </div>
      <el-main class="v3-content-main">
        <transition name="fade-transform" mode="out-in">
          <router-view :key="route.path" />
        </transition>
      </el-main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import NavMenu from '../components/NavMenu'
import Header from '../components/Header'

const route = useRoute()
const userStore = useUserStore()

const isNavMenuOpen = computed(() => userStore.isNavMenuOpen)
</script>

<style scoped>
.v3-header {
  height: 40px;
  border-bottom: 1px solid #eee;
  background: #fff;
}

.v3-main {
  margin-left: 200px;
}

.v3-content-main {
  background: #fff;
  margin: 10px;
  font-size: 14px;
}

/* 路由過渡動畫 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.28s ease;
}

.fade-transform-enter {
  opacity: 0;
  transform: translateX(-20px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
