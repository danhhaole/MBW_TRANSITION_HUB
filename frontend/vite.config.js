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
	base: '/mbw_transition_hub',
	plugins: [
		frappeui({
			frappeProxy: true,
			lucideIcons: true,
			jinjaBootData: true,
			buildConfig: {
				indexHtmlPath: '../mbw_transition_hub/www/mbw_transition_hub.html',
				outDir: '../mbw_transition_hub/public/frontend',
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
				name: 'Transition Hub',
				short_name: 'Transition Hub',
				start_url: '/mbw_transition_hub',
				description: 'Transition Hub .',
				icons: [],
			},
			workbox: {
				globIgnores: ['assets/index-*.css', 'assets/index-*.js'],
			},
		}),
	],
	server: {
		host: true,
		allowedHosts: ['localhost', '127.0.0.1', 'hrm.local', '172.30.57.120','russia-reduction-absolute-carriers.trycloudflare.com'],
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
