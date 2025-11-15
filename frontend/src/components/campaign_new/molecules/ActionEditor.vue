<template>
  <Dialog
    v-model="localShow"
    :options="{
      title: __('Edit Action'),
      size: '4xl'
    }"
  >
    <template #body-content>
      <div v-if="localAction" class="space-y-6">
        <!-- Action Type Header -->
        <div class="flex items-center space-x-3 pb-4 border-b border-gray-200">
          <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
            <FeatherIcon :name="getActionIcon(localAction.action_type)" class="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <h3 class="text-base font-semibold text-gray-900">{{ getActionLabel(localAction.action_type) }}</h3>
            <p class="text-xs text-gray-500">{{ getActionDescription(localAction.action_type) }}</p>
          </div>
        </div>

        <!-- Action Type Selector -->
        <div class="grid grid-cols-2 gap-4">
          <FormControl
            type="select"
            :label="__('Action Type')"
            v-model="localAction.action_type"
            :options="actionTypeOptions"
            @change="handleActionTypeChange"
            required
          />
          <FormControl
            v-if="needsChannelForAction(localAction.action_type)"
            type="select"
            :label="__('Channel')"
            v-model="localAction.channel_type"
            :options="channelOptions"
          />
        </div>

        <!-- Content Editors based on Action Type -->
        <div class="space-y-4">
          <!-- EMAIL Action -->
          <div v-if="localAction.action_type === 'EMAIL'" class="space-y-4">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="mail" class="h-4 w-4 text-blue-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-blue-900">
                    {{ __('Send Email') }}
                  </p>
                  <p class="text-xs text-blue-700">
                    {{ __('This action will send an email to talent when triggered') }}
                  </p>
                </div>
              </div>
            </div>
            
            <EmailContentEditor
              :content="emailContent"
              @update:content="handleEmailContentUpdate"
            />
          </div>

          <!-- MESSAGE Action (Zalo/SMS) -->
          <div v-else-if="localAction.action_type === 'MESSAGE'" class="space-y-4">
            <FormControl
              type="select"
              :label="__('Message Channel')"
              v-model="localAction.channel_type"
              :options="messageChannelOptions"
              required
            />
            
            <!-- Zalo Content Editor -->
            <div v-if="localAction.channel_type === 'Zalo'">
              <ZaloContentEditor
                :content="localAction.content || { blocks: [] }"
                @update:content="localAction.content = $event"
              />
            </div>
            
            <!-- SMS Content -->
            <div v-else-if="localAction.channel_type === 'SMS'">
              <FormControl
                type="textarea"
                :label="__('SMS Message')"
                v-model="localAction.content"
                :placeholder="__('Enter SMS message...')"
                rows="4"
                :maxlength="160"
                required
              />
              <div class="flex justify-between items-center mt-2">
                <p class="text-xs text-gray-500">
                  {{ __('Keep it short and clear (max 160 characters)') }}
                </p>
                <span class="text-xs text-gray-500">
                  {{ (localAction.content?.length || 0) }}/160
                </span>
              </div>
            </div>
          </div>

          <!-- ADD_CUSTOM_FIELD Action -->
          <div v-else-if="localAction.action_type === 'ADD_CUSTOM_FIELD'" class="space-y-4">
            <div class="bg-purple-50 border border-purple-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="edit-3" class="h-4 w-4 text-purple-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-purple-900">
                    {{ __('Update Talent Field') }}
                  </p>
                  <p class="text-xs text-purple-700">
                    {{ __('This action will update a field value in talent profile when triggered') }}
                  </p>
                </div>
              </div>
            </div>
            
            <!-- Field Selection -->
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Select Field') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedFieldName"
                :options="talentFieldOptions"
                :placeholder="__('Search and select field...')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Choose which field to update in talent profile') }}
              </p>
            </div>
            
            <!-- Show selected field info -->
            <div v-if="selectedField" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-medium text-gray-700">{{ __('Field Type') }}:</span>
                  <span class="text-xs text-gray-600">{{ selectedField.fieldtype }}</span>
                </div>
                <div v-if="selectedField.description" class="text-xs text-gray-500">
                  {{ selectedField.description }}
                </div>
              </div>
            </div>
            
            <!-- Field Value Input (dynamic based on field type) -->
            <div v-if="selectedField">
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Field Value') }}
                <span class="text-red-500">*</span>
              </label>
              
              <!-- Select field -->
              <FormControl
                v-if="selectedField.fieldtype === 'Select'"
                type="select"
                v-model="localAction.field_value"
                :options="getSelectOptions(selectedField.options)"
                :placeholder="__('Select value...')"
                required
              />
              
              <!-- Date field -->
              <FormControl
                v-else-if="selectedField.fieldtype === 'Date'"
                type="date"
                v-model="localAction.field_value"
                :placeholder="__('Select date...')"
                required
              />
              
              <!-- Float/Currency field -->
              <FormControl
                v-else-if="['Float', 'Currency', 'Int'].includes(selectedField.fieldtype)"
                type="number"
                v-model="localAction.field_value"
                :placeholder="__('Enter number...')"
                required
              />
              
              <!-- Check field -->
              <FormControl
                v-else-if="selectedField.fieldtype === 'Check'"
                type="checkbox"
                v-model="localAction.field_value"
              />
              
              <!-- Text area fields -->
              <FormControl
                v-else-if="['Text', 'Small Text', 'Long Text'].includes(selectedField.fieldtype)"
                type="textarea"
                v-model="localAction.field_value"
                :placeholder="__('Enter value...')"
                rows="3"
                required
              />
              
              <!-- Default: Data field -->
              <FormControl
                v-else
                type="text"
                v-model="localAction.field_value"
                :placeholder="__('Enter value...')"
                required
              />
              
              <p class="text-xs text-gray-500 mt-1">
                {{ __('This value will be set to the selected field') }}
              </p>
            </div>
          </div>

          <!-- ADD_TAG Action -->
          <div v-else-if="localAction.action_type === 'ADD_TAG'" class="space-y-4">
            <div class="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="plus-circle" class="h-4 w-4 text-green-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-green-900">
                    {{ __('Add Tag to Talent') }}
                  </p>
                  <p class="text-xs text-green-700">
                    {{ __('This action will add the selected tag to talent profile when triggered') }}
                  </p>
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Select Tag to Add') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedTagId"
                :options="tagOptions"
                :placeholder="__('Search and select tag to add...')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Choose the tag that will be added to talent') }}
              </p>
            </div>
            
            <!-- Show selected tag info -->
            <div v-if="selectedTag" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div class="flex items-center space-x-2">
                <div 
                  class="w-4 h-4 rounded"
                  :style="{ backgroundColor: selectedTag.color || '#6B7280' }"
                ></div>
                <div class="flex-1">
                  <p class="text-sm font-medium text-gray-900">{{ selectedTag.title }}</p>
                  <p class="text-xs text-gray-500">{{ selectedTag.name }}</p>
                </div>
                <div class="text-xs text-green-600 font-medium">
                  {{ __('Will be added') }}
                </div>
              </div>
            </div>
          </div>

          <!-- REMOVE_TAG Action -->
          <div v-else-if="localAction.action_type === 'REMOVE_TAG'" class="space-y-4">
            <div class="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="minus-circle" class="h-4 w-4 text-red-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-red-900">
                    {{ __('Remove Tag from Talent') }}
                  </p>
                  <p class="text-xs text-red-700">
                    {{ __('This action will remove the selected tag from talent profile when triggered') }}
                  </p>
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Select Tag to Remove') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedTagId"
                :options="tagOptions"
                :placeholder="__('Search and select tag to remove...')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Choose the tag that will be removed from talent') }}
              </p>
            </div>
            
            <!-- Show selected tag info -->
            <div v-if="selectedTag" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div class="flex items-center space-x-2">
                <div 
                  class="w-4 h-4 rounded"
                  :style="{ backgroundColor: selectedTag.color || '#6B7280' }"
                ></div>
                <div class="flex-1">
                  <p class="text-sm font-medium text-gray-900">{{ selectedTag.title }}</p>
                  <p class="text-xs text-gray-500">{{ selectedTag.name }}</p>
                </div>
                <div class="text-xs text-red-600 font-medium">
                  {{ __('Will be removed') }}
                </div>
              </div>
            </div>
          </div>

          <!-- START_FLOW Action -->
          <div v-else-if="localAction.action_type === 'START_FLOW'" class="space-y-4">
            <div class="bg-teal-50 border border-teal-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="play-circle" class="h-4 w-4 text-teal-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-teal-900">
                    {{ __('Start Another Flow') }}
                  </p>
                  <p class="text-xs text-teal-700">
                    {{ __('This action will trigger another automation flow when executed') }}
                  </p>
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Select Flow to Start') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedFlowId"
                :options="flowOptions"
                :placeholder="__('Search and select flow...')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Choose which flow to start when this action triggers') }}
              </p>
            </div>
            
            <!-- Show selected flow info -->
            <div v-if="selectedFlow" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-medium text-gray-700">{{ selectedFlow.title }}</span>
                  <span class="text-xs px-2 py-0.5 rounded" :class="{
                    'bg-green-100 text-green-700': selectedFlow.status === 'Active',
                    'bg-yellow-100 text-yellow-700': selectedFlow.status === 'Paused',
                    'bg-gray-100 text-gray-700': selectedFlow.status === 'Draft'
                  }">
                    {{ selectedFlow.status }}
                  </span>
                </div>
                <div class="text-xs text-gray-600">
                  {{ selectedFlow.description || __('No description') }}
                </div>
                <div class="flex items-center space-x-2 text-xs text-gray-500">
                  <span>{{ __('Type') }}: {{ selectedFlow.type }}</span>
                  <span>•</span>
                  <span>{{ selectedFlow.name }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- STOP_FLOW Action -->
          <div v-else-if="localAction.action_type === 'STOP_FLOW'" class="space-y-4">
            <div class="bg-orange-50 border border-orange-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="stop-circle" class="h-4 w-4 text-orange-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-orange-900">
                    {{ __('Stop a Flow') }}
                  </p>
                  <p class="text-xs text-orange-700">
                    {{ __('This action will stop a running automation flow') }}
                  </p>
                </div>
              </div>
            </div>
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Select Flow to Stop') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedFlowId"
                :options="flowOptions"
                :placeholder="__('Search and select flow...')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Choose which flow to stop when this action triggers') }}
              </p>
            </div>
            
            <!-- Show selected flow info -->
            <div v-if="selectedFlow" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-medium text-gray-700">{{ selectedFlow.title }}</span>
                  <span class="text-xs px-2 py-0.5 rounded" :class="{
                    'bg-green-100 text-green-700': selectedFlow.status === 'Active',
                    'bg-yellow-100 text-yellow-700': selectedFlow.status === 'Paused',
                    'bg-gray-100 text-gray-700': selectedFlow.status === 'Draft'
                  }">
                    {{ selectedFlow.status }}
                  </span>
                </div>
                <div class="text-xs text-gray-600">
                  {{ selectedFlow.description || __('No description') }}
                </div>
                <div class="flex items-center space-x-2 text-xs text-gray-500">
                  <span>{{ __('Type') }}: {{ selectedFlow.type }}</span>
                  <span>•</span>
                  <span>{{ selectedFlow.name }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- SENT_NOTIFICATION Action -->
          <div v-else-if="localAction.action_type === 'SENT_NOTIFICATION'" class="space-y-4">
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="check-square" class="h-4 w-4 text-blue-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-blue-900">
                    {{ __('Create Task') }}
                  </p>
                  <p class="text-xs text-blue-700">
                    {{ __('This action will create a task and assign it to a team member') }}
                  </p>
                </div>
              </div>
            </div>
            
            <FormControl
              type="text"
              :label="__('Task Subject')"
              v-model="localAction.task_subject"
              :placeholder="__('Enter task subject...')"
              required
            />
            
            <FormControl
              type="textarea"
              :label="__('Task Description')"
              v-model="localAction.task_description"
              :placeholder="__('Describe what needs to be done...')"
              rows="3"
            />
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Assign To') }}
              </label>
              <Autocomplete
                v-model="selectedAssignee"
                :options="userOptions"
                :placeholder="__('Search and select user...')"
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Select who should complete this task') }}
              </p>
            </div>
            
            <div v-if="selectedAssigneeUser" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <div class="flex items-center space-x-2">
                <div class="h-8 w-8 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-medium">
                  {{ selectedAssigneeUser.full_name?.charAt(0) || 'U' }}
                </div>
                <div>
                  <p class="text-xs font-medium text-gray-900">{{ selectedAssigneeUser.full_name }}</p>
                  <p class="text-xs text-gray-500">{{ selectedAssigneeUser.name }}</p>
                </div>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-3">
              <FormControl
                type="select"
                :label="__('Priority')"
                v-model="localAction.task_priority"
                :options="[
                  { label: __('Low'), value: 'Low' },
                  { label: __('Medium'), value: 'Medium' },
                  { label: __('High'), value: 'High' },
                  { label: __('Urgent'), value: 'Urgent' }
                ]"
              />
              
              <FormControl
                type="date"
                :label="__('Due Date')"
                v-model="localAction.task_due_date"
              />
            </div>
          </div>

          <!-- EXTERNAL_REQUEST Action -->
          <div v-else-if="localAction.action_type === 'EXTERNAL_REQUEST'" class="space-y-4">
            <div class="bg-indigo-50 border border-indigo-200 rounded-lg p-3 mb-4">
              <div class="flex items-start">
                <FeatherIcon name="bell" class="h-4 w-4 text-indigo-600 mt-0.5 mr-2" />
                <div>
                  <p class="text-sm font-medium text-indigo-900">
                    {{ __('Send Internal Notification') }}
                  </p>
                  <p class="text-xs text-indigo-700">
                    {{ __('This action will send a notification to selected team members') }}
                  </p>
                </div>
              </div>
            </div>
            
            <FormControl
              type="text"
              :label="__('Notification Title')"
              v-model="localAction.notification_title"
              :placeholder="__('Enter notification title...')"
              required
            />
            
            <FormControl
              type="textarea"
              :label="__('Notification Message')"
              v-model="localAction.notification_message"
              :placeholder="__('Enter the message to send...')"
              rows="4"
              required
            />
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __('Recipients') }}
                <span class="text-red-500">*</span>
              </label>
              <Autocomplete
                v-model="selectedRecipients"
                :options="userOptions"
                :placeholder="__('Search and select users...')"
                multiple
              />
              <p class="text-xs text-gray-500 mt-1">
                {{ __('Select one or more users to receive this notification') }}
              </p>
            </div>
            
            <div v-if="recipientUsers.length > 0" class="bg-gray-50 border border-gray-200 rounded-lg p-3">
              <p class="text-xs font-medium text-gray-700 mb-2">
                {{ __('Selected Recipients') }} ({{ recipientUsers.length }})
              </p>
              <div class="flex flex-wrap gap-2">
                <div v-for="user in recipientUsers" :key="user.name" 
                     class="flex items-center space-x-1 bg-white border border-gray-300 rounded-full px-2 py-1">
                  <div class="h-5 w-5 rounded-full bg-indigo-500 text-white flex items-center justify-center text-xs">
                    {{ user.full_name?.charAt(0) || 'U' }}
                  </div>
                  <span class="text-xs text-gray-900">{{ user.full_name || user.name }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- AI_CALL Action -->
          <div v-else-if="localAction.action_type === 'AI_CALL'" class="space-y-4">
            <FormControl
              type="text"
              :label="__('ATS System')"
              v-model="localAction.ats_system"
              :placeholder="__('Enter ATS system name...')"
              required
            />
            <FormControl
              type="textarea"
              :label="__('Handoff Data (JSON)')"
              v-model="localAction.handoff_data"
              :placeholder="__('Enter handoff data as JSON...')"
              rows="4"
            />
          </div>

          <!-- UNSUBSCRIBE Action -->
          <div v-else-if="localAction.action_type === 'UNSUBSCRIBE'" class="space-y-4">
            <FormControl
              type="textarea"
              :label="__('Unsubscribe Reason (Optional)')"
              v-model="localAction.unsubscribe_reason"
              :placeholder="__('Enter unsubscribe reason...')"
              rows="2"
            />
          </div>
        </div>

        <!-- Delay Configuration -->
        <div class="pt-4 border-t border-gray-200">
          <DelaySelector
            v-model="localAction.delay_minutes"
            :label="__('Delay')"
            :optional="true"
          />
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end space-x-2">
        <Button variant="outline" @click="cancel">
          {{ __('Cancel') }}
        </Button>
        <Button variant="solid" theme="blue" @click="save">
          {{ __('Save Action') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { FeatherIcon, Button, FormControl, Dialog, Autocomplete, call } from 'frappe-ui'
import DelaySelector from './DelaySelector.vue'
import ZaloContentEditor from './ZaloContentEditor.vue'
import EmailContentEditor from './EmailContentEditor.vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  action: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:show', 'save', 'cancel'])

// Local state
const localShow = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

const localAction = ref({})

// Tags state
const tags = ref([])
const loadingTags = ref(false)

// Talent fields state
const talentFields = ref([])
const loadingTalentFields = ref(false)

// Flows state
const flows = ref([])
const loadingFlows = ref(false)

// Users state
const users = ref([])
const loadingUsers = ref(false)

// Computed tag options for Autocomplete
const tagOptions = computed(() => {
  return tags.value.map(tag => ({
    label: tag.title,
    value: tag.name,
    description: tag.name,
    color: tag.color
  }))
})

// Selected tag for Autocomplete v-model
const selectedTagId = computed({
  get: () => {
    // Return the tag_id string for Autocomplete
    return localAction.value.tag_id
  },
  set: (value) => {
    // Handle when Autocomplete sets value
    handleTagSelect(value)
  }
})

// Selected tag info
const selectedTag = computed(() => {
  if (!localAction.value.tag_id) return null
  const tagId = typeof localAction.value.tag_id === 'object' ? localAction.value.tag_id.value : localAction.value.tag_id
  return tags.value.find(tag => tag.name === tagId)
})

// Email content object for EmailContentEditor
const emailContent = computed(() => ({
  email_subject: localAction.value.email_subject || '',
  email_content: localAction.value.email_content || localAction.value.content || '',
  attachments: localAction.value.attachments || [],
  sender_account: localAction.value.sender_account || null
}))

// Handle email content update from EmailContentEditor
const handleEmailContentUpdate = (content) => {
  console.log('📧 Email content updated:', content)
  localAction.value.email_subject = content.email_subject
  localAction.value.email_content = content.email_content
  localAction.value.attachments = content.attachments
  localAction.value.sender_account = content.sender_account
}

// Computed talent field options for Autocomplete
const talentFieldOptions = computed(() => {
  return talentFields.value
    .filter(field => {
      // Filter out system fields and child tables
      return !field.fieldname.startsWith('_') && 
             !['Table', 'Section Break', 'Column Break', 'HTML', 'Button'].includes(field.fieldtype)
    })
    .map(field => ({
      label: field.label,
      value: field.fieldname,
      description: field.fieldtype,
      fieldtype: field.fieldtype
    }))
})

// Selected field for ADD_CUSTOM_FIELD
const selectedFieldName = computed({
  get: () => localAction.value.field_name,
  set: (value) => {
    // If value is object from Autocomplete, extract fieldname
    const fieldname = typeof value === 'object' ? value.value : value
    localAction.value.field_name = fieldname
    
    // Find field metadata
    const field = talentFields.value.find(f => f.fieldname === fieldname)
    if (field) {
      console.log('📝 Field selected:', field)
    }
  }
})

// Get selected field metadata
const selectedField = computed(() => {
  if (!localAction.value.field_name) return null
  const fieldname = typeof localAction.value.field_name === 'object' 
    ? localAction.value.field_name.value 
    : localAction.value.field_name
  return talentFields.value.find(f => f.fieldname === fieldname)
})

// Helper to parse Select field options
const getSelectOptions = (optionsString) => {
  if (!optionsString) return []
  const lines = optionsString.split('\n').filter(line => line.trim())
  return lines.map(line => ({
    label: line.trim(),
    value: line.trim()
  }))
}

// Computed flow options for Autocomplete
const flowOptions = computed(() => {
  return flows.value.map(flow => ({
    label: flow.title || flow.name,
    value: flow.name,
    description: `${flow.type || 'Flow'} - ${flow.status || 'Unknown'}`,
    status: flow.status,
    type: flow.type
  }))
})

// Selected flow for START_FLOW/STOP_FLOW
const selectedFlowId = computed({
  get: () => localAction.value.flow_id,
  set: (value) => {
    // If value is object from Autocomplete, extract flow ID
    const flowId = typeof value === 'object' ? value.value : value
    localAction.value.flow_id = flowId
    
    // Find flow metadata
    const flow = flows.value.find(f => f.name === flowId)
    if (flow) {
      console.log('🔄 Flow selected:', flow)
    }
  }
})

// Get selected flow metadata
const selectedFlow = computed(() => {
  if (!localAction.value.flow_id) return null
  const flowId = typeof localAction.value.flow_id === 'object' 
    ? localAction.value.flow_id.value 
    : localAction.value.flow_id
  return flows.value.find(f => f.name === flowId)
})

// Computed user options for Autocomplete
const userOptions = computed(() => {
  return users.value.map(user => ({
    label: user.full_name || user.name,
    value: user.name,
    description: user.email || user.name,
    full_name: user.full_name,
    email: user.email
  }))
})

// Selected assignee for SENT_NOTIFICATION (single user)
const selectedAssignee = computed({
  get: () => localAction.value.assignee,
  set: (value) => {
    const userId = typeof value === 'object' ? value.value : value
    localAction.value.assignee = userId
    
    const user = users.value.find(u => u.name === userId)
    if (user) {
      console.log('👤 Assignee selected:', user)
    }
  }
})

// Get selected assignee user metadata
const selectedAssigneeUser = computed(() => {
  if (!localAction.value.assignee) return null
  const userId = typeof localAction.value.assignee === 'object' 
    ? localAction.value.assignee.value 
    : localAction.value.assignee
  return users.value.find(u => u.name === userId)
})

// Selected recipients for EXTERNAL_REQUEST (multiple users)
const selectedRecipients = computed({
  get: () => {
    // Parse recipients if it's a string (comma-separated)
    if (typeof localAction.value.recipients === 'string') {
      return localAction.value.recipients.split(',').map(r => r.trim()).filter(Boolean)
    }
    // If it's already an array
    return localAction.value.recipients || []
  },
  set: (value) => {
    // Value can be array of user IDs or array of objects
    let userIds = []
    if (Array.isArray(value)) {
      userIds = value.map(v => typeof v === 'object' ? v.value : v)
    } else if (value) {
      userIds = [typeof value === 'object' ? value.value : value]
    }
    
    // Store as comma-separated string
    localAction.value.recipients = userIds.join(',')
    console.log('👥 Recipients selected:', userIds)
  }
})

// Get selected recipient users metadata
const recipientUsers = computed(() => {
  const recipients = selectedRecipients.value
  if (!recipients || recipients.length === 0) return []
  
  return recipients.map(userId => {
    return users.value.find(u => u.name === userId)
  }).filter(Boolean)
})

// Load tags from API
const loadTags = async () => {
  try {
    loadingTags.value = true
    const result = await call('frappe.client.get_list', {
      doctype: 'Mira Tag',
      fields: ['name', 'title', 'color', 'order'],
      order_by: '`order` asc',
      limit_page_length: 0
    })
    
    if (result) {
      tags.value = result
      console.log('✅ Loaded tags:', tags.value)
    }
  } catch (error) {
    console.error('❌ Error loading tags:', error)
  } finally {
    loadingTags.value = false
  }
}

// Handle tag selection
const handleTagSelect = (selectedValue) => {
  console.log('🏷️ Tag selected:', selectedValue)
  
  // If selectedValue is an object (from Autocomplete), extract the value
  const tagName = typeof selectedValue === 'object' ? selectedValue.value : selectedValue
  
  const tag = tags.value.find(t => t.name === tagName)
  if (tag) {
    localAction.value.tag_id = tag.name      // Store only the tag name (ID)
    localAction.value.tag_name = tag.title
    localAction.value.tag_color = tag.color
    console.log('✅ Tag data set:', { tag_id: tag.name, tag_name: tag.title, tag_color: tag.color })
  }
}

// Load Mira Talent fields from doctype metadata
const loadTalentFields = async () => {
  try {
    loadingTalentFields.value = true
    const result = await call('frappe.client.get', {
      doctype: 'DocType',
      name: 'Mira Talent'
    })
    
    if (result && result.fields) {
      talentFields.value = result.fields
      console.log('✅ Loaded Mira Talent fields:', talentFields.value.length)
    }
  } catch (error) {
    console.error('❌ Error loading Mira Talent fields:', error)
  } finally {
    loadingTalentFields.value = false
  }
}

// Load Mira Flows from API
const loadFlows = async () => {
  try {
    loadingFlows.value = true
    const result = await call('frappe.client.get_list', {
      doctype: 'Mira Flow',
      fields: ['name', 'title', 'description', 'status', 'type', 'campaign_id'],
      filters: [['status', '!=', 'Archived']],
      order_by: 'modified desc',
      limit_page_length: 100
    })
    
    if (result) {
      flows.value = result
      console.log('✅ Loaded flows:', flows.value.length)
    }
  } catch (error) {
    console.error('❌ Error loading flows:', error)
  } finally {
    loadingFlows.value = false
  }
}

// Load system users from API
const loadUsers = async () => {
  try {
    loadingUsers.value = true
    const result = await call('frappe.client.get_list', {
      doctype: 'User',
      fields: ['name', 'full_name', 'email', 'user_image'],
      filters: [['enabled', '=', 1]],
      order_by: 'full_name asc',
      limit_page_length: 0
    })
    
    if (result) {
      users.value = result
      console.log('✅ Loaded users:', users.value.length)
    }
  } catch (error) {
    console.error('❌ Error loading users:', error)
  } finally {
    loadingUsers.value = false
  }
}

// Load tags on mount
onMounted(() => {
  loadTags()
  loadTalentFields()
  loadFlows()
  loadUsers()
})

// Watch for action changes
watch(() => props.action, (newAction) => {
  console.log('👀 ActionEditor received action prop:', newAction)
  if (newAction) {
    localAction.value = { ...newAction }
    console.log('📝 ActionEditor localAction set to:', localAction.value)
    
    // Log tag-specific fields for debugging
    if (newAction.action_type === 'ADD_TAG' || newAction.action_type === 'REMOVE_TAG') {
      console.log('🏷️ Tag fields:', {
        tag_id: localAction.value.tag_id,
        tag_name: localAction.value.tag_name,
        tag_color: localAction.value.tag_color
      })
    }
  }
}, { immediate: true, deep: true })

// Action type options
const actionTypeOptions = [
  { label: __('Send Email'), value: 'EMAIL' },
  { label: __('Send Zalo/SMS Message'), value: 'MESSAGE' },
  { label: __('Update Field Value'), value: 'ADD_CUSTOM_FIELD' },
  { label: __('Add Tag'), value: 'ADD_TAG' },
  { label: __('Remove Tag'), value: 'REMOVE_TAG' },
  { label: __('Stop Tracking'), value: 'UNSUBSCRIBE' },
  { label: __('Start Flow'), value: 'START_FLOW' },
  { label: __('Stop Flow'), value: 'STOP_FLOW' },
  { label: __('Create Task'), value: 'SENT_NOTIFICATION' },
  { label: __('Send Internal Notification'), value: 'EXTERNAL_REQUEST' },
  { label: __('Handoff to ATS'), value: 'AI_CALL' }
]

const channelOptions = [
  { label: __('Email'), value: 'Email' },
  { label: __('SMS'), value: 'SMS' },
  { label: __('Zalo'), value: 'Zalo' },
  { label: __('Messenger'), value: 'Messenger' }
]

const messageChannelOptions = [
  { label: __('Zalo'), value: 'Zalo' },
  { label: __('SMS'), value: 'SMS' }
]

// Helper functions
const getActionIcon = (actionType) => {
  const iconMap = {
    'EMAIL': 'mail',
    'MESSAGE': 'message-circle',
    'ADD_CUSTOM_FIELD': 'edit',
    'ADD_TAG': 'tag',
    'REMOVE_TAG': 'tag',
    'UNSUBSCRIBE': 'user-x',
    'START_FLOW': 'play',
    'STOP_FLOW': 'stop-circle',
    'SENT_NOTIFICATION': 'bell',
    'EXTERNAL_REQUEST': 'external-link',
    'AI_CALL': 'phone'
  }
  return iconMap[actionType] || 'zap'
}

const getActionLabel = (actionType) => {
  const action = actionTypeOptions.find(a => a.value === actionType)
  return action ? action.label : actionType
}

const getActionDescription = (actionType) => {
  const descriptions = {
    'EMAIL': __('Send automated email to talent'),
    'MESSAGE': __('Send Zalo/SMS message to talent'),
    'ADD_CUSTOM_FIELD': __('Update custom field data'),
    'ADD_TAG': __('Add tag to talent profile'),
    'REMOVE_TAG': __('Remove tag from talent profile'),
    'UNSUBSCRIBE': __('Stop tracking talent'),
    'START_FLOW': __('Start another automation flow'),
    'STOP_FLOW': __('Stop current automation flow'),
    'SENT_NOTIFICATION': __('Create task or notification'),
    'EXTERNAL_REQUEST': __('Send internal notification to team'),
    'AI_CALL': __('Handoff talent to ATS system')
  }
  return descriptions[actionType] || ''
}

const needsChannelForAction = (actionType) => {
  return ['EMAIL', 'MESSAGE'].includes(actionType)
}

const handleActionTypeChange = () => {
  // Reset action-specific fields when type changes
  const actionType = localAction.value.action_type
  
  // Clear previous fields
  delete localAction.value.email_subject
  delete localAction.value.email_content
  delete localAction.value.attachments
  delete localAction.value.sender_account
  delete localAction.value.field_name
  delete localAction.value.field_value
  delete localAction.value.field_type
  delete localAction.value.field_label
  delete localAction.value.tag_id
  delete localAction.value.tag_name
  delete localAction.value.tag_color
  delete localAction.value.flow_id
  delete localAction.value.flow_title
  delete localAction.value.flow_type
  delete localAction.value.flow_status
  delete localAction.value.flow_parameters
  delete localAction.value.task_title
  delete localAction.value.task_subject
  delete localAction.value.task_description
  delete localAction.value.task_priority
  delete localAction.value.task_due_date
  delete localAction.value.assignee
  delete localAction.value.assignee_name
  delete localAction.value.assignee_email
  delete localAction.value.notification_title
  delete localAction.value.notification_message
  delete localAction.value.recipients
  delete localAction.value.recipient_names
  delete localAction.value.recipient_count
  delete localAction.value.ats_system
  delete localAction.value.handoff_data
  delete localAction.value.unsubscribe_reason
  
  // Set default channel based on action type
  if (actionType === 'EMAIL') {
    localAction.value.channel_type = 'Email'
  } else if (actionType === 'MESSAGE') {
    localAction.value.channel_type = 'Zalo'
  }
}

// Methods
const save = () => {
  // Build action parameters based on action type
  const actionParams = {}
  
  switch (localAction.value.action_type) {
    case 'EMAIL':
      actionParams.email_subject = localAction.value.email_subject
      actionParams.email_content = localAction.value.email_content
      actionParams.attachments = localAction.value.attachments || []
      actionParams.sender_account = localAction.value.sender_account || null
      // Keep 'content' for backward compatibility
      actionParams.content = localAction.value.email_content
      break
    case 'MESSAGE':
      actionParams.channel = localAction.value.channel_type
      actionParams.content = localAction.value.content
      break
    case 'ADD_CUSTOM_FIELD':
      actionParams.field_name = localAction.value.field_name
      actionParams.field_value = localAction.value.field_value
      // Include field type and label for backend validation
      if (selectedField.value) {
        actionParams.field_type = selectedField.value.fieldtype
        actionParams.field_label = selectedField.value.label
      }
      break
    case 'ADD_TAG':
    case 'REMOVE_TAG':
      actionParams.tag_id = localAction.value.tag_id
      actionParams.tag_name = localAction.value.tag_name
      actionParams.tag_color = localAction.value.tag_color
      break
    case 'START_FLOW':
    case 'STOP_FLOW':
      actionParams.flow_id = localAction.value.flow_id
      // Include flow metadata for reference
      if (selectedFlow.value) {
        actionParams.flow_title = selectedFlow.value.title
        actionParams.flow_type = selectedFlow.value.type
        actionParams.flow_status = selectedFlow.value.status
      }
      break
    case 'SENT_NOTIFICATION':
      actionParams.task_subject = localAction.value.task_subject
      actionParams.task_description = localAction.value.task_description
      actionParams.assignee = localAction.value.assignee
      actionParams.task_priority = localAction.value.task_priority
      actionParams.task_due_date = localAction.value.task_due_date
      // Include assignee metadata for display
      if (selectedAssigneeUser.value) {
        actionParams.assignee_name = selectedAssigneeUser.value.full_name
        actionParams.assignee_email = selectedAssigneeUser.value.email
      }
      break
    case 'EXTERNAL_REQUEST':
      actionParams.notification_title = localAction.value.notification_title
      actionParams.notification_message = localAction.value.notification_message
      actionParams.recipients = localAction.value.recipients
      // Include recipients metadata for display
      if (recipientUsers.value.length > 0) {
        actionParams.recipient_names = recipientUsers.value.map(u => u.full_name || u.name).join(', ')
        actionParams.recipient_count = recipientUsers.value.length
      }
      break
    case 'AI_CALL':
      actionParams.ats_system = localAction.value.ats_system
      actionParams.handoff_data = localAction.value.handoff_data
      break
    case 'UNSUBSCRIBE':
      actionParams.unsubscribe_reason = localAction.value.unsubscribe_reason
      break
  }
  
  // Set action parameters
  localAction.value.action_parameters = actionParams

  console.log('📤 ActionEditor saving action:', localAction.value)
  
  console.log('📤 ActionEditor emitting save:', {
    action_type: localAction.value.action_type,
    action_parameters: actionParams,
    full_action: localAction.value
  })
  
  emit('save', { ...localAction.value })
}

const cancel = () => {
  emit('cancel')
}
</script>
