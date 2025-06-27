import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import vueJsx from '@vitejs/plugin-vue-jsx'
import frappeui from 'frappe-ui/vite'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [frappeui({
    frappeProxy: true,
    lucideIcons: true,
    jinjaBootData: true,
    buildConfig: {
      indexHtmlPath: '../mbw_mira/www/mbw_mira.html',
      outDir: "../mbw_mira/public/frontend",
      emptyOutDir: true,
      sourcemap: true,
    },
  }),
  vueJsx(), vue(), VitePWA({
    registerType: "autoUpdate",
    devOptions: { enabled: false },
    manifest: {
      display: "standalone",
      name: "MBW Mira",
      short_name: "MBW Mira",
      start_url: "/mbw_mira",
      description:
        "MBW Mira .",
      icons: [

      ],
    }
  })],
  server: {
    port: 8080
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  build: {
    outDir: "../mbw_mira/public/frontend",
    emptyOutDir: true,
    commonjsOptions: {
      include: [/tailwind.config.js/, /node_modules/],
    },
    sourcemap: true,
    rollupOptions: {
      output: {
        format: 'esm'
      }
    }
  },
  optimizeDeps: {
    include: ['frappe-ui > feather-icons', 'showdown', 'engine.io-client', 'tailwind.config.js',
      'prosemirror-state',
      'prosemirror-view',
      'lowlight', "highlight.js"],
    esbuildOptions: {
      format: 'esm',
      mainFields: ['module', 'main'],
      resolveExtensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json'],
    }
  },
})
