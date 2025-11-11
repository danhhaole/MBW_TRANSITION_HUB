<template>
  <div class="space-y-6 animate-fadeIn">
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900">
          {{ __('Select Job Opening') }}
        </h3>
        <Badge theme="purple" variant="subtle">
          {{ __('Recruitment') }}
        </Badge>
      </div>

      <p class="text-gray-600 mb-6">
        {{ __('Select the job opening you want to recruit for in this campaign.') }}
      </p>

      <!-- Job Opening Selection Method -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div
          class="border-2 rounded-lg p-4 cursor-pointer transition-all"
          :class="selectionMethod === 'existing' ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'"
          @click="selectionMethod = 'existing'"
        >
          <FeatherIcon 
            name="briefcase" 
            class="h-6 w-6 mb-2"
            :class="selectionMethod === 'existing' ? 'text-purple-600' : 'text-gray-400'"
          />
          <h4 class="text-sm font-semibold text-gray-900">
            {{ __('Existing Job Opening') }}
          </h4>
          <p class="text-xs text-gray-600 mt-1">
            {{ __('Select from active job openings') }}
          </p>
        </div>

        <div
          class="border-2 rounded-lg p-4 cursor-pointer transition-all"
          :class="selectionMethod === 'create_new' ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'"
          @click="selectionMethod = 'create_new'"
        >
          <FeatherIcon 
            name="plus-circle" 
            class="h-6 w-6 mb-2"
            :class="selectionMethod === 'create_new' ? 'text-purple-600' : 'text-gray-400'"
          />
          <h4 class="text-sm font-semibold text-gray-900">
            {{ __('Create New Job Opening') }}
          </h4>
          <p class="text-xs text-gray-600 mt-1">
            {{ __('Create a new job opening') }}
          </p>
        </div>
      </div>

      <!-- Content based on selection -->
      <div class="border-t border-gray-200 pt-6">
        <div v-if="selectionMethod === 'existing'">
          <div class="bg-gray-50 rounded-lg p-8 text-center">
            <FeatherIcon name="search" class="h-12 w-12 text-gray-400 mx-auto mb-3" />
            <p class="text-gray-500 mb-2">
              {{ __('Job opening selector will be implemented here') }}
            </p>
            <p class="text-xs text-gray-400">
              {{ __('Search and select from your active job openings') }}
            </p>
          </div>
        </div>

        <div v-else-if="selectionMethod === 'create_new'">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Job Title') }}
              </label>
              <FormControl
                v-model="newJobTitle"
                type="text"
                :placeholder="__('e.g., Senior Frontend Developer')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Department') }}
              </label>
              <FormControl
                v-model="newJobDepartment"
                type="text"
                :placeholder="__('e.g., Engineering')"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Location') }}
              </label>
              <FormControl
                v-model="newJobLocation"
                type="text"
                :placeholder="__('e.g., Ho Chi Minh City')"
              />
            </div>

            <div class="bg-blue-50 rounded-lg p-4 border border-blue-200">
              <p class="text-sm text-blue-800">
                {{ __('You can add more details after creating the campaign') }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Selected Job Preview -->
      <div class="mt-6 border-t border-gray-200 pt-6">
        <h4 class="text-sm font-semibold text-gray-900 mb-3">
          {{ __('Selected Job Opening') }}
        </h4>
        <div class="bg-purple-50 rounded-lg p-4 border border-purple-200">
          <p class="text-sm text-purple-800">
            {{ __('No job opening selected yet') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FeatherIcon, Badge, FormControl } from 'frappe-ui'

const selectionMethod = ref('existing')
const newJobTitle = ref('')
const newJobDepartment = ref('')
const newJobLocation = ref('')

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
