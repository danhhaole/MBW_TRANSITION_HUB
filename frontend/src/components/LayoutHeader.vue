<template>
  <template v-if="useTeleport">
    <Teleport :to="target" v-if="showHeader">
      <slot>
        <header class="flex h-10.5 items-center justify-between py-[7px] sm:pl-5 pl-2">
          <div class="flex items-center gap-2">
            <slot name="left-header" />
          </div>
          <div class="flex items-center gap-2">
            <slot name="right-header" class="flex items-center gap-2" />
          </div>
        </header>
      </slot>
    </Teleport>
  </template>
  <template v-else>
    <div :class="sticky ? stickyClasses : ''">
      <slot>
        <header class="flex h-10.5 items-center justify-between py-[7px] sm:pl-5 pl-2">
          <div class="flex items-center gap-2">
            <slot name="left-header" />
          </div>
          <div class="flex items-center gap-2">
            <slot name="right-header" class="flex items-center gap-2" />
          </div>
        </header>
      </slot>
    </div>
  </template>
</template>
<script setup>
import { ref, nextTick } from 'vue'

const props = defineProps({
  useTeleport: { type: Boolean, default: true },
  target: { type: String, default: '#app-header' },
  sticky: { type: Boolean, default: false },
  stickyClasses: {
    type: String,
    default: 'sticky top-0 z-50 bg-white/80 backdrop-blur border-b',
  },
})

const showHeader = ref(false)

nextTick(() => {
  showHeader.value = true
})
</script>
