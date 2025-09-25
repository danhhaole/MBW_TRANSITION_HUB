<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <div class="flex space-x-3">
          <Button variant="solid" theme="blue" @click="goBack">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </template>
            {{ __('Back') }}
          </Button>
        </div>
      </template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h1 class="text-2xl font-bold mb-4">{{ data.full_name || __('Loading...') }}</h1>
        
        <!-- Basic Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <div>
              <label class="text-sm text-gray-600 font-medium">{{ __('Full Name') }}</label>
              <p class="text-sm mt-1">{{ data.full_name || __('None') }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600 font-medium">{{ __('Email') }}</label>
              <p class="text-sm mt-1">{{ data.email || __('None') }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600 font-medium">{{ __('Phone') }}</label>
              <p class="text-sm mt-1">{{ data.phone || __('None') }}</p>
            </div>
          </div>
          <div class="space-y-3">
            <div>
              <label class="text-sm text-gray-600 font-medium">{{ __('Source') }}</label>
              <p class="text-sm mt-1">{{ data.source || __('None') }}</p>
            </div>
            <div>
              <label class="text-sm text-gray-600 font-medium">{{ __('Status') }}</label>
              <div class="mt-1">
                <span :class="badgeClass(data.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                  {{ data.status || __('None') }}
                </span>
              </div>
            </div>
            <div>
              <label class="text-sm text-gray-600 font-medium">{{ __('Created Date') }}</label>
              <p class="text-sm mt-1">{{ formatDateTime(data.creation) || __('None') }}</p>
            </div>
          </div>
        </div>

        <!-- Skills and CV Section -->
        <div v-if="data.skills || data.cv_original_url" class="mt-6 pt-6 border-t border-gray-200">
          <h2 class="text-lg font-semibold mb-4">{{ __('Skills & CV') }}</h2>
          
          <div v-if="data.skills" class="mb-4">
            <label class="text-sm text-gray-600 font-medium">{{ __('Skills') }}</label>
            <div class="mt-1">
              <div v-if="Array.isArray(processedSkills) && processedSkills.length > 0" class="flex flex-wrap gap-2">
                <span v-for="skill in processedSkills" :key="skill" 
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200">
                  {{ skill }}
                </span>
              </div>
              <p v-else class="text-sm text-gray-500">{{ data.skills || __('None') }}</p>
            </div>
          </div>
          
          <div v-if="data.cv_original_url" class="mb-4">
            <label class="text-sm text-gray-600 font-medium">{{ __('CV Link') }}</label>
            <div class="mt-1">
              <a :href="data.cv_original_url" target="_blank" rel="noopener noreferrer"
                 class="inline-flex items-center text-blue-600 hover:text-blue-800 hover:underline text-sm">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                {{ __('View CV') }}
              </a>
            </div>
          </div>
        </div>

        <!-- Show Skills and CV sections even if empty -->
        <div v-else class="mt-6 pt-6 border-t border-gray-200">
          <h2 class="text-lg font-semibold mb-4">{{ __('Skills & CV') }}</h2>
          
          <div class="mb-4">
            <label class="text-sm text-gray-600 font-medium">{{ __('Skills') }}</label>
            <p class="text-sm mt-1 text-gray-500">{{ __('None') }}</p>
          </div>
          
          <div class="mb-4">
            <label class="text-sm text-gray-600 font-medium">{{ __('CV Link') }}</label>
            <p class="text-sm mt-1 text-gray-500">{{ __('None') }}</p>
          </div>
        </div>

        <!-- Additional Information -->
        <div v-if="data.headline || data.ai_summary" class="mt-6 pt-6 border-t border-gray-200">
          <h2 class="text-lg font-semibold mb-4">{{ __('Additional Information') }}</h2>
          
          <div v-if="data.headline" class="mb-4">
            <label class="text-sm text-gray-600 font-medium">{{ __('Headline') }}</label>
            <p class="text-sm mt-1">{{ data.headline }}</p>
          </div>
          
          <div v-if="data.ai_summary" class="mb-4">
            <label class="text-sm text-gray-600 font-medium">{{ __('AI Summary') }}</label>
            <div class="prose max-w-none mt-1" v-html="data.ai_summary"></div>
          </div>
        </div>

        <!-- Show Additional Information section even if empty -->
        <div v-else class="mt-6 pt-6 border-t border-gray-200">
          <h2 class="text-lg font-semibold mb-4">{{ __('Additional Information') }}</h2>
          
          <div class="mb-4">
            <label class="text-sm text-gray-600 font-medium">{{ __('Headline') }}</label>
            <p class="text-sm mt-1 text-gray-500">{{ __('None') }}</p>
          </div>
          
          <div class="mb-4">
            <label class="text-sm text-gray-600 font-medium">{{ __('AI Summary') }}</label>
            <p class="text-sm mt-1 text-gray-500">{{ __('None') }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Breadcrumbs, Button } from 'frappe-ui'
import { call } from 'frappe-ui'

const route = useRoute()
const router = useRouter()
const data = reactive({})

const breadcrumbs = computed(() => [
  { label: __('Candidates'), route: { name: 'CandidateManagementSimple' } },
  { label: data.full_name || __('Loading...'), route: { name: 'CandidateDetailSimpleView' } }
])

// Process skills to handle both string and array formats
const processedSkills = computed(() => {
  if (!data.skills) return []
  
  // If it's already an array, return it
  if (Array.isArray(data.skills)) {
    return data.skills
  }
  
  // If it's a string, try to parse it
  if (typeof data.skills === 'string') {
    try {
      // Try to parse as JSON array first
      const parsed = JSON.parse(data.skills)
      if (Array.isArray(parsed)) {
        return parsed
      }
    } catch (e) {
      // If not JSON, split by comma
      return data.skills.split(',').map(skill => skill.trim()).filter(skill => skill)
    }
  }
  
  return []
})

const load = async () => {
  const res = await call('frappe.client.get', { 
    doctype: 'Candidate', 
    name: route.params.id,
    fields: ['*']
  })
  Object.assign(data, res)
}

const goBack = () => router.push({ name: 'CandidateManagementSimple' })

const badgeClass = (status) => ({
  'NEW': 'bg-gray-100 text-gray-800',
  'SOURCED': 'bg-blue-100 text-blue-800',
  'NURTURING': 'bg-yellow-100 text-yellow-800',
  'ENGAGED': 'bg-green-100 text-green-800',
  'ARCHIVED': 'bg-red-100 text-red-800'
}[status] || 'bg-gray-100 text-gray-800')

const formatDateTime = (date) => date ? new Date(date).toLocaleString('vi-VN') : ''

onMounted(async () => {
  if (route.params.id && route.params.id !== 'new') {
    await load()
  }
})
</script> 