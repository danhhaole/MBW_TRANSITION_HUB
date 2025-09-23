<template>
  <div class="facebook-connection-form">
    <!-- Platform Info Banner -->
    <div class="flex items-center gap-4 p-4 bg-blue-50 rounded-lg mb-6">
      <div class="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center">
        <FeatherIcon name="facebook" class="w-6 h-6 text-white" />
      </div>
      <div>
        <h3 class="font-semibold text-gray-900">{{__('Facebook Integration')}}</h3>
        <p class="text-sm text-gray-600">
          {{ isEdit ? __('Update your Facebook connection settings') : __('Connect your Facebook account to manage pages and posts') }}
        </p>
      </div>
    </div>

    <!-- Connection Form -->
    <div class="space-y-6">
      <!-- Basic Information -->
      <div class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Basic Information')}}</h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- <FormControl
            :label="__('Tenant Name')"
            v-model="localFormData.tenant_name"
            :placeholder="__('Your organization name')"
            :required="true"
            :error="validationErrors.tenant_name"
          /> -->
          
          <FormControl
            :label="__('User Email')"
            type="email"
            v-model="localFormData.user_email"
            :placeholder="__('your-email@domain.com')"
            :required="true"
            :error="validationErrors.user_email"
          />
        </div>

        <FormControl
          :label="__('Full Name')"
          v-model="localFormData.full_name"
          :placeholder="__('Your full name')"
          :required="true"
          :error="validationErrors.full_name"
        />
      </div>

      <!-- Current Connected Accounts (Show in edit mode) -->
      <div v-if="isEdit && (props.connectedAccounts.length > 0 || props.existingConnection?.accounts?.length > 0)" class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Connected Accounts')}}</h4>
        
        <div class="bg-green-50 rounded-lg p-4">
          <div class="flex items-center gap-2 mb-3">
            <FeatherIcon name="check-circle" class="w-5 h-5 text-green-600" />
            <h5 class="font-medium text-green-800">{{__('Active Facebook Accounts')}}</h5>
          </div>
          
          <div class="space-y-2">
            <div 
              v-for="account in (props.connectedAccounts.length > 0 ? props.connectedAccounts : props.existingConnection?.accounts || [])" 
              :key="account.external_account_id"
              class="flex items-center justify-between p-3 bg-white rounded border"
            >
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <FeatherIcon name="facebook" class="w-4 h-4 text-blue-600" />
                </div>
                <div>
                  <div class="font-medium text-gray-900">{{ account.account_name }}</div>
                  <div class="text-xs text-gray-500">{{ account.account_type }} • ID: {{ account.external_account_id }}</div>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <Badge v-if="account.is_primary" variant="success" size="sm">{{__('Primary')}}</Badge>
                <Badge :variant="account.is_active ? 'success' : 'gray'" size="sm">
                  {{ account.is_active ? __('Active') : __('Inactive') }}
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="space-y-4">
        <div class="flex items-center justify-between border-b pb-2">
          <h4 class="font-medium text-gray-900">{{__('OAuth Configuration')}}</h4>
          <Button
            @click="showAppSetupGuide = !showAppSetupGuide"
            variant="ghost"
            size="sm"
          >
            <template #prefix>
              <FeatherIcon name="help-circle" class="w-4 h-4" />
            </template>
            {{__('Setup Guide')}}
          </Button>
        </div>

        <!-- Setup Guide (Collapsible) -->
        <div v-if="showAppSetupGuide" class="bg-gray-50 rounded-lg p-4 space-y-3">
          <h5 class="font-medium text-gray-800">{{__('OAuth Setup Instructions:')}}</h5>
          <ol class="text-sm text-gray-700 space-y-2 list-decimal list-inside">
            <li>{{__('Contact system administrator for OAuth configuration')}}</li>
            <li>{{__('Your organization\'s Facebook App will be configured centrally')}}</li>
            <li>{{__('Connection will be established through secure OAuth flow')}}</li>
            <li>{{__('No sensitive credentials need to be entered manually')}}</li>
          </ol>
          <div class="text-xs text-gray-600 bg-white p-2 rounded border">
            <strong>{{__('Callback URL:')}}</strong> {{ computedRedirectUrl }}
          </div>
        </div>

        <!-- OAuth Connection Info -->
        <div class="bg-blue-50 rounded-lg p-4">
          <div class="flex items-start gap-3">
            <FeatherIcon name="shield-check" class="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <h5 class="font-medium text-blue-900">{{__('Secure OAuth Connection')}}</h5>
              <p class="text-sm text-blue-700 mt-1">
                {{__('This connection uses OAuth 2.0 for secure authentication. Your Facebook credentials are never stored on our servers.')}}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Advanced Settings -->
      <div v-if="showAdvancedSettings" class="space-y-4">
        <h4 class="font-medium text-gray-900 border-b pb-2">{{__('Advanced Settings')}}</h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormControl
            :label="__('Connection Timeout (seconds)')"
            type="number"
            v-model="localFormData.timeout"
            :placeholder="__('30')"
            :error="validationErrors.timeout"
          />
          
          <FormControl
            :label="__('Max Retry Attempts')"
            type="number"
            v-model="localFormData.max_retries"
            :placeholder="__('3')"
            :error="validationErrors.max_retries"
          />
        </div>

        <div class="flex items-center space-x-3">
          <input
            id="auto-sync"
            type="checkbox"
            v-model="localFormData.auto_sync_accounts"
            class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          >
          <label for="auto-sync" class="text-sm">
            <span class="font-medium text-gray-900">{{__('Auto-sync accounts')}}</span>
            <span class="block text-xs text-gray-500">{{__('Automatically sync Facebook pages and accounts')}}</span>
          </label>
        </div>
      </div>

      <!-- Test Connection -->
      <div v-if="isEdit" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div class="flex items-center justify-between">
          <div>
            <h5 class="font-medium text-gray-900">{{__('Test Connection')}}</h5>
            <p class="text-sm text-gray-600">{{__('Verify that your Facebook connection is working')}}</p>
          </div>
          <Button
            @click="testConnection"
            variant="outline"
            size="sm"
            :loading="isTesting"
          >
            <template #prefix>
              <FeatherIcon name="zap" class="w-4 h-4" />
            </template>
            {{__('Test')}}
          </Button>
        </div>
        
        <div v-if="testResult" class="mt-3 p-3 rounded border" :class="testResult.success ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'">
          <div class="flex items-center gap-2">
            <FeatherIcon 
              :name="testResult.success ? 'check-circle' : 'x-circle'" 
              class="w-4 h-4"
              :class="testResult.success ? 'text-green-600' : 'text-red-600'"
            />
            <span class="text-sm font-medium" :class="testResult.success ? 'text-green-800' : 'text-red-800'">
              {{ testResult.message }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex justify-between items-center pt-6 border-t">
      <Button
        @click="toggleAdvancedSettings"
        variant="ghost"
        size="sm"
      >
        {{ showAdvancedSettings ? __('Hide') : __('Show') }} {{__('Advanced Settings')}}
      </Button>
      
      <div class="flex gap-3">
        <Button
          @click="handleCancel"
          variant="ghost"
        >
          {{__('Cancel')}}
        </Button>
        
        <Button
          @click="handleSubmit"
          variant="solid"
          :loading="isSubmitting"
          :disabled="!isFormValid"
        >
          {{ isEdit ? __('Update Connection') : __('Connect Facebook') }}
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick, shallowRef } from 'vue'
import { Button, FormControl, FeatherIcon, call } from 'frappe-ui'
import useToast from '@/composables/useToast'

// Props
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

// Emits
const emit = defineEmits(['update:modelValue', 'submit', 'cancel'])
import { usersStore } from "@/stores/user";
const { warning: toastWarning } = useToast()
// Reactive state
const isSubmitting = ref(false)
const isTesting = ref(false)
const showAppSetupGuide = ref(false)
const showAdvancedSettings = ref(false)
const testResult = shallowRef(null)
const validationErrors = ref({})
const { userResource, allUsers, getUser } = usersStore();
// Default form structure - updated to remove App ID/Secret
const defaultFormData = {
  tenant_name: '',
  user_email: getUser?.data?.email,
  full_name: getUser?.data?.full_name,
  hook_url: '',
  redirect_url: '',
  timeout: 30,
  max_retries: 3,
  permissions: ['pages_manage_posts', 'pages_read_engagement'],
  auto_sync_accounts: true
}

// Local form data - avoid direct v-model binding to prevent loops
const localFormData = ref({ ...defaultFormData })

// Available Facebook permissions
const availablePermissions = [
  {
    key: 'pages_manage_posts',
    label: __('Manage Page Posts'),
    description: __('Create, edit and delete posts on connected pages')
  },
  {
    key: 'pages_read_engagement',
    label: __('Read Page Engagement'),
    description: __('View likes, comments, and engagement metrics')
  },
  {
    key: 'pages_show_list',
    label: __('List Pages'),
    description: __('Access list of pages user manages')
  },
  {
    key: 'pages_manage_metadata',
    label: __('Manage Page Info'),
    description: __('Update page information and settings')
  },
  {
    key: 'pages_read_user_content',
    label: __('Read User Content'),
    description: __('Read content posted by users on pages')
  }
]

// Computed properties
const computedRedirectUrl = computed(() => {
  const check_redirect_url = localFormData.value.redirect_url
  console.log(check_redirect_url)
  const check_window_location = `${window.location.origin}/api/auth/facebook/callback`
  console.log(check_window_location)
  return localFormData.value.redirect_url || `${window.location.origin}/api/auth/facebook/callback`
})

const isFormValid = computed(() => {
  const form = localFormData.value
  return !!(
    form.user_email &&
    form.full_name &&
    isValidEmail(form.user_email) &&
    Object.keys(validationErrors.value).length === 0
  )
})

// Helper methods
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const validateForm = () => {
  const errors = {}
  const form = localFormData.value

  if (!form.user_email) {
    errors.user_email = __('Email is required')
  } else if (!isValidEmail(form.user_email)) {
    errors.user_email = __('Please enter a valid email address')
  }

  if (!form.full_name) {
    errors.full_name = __('Full name is required')
  }

  if (form.hook_url && !isValidUrl(form.hook_url)) {
    errors.hook_url = __('Please enter a valid URL')
  }

  if (form.timeout && (form.timeout < 5 || form.timeout > 300)) {
    errors.timeout = __('Timeout should be between 5 and 300 seconds')
  }

  if (form.max_retries && (form.max_retries < 1 || form.max_retries > 10)) {
    errors.max_retries = __('Max retries should be between 1 and 10')
  }

  validationErrors.value = errors
  return Object.keys(errors).length === 0
}

const isValidUrl = (string) => {
  try {
    new URL(string)
    return true
  } catch (_) {
    return false
  }
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

const testConnection = async () => {
  if (!isFormValid.value) {
    toastWarning(`${__('Validation Error')}: ${__('Please fix form errors before testing')}`)
    return
  }

  isTesting.value = true
  testResult.value = null

  try {
    const response = await call('mbw_mira.api.external_connections.test_connection', {
      connection_id: props.existingConnection.connection_id || props.existingConnection.name
    })

    const res = response?.message || response
    if (res?.success) {
      testResult.value = {
        success: true,
        message: res?.message || __('Connection test successful! Facebook OAuth is configured properly.')
      }
    } else {
      testResult.value = {
        success: false,
        message: res?.message || __('Connection test failed')
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
    toastWarning(`${__('Validation Error')}: ${__('Please fix the errors in the form')}`)
    return
  }

  isSubmitting.value = true
  try {
    // Prepare data for submission
    const submitData = {
      tenant_name: localFormData.value.tenant_name,
      user_email: localFormData.value.user_email,
      full_name: localFormData.value.full_name,
      app_id: localFormData.value.app_id,
      app_secret: localFormData.value.app_secret,
      hook_url: localFormData.value.hook_url || '',
      redirect_url: computedRedirectUrl.value,
      api_version: localFormData.value.api_version || 'v18.0',
      timeout: parseInt(localFormData.value.timeout) || 30,
      permissions: [...localFormData.value.permissions],
      auto_sync_accounts: localFormData.value.auto_sync_accounts,
      platform_type: 'Facebook'
    }

    // Emit to parent
    emit('submit', submitData)
    
  } catch (error) {
    console.error('Form submission error:', error)
    toastWarning(`${__('Error')}: ${error.message || __('Failed to submit form')}`)
  } finally {
    isSubmitting.value = false
  }
}

const handleCancel = () => {
  // Reset form to original state
  if (props.isEdit && props.existingConnection) {
    loadExistingData()
  } else {
    Object.assign(localFormData.value, { ...defaultFormData })
  }
  
  validationErrors.value = {}
  testResult.value = null
  emit('cancel')
}

// Model value synchronization with debouncing to prevent loops
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
      user_email: existing.user_email || '',
      full_name: existing.full_name || '',
      hook_url: existing.hook_url || '',
      redirect_url: existing.redirect_url || computedRedirectUrl.value,
      timeout: existing.timeout || 30,
      max_retries: existing.max_retries || 3,
      permissions: existing.permissions || [...defaultFormData.permissions],
      auto_sync_accounts: existing.auto_sync_accounts ?? true
    })
  }
}

// Watchers with proper debouncing
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

// Initialize form data properly
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
  
  nextTick(() => {
    validateForm()
    emitModelUpdate()
  })
})
</script>

<style scoped>
.facebook-connection-form {
  max-width: 100%;
}

/* Custom form styling */
::deep(.form-control) {
  margin-bottom: 0;
}

::deep(.form-control .form-label) {
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

::deep(.form-control .form-input) {
  border-radius: 0.5rem;
  border: 1px solid #d1d5db;
  padding: 0.75rem;
  transition: all 0.2s;
}

::deep(.form-control .form-input:focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

::deep(.form-control .form-error) {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

::deep(.form-control .form-help) {
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Prevent layout shifts */
.grid {
  min-height: 0;
}

/* Loading state styling */
.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  items-center: center;
  justify-content: center;
  z-index: 10;
}
</style>