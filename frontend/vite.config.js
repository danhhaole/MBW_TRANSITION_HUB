import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import vueJsx from '@vitejs/plugin-vue-jsx'
import frappeui from 'frappe-ui/vite'
import { VitePWA } from 'vite-plugin-pwa'
import { fileURLToPath } from "url";

// ESM-safe __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// https://vitejs.dev/config/
export default defineConfig({
	base: '/mbw_mira/',
	plugins: [
		frappeui({
			frappeProxy: true,
			lucideIcons: true,
			jinjaBootData: true,
			buildConfig: {
				indexHtmlPath: '../mbw_mira/www/mbw_mira.html',
				outDir: '../mbw_mira/public/frontend',
				emptyOutDir: true,
				sourcemap: true,
			},
		}),
		vueJsx(),
		vue(),
		VitePWA({
			registerType: 'autoUpdate',
			devOptions: { enabled: false },
			manifest: {
				display: 'standalone',
				name: 'MBW Mira',
				short_name: 'MBW Mira',
				start_url: '/mbw_mira',
				description: 'MBW Mira .',
				icons: [],
			},
			workbox: {
				globIgnores: ['assets/index-*.css', 'assets/index-*.js'],
			},
		}),
	],
	server: {
		host: true,
		allowedHosts: ['localhost', '127.0.0.1', 'mira.local', '172.30.57.120'],
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src'),
		},
	},
	optimizeDeps: {
		include: [
			'frappe-ui > feather-icons',
			'showdown',
			'engine.io-client',
			'tailwind.config.js',
			'prosemirror-state',
			'prosemirror-view',
			'lowlight',
			'highlight.js',
			'grapesjs',
      'grapesjs-preset-webpage',
      'grapesjs-plugin-export',
      'grapesjs-navbar',
      'grapesjs-plugin-forms',
		],
		esbuildOptions: {
			format: 'esm',
			mainFields: ['module', 'main'],
			resolveExtensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json'],
		},
	}
})
