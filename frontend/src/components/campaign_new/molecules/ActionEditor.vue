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
            <FormControl
              type="text"
              :label="__('Email Subject')"
              v-model="localAction.email_subject"
              :placeholder="__('Enter email subject...')"
              required
            />
            <FormControl
              type="textarea"
              :label="__('Email Content')"
              v-model="localAction.content"
              :placeholder="__('Enter email content...')"
              rows="6"
              required
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
            <FormControl
              type="text"
              :label="__('Field Name')"
              v-model="localAction.field_name"
              :placeholder="__('Enter field name...')"
              required
            />
            <FormControl
              type="text"
              :label="__('Field Value')"
              v-model="localAction.field_value"
              :placeholder="__('Enter field value...')"
              required
            />
          </div>

          <!-- ADD_TAG / REMOVE_TAG Action -->
          <div v-else-if="['ADD_TAG', 'REMOVE_TAG'].includes(localAction.action_type)" class="space-y-4">
            <FormControl
              type="text"
              :label="__('Tag Name')"
              v-model="localAction.tag_name"
              :placeholder="__('Enter tag name...')"
              required
            />
            <FormControl
              type="textarea"
              :label="__('Tag Description (Optional)')"
              v-model="localAction.tag_description"
              :placeholder="__('Enter tag description...')"
              rows="2"
            />
          </div>

          <!-- START_FLOW / STOP_FLOW Action -->
          <div v-else-if="['START_FLOW', 'STOP_FLOW'].includes(localAction.action_type)" class="space-y-4">
            <FormControl
              type="text"
              :label="__('Flow ID')"
              v-model="localAction.flow_id"
              :placeholder="__('Enter flow ID...')"
              required
            />
            <FormControl
              type="textarea"
              :label="__('Flow Parameters (JSON)')"
              v-model="localAction.flow_parameters"
              :placeholder="__('Enter flow parameters as JSON...')"
              rows="3"
            />
          </div>

          <!-- SENT_NOTIFICATION Action -->
          <div v-else-if="localAction.action_type === 'SENT_NOTIFICATION'" class="space-y-4">
            <FormControl
              type="text"
              :label="__('Task Title')"
              v-model="localAction.task_title"
              :placeholder="__('Enter task title...')"
              required
            />
            <FormControl
              type="textarea"
              :label="__('Task Description')"
              v-model="localAction.task_description"
              :placeholder="__('Enter task description...')"
              rows="3"
              required
            />
            <FormControl
              type="text"
              :label="__('Assignee')"
              v-model="localAction.assignee"
              :placeholder="__('Enter assignee email or ID...')"
            />
          </div>

          <!-- EXTERNAL_REQUEST Action -->
          <div v-else-if="localAction.action_type === 'EXTERNAL_REQUEST'" class="space-y-4">
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
              :placeholder="__('Enter notification message...')"
              rows="3"
              required
            />
            <FormControl
              type="text"
              :label="__('Recipients')"
              v-model="localAction.recipients"
              :placeholder="__('Enter recipient emails (comma separated)...')"
            />
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
import { ref, computed, watch } from 'vue'
import { FeatherIcon, Button, FormControl, Dialog } from 'frappe-ui'
import DelaySelector from './DelaySelector.vue'
import ZaloContentEditor from './ZaloContentEditor.vue'

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

// Watch for action changes
watch(() => props.action, (newAction) => {
  if (newAction) {
    localAction.value = { ...newAction }
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
  delete localAction.value.field_name
  delete localAction.value.field_value
  delete localAction.value.tag_name
  delete localAction.value.tag_description
  delete localAction.value.flow_id
  delete localAction.value.flow_parameters
  delete localAction.value.task_title
  delete localAction.value.task_description
  delete localAction.value.assignee
  delete localAction.value.notification_title
  delete localAction.value.notification_message
  delete localAction.value.recipients
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
      actionParams.subject = localAction.value.email_subject
      actionParams.content = localAction.value.content
      break
    case 'MESSAGE':
      actionParams.channel = localAction.value.channel_type
      actionParams.content = localAction.value.content
      break
    case 'ADD_CUSTOM_FIELD':
      actionParams.field_name = localAction.value.field_name
      actionParams.field_value = localAction.value.field_value
      break
    case 'ADD_TAG':
    case 'REMOVE_TAG':
      actionParams.tag_name = localAction.value.tag_name
      actionParams.tag_description = localAction.value.tag_description
      break
    case 'START_FLOW':
    case 'STOP_FLOW':
      actionParams.flow_id = localAction.value.flow_id
      actionParams.flow_parameters = localAction.value.flow_parameters
      break
    case 'SENT_NOTIFICATION':
      actionParams.task_title = localAction.value.task_title
      actionParams.task_description = localAction.value.task_description
      actionParams.assignee = localAction.value.assignee
      break
    case 'EXTERNAL_REQUEST':
      actionParams.notification_title = localAction.value.notification_title
      actionParams.notification_message = localAction.value.notification_message
      actionParams.recipients = localAction.value.recipients
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
  
  emit('save', { ...localAction.value })
}

const cancel = () => {
  emit('cancel')
}
</script>
