import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
//@ts-ignore
import path from "path";

//@ts-ignore
const src = path.resolve(__dirname, "src");

// https://vite.dev/config/
export default defineConfig(() => {
  return {
    resolve: {
      alias: {
        "@": src
      }
    },
    envDir: path.resolve(__dirname, '../'),
    build: {
      rollupOptions: {
        input: {
          main: './index.html',
          notfound: './public/404.html'
        }
      }
    },
    plugins: [react()],
  }
})
