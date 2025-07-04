<template>
  <component :is="layout" >
    <router-view />
  </component>
  
  <!-- Global Toast Container -->
  <ToastContainer />
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import { sessionStore as session } from '@/stores/session'
import PublicLayout from './layouts/PublicLayout.vue'
import PrivateLayout from './layouts/PrivateLayout.vue'
import ToastContainer from '@/components/shared/ToastContainer.vue'

const route = useRoute()

const layout = computed(() => {
  const layoutType = route.meta.layout
  return layoutType === 'private' && session().isLoggedIn ? PrivateLayout : PublicLayout
})
</script>
