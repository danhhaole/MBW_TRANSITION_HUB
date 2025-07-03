import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default createVuetify({
    components,
    directives,
    icons: {
        defaultSet: 'mdi'
    },
    theme: {
        defaultTheme: 'light',
        themes: {
            light: {
                colors: {
                    primary: '#4f46e5',
                    secondary: '#64748b',
                    accent: '#6366f1',
                    error: '#dc2626',
                    info: '#0ea5e9',
                    success: '#16a34a',
                    warning: '#d97706',
                    surface: '#ffffff',
                    background: '#f8fafc',
                    'on-surface': '#0f172a',
                    'on-background': '#334155',
                    'surface-variant': '#f1f5f9',
                    'on-surface-variant': '#64748b',
                }
            },
            dark: {
                colors: {
                    primary: '#6366f1',
                    secondary: '#64748b',
                    accent: '#818cf8',
                    error: '#f87171',
                    info: '#38bdf8',
                    success: '#4ade80',
                    warning: '#fbbf24',
                    surface: '#1e293b',
                    background: '#0f172a',
                    'on-surface': '#f8fafc',
                    'on-background': '#cbd5e1',
                    'surface-variant': '#334155',
                    'on-surface-variant': '#94a3b8',
                }
            }
        }
    },
    defaults: {
        VBtn: { 
            elevation: 1, 
            variant: 'flat',
            style: 'text-transform: none;'
        },
        VCard: {
            elevation: 1,
            rounded: 'lg'
        },
        VChip: {
            rounded: 'lg'
        },
        VTextField: {
            variant: 'outlined',
            density: 'comfortable'
        },
        VTextarea: {
            variant: 'outlined',
            density: 'comfortable'
        },
        VSelect: {
            variant: 'outlined',
            density: 'comfortable'
        },
        VAutocomplete: {
            variant: 'outlined',
            density: 'comfortable'
        }
    }
})
