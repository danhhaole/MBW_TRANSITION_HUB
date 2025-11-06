<template>
  <Dialog
    v-model="isOpen"
    :options="{
      title: isEditMode ? __('Edit Flow Template') : __('Create Flow Template'),
      size: '2xl',
    }"
    :disableOutsideClickToClose="true"
  >
    <template #body-content>
      <div class="space-y-6">
        <!-- Basic Information Section -->
        <div class="space-y-4">
          <h3 class="text-sm font-semibold text-gray-900 border-b pb-2">
            {{ __('Basic Information') }}
          </h3>
          
          <div class="grid grid-cols-2 gap-4">
            <!-- Template Name -->
            <div class="col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ __('Template Name') }} <span class="text-red-500">*</span>
              </label>
              <FormControl
                v-model="formData.name_template"
                type="text"
                :placeholder="__('Enter template name')"
              />
              <p v-if="errors.name_template" class="text-xs text-red-500 mt-1">
                {{ errors.name_template }}
              </p>
            </div>

            <!-- Alias -->
            <div class="col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ __('Alias') }}
              </label>
              <FormControl
                v-model="formData.alias"
                type="text"
                :placeholder="__('URL-friendly identifier')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Used for URL routing (optional)') }}
              </p>
            </div>

            <!-- Description -->
            <div class="col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ __('Description') }}
              </label>
              <textarea
                v-model="formData.description"
                rows="3"
                :placeholder="__('Describe what this template does...')"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <!-- Type -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ __('Type') }} <span class="text-red-500">*</span>
              </label>
              <Select
                v-model="formData.type"
                :options="typeOptions"
                :placeholder="__('Select type')"
              />
              <p v-if="errors.type" class="text-xs text-red-500 mt-1">
                {{ errors.type }}
              </p>
            </div>

            <!-- Order Number -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ __('Order Number') }}
              </label>
              <FormControl
                v-model.number="formData.order_no"
                type="number"
                :placeholder="__('Display order (default: 999)')"
              />
            </div>
          </div>
        </div>

        <!-- Classification Section -->
        <div class="space-y-4">
          <h3 class="text-sm font-semibold text-gray-900 border-b pb-2">
            {{ __('Classification') }}
          </h3>
          
          <div class="grid grid-cols-3 gap-4">
            <!-- Is Default Template -->
            <div class="flex items-center space-x-2">
              <input
                v-model="formData.is_default"
                type="checkbox"
                :true-value="1"
                :false-value="0"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label class="text-sm text-gray-700">
                {{ __('System Template') }}
              </label>
            </div>

            <!-- Is Premium -->
            <div class="flex items-center space-x-2">
              <input
                v-model="formData.is_premium"
                type="checkbox"
                :true-value="1"
                :false-value="0"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label class="text-sm text-gray-700">
                {{ __('Premium') }}
              </label>
            </div>

            <!-- Is Suggestion -->
            <div class="flex items-center space-x-2">
              <input
                v-model="formData.is_suggestion"
                type="checkbox"
                :true-value="1"
                :false-value="0"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label class="text-sm text-gray-700">
                {{ __('Recommended') }}
              </label>
            </div>
          </div>
        </div>

        <!-- Scope & Permissions Section -->
        <div class="space-y-4">
          <h3 class="text-sm font-semibold text-gray-900 border-b pb-2">
            {{ __('Scope & Permissions') }}
          </h3>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ __('Scope Type') }} <span class="text-red-500">*</span>
            </label>
            <Select
              v-model="formData.scope_type"
              :options="scopeOptions"
              :placeholder="__('Select scope')"
            />
            <p class="text-xs text-gray-500 mt-1">
              {{ getScopeDescription(formData.scope_type) }}
            </p>
          </div>
        </div>

        <!-- Template Configuration Section -->
        <div class="space-y-4">
          <h3 class="text-sm font-semibold text-gray-900 border-b pb-2">
            {{ __('Template Configuration') }}
          </h3>
          
          <div class="grid grid-cols-2 gap-4">
            <!-- Channel -->
            <div class="col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ __('Channel') }} <span class="text-red-500">*</span>
              </label>
              <Select
                v-model="formData.channel"
                :options="channelOptions"
                :placeholder="__('Select channel')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ getChannelDescription(formData.channel) }}
              </p>
              <p v-if="errors.channel" class="text-xs text-red-500 mt-1">
                {{ errors.channel }}
              </p>
            </div>

            <!-- Target Type -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ __('Target Type') }}
              </label>
              <Select
                v-model="formData.target_type"
                :options="targetTypeOptions"
                :placeholder="__('Select target type')"
              />
            </div>

            <!-- Flow Parent ID -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ __('Flow Parent ID') }}
              </label>
              <FormControl
                v-model="formData.flow_parent_id"
                type="text"
                :placeholder="__('Parent flow reference (optional)')"
              />
            </div>
          </div>
        </div>

        <!-- Trigger Section -->
        <div class="space-y-4">
          <h3 class="text-sm font-semibold text-gray-900 border-b pb-2">
            {{ __('Trigger') }}
          </h3>
          
          <div class="space-y-3">
            <!-- Selected Trigger -->
            <div v-if="selectedTrigger" class="group relative p-3 border border-gray-200 rounded-lg bg-gray-50">
              <button
                @click="removeTrigger"
                class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-600 flex items-center justify-center"
              >
                <FeatherIcon name="x" class="h-3 w-3" />
              </button>
              
              <div class="flex items-start space-x-3">
                <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <FeatherIcon :name="selectedTrigger.icon || 'zap'" class="h-4 w-4 text-blue-600" />
                </div>
                <div class="flex-1 min-w-0">
                  <h4 class="text-sm font-medium text-gray-900">{{ selectedTrigger.trigger_name }}</h4>
                  <p class="text-xs text-gray-500 mt-1">{{ selectedTrigger.description }}</p>
                </div>
              </div>
            </div>
            
            <!-- Add Trigger Button -->
            <Button
              v-else
              variant="outline"
              size="sm"
              class="w-full"
              @click="showAddTrigger = true"
            >
              <template #prefix>
                <FeatherIcon name="plus" class="w-4 h-4" />
              </template>
              {{ __('Select Trigger') }}
            </Button>
          </div>
        </div>

        <!-- Action Section -->
        <div v-if="formData.channel" class="space-y-4">
          <h3 class="text-sm font-semibold text-gray-900 border-b pb-2">
            {{ __('Action') }}
          </h3>
          
          <!-- Email Content -->
          <div v-if="formData.channel === 'Email'">
            <EmailEditor
              :content="emailContent"
              @update:content="updateEmailContent"
              :readonly="false"
            />
          </div>

          <!-- Message Content (SMS, Zalo, Messenger) -->
          <div v-else>
            <ZaloEditor
              :content="messageContent"
              @update:content="updateMessageContent"
              :readonly="false"
            />
          </div>
        </div>

        <!-- CTA Section -->
        <div class="space-y-4">
          <h3 class="text-sm font-semibold text-gray-900 border-b pb-2">
            {{ __('Call to Action') }}
          </h3>
          
          <div class="space-y-3">
            <!-- Has URL CTA -->
            <div class="flex items-center space-x-2">
              <input
                v-model="formData.is_has_url_cta"
                type="checkbox"
                :true-value="1"
                :false-value="0"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label class="text-sm text-gray-700">
                {{ __('Has URL CTA') }}
              </label>
            </div>

            <!-- CTA URL -->
            <div v-if="formData.is_has_url_cta === 1">
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ __('CTA URL') }}
              </label>
              <FormControl
                v-model="formData.url_cta"
                type="text"
                :placeholder="__('https://example.com/documentation')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Link to documentation or additional resources') }}
              </p>
            </div>
          </div>
        </div>

        <!-- Thumbnail Upload Section -->
        <div class="space-y-4">
          <h3 class="text-sm font-semibold text-gray-900 border-b pb-2">
            {{ __('Thumbnail') }}
          </h3>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Template Thumbnail') }}
            </label>
            
            <!-- Current Thumbnail Preview -->
            <div v-if="formData.thumbnail" class="mb-3">
              <img
                :src="formData.thumbnail"
                alt="Thumbnail preview"
                class="w-48 h-32 object-cover rounded-lg border border-gray-200"
              />
              <Button
                variant="outline"
                theme="red"
                size="sm"
                class="mt-2"
                @click="handleRemoveThumbnail"
              >
                <template #prefix>
                  <FeatherIcon name="trash-2" class="w-3 h-3" />
                </template>
                {{ __('Remove') }}
              </Button>
            </div>

            <!-- File Uploader -->
            <div v-else>
              <FileUploader
                :fileTypes="['image/*']"
                :validateFile="validateThumbnailFile"
                @success="handleFileUploadSuccess"
              >
                <template #default="{ file, uploading, progress, uploaded, message, error, total, success, openFileSelector }">
                  <div 
                    @click="openFileSelector()"
                    class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors cursor-pointer"
                  >
                    <div v-if="uploading">
                      <FeatherIcon name="loader" class="w-8 h-8 mx-auto text-blue-500 animate-spin mb-2" />
                      <p class="text-sm text-gray-600">{{ __('Uploading...') }} {{ progress }}%</p>
                    </div>
                    <div v-else-if="error">
                      <FeatherIcon name="alert-circle" class="w-8 h-8 mx-auto text-red-500 mb-2" />
                      <p class="text-sm text-red-600">{{ error }}</p>
                      <Button
                        variant="outline"
                        size="sm"
                        class="mt-2"
                        @click.stop="openFileSelector()"
                      >
                        {{ __('Try Again') }}
                      </Button>
                    </div>
                    <div v-else>
                      <FeatherIcon name="image" class="w-12 h-12 mx-auto text-gray-400 mb-2" />
                      <p class="text-sm text-gray-700 font-medium mb-1">
                        {{ __('Click to upload or drag and drop') }}
                      </p>
                      <p class="text-xs text-gray-500">
                        {{ __('PNG, JPG, GIF, WebP or SVG (max 5MB)') }}
                      </p>
                      <p class="text-xs text-gray-400 mt-2">
                        {{ __('Recommended size: 400x300px') }}
                      </p>
                    </div>
                  </div>
                </template>
              </FileUploader>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-between w-full">
        <Button
          variant="outline"
          theme="gray"
          @click="closeModal"
        >
          {{ __('Cancel') }}
        </Button>
        <Button
          theme="blue"
          @click="handleSubmit"
          :loading="loading"
        >
          <template #prefix>
            <FeatherIcon :name="isEditMode ? 'save' : 'plus'" class="w-4 h-4" />
          </template>
          {{ isEditMode ? __('Update Template') : __('Create Template') }}
        </Button>
      </div>
    </template>
  </Dialog>

  <!-- Add Trigger Modal -->
  <Dialog v-model="isAddTriggerOpen" :options="{ title: __('Add Trigger'), size: 'md' }">
    <template #body-content>
      <div class="space-y-4" @click.stop>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __('Search trigger') }}
          </label>
          <FormControl
            v-model="triggerSearch"
            type="text"
            :placeholder="__('Search trigger')"
          />
        </div>
        <div class="max-h-60 overflow-y-auto">
          <div class="space-y-2">
            <div
              v-for="trigger in filteredTriggerOptions"
              :key="trigger.id"
              class="p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
              @click.stop="handleAddTrigger(trigger)"
            >
              <h4 class="text-sm font-medium text-gray-900">
                {{ trigger.name }}
              </h4>
              <p class="text-xs text-gray-500">{{ trigger.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, Select, FormControl, FeatherIcon, FileUploader } from 'frappe-ui'
import EmailEditor from '@/components/campaign/content-editors/EmailEditor.vue'
import ZaloEditor from '@/components/campaign/content-editors/ZaloEditor.vue'

// Props
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  template: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['close', 'submit'])

// Local state
const errors = ref({})

// Computed for dialog state
const isOpen = computed({
  get: () => props.show,
  set: (value) => {
    if (!value) {
      emit('close')
    }
  }
})

const isAddTriggerOpen = computed({
  get: () => showAddTrigger.value,
  set: (value) => {
    showAddTrigger.value = value
  }
})

// Form data with default values
const formData = ref({
  name_template: '',
  alias: '',
  description: '',
  thumbnail: '',
  type: 'FLOW',
  order_no: 999,
  is_default: 0,
  is_premium: 0,
  is_suggestion: 0,
  scope_type: 'PRIVATE',
  channel: '',
  target_type: '',
  flow_parent_id: '',
  configuration_json: '',
  is_has_url_cta: 0,
  url_cta: ''
})

// Trigger and Action (only 1 each)
const selectedTrigger = ref(null)
const showAddTrigger = ref(false)
const triggerSearch = ref('')

// Content data based on channel type
const emailContent = ref({
  email_subject: '',
  email_content: '',
  attachments: []
})

const messageContent = ref({
  blocks: [
    {
      id: Date.now(),
      type: 'text',
      text_content: ''
    }
  ]
})

// Computed
const isEditMode = computed(() => !!props.template)

// Options
const typeOptions = [
  { label: __('Flow'), value: 'FLOW' },
  { label: __('Sequence'), value: 'SEQUENCE' },
  { label: __('Campaign'), value: 'CAMPAIGN' }
]

const scopeOptions = [
  { label: __('Private'), value: 'PRIVATE' },
  { label: __('Team'), value: 'TEAM' },
  { label: __('Organization'), value: 'ORGANIZATION' },
  { label: __('Public'), value: 'PUBLIC' }
]

const channelOptions = [
  { label: 'Email', value: 'Email' },
  { label: 'SMS', value: 'SMS' },
  { label: 'Zalo', value: 'Zalo' },
  { label: 'Messenger', value: 'Messenger' }
]

const targetTypeOptions = [
  { label: __('Talent'), value: 'Talent' },
  { label: __('Talent Pool'), value: 'Talent Pool' },
  { label: __('Applicant'), value: 'Applicant' }
]

const availableTriggers = [
  {
    id: 'on_create',
    name: 'On Create',
    description: 'Trigger when creating a new record',
    icon: 'plus-circle',
    event_type: 'ON_CREATE'
  },
  {
    id: 'on_update',
    name: 'On Update',
    description: 'Trigger when updating a record',
    icon: 'edit',
    event_type: 'ON_UPDATE'
  },
  {
    id: 'on_tag_added',
    name: 'On Tag Added',
    description: 'Trigger when a tag is added to a record',
    icon: 'tag',
    event_type: 'ON_TAG_ADDED'
  },
  {
    id: 'on_status_changed',
    name: 'On Status Changed',
    description: 'Trigger when a record status changes',
    icon: 'refresh-cw',
    event_type: 'ON_STATUS_CHANGED'
  },
  {
    id: 'on_sequence_completed',
    name: 'On Sequence Completed',
    description: 'Trigger when a sequence is completed',
    icon: 'check-circle',
    event_type: 'ON_SEQUENCE_COMPLETED'
  },
  {
    id: 'on_scheduled_time',
    name: 'On Scheduled Time',
    description: 'Trigger when a scheduled time is reached',
    icon: 'clock',
    event_type: 'ON_SCHEDULED_TIME'
  },
  {
    id: 'on_score_reached',
    name: 'On Score Reached',
    description: 'Trigger when a score is reached',
    icon: 'target',
    event_type: 'ON_SCORE_REACHED'
  },
  {
    id: 'custom_event',
    name: 'Custom Event',
    description: 'Trigger by a custom event',
    icon: 'settings',
    event_type: 'CUSTOM_EVENT'
  },
  {
    id: 'form_submit',
    name: 'Form Submitted',
    description: 'Trigger when a form is submitted',
    icon: 'file-text',
    event_type: 'Form_Submitted'
  }
]

// Computed
const filteredTriggerOptions = computed(() => {
  if (!triggerSearch.value) return availableTriggers
  return availableTriggers.filter(
    (trigger) =>
      trigger.name.toLowerCase().includes(triggerSearch.value.toLowerCase()) ||
      trigger.description.toLowerCase().includes(triggerSearch.value.toLowerCase())
  )
})

// Watch for prop changes
watch(() => props.show, (newValue) => {
  if (newValue) {
    if (props.template) {
      loadTemplateData()
    } else {
      resetForm()
    }
  }
}, { flush: 'post' })

// Methods
const loadTemplateData = () => {
  if (props.template) {
    formData.value = {
      name_template: props.template.name_template || '',
      alias: props.template.alias || '',
      description: props.template.description || '',
      thumbnail: props.template.thumbnail || '',
      type: props.template.type || 'FLOW',
      order_no: props.template.order_no || 999,
      is_default: props.template.is_default || 0,
      is_premium: props.template.is_premium || 0,
      is_suggestion: props.template.is_suggestion || 0,
      scope_type: props.template.scope_type || 'PRIVATE',
      channel: props.template.channel || '',
      target_type: props.template.target_type || '',
      flow_parent_id: props.template.flow_parent_id || '',
      configuration_json: props.template.configuration_json || '',
      is_has_url_cta: props.template.is_has_url_cta || 0,
      url_cta: props.template.url_cta || ''
    }
    
    // Load trigger from template_triggers child table
    if (props.template.template_triggers && props.template.template_triggers.length > 0) {
      const trigger = props.template.template_triggers[0]
      selectedTrigger.value = {
        trigger_name: trigger.trigger_name,
        trigger_type: trigger.trigger_type,
        target_type: trigger.target_type,
        channel: trigger.channel,
        description: trigger.description,
        icon: getTriggerIcon(trigger.trigger_type)
      }
    }
    
    // Load action content from template_actions child table
    if (props.template.template_actions && props.template.template_actions.length > 0) {
      const action = props.template.template_actions[0]
      if (action.action_parameters) {
        try {
          const params = JSON.parse(action.action_parameters)
          // ✅ Load from "template" (new structure)
          if (params.template) {
            emailContent.value = params.template
          }
          // ⚠️ Fallback to old structure for backward compatibility
          else if (params.email_content) {
            emailContent.value = params.email_content
          }
          
          if (params.zalo_content) {
            messageContent.value = params.zalo_content
          }
          if (params.sms_content) {
            messageContent.value = params.sms_content
          }
        } catch (e) {
          console.error('Error parsing action_parameters:', e)
        }
      }
    }
  }
}

const resetForm = () => {
  formData.value = {
    name_template: '',
    alias: '',
    description: '',
    thumbnail: '',
    type: 'FLOW',
    order_no: 999,
    is_default: 0,
    is_premium: 0,
    is_suggestion: 0,
    scope_type: 'PRIVATE',
    channel: '',
    target_type: '',
    flow_parent_id: '',
    configuration_json: '',
    is_has_url_cta: 0,
    url_cta: ''
  }
  selectedTrigger.value = null
  emailContent.value = {
    email_subject: '',
    email_content: '',
    attachments: []
  }
  messageContent.value = {
    blocks: [
      {
        id: Date.now(),
        type: 'text',
        text_content: ''
      }
    ]
  }
  errors.value = {}
}

const validateForm = () => {
  errors.value = {}
  
  // Required fields
  if (!formData.value.name_template || !formData.value.name_template.trim()) {
    errors.value.name_template = __('Template name is required')
  }
  
  if (!formData.value.type) {
    errors.value.type = __('Type is required')
  }
  
  if (!formData.value.scope_type) {
    errors.value.scope_type = __('Scope type is required')
  }
  
  if (!formData.value.channel) {
    errors.value.channel = __('Channel is required')
  }
  
  return Object.keys(errors.value).length === 0
}

const handleSubmit = () => {
  if (!validateForm()) {
    return
  }
  
  // Clean up data
  const submitData = { ...formData.value }
  
  // Trim string fields
  submitData.name_template = submitData.name_template.trim()
  if (submitData.alias) submitData.alias = submitData.alias.trim()
  if (submitData.description) submitData.description = submitData.description.trim()
  
  // Convert checkboxes to integers
  submitData.is_default = submitData.is_default ? 1 : 0
  submitData.is_premium = submitData.is_premium ? 1 : 0
  submitData.is_suggestion = submitData.is_suggestion ? 1 : 0
  submitData.is_has_url_cta = submitData.is_has_url_cta ? 1 : 0
  
  // Build template_triggers child table
  submitData.template_triggers = []
  if (selectedTrigger.value) {
    submitData.template_triggers.push({
      trigger_name: selectedTrigger.value.trigger_name,
      trigger_type: selectedTrigger.value.trigger_type,
      target_type: selectedTrigger.value.target_type || formData.value.target_type,
      channel: selectedTrigger.value.channel || formData.value.channel,
      description: selectedTrigger.value.description,
      status: 'ACTIVE',
      order: 0,
      is_default: 1
    })
  }
  
  // Build template_actions child table
  submitData.template_actions = []
  const actionParams = {}
  
  if (submitData.channel === 'Email') {
    // ✅ Save to "template" (new structure)
    actionParams.template = emailContent.value
    submitData.template_actions.push({
      action_name: 'Send Email',
      action_type: 'EMAIL',
      channel_type: 'Email',
      action_parameters: JSON.stringify(actionParams),
      status: 'ACTIVE',
      order: 0,
      is_default: 1
    })
  } else {
    if (submitData.channel === 'Zalo') {
      actionParams.zalo_content = messageContent.value
    } else if (submitData.channel === 'SMS') {
      actionParams.sms_content = messageContent.value
    }
    submitData.template_actions.push({
      action_name: `Send ${submitData.channel}`,
      action_type: submitData.channel.toUpperCase(),
      channel_type: submitData.channel,
      action_parameters: JSON.stringify(actionParams),
      status: 'ACTIVE',
      order: 0,
      is_default: 1
    })
  }
  
  emit('submit', submitData)
}

const handleAddTrigger = (trigger) => {
  selectedTrigger.value = {
    trigger_name: trigger.name,
    trigger_type: trigger.event_type,
    description: trigger.description,
    icon: trigger.icon
  }
  showAddTrigger.value = false
  triggerSearch.value = ''
}

const removeTrigger = () => {
  selectedTrigger.value = null
}

const getTriggerIcon = (triggerType) => {
  const iconMap = {
    'ON_CREATE': 'plus-circle',
    'ON_UPDATE': 'edit',
    'ON_TAG_ADDED': 'tag',
    'ON_STATUS_CHANGED': 'refresh-cw',
    'ON_SEQUENCE_COMPLETED': 'check-circle',
    'ON_SCHEDULED_TIME': 'clock',
    'ON_SCORE_REACHED': 'target',
    'CUSTOM_EVENT': 'settings',
    'Form_Submitted': 'file-text'
  }
  return iconMap[triggerType] || 'zap'
}

const updateEmailContent = (newContent) => {
  // Only update if content actually changed to prevent infinite loops
  if (JSON.stringify(emailContent.value) !== JSON.stringify(newContent)) {
    emailContent.value = { ...newContent }
  }
}

const updateMessageContent = (newContent) => {
  // Only update if content actually changed to prevent infinite loops
  if (JSON.stringify(messageContent.value) !== JSON.stringify(newContent)) {
    messageContent.value = { ...newContent }
  }
}

const closeModal = () => {
  emit('close')
}

const getScopeDescription = (scope) => {
  const descriptions = {
    'PRIVATE': __('Only you can see and use this template'),
    'TEAM': __('Your team members can see and use this template'),
    'ORGANIZATION': __('Everyone in your organization can see and use this template'),
    'PUBLIC': __('Anyone can see and use this template')
  }
  return descriptions[scope] || ''
}

const validateThumbnailFile = (fileObject) => {
  // Validate file size (max 5MB)
  const maxSize = 5 * 1024 * 1024 // 5MB in bytes
  if (fileObject.size > maxSize) {
    return __('File size must be less than 5MB')
  }
  
  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml']
  if (!allowedTypes.includes(fileObject.type)) {
    return __('Only image files are allowed (JPG, PNG, GIF, WebP, SVG)')
  }
  
  // Return null if valid (no error)
  return null
}

const handleFileUploadSuccess = (file) => {
  if (file && file.file_url) {
    formData.value.thumbnail = file.file_url
  }
}

const handleRemoveThumbnail = () => {
  formData.value.thumbnail = ''
}

const getChannelDescription = (channel) => {
  const descriptions = {
    'Email': __('Send emails with rich HTML content and attachments'),
    'SMS': __('Send plain text messages via SMS (160 characters recommended)'),
    'Zalo': __('Send messages through Zalo OA with text, images, and buttons'),
    'Messenger': __('Send messages through Facebook Messenger with rich media')
  }
  return descriptions[channel] || ''
}

</script>
