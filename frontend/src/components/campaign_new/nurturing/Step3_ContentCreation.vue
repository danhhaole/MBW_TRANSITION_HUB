<template>
  <div class="space-y-6 animate-fadeIn">
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900">
          {{ __('Create Nurturing Content') }}
        </h3>
        <Badge theme="green" variant="subtle">
          {{ selectedChannel || __('No Channel') }}
        </Badge>
      </div>

      <p class="text-gray-600 mb-6">
        {{ __('Create personalized content to build and maintain relationships with your audience.') }}
      </p>

      <!-- Nurturing Strategy -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-3">
          {{ __('Nurturing Strategy') }}
        </label>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            class="border-2 rounded-lg p-4 cursor-pointer transition-all"
            :class="strategy === 'single_touch' ? 'border-green-500 bg-green-50' : 'border-gray-200 hover:border-gray-300'"
            @click="strategy = 'single_touch'"
          >
            <FeatherIcon 
              name="send" 
              class="h-6 w-6 mb-2"
              :class="strategy === 'single_touch' ? 'text-green-600' : 'text-gray-400'"
            />
            <h4 class="text-sm font-semibold text-gray-900">
              {{ __('Single Touch') }}
            </h4>
            <p class="text-xs text-gray-600 mt-1">
              {{ __('One-time communication') }}
            </p>
          </div>

          <div
            class="border-2 rounded-lg p-4 cursor-pointer transition-all"
            :class="strategy === 'sequence' ? 'border-green-500 bg-green-50' : 'border-gray-200 hover:border-gray-300'"
            @click="strategy = 'sequence'"
          >
            <FeatherIcon 
              name="repeat" 
              class="h-6 w-6 mb-2"
              :class="strategy === 'sequence' ? 'text-green-600' : 'text-gray-400'"
            />
            <h4 class="text-sm font-semibold text-gray-900">
              {{ __('Sequence') }}
            </h4>
            <p class="text-xs text-gray-600 mt-1">
              {{ __('Multi-step nurturing flow') }}
            </p>
          </div>
        </div>
      </div>

      <!-- Content Editor -->
      <div class="border-t border-gray-200 pt-6">
        <div class="bg-gray-50 rounded-lg p-8 text-center border-2 border-dashed border-gray-300">
          <FeatherIcon name="edit-3" class="h-12 w-12 text-gray-400 mx-auto mb-3" />
          <p class="text-gray-500 mb-2">
            {{ __('Nurturing content editor will be implemented here') }}
          </p>
          <p class="text-xs text-gray-400">
            {{ __('Personalized messaging with relationship-building focus') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FeatherIcon, Badge } from 'frappe-ui'

defineProps({
  selectedChannel: String
})

const strategy = ref('single_touch')
const __ = (text) => text
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
