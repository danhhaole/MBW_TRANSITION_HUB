import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
//import { initSocket } from './socket'
import router from './router'
// import translationPlugin from './translation'
//import { posthogPlugin } from './telemetry'
import App from './App.vue'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
// Vuetify theme (tuỳ chọn)
const vuetify = createVuetify({
  components,
  directives,
})
import {
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
app.use(pinia)
app.use(router)
app.use(vuetify)
// app.use(translationPlugin)
//app.use(posthogPlugin)


for (let key in globalComponents) {
    app.component(key, globalComponents[key])
  }
app.mount('#app')
