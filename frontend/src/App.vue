<template>
  <FrappeUIProvider>
    <component :is="layoutComponent">
      <router-view />
    </component>
    <Dialogs />
    <ChangeLanguage />
  </FrappeUIProvider>
  <Toast />
</template>

<script setup>
import { Dialogs } from '@/utils/dialogs'
import { sessionStore as session } from '@/stores/session'
import { FrappeUIProvider, setConfig } from 'frappe-ui'
import { computed, defineAsyncComponent, onMounted } from 'vue'
import Toast from '@/components/ui/Toast.vue'
import ChangeLanguage from '@/components/Settings/ChangeLanguage.vue'

const MobileLayout = defineAsyncComponent(
  () => import('./components/Layouts/MobileLayout.vue'),
)
const DesktopLayout = defineAsyncComponent(
  () => import('./components/Layouts/DesktopLayout.vue'),
)
const PublicLayout = defineAsyncComponent(
  () => import('./components/Layouts/PublicLayout.vue'),
)

// Chọn layout component phù hợp
const layoutComponent = computed(() => {
  if (!session().isLoggedIn) return PublicLayout
  return window.innerWidth < 640 ? MobileLayout : DesktopLayout
})

// Thiết lập timezone
setConfig('systemTimezone', window.timezone?.system || null)
setConfig('localTimezone', window.timezone?.user || null)
</script>