import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// Vite 配置：开发服务器 + 前后端联调代理
export default defineConfig({
  plugins: [vue()],
  build: {
    // Element Plus / ECharts 全量引入体积较大，提高警告阈值（按需引入留作后续优化）
    chunkSizeWarningLimit: 1200,
    rollupOptions: {
      output: {
        // 把大依赖拆成独立 chunk，减小主包体积、提升加载速度
        manualChunks: {
          vue: ["vue", "vue-router"],
          element: ["element-plus", "@element-plus/icons-vue"],
          echarts: ["echarts"],
        },
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      // 所有 /api 开头的请求转发到 FastAPI 后端（8000）
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
