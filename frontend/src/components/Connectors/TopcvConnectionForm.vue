<template>
  <div class="topcv-connection-form">
    <!-- Platform Info Banner -->
    <!-- <div class="flex items-center gap-4 p-4 bg-purple-50 rounded-lg mb-6">
      <div class="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center">
        <FeatherIcon name="briefcase" class="w-6 h-6 text-white" />
      </div>
      <div>
        <h3 class="font-semibold text-gray-900">{{__('TopCV Integration')}}</h3>
        <p class="text-sm text-gray-600">
          {{ isEdit ? __('Update your TopCV connection settings') : __('Connect your TopCV account to manage job postings') }}
        </p>
      </div>
    </div> -->

    <!-- Current Connected Accounts (Show in edit mode) -->
    <div v-if="isEdit && hasConnectedAccounts" class="space-y-4 mb-6">
      <h4 class="font-medium text-gray-900 border-b pb-2">{{ __('Connected Accounts') }}</h4>

      <div class="bg-green-50 rounded-lg p-4">
        <div class="flex items-center gap-2 mb-3">
          <FeatherIcon name="check-circle" class="w-5 h-5 text-green-600" />
          <h5 class="font-medium text-green-800">{{ __('Active TopCV Accounts') }}</h5>
        </div>

        <div class="space-y-2">
          <div v-for="account in connectedAccountsList" :key="account.external_account_id"
            class="flex items-center justify-between p-3 bg-white rounded border">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                <FeatherIcon name="briefcase" class="w-4 h-4 text-purple-600" />
              </div>
              <div>
                <div class="font-medium text-gray-900">{{ account.account_name }}</div>
                <div class="text-xs text-gray-500">{{ account.account_type }} • ID: {{ account.external_account_id }}
                </div>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <Badge v-if="account.is_primary" variant="success" size="sm">{{ __('Primary') }}</Badge>
              <Badge :variant="account.is_active ? 'success' : 'gray'" size="sm">
                {{ account.is_active ? __('Active') : __('Inactive') }}
              </Badge>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Connection Form -->
    <div class="space-y-6">
      <!-- Basic Information -->
      <!-- <div class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">{{ __('Basic Information') }}</h4>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormControl :label="__('Tenant Name')" v-model="localFormData.tenant_name"
            :placeholder="__('Your organization tenant name')" :required="true" :error="validationErrors.tenant_name"
            :description="__('Unique identifier for your organization')" />
        </div>
      </div> -->

      <!-- TopCV API Configuration -->
      <div class="space-y-4">
        <div class="flex items-center justify-between border-b pb-2">
          <h4 class="font-medium text-gray-900">{{ __('TopCV API Configuration') }}</h4>
          <Button @click="showApiSetupGuide = !showApiSetupGuide" variant="ghost" size="sm">
            <template #prefix>
              <FeatherIcon name="help-circle" class="w-4 h-4" />
            </template>
            {{ __('Setup Guide') }}
          </Button>
        </div>

        <!-- Setup Guide (Collapsible) -->
        <div v-if="showApiSetupGuide" class="bg-gray-50 rounded-lg p-4 space-y-3">
          <h5 class="font-medium text-gray-800">{{ __('TopCV API Setup Instructions:') }}</h5>
          <ol class="text-sm text-gray-700 space-y-2 list-decimal list-inside">
            <li>{{ __('Login to your TopCV employer account') }}</li>
            <li>{{ __('Navigate to "API Settings" or "Developer Settings" section') }}</li>
            <li>{{ __('Generate or retrieve your API Key and Secret Key') }}</li>
            <li>{{ __('Copy the credentials and paste them in the form below') }}</li>
            <li>{{ __('Configure webhook URL for receiving notifications') }}</li>
          </ol>
          <div class="text-xs text-gray-600 bg-white p-2 rounded border">
            <strong>{{ __('Webhook URL:') }}</strong> {{ computedHookUrl }}
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormControl :label="__('API Key')" type="password" v-model="localFormData.api_key"
            :placeholder="__('Enter your TopCV API Key')" :required="true" :error="validationErrors.api_key"
            :description="__('Get this from TopCV API settings')" />

          <FormControl :label="__('Secret Key')" type="password" v-model="localFormData.client_secret"
            :placeholder="__('Enter your TopCV Secret Key')" :required="true" :error="validationErrors.client_secret"
            :description="__('Keep this secure - never share publicly')" />
        </div>

        <!-- API Security Info -->
        <div class="bg-blue-50 rounded-lg p-4">
          <div class="flex items-start gap-3">
            <FeatherIcon name="shield-check" class="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <h5 class="font-medium text-blue-900">{{ __('Secure API Connection') }}</h5>
              <p class="text-sm text-blue-700 mt-1">
                {{ __('Your API credentials are encrypted and stored securely. They are used only for authorized TopCV operations.')}}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Connection Settings -->
      <!-- <div class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Connection Settings')}}</h4>
        
        <FormControl
          :label="__('Hook URL')"
          v-model="localFormData.hook_url"
          :placeholder="__('https://your-domain.com/api/webhooks/topcv')"
          :required="true"
          :error="validationErrors.hook_url"
          :description="__('URL where TopCV will send webhook notifications')"
        />

        <div class="space-y-3">
          <h5 class="text-sm font-medium text-gray-700">{{__('TopCV Permissions')}}</h5>
          <div class="space-y-2">
            <div 
              v-for="permission in availablePermissions" 
              :key="permission.key"
              class="flex items-center space-x-3"
            >
              <input
                :id="`permission-${permission.key}`"
                type="checkbox"
                :checked="localFormData.permissions.includes(permission.key)"
                @change="togglePermission(permission.key)"
                class="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
              >
              <label :for="`permission-${permission.key}`" class="text-sm">
                <span class="font-medium text-gray-900">{{ __(permission.label) }}</span>
                <span class="block text-xs text-gray-500">{{ __(permission.description) }}</span>
              </label>
            </div>
          </div>
        </div>
      </div> -->

      <!-- Job Management Settings -->
      <!-- <div class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Job Management Settings')}}</h4>
        
        <div class="space-y-3">
          <div class="flex items-center space-x-3">
            <input
              id="auto-post-jobs"
              type="checkbox"
              v-model="localFormData.auto_post_jobs"
              class="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
            >
            <label for="auto-post-jobs" class="text-sm">
              <span class="font-medium text-gray-900">{{__('Auto-post jobs')}}</span>
              <span class="block text-xs text-gray-500">{{__('Automatically post new jobs to TopCV')}}</span>
            </label>
          </div>

          <div class="flex items-center space-x-3">
            <input
              id="auto-import-applications"
              type="checkbox"
              v-model="localFormData.auto_import_applications"
              class="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
            >
            <label for="auto-import-applications" class="text-sm">
              <span class="font-medium text-gray-900">{{__('Auto-import applications')}}</span>
              <span class="block text-xs text-gray-500">{{__('Automatically import job applications from TopCV')}}</span>
            </label>
          </div>

          <div class="flex items-center space-x-3">
            <input
              id="sync-candidate-profiles"
              type="checkbox"
              v-model="localFormData.sync_candidate_profiles"
              class="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
            >
            <label for="sync-candidate-profiles" class="text-sm">
              <span class="font-medium text-gray-900">{{__('Sync candidate profiles')}}</span>
              <span class="block text-xs text-gray-500">{{__('Import candidate CV and profile information')}}</span>
            </label>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormControl
            :label="__('Default job duration (days)')"
            type="number"
            v-model="localFormData.job_duration"
            :placeholder="__('30')"
            :error="validationErrors.job_duration"
            :description="__('How long jobs stay active on TopCV')"
          />

          <FormControl
            :label="__('Sync frequency')"
            type="select"
            v-model="localFormData.sync_frequency"
            :options="syncFrequencyOptions"
            :description="__('How often to sync data from TopCV')"
          />
        </div>
      </div> -->

      <!-- Advanced Settings -->
      <!-- <div v-if="showAdvancedSettings" class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Advanced Settings')}}</h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormControl
            :label="__('Connection timeout (seconds)')"
            type="number"
            v-model="localFormData.timeout"
            :placeholder="__('30')"
            :error="validationErrors.timeout"
            :description="__('Request timeout for TopCV API calls')"
          />
          
          <FormControl
            :label="__('Max retry attempts')"
            type="number"
            v-model="localFormData.max_retries"
            :placeholder="__('3')"
            :error="validationErrors.max_retries"
            :description="__('Maximum retry attempts for failed requests')"
          />
        </div>

        <div class="space-y-3">
          <div class="flex items-center space-x-3">
            <input
              id="enable-resume-search"
              type="checkbox"
              v-model="localFormData.enable_resume_search"
              class="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
            >
            <label for="enable-resume-search" class="text-sm">
              <span class="font-medium text-gray-900">{{__('Enable resume search')}}</span>
              <span class="block text-xs text-gray-500">{{__('Access TopCV resume database for candidate search')}}</span>
            </label>
          </div>

          <div class="flex items-center space-x-3">
            <input
              id="debug-mode"
              type="checkbox"
              v-model="localFormData.debug_mode"
              class="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
            >
            <label for="debug-mode" class="text-sm">
              <span class="font-medium text-gray-900">{{__('Enable debug mode')}}</span>
              <span class="block text-xs text-gray-500">{{__('Enable detailed logging for troubleshooting')}}</span>
            </label>
          </div>
        </div>

        <FormControl
          :label="__('Daily search limit')"
          type="number"
          v-model="localFormData.daily_search_limit"
          :placeholder="__('100')"
          :description="__('Maximum resume searches per day')"
        />
      </div> -->

      <!-- Test Connection -->
      <div v-if="isEdit" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div class="flex items-center justify-between">
          <div>
            <h5 class="font-medium text-gray-900">{{ __('Test Connection') }}</h5>
            <p class="text-sm text-gray-600">{{ __('Verify that your TopCV connection is working') }}</p>
          </div>
          <Button @click="testConnection" variant="outline" size="sm" :loading="isTesting">
            <template #prefix>
              <FeatherIcon name="zap" class="w-4 h-4" />
            </template>
            {{ __('Test') }}
          </Button>
        </div>

        <div v-if="testResult" class="mt-3 p-3 rounded border"
          :class="testResult.success ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'">
          <div class="flex items-center gap-2">
            <FeatherIcon :name="testResult.success ? 'check-circle' : 'x-circle'" class="w-4 h-4"
              :class="testResult.success ? 'text-green-600' : 'text-red-600'" />
            <span class="text-sm font-medium" :class="testResult.success ? 'text-green-800' : 'text-red-800'">
              {{ testResult.message }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex justify-between items-center pt-6 border-t">
      <!-- <Button
        @click="toggleAdvancedSettings"
        variant="ghost"
        size="sm"
      >
        {{ showAdvancedSettings ? __('Hide') : __('Show') }} {{__('Advanced Settings')}}
      </Button> -->

      <div class="flex gap-3">
        <Button @click="handleCancel" variant="ghost">
          {{ __('Cancel') }}
        </Button>

        <Button @click="handleSubmit" variant="solid" :loading="isSubmitting" :disabled="!isFormValid">
          {{ isEdit ? __('Update Connection') : __('Connect TopCV') }}
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick, shallowRef } from 'vue'
import { Button, FormControl, FeatherIcon, Badge, toast, call } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  },
  platform: {
    type: Object,
    required: true
  },
  isEdit: {
    type: Boolean,
    default: false
  },
  existingConnection: {
    type: Object,
    default: () => ({})
  },
  connectedAccounts: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'submit', 'cancel'])
import { usersStore } from "@/stores/user";
const { userResource, allUsers, getUser } = usersStore();
// State
const isSubmitting = ref(false)
const isTesting = ref(false)
const showApiSetupGuide = ref(false)
const showAdvancedSettings = ref(false)
const testResult = shallowRef(null)
const validationErrors = ref({})

// Form data
const defaultFormData = {
  user_email: getUser?.data?.email,
  full_name: getUser?.data?.full_name,
  tenant_name: '',
  api_key: '',
  client_secret: '',
  hook_url: '',
  redirect_url: '',
  timeout: 30,
  max_retries: 3,
  permissions: ['job_posting', 'application_management', 'candidate_search'],
  auto_post_jobs: true,
  auto_import_applications: true,
  sync_candidate_profiles: true,
  job_duration: 30,
  sync_frequency: 'Hourly',
  enable_resume_search: false,
  debug_mode: false,
  daily_search_limit: 100
}

const localFormData = ref({ ...defaultFormData })

// Available permissions
const availablePermissions = [
  {
    key: 'job_posting',
    label: 'Job Posting',
    description: 'Create and manage job postings'
  },
  {
    key: 'application_management',
    label: 'Application Management',
    description: 'Access and manage job applications'
  },
  {
    key: 'candidate_search',
    label: 'Candidate Search',
    description: 'Search and access resume database'
  },
  {
    key: 'company_profile',
    label: 'Company Profile',
    description: 'Manage company profile and information'
  },
  {
    key: 'analytics',
    label: 'Analytics & Reports',
    description: 'Access hiring analytics and reports'
  },
  {
    key: 'bulk_operations',
    label: 'Bulk Operations',
    description: 'Perform bulk operations on jobs and applications'
  }
]

// Sync frequency options
const syncFrequencyOptions = [
  { label: __('Every 5 minutes'), value: 'Every 5 minutes' },
  { label: __('Every 15 minutes'), value: 'Every 15 minutes' },
  { label: __('Every 30 minutes'), value: 'Every 30 minutes' },
  { label: __('Every hour'), value: 'Hourly' },
  { label: __('Real-time'), value: 'Real-time' },
  { label: __('Daily'), value: 'daily' }
]

// Computed
const computedHookUrl = computed(() => {
  return localFormData.value.hook_url || ''
})

const computedRedirectUrl = computed(() => {
  return localFormData.value.redirect_url || ''
})

const isFormValid = computed(() => {
  const form = localFormData.value
  console.log(form)
  return !!(
    form.api_key?.trim() &&
    form.client_secret?.trim() &&
    Object.keys(validationErrors.value).length === 0
  )
})

const hasConnectedAccounts = computed(() => {
  return connectedAccountsList.value.length > 0
})

const connectedAccountsList = computed(() => {
  return props.connectedAccounts.length > 0
    ? props.connectedAccounts
    : props.existingConnection?.accounts || []
})

// Helper methods
const isValidUrl = (string) => {
  try {
    new URL(string)
    return true
  } catch (_) {
    return false
  }
}

const validateForm = () => {
  const errors = {}
  const form = localFormData.value

  

  if (!form.api_key?.trim()) {
    errors.api_key = __('API Key is required')
  }

  if (!form.client_secret?.trim()) {
    errors.client_secret = __('Secret Key is required')
  }



  // if (form.timeout && (form.timeout < 5 || form.timeout > 300)) {
  //   errors.timeout = __('Timeout should be between 5 and 300 seconds')
  // }

  // if (form.max_retries && (form.max_retries < 1 || form.max_retries > 10)) {
  //   errors.max_retries = __('Max retries should be between 1 and 10')
  // }

  // if (form.job_duration && (form.job_duration < 1 || form.job_duration > 365)) {
  //   errors.job_duration = __('Job duration should be between 1 and 365 days')
  // }

  // if (form.daily_search_limit && (form.daily_search_limit < 1 || form.daily_search_limit > 1000)) {
  //   errors.daily_search_limit = __('Daily search limit should be between 1 and 1000')
  // }

  validationErrors.value = errors
  return Object.keys(errors).length === 0
}

const togglePermission = (permissionKey) => {
  const permissions = [...localFormData.value.permissions]
  const index = permissions.indexOf(permissionKey)

  if (index > -1) {
    permissions.splice(index, 1)
  } else {
    permissions.push(permissionKey)
  }

  localFormData.value.permissions = permissions
  emitModelUpdate()
}

const toggleAdvancedSettings = () => {
  showAdvancedSettings.value = !showAdvancedSettings.value
}

// API Methods - Following Facebook pattern
const testConnection = async () => {
  if (!isFormValid.value) {
    toast({
      title: __('Validation Error'),
      text: __('Please fix form errors before testing'),
      icon: 'x',
      iconClasses: 'text-red-600'
    })
    return
  }

  isTesting.value = true
  testResult.value = null

  try {
    const response = await call('mbw_mira.api.external_connections.test_connection', {
      tenant_name: localFormData.value.tenant_name,
      connection_id:props.existingConnection.connection_id
    })

    if (response?.status === 'Success') {
      testResult.value = {
        success: true,
        message: __('Connection test successful! TopCV API is configured properly.')
      }
    } else {
      testResult.value = {
        success: false,
        message: response?.message || __('Connection test failed')
      }
    }

  } catch (error) {
    console.error('Connection test error:', error)
    testResult.value = {
      success: false,
      message: error.message || __('Failed to test connection')
    }
  } finally {
    isTesting.value = false
  }
}

// Event handlers
const handleSubmit = async () => {
  if (!validateForm()) {
    toast({
      title: __('Validation Error'),
      text: __('Please fix the errors in the form'),
      icon: 'x',
      iconClasses: 'text-red-600'
    })
    return
  }

  isSubmitting.value = true

  const submitData = {
    tenant_name: localFormData.value.tenant_name.trim(),
    api_key: localFormData.value.api_key.trim(),
    secret_key: localFormData.value.client_secret.trim(),
    hook_url: localFormData.value.hook_url.trim(),
    user_email:localFormData.value.user_email,
    full_name:localFormData.value.full_name
  }
  console.log(submitData)
  emit('submit', submitData)

}

const handleCancel = () => {
  if (props.isEdit && props.existingConnection) {
    loadExistingData()
  } else {
    Object.assign(localFormData.value, { ...defaultFormData })
  }

  validationErrors.value = {}
  testResult.value = null
  emit('cancel')
}

const emitModelUpdate = () => {
  nextTick(() => {
    emit('update:modelValue', { ...localFormData.value })
  })
}

const loadExistingData = () => {
  if (props.existingConnection) {
    const existing = props.existingConnection
    Object.assign(localFormData.value, {
      tenant_name: existing.tenant_name || '',
      api_key: existing.api_key || '',
      client_secret: existing.secret_key || '',
      hook_url: existing.hook_url || '',
      redirect_url: existing.redirect_url || computedRedirectUrl.value,
      timeout: existing.timeout || 30,
      max_retries: existing.max_retries || 3,
      permissions: existing.permissions || [...defaultFormData.permissions],
      auto_post_jobs: existing.auto_post_jobs ?? true,
      auto_import_applications: existing.auto_import_applications ?? true,
      sync_candidate_profiles: existing.sync_candidate_profiles ?? true,
      job_duration: existing.job_duration || 30,
      sync_frequency: existing.sync_frequency || 'Hourly',
      enable_resume_search: existing.enable_resume_search || false,
      debug_mode: existing.debug_mode || false,
      daily_search_limit: existing.daily_search_limit || 100
    })
  }
}

// Watchers
let updateTimeout = null
watch(localFormData, () => {
  if (updateTimeout) {
    clearTimeout(updateTimeout)
  }

  updateTimeout = setTimeout(() => {
    validateForm()
    emitModelUpdate()
  }, 300)
}, {
  deep: true,
  flush: 'post'
})

watch(() => props.modelValue, (newValue) => {
  if (newValue && typeof newValue === 'object') {
    const currentDataString = JSON.stringify(localFormData.value)
    const newDataString = JSON.stringify({ ...defaultFormData, ...newValue })

    if (currentDataString !== newDataString) {
      Object.assign(localFormData.value, { ...defaultFormData, ...newValue })
    }
  }
}, {
  immediate: false,
  deep: true
})

// Lifecycle
onMounted(() => {
  if (props.isEdit && props.existingConnection) {
    loadExistingData()
  } else if (props.modelValue && Object.keys(props.modelValue).length > 0) {
    Object.assign(localFormData.value, { ...defaultFormData, ...props.modelValue })
  }

  if (!localFormData.value.redirect_url) {
    localFormData.value.redirect_url = computedRedirectUrl.value
  }

  if (!localFormData.value.hook_url) {
    localFormData.value.hook_url = computedHookUrl.value
  }

  nextTick(() => {
    validateForm()
    emitModelUpdate()
  })
})
</script>

<style scoped>
.topcv-connection-form {
  max-width: 100%;
}

:deep(.form-control) {
  margin-bottom: 0;
}

:deep(.form-control .form-label) {
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

:deep(.form-control .form-input) {
  border-radius: 0.5rem;
  border: 1px solid #d1d5db;
  padding: 0.75rem;
  transition: all 0.2s;
}

:deep(.form-control .form-input:focus) {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

:deep(.form-control .form-error) {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

:deep(.form-control .form-help) {
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.grid {
  min-height: 0;
}

.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}
</style>