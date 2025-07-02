import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
//import { initSocket } from './socket'
import router from './router'
// import translationPlugin from './translation'
//import { posthogPlugin } from './telemetry'
import App from './App.vue'

// Vuetify
import vuetify from './plugins/vuetify'
// Vuetify theme (tuỳ chọn)


import {
    setConfig,
    frappeRequest,
  } from 'frappe-ui'

// create a pinia instance
let pinia = createPinia()
let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)
app.use(pinia)
app.use(router)
app.use(vuetify)
// app.use(translationPlugin)
//app.use(posthogPlugin)

app.mount('#app')
