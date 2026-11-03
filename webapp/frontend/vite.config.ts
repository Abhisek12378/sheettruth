import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The production build lands in app/static, which the FastAPI server serves at "/".
// During development the API calls are proxied to a locally running server.
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../backend/static',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
