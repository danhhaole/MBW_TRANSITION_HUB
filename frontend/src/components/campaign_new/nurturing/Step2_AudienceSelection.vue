<template>
  <div class="space-y-6 animate-fadeIn">
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900">
          {{ __('Select Audience to Nurture') }}
        </h3>
        <Badge theme="green" variant="subtle">
          {{ __('Nurturing') }}
        </Badge>
      </div>

      <p class="text-gray-600 mb-6">
        {{ __('Select existing contacts or talent pools to nurture relationships with.') }}
      </p>

      <!-- Audience Source Selection -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div
          class="border-2 rounded-lg p-4 cursor-pointer transition-all"
          :class="audienceSource === 'existing_contacts' ? 'border-green-500 bg-green-50' : 'border-gray-200 hover:border-gray-300'"
          @click="audienceSource = 'existing_contacts'"
        >
          <FeatherIcon 
            name="user-check" 
            class="h-6 w-6 mb-2"
            :class="audienceSource === 'existing_contacts' ? 'text-green-600' : 'text-gray-400'"
          />
          <h4 class="text-sm font-semibold text-gray-900">
            {{ __('Existing Contacts') }}
          </h4>
          <p class="text-xs text-gray-600 mt-1">
            {{ __('Nurture your current contacts') }}
          </p>
        </div>

        <div
          class="border-2 rounded-lg p-4 cursor-pointer transition-all"
          :class="audienceSource === 'talent_pool' ? 'border-green-500 bg-green-50' : 'border-gray-200 hover:border-gray-300'"
          @click="audienceSource = 'talent_pool'"
        >
          <FeatherIcon 
            name="users" 
            class="h-6 w-6 mb-2"
            :class="audienceSource === 'talent_pool' ? 'text-green-600' : 'text-gray-400'"
          />
          <h4 class="text-sm font-semibold text-gray-900">
            {{ __('Talent Pool') }}
          </h4>
          <p class="text-xs text-gray-600 mt-1">
            {{ __('Select from talent pools') }}
          </p>
        </div>

        <div
          class="border-2 rounded-lg p-4 cursor-pointer transition-all"
          :class="audienceSource === 'segment' ? 'border-green-500 bg-green-50' : 'border-gray-200 hover:border-gray-300'"
          @click="audienceSource = 'segment'"
        >
          <FeatherIcon 
            name="target" 
            class="h-6 w-6 mb-2"
            :class="audienceSource === 'segment' ? 'text-green-600' : 'text-gray-400'"
          />
          <h4 class="text-sm font-semibold text-gray-900">
            {{ __('Segment') }}
          </h4>
          <p class="text-xs text-gray-600 mt-1">
            {{ __('Target specific segments') }}
          </p>
        </div>
      </div>

      <!-- Content Placeholder -->
      <div class="border-t border-gray-200 pt-6">
        <div class="bg-gray-50 rounded-lg p-8 text-center">
          <FeatherIcon name="heart" class="h-12 w-12 text-gray-400 mx-auto mb-3" />
          <p class="text-gray-500">
            {{ __('Audience selector for nurturing will be implemented here') }}
          </p>
        </div>
      </div>

      <!-- Audience Stats -->
      <div class="mt-6 border-t border-gray-200 pt-6">
        <div class="bg-green-50 rounded-lg p-4">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-green-900">
              {{ __('Contacts to Nurture:') }}
            </span>
            <span class="text-lg font-bold text-green-600">
              0 {{ __('contacts') }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FeatherIcon, Badge } from 'frappe-ui'

const audienceSource = ref('existing_contacts')
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
