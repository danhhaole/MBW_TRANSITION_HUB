<template>
  <div class="space-y-6 animate-fadeIn">
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900">
          {{ __('Target Candidates') }}
        </h3>
        <Badge theme="purple" variant="subtle">
          {{ __('Recruitment') }}
        </Badge>
      </div>

      <p class="text-gray-600 mb-6">
        {{ __('Define your ideal candidate profile and target audience for this recruitment campaign.') }}
      </p>

      <!-- Candidate Source -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-3">
          {{ __('Candidate Source') }}
        </label>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div
            class="border-2 rounded-lg p-4 cursor-pointer transition-all"
            :class="candidateSource === 'talent_pool' ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'"
            @click="candidateSource = 'talent_pool'"
          >
            <FeatherIcon 
              name="database" 
              class="h-6 w-6 mb-2"
              :class="candidateSource === 'talent_pool' ? 'text-purple-600' : 'text-gray-400'"
            />
            <h4 class="text-sm font-semibold text-gray-900">
              {{ __('Talent Pool') }}
            </h4>
            <p class="text-xs text-gray-600 mt-1">
              {{ __('From existing talent pools') }}
            </p>
          </div>

          <div
            class="border-2 rounded-lg p-4 cursor-pointer transition-all"
            :class="candidateSource === 'external' ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'"
            @click="candidateSource = 'external'"
          >
            <FeatherIcon 
              name="globe" 
              class="h-6 w-6 mb-2"
              :class="candidateSource === 'external' ? 'text-purple-600' : 'text-gray-400'"
            />
            <h4 class="text-sm font-semibold text-gray-900">
              {{ __('External Sources') }}
            </h4>
            <p class="text-xs text-gray-600 mt-1">
              {{ __('Import from job boards') }}
            </p>
          </div>

          <div
            class="border-2 rounded-lg p-4 cursor-pointer transition-all"
            :class="candidateSource === 'custom' ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'"
            @click="candidateSource = 'custom'"
          >
            <FeatherIcon 
              name="filter" 
              class="h-6 w-6 mb-2"
              :class="candidateSource === 'custom' ? 'text-purple-600' : 'text-gray-400'"
            />
            <h4 class="text-sm font-semibold text-gray-900">
              {{ __('Custom Criteria') }}
            </h4>
            <p class="text-xs text-gray-600 mt-1">
              {{ __('Define custom filters') }}
            </p>
          </div>
        </div>
      </div>

      <!-- Candidate Criteria -->
      <div class="border-t border-gray-200 pt-6">
        <h4 class="text-sm font-semibold text-gray-900 mb-4">
          {{ __('Ideal Candidate Profile') }}
        </h4>
        <div class="bg-gray-50 rounded-lg p-8 text-center">
          <FeatherIcon name="user-plus" class="h-12 w-12 text-gray-400 mx-auto mb-3" />
          <p class="text-gray-500 mb-2">
            {{ __('Candidate criteria builder will be implemented here') }}
          </p>
          <p class="text-xs text-gray-400">
            {{ __('Skills, experience, location, and other requirements') }}
          </p>
        </div>
      </div>

      <!-- Candidate Pool Stats -->
      <div class="mt-6 border-t border-gray-200 pt-6">
        <div class="bg-purple-50 rounded-lg p-4 border border-purple-200">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-purple-900">
              {{ __('Potential Candidates:') }}
            </span>
            <span class="text-lg font-bold text-purple-600">
              0 {{ __('candidates') }}
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

const candidateSource = ref('talent_pool')
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
