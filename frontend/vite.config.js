import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const port = env.VITE_PORT || 19528

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    server: {
      port: parseInt(port),
      host: '0.0.0.0',
      open: false,
      proxy: {
        '/api/': {
          target: env.VUE_APP_CORE_HOST || 'http://127.0.0.1:18000',
          changeOrigin: true
        },
        '/ws/': {
          target: 'ws://127.0.0.1:8082',
          changeOrigin: true,
          ws: true
        },
        '^/(core|static|media)/': {
          target: env.VUE_APP_CORE_HOST || 'http://127.0.0.1:18000',
          changeOrigin: true
        }
      }
    },
    build: {
      outDir: 'lina',
      assetsDir: 'assets',
      sourcemap: false,
      chunkSizeWarningLimit: 1500
    },
    css: {
      preprocessorOptions: {
        scss: {
          // Add global SCSS variables if needed
        }
      }
    }
  }
})
