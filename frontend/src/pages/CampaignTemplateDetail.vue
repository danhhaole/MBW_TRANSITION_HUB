<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <div class="flex items-center space-x-3">
          <!-- Back Button -->
          <Button
            variant="outline"
            theme="gray"
            @click="handleBack"
          >
            <template #prefix>
              <FeatherIcon name="arrow-left" class="w-4 h-4" />
            </template>
            {{ __('Back to Templates') }}
          </Button>

          <!-- Edit Template Button -->
          <Button
            v-if="template"
            variant="solid"
            theme="blue"
            @click="handleEditTemplate"
            :loading="loading"
          >
            <template #prefix>
              <FeatherIcon name="edit" class="w-4 h-4" />
            </template>
            {{ __('Edit Template') }}
          </Button>

          <!-- Add Step Button -->
          <Button
            v-if="template"
            variant="solid"
            theme="green"
            @click="handleAddStep"
            :loading="loading"
          >
            <template #prefix>
              <FeatherIcon name="plus" class="w-4 h-4" />
            </template>
            {{ __('Add Step') }}
          </Button>
        </div>
      </template>
    </LayoutHeader>

    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <div class="flex justify-center items-center">
          <div class="flex items-center space-x-2 text-gray-600">
            <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
              </path>
            </svg>
            <span>{{ __('Loading template details...') }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <div class="text-center">
          <svg class="mx-auto h-12 w-12 text-red-400" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">{{ __('Error loading template') }}</h3>
          <p class="mt-1 text-sm text-gray-500">{{ error }}</p>
          <div class="mt-6">
            <Button @click="loadTemplate" variant="solid" theme="blue">
              {{ __('Try Again') }}
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else-if="template" class="container mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Template Information Card -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                  </path>
                </svg>
              </div>
              <div>
                <h1 class="text-xl font-semibold text-gray-900">{{ template.template_name }}</h1>
                <p class="text-sm text-gray-500">{{ template.name }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 rounded-full" :class="getStatusColor(template.is_active)"></div>
              <span class="text-sm font-medium" :class="template.is_active ? 'text-green-700' : 'text-gray-700'">
                {{ template.display_status }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="px-6 py-4">
          <dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <dt class="text-sm font-medium text-gray-500">{{ __('Campaign Type') }}</dt>
              <dd class="mt-1">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium"
                  :class="getTypeColor(template.campaign_type)">
                  {{ template.type_display || template.campaign_type }}
                </span>
              </dd>
            </div>
            
            <div>
              <dt class="text-sm font-medium text-gray-500">{{ __('Total Steps') }}</dt>
              <dd class="mt-1 flex items-center text-sm text-gray-900">
                <svg class="w-4 h-4 text-gray-400 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
                {{ template.step_count || 0 }} {{ __('steps') }}
              </dd>
            </div>
            
            <div>
              <dt class="text-sm font-medium text-gray-500">{{ __('Last Modified') }}</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ formatDate(template.modified) }}</dd>
            </div>
            
            <div>
              <dt class="text-sm font-medium text-gray-500">{{ __('Modified By') }}</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ template.modified_by || template.owner }}</dd>
            </div>
          </dl>
          
          <div v-if="template.description" class="mt-6">
            <dt class="text-sm font-medium text-gray-500 mb-2">{{ __('Description') }}</dt>
            <dd class="text-sm text-gray-900 p-3 bg-gray-50 rounded-md">{{ template.description }}</dd>
          </div>
        </div>
      </div>

      <!-- Template Steps -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-lg font-medium text-gray-900">{{ __('Template Steps') }}</h2>
              <p class="text-sm text-gray-500">{{ __('Configure the sequence of actions for this campaign template') }}</p>
            </div>
            <Button
              variant="solid"
              theme="blue"
              @click="handleAddStep"
              size="sm"
            >
              <template #prefix>
                <FeatherIcon name="plus" class="w-4 h-4" />
              </template>
              {{ __('Add Step') }}
            </Button>
          </div>
        </div>

        <!-- Steps Loading -->
        <div v-if="stepsLoading" class="p-8">
          <div class="flex justify-center items-center">
            <div class="flex items-center space-x-2 text-gray-600">
              <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              <span>{{ __('Loading steps...') }}</span>
            </div>
          </div>
        </div>

        <!-- Empty Steps State -->
        <div v-else-if="!steps || steps.length === 0" class="p-8">
          <div class="text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">{{ __('No steps configured') }}</h3>
            <p class="mt-1 text-sm text-gray-500">{{ __('Add steps to define the campaign workflow.') }}</p>
            <div class="mt-6">
              <Button variant="solid" theme="blue" @click="handleAddStep">
                <template #prefix>
                  <FeatherIcon name="plus" class="w-4 h-4" />
                </template>
                {{ __('Add First Step') }}
              </Button>
            </div>
          </div>
        </div>

        <!-- Steps List -->
        <div v-else class="divide-y divide-gray-200">
          <div v-for="(step, index) in steps" :key="step.name"
            class="p-6 hover:bg-gray-50 transition-colors duration-150">
            <div class="flex items-start justify-between">
              <div class="flex items-start space-x-4 flex-1">
                <!-- Step Number -->
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center text-sm font-medium">
                    {{ step.step_order }}
                  </div>
                </div>
                
                <!-- Step Content -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center space-x-3 mb-2">
                    <h3 class="text-base font-medium text-gray-900">{{ step.campaign_step_name }}</h3>
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getActionTypeColor(step.action_type)">
                      {{ step.action_type_display }}
                    </span>
                  </div>
                  
                  <div class="flex items-center space-x-6 text-sm text-gray-500 mb-3">
                    <div class="flex items-center space-x-1">
                      <FeatherIcon name="clock" class="w-4 h-4" />
                      <span>{{ step.delay_display }}</span>
                    </div>
                    <div v-if="step.has_content" class="flex items-center space-x-1">
                      <FeatherIcon name="file-text" class="w-4 h-4" />
                      <span>{{ __('Has content') }}</span>
                    </div>
                    <div v-if="step.has_config" class="flex items-center space-x-1">
                      <FeatherIcon name="settings" class="w-4 h-4" />
                      <span>{{ __('Configured') }}</span>
                    </div>
                  </div>
                  
                  <!-- Step Content Preview -->
                  <div v-if="step.template_content" class="mt-3">
                    <div class="bg-gray-50 rounded-md p-3">
                      <p class="text-sm text-gray-700 line-clamp-3">{{ step.template_content }}</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Step Actions -->
              <div class="flex items-center space-x-2 ml-4">
                <!-- Move Up -->
                <button
                  v-if="index > 0"
                  @click="handleMoveStep(step, 'up')"
                  class="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                  :title="__('Move Up')"
                >
                  <FeatherIcon name="chevron-up" class="w-4 h-4" />
                </button>
                
                <!-- Move Down -->
                <button
                  v-if="index < steps.length - 1"
                  @click="handleMoveStep(step, 'down')"
                  class="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                  :title="__('Move Down')"
                >
                  <FeatherIcon name="chevron-down" class="w-4 h-4" />
                </button>
                
                <!-- Edit -->
                <button
                  @click="handleEditStep(step)"
                  class="p-1 text-gray-400 hover:text-blue-600 transition-colors"
                  :title="__('Edit Step')"
                >
                  <FeatherIcon name="edit" class="w-4 h-4" />
                </button>
                
                <!-- Duplicate -->
                <button
                  @click="handleDuplicateStep(step)"
                  class="p-1 text-gray-400 hover:text-green-600 transition-colors"
                  :title="__('Duplicate Step')"
                >
                  <FeatherIcon name="copy" class="w-4 h-4" />
                </button>
                
                <!-- Delete -->
                <button
                  @click="handleDeleteStep(step)"
                  class="p-1 text-gray-400 hover:text-red-600 transition-colors"
                  :title="__('Delete Step')"
                >
                  <FeatherIcon name="trash-2" class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Template Form Modal -->
    <CampaignTemplateFormModal
      v-if="showTemplateModal"
      v-model="showTemplateModal"
      :template="template"
      @saved="handleTemplateSaved"
    />

    <!-- Step Form Modal -->
    <CampaignTemplateStepFormModal
      v-if="showStepModal"
      v-model="showStepModal"
      :template-name="template?.name"
      :step="selectedStep"
      @saved="handleStepSaved"
    />

    <!-- Delete Step Confirmation Modal -->
    <div v-if="showDeleteStepModal" class="fixed z-50 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                <svg class="h-6 w-6 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-gray-900">{{ __('Delete Step') }}</h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    {{ __('Are you sure you want to delete step "{0}"? This action cannot be undone. All following steps will be reordered.', [stepToDelete?.campaign_step_name]) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              @click="confirmDeleteStep"
              :disabled="deleteStepLoading"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="deleteStepLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ deleteStepLoading ? __('Deleting...') : __('Delete') }}
            </button>
            <button
              @click="showDeleteStepModal = false"
              :disabled="deleteStepLoading"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ __('Cancel') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Toast Container -->
  <ToastContainer />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import LayoutHeader from '@/components/LayoutHeader.vue'
import CampaignTemplateFormModal from '@/components/CampaignTemplateFormModal.vue'
import CampaignTemplateStepFormModal from '@/components/CampaignTemplateStepFormModal.vue'
import { useCampaignTemplateStore } from '@/stores/campaignTemplate.js'
import { useCampaignTemplateStepStore } from '@/stores/campaignTemplateStep.js'
import { useToast } from '@/composables/useToast.js'
import { ToastContainer } from '@/components/shared'

// Router
const router = useRouter()
const route = useRoute()

// Toast
const { showSuccess, showError } = useToast()

// Store
const campaignTemplateStore = useCampaignTemplateStore()
const campaignTemplateStepStore = useCampaignTemplateStepStore()

// Page setup
const templateId = ref(route.params.id)
const breadcrumbs = computed(() => [
  { label: 'Settings', route: { name: 'Settings' } },
  { label: 'Campaign Templates', route: { name: 'CampaignTemplateManagement' } },
  { label: template.value?.template_name || 'Template Detail', route: { name: 'CampaignTemplateDetail', params: { id: templateId.value } } }
])

// Reactive data
const loading = ref(false)
const stepsLoading = ref(false)
const error = ref(null)
const template = ref(null)
const steps = ref([])

// Modals
const showTemplateModal = ref(false)
const showStepModal = ref(false)
const showDeleteStepModal = ref(false)
const selectedStep = ref(null)
const stepToDelete = ref(null)
const deleteStepLoading = ref(false)

// Methods
const loadTemplate = async () => {
  loading.value = true
  error.value = null

  try {
    const result = await campaignTemplateStore.fetchTemplateById(templateId.value)
    
    if (result.success) {
      template.value = result.data
      steps.value = result.data.steps || []
    } else {
      error.value = result.error || __('Template not found')
    }
  } catch (err) {
    console.error('Error loading template:', err)
    error.value = __('An error occurred while loading template')
  } finally {
    loading.value = false
  }
}

const loadSteps = async () => {
  if (!template.value) return
  
  stepsLoading.value = true
  try {
    const result = await campaignTemplateStepStore.fetchStepsByTemplate(template.value.name)
    
    if (result.success) {
      steps.value = result.data || []
    }
  } catch (err) {
    console.error('Error loading steps:', err)
  } finally {
    stepsLoading.value = false
  }
}

// Event handlers
const handleBack = () => {
  router.push({ name: 'CampaignTemplateManagement' })
}

const handleEditTemplate = () => {
  showTemplateModal.value = true
}

const handleAddStep = () => {
  selectedStep.value = null
  showStepModal.value = true
}

const handleEditStep = (step) => {
  selectedStep.value = step
  showStepModal.value = true
}

const handleDeleteStep = (step) => {
  stepToDelete.value = step
  showDeleteStepModal.value = true
}

const handleDuplicateStep = async (step) => {
  try {
    // Create a copy of the step with modified name and order
    const copyData = {
      template: template.value.name,
      campaign_step_name: `${step.campaign_step_name} (Copy)`,
      action_type: step.action_type,
      step_order: steps.value.length + 1,
      delay_in_days: step.delay_in_days || 0,
      template_content: step.template_content || '',
      action_config: step.action_config || null
    }
    
    const result = await campaignTemplateStepStore.createStep(copyData)
    
    if (result.success) {
      showSuccess(__('Step duplicated successfully'))
      
      await loadSteps()
    } else {
      showError(result.error || __('Failed to duplicate step'))
    }
  } catch (err) {
    console.error('Error duplicating step:', err)
    showError(__('An error occurred while duplicating step'))
  }
}

const handleMoveStep = async (step, direction) => {
  try {
    const result = await campaignTemplateStepStore.moveStep(step.name, direction)

    if (result.success) {
      showSuccess(result.message)
      
      await loadSteps()
    } else {
      showError(result.error || __('Failed to move step'))
    }
  } catch (err) {
    console.error('Error moving step:', err)
    showError(__('An error occurred while moving step'))
  }
}

const confirmDeleteStep = async () => {
  if (!stepToDelete.value) return

  deleteStepLoading.value = true
  try {
    const result = await campaignTemplateStepStore.deleteStep(stepToDelete.value.name)
    
    if (result.success) {
      showSuccess(result.message || __('Step deleted successfully'))
      
      showDeleteStepModal.value = false
      stepToDelete.value = null
      await loadSteps()
    } else {
      showError(result.error || __('Failed to delete step'))
    }
  } catch (err) {
    console.error('Error deleting step:', err)
    showError(__('An error occurred while deleting step'))
  } finally {
    deleteStepLoading.value = false
  }
}

const handleTemplateSaved = () => {
  showTemplateModal.value = false
  loadTemplate()
}

const handleStepSaved = () => {
  showStepModal.value = false
  selectedStep.value = null
  loadSteps()
}

// Utility functions
const formatDate = (dateString) => {
  if (!dateString) return ''
  
  try {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return dateString
  }
}

const getTypeColor = (type) => {
  const colors = {
    'Email': 'bg-blue-100 text-blue-800',
    'SMS': 'bg-green-100 text-green-800',
    'Ads': 'bg-purple-100 text-purple-800',
    'Social Media': 'bg-pink-100 text-pink-800',
    'Direct Mail': 'bg-orange-100 text-orange-800'
  }
  return colors[type] || 'bg-gray-100 text-gray-800'
}

const getStatusColor = (isActive) => {
  return isActive ? 'bg-green-400' : 'bg-gray-400'
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

// Lifecycle
onMounted(() => {
  loadTemplate()
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 