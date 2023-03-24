/// <reference types="vitest" />

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  test: {
    coverage: {
      provider: 'c8',
      reporter: 'lcov',
      include: ['test/*.spec.ts']
    }
  }
})
