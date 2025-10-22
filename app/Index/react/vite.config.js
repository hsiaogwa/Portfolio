// vite.config.js
import { defineConfig } from 'vite'

export default defineConfig({
  // 根目錄 (可選，默認為當前目錄)
  root: '.', 

  // 輸出目錄
  build: {
    outDir: 'dist',           // 構建輸出到 dist/
    minify: true,             // 啟用最小化 (Terser)
    sourcemap: false,         // 生產環境關閉 sourcemap (防止洩露原始碼)
  },

  // 開發伺服器配置 (可選)
  server: {
    port: 3000,
    open: true,
  }
})