import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
//import { initSocket } from './socket'
import router from './router'
// import translationPlugin from './translation'
//import { posthogPlugin } from './telemetry'
import App from './App.vue'

import {
    FrappeUI,
    Button,
    Input,
    TextInput,
    FormControl,
    ErrorMessage,
    Dialog,
    Alert,
    Badge,
    setConfig,
    frappeRequest,
    FeatherIcon,
  } from 'frappe-ui'


  let globalComponents = {
    Button,
    TextInput,
    Input,
    FormControl,
    ErrorMessage,
    Dialog,
    Alert,
    Badge,
    FeatherIcon,
  }

// create a pinia instance
let pinia = createPinia()
let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)
app.use(FrappeUI)
app.use(pinia)
app.use(router)
// app.use(translationPlugin)
//app.use(posthogPlugin)

for (let key in globalComponents) {
    app.component(key, globalComponents[key])
  }
app.mount('#app')
