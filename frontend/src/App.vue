<template>
  <FrappeUIProvider>
      <router-view />
  </FrappeUIProvider>
</template>


<script setup>
import { FrappeUIProvider, setConfig } from 'frappe-ui'
setConfig('systemTimezone', window.timezone?.system || null)
setConfig('localTimezone', window.timezone?.user || null)
</script>