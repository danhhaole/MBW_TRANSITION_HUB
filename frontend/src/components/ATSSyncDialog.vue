<template>
  <Dialog
    v-model="isOpen"
    :options="{
      size: '4xl',
    }"
    
  >
    <template #body-title>
      <div class="mb-6">
        <div class="flex items-start justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">
              {{ __('Sync Positions from ATS') }}
            </h3>
            <p class="text-sm text-gray-500 mt-1">
              {{ __('Import position data from your ATS system to create talent pools.') }}
            </p>
          </div>
        </div>
      </div>
      
      
    </template>

    <template #body-content>
        <!-- Step Indicator -->
      <div class="mb-8 px-12">
        <div class="flex items-start justify-between w-full">
          <!-- Step 1 -->
          <div class="flex flex-col items-center" style="min-width: 140px;">
            <div
              :class="[
                'flex items-center justify-center w-12 h-12 rounded-full border-2 transition-all duration-200',
                currentStep >= 1
                  ? 'bg-blue-600 border-blue-600 text-white shadow-md'
                  : 'border-gray-300 text-gray-400 bg-white'
              ]"
            >
              <span v-if="currentStep > 1" class="text-lg">✓</span>
              <span v-else class="text-sm font-semibold">1</span>
            </div>
            <span
              :class="[
                'mt-2 text-sm font-medium text-center',
                currentStep >= 1 ? 'text-gray-900' : 'text-gray-400'
              ]"
            >
              {{ __('Select Connection') }}
            </span>
          </div>
          
          <!-- Connector 1 -->
          <div class="flex-1 pt-6 px-8">
            <div
              :class="[
                'h-0.5 w-full transition-all duration-300',
                currentStep >= 2 ? 'bg-blue-600' : 'bg-gray-300'
              ]"
            ></div>
          </div>
          
          <!-- Step 2 -->
          <div class="flex flex-col items-center" style="min-width: 140px;">
            <div
              :class="[
                'flex items-center justify-center w-12 h-12 rounded-full border-2 transition-all duration-200',
                currentStep >= 2
                  ? 'bg-blue-600 border-blue-600 text-white shadow-md'
                  : 'border-gray-300 text-gray-400 bg-white'
              ]"
            >
              <span v-if="currentStep > 2" class="text-lg">✓</span>
              <span v-else class="text-sm font-semibold">2</span>
            </div>
            <span
              :class="[
                'mt-2 text-sm font-medium text-center',
                currentStep >= 2 ? 'text-gray-900' : 'text-gray-400'
              ]"
            >
              {{ __('Filter Conditions') }}
            </span>
          </div>
          
        </div>
      </div>
      <div class="min-h-[400px]">
        <!-- Step 1: Select ATS Connection -->
        <div v-if="currentStep === 1 && !showConnectionForm" class="space-y-4">
          <div class="flex items-center justify-between mb-4">
            <div class="text-sm text-gray-600">
              {{ __('Select an active ATS connection to sync positions from:') }}
            </div>
            <!-- <Button
              variant="solid"
              theme="gray"
              size="sm"
              @click="showConnectionForm = true"
            >
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
              {{ __('Create Connection') }}
            </Button> -->
          </div>
          
          <!-- Loading State -->
          <div v-if="loadingConnections" class="flex items-center justify-center py-12">
            <LoadingIndicator class="w-8 h-8" />
            <span class="ml-3 text-gray-600">{{ __('Loading connections...') }}</span>
          </div>
          
          <!-- Connections List -->
          <div v-else-if="atsConnections.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              v-for="connection in atsConnections"
              :key="connection.name"
              @click="selectConnection(connection)"
              :class="[
                'border rounded-lg p-4 cursor-pointer transition-all',
                selectedConnection?.name === connection.name
                  ? 'border-blue-500 bg-blue-50 shadow-sm'
                  : 'border-gray-200 hover:border-blue-300 hover:shadow-sm'
              ]"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <h4 class="font-medium text-gray-900">{{ connection.source_title }}</h4>
                  <p class="text-sm text-gray-500 mt-1">{{ connection.source_name }}</p>
                  <div class="flex items-center gap-2 mt-2">
                    <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {{ connection.status }}
                    </span>
                    <span class="text-xs text-gray-500">{{ connection.source_type }}</span>
                  </div>
                </div>
                <div
                  v-if="selectedConnection?.name === connection.name"
                  class="flex-shrink-0 w-5 h-5 rounded-full bg-blue-600 flex items-center justify-center"
                >
                  <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-else class="text-center py-12 border rounded-lg bg-gray-50">
            <FeatherIcon name="database" class="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p class="text-gray-500 mb-2">{{ __('No active ATS connections found') }}</p>
            <p class="text-sm text-gray-400 mb-4">
              {{ __('Please configure an ATS data source first.') }}
            </p>
            <Button
              variant="solid" theme="gray"
              @click="showConnectionForm = true"
            >
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
              {{ __('Create New Connection') }}
            </Button>
          </div>
          
          <!-- Sync History Section -->
          <div v-if="selectedConnection" class="mt-6 border-t pt-6">
            <div class="flex items-center justify-between mb-4">
              <h4 class="font-medium text-gray-900">{{ __('Sync History') }}</h4>
              <Button
                variant="outline"
                size="sm"
                @click="fetchSyncLogs"
                :loading="loadingSyncLogs"
              >
                <template #prefix>
                  <FeatherIcon name="refresh-cw" class="h-4 w-4" />
                </template>
                {{ __('Refresh') }}
              </Button>
            </div>
            
            <!-- Loading State -->
            <div v-if="loadingSyncLogs" class="flex items-center justify-center py-12">
              <LoadingIndicator class="w-8 h-8" />
              <span class="ml-3 text-gray-600">{{ __('Loading sync logs...') }}</span>
            </div>
            
            <!-- Sync Logs Table -->
            <div v-else-if="syncLogs.length > 0" class="border rounded-lg overflow-hidden overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {{ __('Status') }}
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {{ __('Records') }}
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {{ __('Start Time') }}
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {{ __('End Time') }}
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {{ __('Details') }}
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="log in syncLogs" :key="log.name" class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span
                        :class="[
                          'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                          getStatusClass(log.status)
                        ]"
                      >
                        {{ log.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div class="flex items-center gap-2">
                        <span class="text-green-600 font-medium">{{ log.success_count || 0 }}</span>
                        <span class="text-gray-400">/</span>
                        <span class="text-gray-600">{{ log.total_records || 0 }}</span>
                        <span v-if="log.failed_count > 0" class="text-red-600">({{ log.failed_count }} failed)</span>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatDateTime(log.start_time) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ log.end_time ? formatDateTime(log.end_time) : '-' }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500 truncate">
                      <div class="max-w-xs truncate" :title="log.details">
                        {{ log.details || '-' }}
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Empty State -->
            <div v-else class="text-center py-12 border rounded-lg bg-gray-50">
              <FeatherIcon name="clock" class="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p class="text-gray-500">{{ __('No sync history found') }}</p>
            </div>
          </div>
        </div>

        <!-- Create Connection Form -->
        <div v-if="currentStep === 1 && showConnectionForm" class="space-y-6">
          <!-- Back Button -->
          <div class="flex items-center gap-2 mb-4">
            <button
              @click="showConnectionForm = false"
              class="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-900"
            >
              <FeatherIcon name="arrow-left" class="h-4 w-4" />
              {{ __('Back to Connections') }}
            </button>
          </div>

          <!-- ATS Info Header -->
          <div class="bg-gray-50 rounded-lg p-4 flex items-start gap-3">
            <div class="flex-shrink-0 w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
              <FeatherIcon name="briefcase" class="w-6 h-6 text-red-600" />
            </div>
            <div>
              <h4 class="font-medium text-gray-900">MobiWork ATS</h4>
              <p class="text-sm text-gray-500 mt-1">
                {{ __('Connect MobiWork Applicant Tracking System') }}
              </p>
            </div>
          </div>

          <!-- Basic Information Section -->
          <div>
            <h4 class="text-sm font-semibold text-gray-900 mb-4">{{ __('Basic Information') }}</h4>
            
            <div class="space-y-4">
              <!-- Connection Title -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ __('Connection Title') }} <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="formData.source_title"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                  :placeholder="__('Enter connection title')"
                />
                <p v-if="errors.source_title" class="text-sm text-red-600 mt-1">{{ errors.source_title }}</p>
              </div>

              <!-- Same Site Checkbox -->
              <div class="flex items-start gap-2">
                <input
                  v-model="formData.same_site"
                  type="checkbox"
                  id="same_site"
                  class="mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <label for="same_site" class="text-sm text-gray-700">
                  <span class="font-medium">{{ __('Same Site') }}</span>
                  <p class="text-gray-500 mt-0.5">
                    {{ __('Check if this ATS runs on the same site (no need to enter API Base URL)') }}
                  </p>
                </label>
              </div>
            </div>
          </div>

          <!-- API Configuration Section -->
          <div>
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-sm font-semibold text-gray-900">{{ __('API Configuration') }}</h4>
            </div>

            <div class="space-y-4">
              <!-- API Base URL (conditional) -->
              <div v-if="!formData.same_site">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ __('API Base URL') }} <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="formData.api_base_url"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                  :placeholder="__('https://your-ats-domain.com')"
                />
                <p v-if="errors.api_base_url" class="text-sm text-red-600 mt-1">{{ errors.api_base_url }}</p>
              </div>

              <!-- API Key -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ __('API Key') }} <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="formData.api_key"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                  :placeholder="__('Enter your API key')"
                />
                <p v-if="errors.api_key" class="text-sm text-red-600 mt-1">{{ errors.api_key }}</p>
              </div>

              <!-- API Secret -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ __('API Secret') }} <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="formData.api_secret"
                  type="password"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                  :placeholder="__('Enter your API secret')"
                />
                <p v-if="errors.api_secret" class="text-sm text-red-600 mt-1">{{ errors.api_secret }}</p>
              </div>
            </div>
          </div>

          <!-- Info Box -->
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div class="flex items-start gap-2">
              <FeatherIcon name="shield" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <div class="text-sm">
                <p class="font-medium text-blue-900">{{ __('Secure API Connection') }}</p>
                <p class="text-blue-700 mt-1">
                  {{ __('This connection uses API Key authentication for secure data exchange. Your credentials are encrypted and never shared.') }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 2: Filter Conditions -->
        <div v-if="currentStep === 2" class="space-y-4">
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
            <div class="flex items-start">
              <FeatherIcon name="info" class="h-5 w-5 text-blue-600 mt-0.5 mr-2" />
              <div>
                <h4 class="text-sm font-medium text-blue-900">{{ __('Selected Connection') }}</h4>
                <p class="text-sm text-blue-700 mt-1">
                  {{ selectedConnection?.source_title }} ({{ selectedConnection?.source_name }})
                </p>
              </div>
            </div>
          </div>
          
          <ConditionsBuilder
            ref="conditionsBuilderRef"
            v-model="filterConditions"
            doctype="Mira Talent"
            :title="__('Filter Conditions')"
            :description="__('Add conditions to filter which positions to sync. Leave empty to sync all active positions.')"
            :show-preview="false"
            :validate-on-change="false"
          />
        </div>

      </div>
    </template>

    <template #actions>
      <div class="flex justify-between items-center pt-4 border-t border-gray-200">
        <Button
          v-if="currentStep > 1 && !showConnectionForm"
          variant="outline"
          theme="gray"
          @click="previousStep"
        >
          <template #prefix>
            <FeatherIcon name="chevron-left" class="h-4 w-4" />
          </template>
          {{ __('Back') }}
        </Button>
        <div v-else></div>
        
        <div class="flex gap-2">
          <Button
            variant="outline"
            theme="gray"
            @click="closeDialog"
          >
            {{ __('Cancel') }}
          </Button>
          
          <!-- Show Create Connection button when in form view -->
          <Button
            v-if="showConnectionForm"
            variant="solid"
            theme="gray"
            @click="handleCreateConnection"
            :loading="creating"
          >
            {{ __('Connect ATS') }}
          </Button>
          
          <!-- Show Next button for Step 1 (not in form) -->
          <Button
            v-else-if="currentStep < 2"
            variant="solid"
            theme="gray"
            @click="nextStep"
            :disabled="!canProceed"
          >
            {{ __('Next') }}
            <template #suffix>
              <FeatherIcon name="chevron-right" class="h-4 w-4" />
            </template>
          </Button>
          
          <!-- Show Start Sync button for Step 2 -->
          <Button
            v-else
            variant="solid"
            theme="gray"
            @click="startSync"
            :disabled="!canProceed"
            :loading="syncing"
          >
            {{ __('Start Sync') }}
          </Button>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, FeatherIcon, LoadingIndicator } from 'frappe-ui'
import ConditionsBuilder from '@/components/ConditionsFilter/ConditionsBuilder.vue'
import { useToast } from '@/composables/useToast'
import { call } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const { showSuccess, showError } = useToast()

// State
const currentStep = ref(1)
const isOpen = ref(props.modelValue)
const loadingConnections = ref(false)
const loadingSyncLogs = ref(false)
const syncing = ref(false)
const atsConnections = ref([])
const selectedConnection = ref(null)
const filterConditions = ref([])
const syncLogs = ref([])
const conditionsBuilderRef = ref(null)
const showConnectionForm = ref(false)
const creating = ref(false)
const formData = ref({
  source_title: '',
  source_type: 'ATS',
  source_name: 'MBW ATS',
  same_site: false,
  api_base_url: '',
  auth_method: 'API Key',
  api_key: '',
  api_secret: '',
  sync_direction: 'Both',
  status: 'Active',
  is_active: 1
})
const errors = ref({})

// Computed
const canProceed = computed(() => {
  if (currentStep.value === 1) {
    return selectedConnection.value !== null
  }
  return true
})

// Watch dialog state
watch(() => props.modelValue, (newValue) => {
  isOpen.value = newValue
  if (newValue) {
    resetDialog()
    fetchATSConnections()
  }
})

watch(isOpen, (newValue) => {
  emit('update:modelValue', newValue)
})

// Methods
const resetDialog = () => {
  currentStep.value = 1
  selectedConnection.value = null
  filterConditions.value = []
  syncLogs.value = []
  syncing.value = false
  showConnectionForm.value = false
  resetFormData()
}

const resetFormData = () => {
  formData.value = {
    source_title: '',
    source_type: 'ATS',
    source_name: 'MBW ATS',
    same_site: false,
    api_base_url: '',
    auth_method: 'API Key',
    api_key: '',
    api_secret: '',
    sync_direction: 'Both',
    status: 'Active',
    is_active: 1
  }
  errors.value = {}
}

const validateForm = () => {
  errors.value = {}
  
  if (!formData.value.source_title) {
    errors.value.source_title = __('Connection title is required')
  }
  
  if (!formData.value.same_site && !formData.value.api_base_url) {
    errors.value.api_base_url = __('API Base URL is required when not using same site')
  }
  
  if (!formData.value.api_key) {
    errors.value.api_key = __('API Key is required')
  }
  
  if (!formData.value.api_secret) {
    errors.value.api_secret = __('API Secret is required')
  }
  
  return Object.keys(errors.value).length === 0
}

const handleCreateConnection = async () => {
  if (!validateForm()) {
    showError(__('Please fill in all required fields'))
    return
  }
  
  creating.value = true
  try {
    const response = await call('frappe.client.insert', {
      doc: {
        doctype: 'Mira Data Source',
        ...formData.value
      }
    })
    
    if (response) {
      showSuccess(__('ATS connection created successfully'))
      // Hide form and reload connections
      showConnectionForm.value = false
      await fetchATSConnections()
      // Auto-select the newly created connection
      selectedConnection.value = response
      // Load sync logs for this connection
      fetchSyncLogs()
      resetFormData()
    }
  } catch (error) {
    console.error('Error creating ATS connection:', error)
    showError(error.message || __('Failed to create ATS connection'))
  } finally {
    creating.value = false
  }
}

const closeDialog = () => {
  isOpen.value = false
  emit('update:modelValue', false)
}

const selectConnection = (connection) => {
  selectedConnection.value = connection
  // Load sync logs for this connection
  fetchSyncLogs()
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const nextStep = async () => {
  if (currentStep.value === 1) {
    // Move to filter conditions
    currentStep.value = 2
  }
}

const fetchATSConnections = async () => {
  loadingConnections.value = true
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Mira Data Source',
      filters: {
        source_type: 'ATS',
        is_active: 1,
        status: 'Active'
      },
      fields: ['name', 'source_title', 'source_name', 'source_type', 'status'],
      limit_page_length: 50
    })
    
    atsConnections.value = response || []
  } catch (error) {
    console.error('Error fetching ATS connections:', error)
    showError(__('Failed to load ATS connections'))
  } finally {
    loadingConnections.value = false
  }
}

const startSync = async () => {
  if (!selectedConnection.value) {
    showError(__('Please select a connection'))
    return
  }
  
  syncing.value = true
  try {
    const response = await call('mbw_mira.api.sync_segment.sync_positions', {
      data_source_name: selectedConnection.value.name
    })
    
    if (response.status === 'success') {
      showSuccess(response.message || __('Sync started successfully. The process is running in the background.'))
      emit('success')
      // Reset all selections and go back to step 1
      selectedConnection.value = null
      filterConditions.value = []
      syncLogs.value = []
      currentStep.value = 1
    } else {
      showError(response.message || __('Sync failed'))
    }
  } catch (error) {
    console.error('Error starting sync:', error)
    showError(error.message || __('Failed to start sync'))
  } finally {
    syncing.value = false
  }
}

const fetchSyncLogs = async () => {
  if (!selectedConnection.value) return
  
  loadingSyncLogs.value = true
  try {
    const response = await call('frappe.client.get_list', {
      doctype: 'Mira ATS Sync Log',
      filters: {
        connection: selectedConnection.value.name,
        sync_type: 'Position to Segment'
      },
      fields: [
        'name',
        'status',
        'start_time',
        'end_time',
        'total_records',
        'success_count',
        'failed_count',
        'details'
      ],
      order_by: 'start_time desc',
      limit_page_length: 10
    })
    
    syncLogs.value = response || []
  } catch (error) {
    console.error('Error fetching sync logs:', error)
    showError(__('Failed to load sync history'))
  } finally {
    loadingSyncLogs.value = false
  }
}

const getStatusClass = (status) => {
  const statusMap = {
    'In Progress': 'bg-blue-100 text-blue-800',
    'Completed': 'bg-green-100 text-green-800',
    'Partially Completed': 'bg-yellow-100 text-yellow-800',
    'Failed': 'bg-red-100 text-red-800'
  }
  return statusMap[status] || 'bg-gray-100 text-gray-800'
}

const formatDateTime = (dateTime) => {
  if (!dateTime) return '-'
  const date = new Date(dateTime)
  return date.toLocaleString('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>
