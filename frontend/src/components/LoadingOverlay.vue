<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-200"
      leave-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <div
        v-if="show"
        class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center"
        :class="customClass"
      >
        <div class="bg-white rounded-lg p-6 shadow-xl max-w-sm">
          <div class="flex flex-col items-center space-y-4">
            <!-- Loading Spinner -->
            <FeatherIcon
              :name="icon"
              class="w-12 h-12 animate-spin"
              :class="iconClass"
            />
            
            <!-- Title -->
            <p class="text-gray-700 font-medium text-center">
              {{ title || __('Processing...') }}
            </p>
            
            <!-- Description -->
            <p v-if="description" class="text-sm text-gray-500 text-center">
              {{ description }}
            </p>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { FeatherIcon } from 'frappe-ui'

// Props
defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: 'Please wait, do not close this page'
  },
  icon: {
    type: String,
    default: 'loader'
  },
  iconClass: {
    type: String,
    default: 'text-blue-500'
  },
  customClass: {
    type: String,
    default: ''
  }
})
</script>
