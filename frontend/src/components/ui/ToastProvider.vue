<template>
  <div>
    <!-- Main content slot -->
    <slot />
    
    <!-- Toast container -->
    <Teleport to="body">
      <Toast />
    </Teleport>
  </div>
</template>

<script setup>
import Toast from './Toast.vue'
</script>
