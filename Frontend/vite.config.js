import {defineConfig, loadEnv} from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig(({mode}) => {
    const env = loadEnv(mode, process.cwd(), '')
    return {
        base: '/iter3/',
        plugins: [vue()],
        resolve: {
            alias: {
                '@': path.resolve(__dirname, './src'),
            },
        },
        define: {
            __PASSWORD_HASH__: JSON.stringify(env.VITE_PASSWORD_HASH || '')
        },
        server: {
            port: 8080,
            proxy: {
                '/api': {
                    target: 'http://localhost:3000',
                    changeOrigin: true,
                    secure: false,
                }
            }
        },
        build: {
            outDir: 'dist',
            assetsDir: 'assets',
            sourcemap: true,
        }
    }
})