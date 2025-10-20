<template>
  <Dialog
    :model-value="show"
    @update:model-value="$emit('close')"
    :options="{
      title: __('Tag Details'),
      size: 'lg'
    }"
  >
    <template #body-content>
      <div v-if="tag" class="space-y-6">
        <!-- Tag Preview -->
        <div class="bg-gray-50 rounded-lg p-4">
          <div class="flex items-center">
            <div class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center mr-4"
                 :style="{ backgroundColor: tag.color + '20', color: tag.color }">
              <FeatherIcon name="tag" class="w-5 h-5" />
            </div>
            <div class="flex-1">
              <h4 class="text-lg font-semibold text-gray-900">{{ tag.title }}</h4>
              <p class="text-sm text-gray-500">{{ tag.name }}</p>
            </div>
          </div>
        </div>

        <!-- Details Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Basic Info -->
          <div class="space-y-4">
            <h5 class="text-sm font-medium text-gray-900 border-b border-gray-200 pb-2">
              {{ __('Basic Information') }}
            </h5>
            
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">{{ __('Name') }}:</span>
                <span class="text-sm font-medium text-gray-900">{{ tag.title }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">{{ __('ID') }}:</span>
                <span class="text-sm font-mono text-gray-600">{{ tag.name }}</span>
              </div>
              
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-500">{{ __('Color') }}:</span>
                <div class="flex items-center space-x-2">
                  <div class="w-4 h-4 rounded border border-gray-200"
                       :style="{ backgroundColor: tag.color }"></div>
                  <span class="text-sm font-mono text-gray-600">{{ tag.color }}</span>
                </div>
              </div>
              
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">{{ __('Order') }}:</span>
                <span class="text-sm font-medium text-gray-900">{{ tag.order || 0 }}</span>
              </div>
            </div>
          </div>

          <!-- Metadata -->
          <div class="space-y-4">
            <h5 class="text-sm font-medium text-gray-900 border-b border-gray-200 pb-2">
              Thông tin hệ thống
            </h5>
            
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">{{ __('Created by') }}:</span>
                <span class="text-sm font-medium text-gray-900">{{ tag.owner || 'N/A' }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">{{ __('Created at') }}:</span>
                <span class="text-sm text-gray-600">{{ tag.formatted_created_at }}</span>
              </div>
              
              <div class="flex justify-between">
                <span class="text-sm text-gray-500">{{ __('Updated at') }}:</span>
                <span class="text-sm text-gray-600">{{ tag.formatted_modified }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Usage Statistics (placeholder) -->
        <div class="space-y-4">
          <h5 class="text-sm font-medium text-gray-900 border-b border-gray-200 pb-2">
            {{ __('Usage Statistics') }}
          </h5>
          
          <div class="grid grid-cols-3 gap-4">
            <div class="bg-blue-50 rounded-lg p-3 text-center">
              <div class="text-lg font-semibold text-blue-600">0</div>
              <div class="text-xs text-blue-500">{{ __('Campaigns') }}</div>
            </div>
            <div class="bg-green-50 rounded-lg p-3 text-center">
              <div class="text-lg font-semibold text-green-600">0</div>
              <div class="text-xs text-green-500">{{ __('Contacts') }}</div>
            </div>
            <div class="bg-purple-50 rounded-lg p-3 text-center">
              <div class="text-lg font-semibold text-purple-600">0</div>
              <div class="text-xs text-purple-500">{{ __('Templates') }}</div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <Button
        variant="solid"
        theme="blue"
        @click="$emit('close')"
      >
        Đóng
      </Button>
    </template>
  </Dialog>
</template>

<script setup>
import { Button, Dialog, FeatherIcon } from 'frappe-ui'

// Props
defineProps({
  show: {
    type: Boolean,
    default: false
  },
  tag: {
    type: Object,
    default: null
  }
})

// Emits
defineEmits(['close'])
</script>
