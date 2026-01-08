import './index.css'

// Vue Flow styles
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import '@vue-flow/controls/dist/style.css'
import '@vue-flow/minimap/dist/style.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createDialog } from './utils/dialogs'
import { initSocket } from './socket'
import router from './router'
import translationPlugin from './translation'
import { posthogPlugin } from './telemetry'
import { usersStore } from './stores/user'
import { usePermissionStore } from './stores/permission'
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
// app.use(FrappeUI)
app.use(pinia)
app.use(router)
app.use(translationPlugin)
app.use(posthogPlugin)
for (let key in globalComponents) {
  app.component(key, globalComponents[key])
}

app.config.globalProperties.$dialog = createDialog

async function bootstrap() {
  const { userResource, allUsers, getUser } = usersStore()
  const permissionStore = usePermissionStore()

  try {
    // Đảm bảo đã load user data
    await getUser.promise
    
    // Kiểm tra xem getUser.data có tồn tại và có roles không
    if (getUser.data && getUser.data.roles) {
      await permissionStore.loadFeatures()
    } else {
      
    }
  } catch (error) {
    console.error('Error loading user data:', error)
    // Khởi tạo với quyền truy cập trống nếu có lỗi
  }

  app.provide('$user', userResource)
  app.provide('$allUsers', allUsers)
  app.config.globalProperties.$user = userResource

  let socket
  if (import.meta.env.DEV) {
    try {
      const values = await frappeRequest({
        url: '/api/method/mbw_transition_hub.www.mbw_transition_hub.get_context_for_dev',
      })
      for (let key in values) {
        window[key] = values[key]
      }
    } catch (err) {
      console.error('Error loading dev context:', err)
    }
    
    socket = initSocket()
    app.config.globalProperties.$socket = socket
    window.$dialog = createDialog
  } else {
    socket = initSocket()
    app.config.globalProperties.$socket = socket
  }

  app.mount('#app')
}

bootstrap()
