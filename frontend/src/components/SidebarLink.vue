<template>
  <button
  class="
    flex items-center rounded transition-colors duration-200 focus:outline-none focus-visible:ring-2 ring-offset-1
  "
  :class="[
    isActive
      ? 'bg-primary-50 text-primary-700 font-semibold'
      : 'hover:bg-gray-100 text-gray-600',
    isCollapsed ? 'justify-center h-10' : 'px-3 py-1.5',
  ]"
  @click="handleClick"
>
  <div class="flex w-full items-center justify-between ">
    <div class="flex items-center ">
      <Tooltip :text="label" placement="right" :disabled="!isCollapsed">
        <slot name="icon">
          <span class="grid place-items-center flex-shrink-0">
            <FeatherIcon
              v-if="typeof icon === 'string'"
              :name="icon"
              class="w-4 h-4 text-gray-500"
            />
            <component
              v-else
              :is="icon"
              class="w-4 h-4 text-gray-500"
            />
          </span>
        </slot>
      </Tooltip>

      <Tooltip
        :text="label"
        placement="right"
        :disabled="isCollapsed"
        :hoverDelay="1.5"
      >
        <span
          class="
            ml-3 flex-1 truncate  whitespace-nowrap
            text-sm font-medium leading-4 duration-300 ease-in-out
          "
          :class="
            isCollapsed
              ? 'ml-0 w-0 opacity-0'
              : 'w-auto opacity-100'
          "
        >
          {{ label }}
        </span>
      </Tooltip>
    </div>

    <slot name="right" />
  </div>
</button>

</template>

<script setup>
import { Tooltip } from 'frappe-ui'
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { isMobileView, mobileSidebarOpened } from '@/composables/settings'

const router = useRouter()
const route = useRoute()

const props = defineProps({
  icon: {
    type: [Object, String, Function],
  },
  label: {
    type: String,
    default: '',
  },
  to: {
    type: [Object, String],
    default: '',
  },
  isCollapsed: {
    type: Boolean,
    default: false,
  },
})

function handleClick() {
  if (!props.to) return
  if (typeof props.to === 'object') {
    router.push(props.to)
  } else {
    router.push({ name: props.to })
  }
  if (isMobileView.value) {
    mobileSidebarOpened.value = false
  }
}

const isActive = computed(() => {
  if (!props.to) return false
  if (typeof props.to === 'object' && route.query.view) {
    return route.query.view == props.to?.query?.view
  }
  return route.name === props.to
})
</script>
