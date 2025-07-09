<template>
  <div
    class="grid h-full place-items-center px-4 py-20 text-center text-lg text-ink-gray-5"
  >
    <div class="space-y-2">
      <div>Invalid page or not permitted to access</div>
      <Button :route="{ name: 'Dashboard' }">
        <template #prefix><LeadsIcon class="w-4" /></template>
        Dashboard
      </Button>
    </div>
  </div>
</template>

<script setup>
import LeadsIcon from '@/components/Icons/LeadsIcon.vue'
</script>
