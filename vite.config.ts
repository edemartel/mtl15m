/// <reference types="vitest" />

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VueI18nPlugin({
      runtimeOnly: false,
      include: path.resolve(__dirname, "./src/locales/**"),
    })],
  test: {
    coverage: {
      provider: 'c8',
      reporter: 'lcov',
      include: ['test/*.spec.ts']
    }
  }
})
