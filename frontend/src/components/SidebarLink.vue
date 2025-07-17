<template>
  <button
    class="
      flex items-center rounded transition-colors duration-200
      focus:outline-none focus-visible:ring-2 ring-offset-1
    "
    :class="[
      isActive
        ? 'bg-gray-100 text-gray-900 font-semibold'
        : 'hover:bg-gray-100 text-gray-600',
      'px-2 py-1.5'
    ]"
    @click="handleClick"
  >
    <div class="flex items-center justify-between overflow-hidden">
      <div class="flex items-center overflow-hidden">
        <!-- Icon -->
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

        <!-- Label -->
        <Tooltip
          :text="label"
          placement="right"
          :disabled="isCollapsed"
          :hoverDelay="1.5"
        >
          <span
            class="
              ml-3 truncate whitespace-nowrap
              text-sm font-medium leading-4
              transition-all duration-300 ease-in-out overflow-hidden
            "
            :class="
              isCollapsed
                ? 'max-w-0 opacity-0'
                : 'max-w-[160px] opacity-100'
            "
          >
            {{ label }}
          </span>
        </Tooltip>
      </div>

      <slot name="right" v-if="!isCollapsed" />
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
