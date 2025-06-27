<template>
  <FrappeUIProvider>
    <Layout >
      <router-view />
    </Layout>
  </FrappeUIProvider>
</template>


<script setup>
import { FrappeUIProvider, setConfig } from 'frappe-ui'
setConfig('systemTimezone', window.timezone?.system || null)
setConfig('localTimezone', window.timezone?.user || null)
</script>