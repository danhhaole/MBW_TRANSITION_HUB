<template>
  <div v-if="show" class="fixed z-50 inset-0 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="handleClose"></div>
      
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
      
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
        <!-- Header -->
        <div class="bg-white px-6 pt-6 pb-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                {{ __('Campaign Workflow Preview') }}
              </h3>
              <p class="mt-1 text-sm text-gray-500">
                {{ __('Preview how this template will execute in a campaign') }}
              </p>
            </div>
            <Button
              variant="ghost"
              size="sm"
              @click="handleClose"
            >
              <template #icon>
                <FeatherIcon name="x" class="w-6 h-6" />
              </template>
            </Button>
          </div>
        </div>

        <!-- Content -->
        <div class="bg-white px-6 pt-6 pb-4 max-h-[70vh] overflow-y-auto">
          <!-- Debug Info -->
          <div class="mb-4 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs">
            <div>Loading: {{ loading }}</div>
            <div>Error: {{ error }}</div>  
            <div>Template ID: {{ templateId }}</div>
            <div>Template exists: {{ !!template }}</div>
            <div>Steps count: {{ templateSteps.length }}</div>
          </div>
          
          <div v-if="loading" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            <p class="ml-3 text-gray-600">{{ __('Loading template...') }}</p>
          </div>
          
          <div v-else-if="error" class="text-center py-8">
            <div class="text-red-600 mb-2">{{ error }}</div>
            <Button variant="outline" theme="gray" @click="loadTemplate">
              {{ __('Retry') }}
            </Button>
          </div>
          
          <div v-else-if="template">
            <!-- Template Overview -->
            <div class="mb-8 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
              <div class="flex items-start space-x-4">
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <FeatherIcon name="zap" class="w-6 h-6 text-blue-600" />
                  </div>
                </div>
                <div class="flex-1">
                  <h4 class="text-lg font-semibold text-gray-900">{{ template.template_name }}</h4>
                  <p class="text-sm text-gray-600 mt-1">{{ template.description || __('No description provided') }}</p>
                  <div class="flex items-center mt-3 space-x-4">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      {{ template.campaign_type }}
                    </span>
                    <span class="text-sm text-gray-500">
                      {{ templateSteps.length }} {{ __('steps') }}
                    </span>
                    <span class="text-sm text-gray-500">
                      {{ getTotalDuration() }} {{ __('days total duration') }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Campaign Flow Timeline -->
            <div class="space-y-6">
              <h5 class="text-lg font-semibold text-gray-900 flex items-center">
                <FeatherIcon name="play-circle" class="w-5 h-5 mr-2 text-green-600" />
                {{ __('Campaign Execution Flow') }}
              </h5>
              
              <div v-if="templateSteps.length === 0" class="text-center py-8 bg-gray-50 rounded-lg">
                <FeatherIcon name="inbox" class="w-12 h-12 text-gray-400 mx-auto mb-3" />
                <p class="text-gray-500">{{ __('No steps defined yet') }}</p>
              </div>
              
              <div v-else class="relative">
                <!-- Timeline line -->
                <div class="absolute left-8 top-0 bottom-0 w-0.5 bg-gray-200"></div>
                
                <div class="space-y-6">
                  <div 
                    v-for="(step, index) in sortedSteps" 
                    :key="step.name"
                    class="relative flex items-start space-x-4"
                  >
                    <!-- Timeline dot -->
                    <div class="relative z-10">
                      <div class="flex items-center justify-center w-8 h-8 rounded-full border-2 border-white bg-white shadow-md"
                           :class="getStepStatusColor(step.action_type)">
                        <FeatherIcon :name="getStepIcon(step.action_type)" class="w-4 h-4 text-white" />
                      </div>
                      <!-- Day indicator -->
                      <div v-if="getStepDay(step, index) > 0" 
                           class="absolute -top-3 -right-1 bg-indigo-100 text-indigo-800 text-xs font-medium px-1.5 py-0.5 rounded-full">
                        Day {{ getStepDay(step, index) }}
                      </div>
                    </div>
                    
                    <!-- Step content -->
                    <div class="flex-1 min-w-0 pb-6">
                      <div class="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                        <div class="flex items-center justify-between">
                          <div class="flex items-center space-x-3">
                            <h6 class="text-sm font-semibold text-gray-900">
                              {{ step.campaign_step_name }}
                            </h6>
                            <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium"
                                  :class="getActionTypeColor(step.action_type)">
                              {{ getActionTypeDisplay(step.action_type) }}
                            </span>
                          </div>
                          <div class="text-xs text-gray-500">
                            Step {{ step.step_order }}
                          </div>
                        </div>
                        
                        <div v-if="step.delay_in_days > 0" class="mt-2 flex items-center text-sm text-gray-600">
                          <FeatherIcon name="clock" class="w-4 h-4 mr-1" />
                          {{ __('Wait') }} {{ step.delay_in_days }} {{ step.delay_in_days === 1 ? __('day') : __('days') }}
                        </div>
                        
                        <div v-if="step.template_content" class="mt-3 p-3 bg-gray-50 rounded-md">
                          <p class="text-sm text-gray-700 font-medium mb-1">{{ __('Content Preview:') }}</p>
                          <p class="text-sm text-gray-600 italic">
                            "{{ step.template_content.length > 100 ? step.template_content.substring(0, 100) + '...' : step.template_content }}"
                          </p>
                        </div>
                        
                        <div v-if="step.action_config && Object.keys(step.action_config).length > 0" class="mt-3">
                          <p class="text-xs text-gray-500 font-medium mb-1">{{ __('Configuration:') }}</p>
                          <div class="flex flex-wrap gap-2">
                            <span v-for="(value, key) in step.action_config" :key="key"
                                  class="inline-flex items-center px-2 py-1 rounded text-xs bg-yellow-100 text-yellow-800">
                              {{ key }}: {{ value }}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Summary -->
            <div class="mt-8 p-4 bg-gray-50 rounded-lg">
              <h6 class="text-sm font-semibold text-gray-900 mb-2">{{ __('Campaign Summary') }}</h6>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-500">{{ __('Total Steps:') }}</span>
                  <span class="font-medium text-gray-900 ml-2">{{ templateSteps.length }}</span>
                </div>
                <div>
                  <span class="text-gray-500">{{ __('Duration:') }}</span>
                  <span class="font-medium text-gray-900 ml-2">{{ getTotalDuration() }} {{ __('days') }}</span>
                </div>
                <div>
                  <span class="text-gray-500">{{ __('Email Steps:') }}</span>
                  <span class="font-medium text-gray-900 ml-2">{{ getStepCountByType('SEND_EMAIL') }}</span>
                </div>
                <div>
                  <span class="text-gray-500">{{ __('Manual Tasks:') }}</span>
                  <span class="font-medium text-gray-900 ml-2">{{ getStepCountByType('MANUAL_CALL') + getStepCountByType('MANUAL_TASK') }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- No Template Found -->
          <div v-else class="text-center py-8">
            <FeatherIcon name="inbox" class="w-12 h-12 text-gray-400 mx-auto mb-3" />
            <p class="text-gray-500 mb-2">{{ __('No template data available') }}</p>
            <Button variant="outline" theme="gray" @click="loadTemplate">
              {{ __('Reload') }}
            </Button>
          </div>
        </div>

        <!-- Footer -->
        <div class="bg-gray-50 px-6 py-3 flex justify-end">
          <Button variant="outline" theme="gray" @click="handleClose">
            {{ __('Close') }}
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import { useCampaignTemplateStore } from '@/stores/campaignTemplate.js'

// i18n fallback
const __ = (text) => text

// Store
const campaignTemplateStore = useCampaignTemplateStore()

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  templateId: {
    type: String,
    required: true
  }
})

// Emits
const emit = defineEmits(['update:modelValue'])

// Computed
const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Reactive data
const loading = ref(false)
const error = ref('')
const template = ref(null)
const templateSteps = ref([])

// Computed
const sortedSteps = computed(() => {
  return [...templateSteps.value].sort((a, b) => a.step_order - b.step_order)
})

// Methods
const loadTemplate = async () => {
  console.log('Preview Modal - Loading template:', props.templateId)
  
  if (!props.templateId) {
    console.log('Preview Modal - No templateId provided')
    error.value = __('No template ID provided')
    return
  }
  
  loading.value = true
  error.value = ''

  try {
    console.log('Preview Modal - Calling service...')
    const result = await campaignTemplateStore.fetchTemplateById(props.templateId)
    console.log('Preview Modal - Service result:', result)
    
    if (result.success) {
      template.value = result.data
      templateSteps.value = result.data.steps || []
      console.log('Preview Modal - Template loaded:', template.value)
      console.log('Preview Modal - Steps loaded:', templateSteps.value.length)
    } else {
      error.value = result.error || __('Failed to load template')
      console.log('Preview Modal - Load failed:', error.value)
    }
  } catch (err) {
    console.error('Preview Modal - Error loading template:', err)
    error.value = __('An error occurred while loading template')
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  show.value = false
}

const getTotalDuration = () => {
  return templateSteps.value.reduce((total, step) => total + (step.delay_in_days || 0), 0)
}

const getStepDay = (step, index) => {
  let day = 1
  for (let i = 0; i < index; i++) {
    day += sortedSteps.value[i].delay_in_days || 0
  }
  return day + (step.delay_in_days || 0)
}

const getStepCountByType = (type) => {
  return templateSteps.value.filter(step => step.action_type === type).length
}

const getStepIcon = (actionType) => {
  const icons = {
    'SEND_EMAIL': 'mail',
    'SEND_SMS': 'message-square',
    'MANUAL_CALL': 'phone',
    'MANUAL_TASK': 'clipboard'
  }
  return icons[actionType] || 'circle'
}

const getStepStatusColor = (actionType) => {
  const colors = {
    'SEND_EMAIL': 'bg-blue-500',
    'SEND_SMS': 'bg-green-500',
    'MANUAL_CALL': 'bg-yellow-500',
    'MANUAL_TASK': 'bg-purple-500'
  }
  return colors[actionType] || 'bg-gray-500'
}

const getActionTypeColor = (actionType) => {
  const colors = {
    'SEND_EMAIL': 'bg-blue-100 text-blue-800',
    'SEND_SMS': 'bg-green-100 text-green-800',
    'MANUAL_CALL': 'bg-yellow-100 text-yellow-800',
    'MANUAL_TASK': 'bg-purple-100 text-purple-800'
  }
  return colors[actionType] || 'bg-gray-100 text-gray-800'
}

const getActionTypeDisplay = (actionType) => {
  const displays = {
    'SEND_EMAIL': __('Send Email'),
    'SEND_SMS': __('Send SMS'),
    'MANUAL_CALL': __('Manual Call'),
    'MANUAL_TASK': __('Manual Task')
  }
  return displays[actionType] || actionType
}

// Watchers
watch(show, (newValue) => {
  if (newValue) {
    loadTemplate()
  }
})
</script>

<style scoped>
/* Add any component-specific styles here */
</style> 