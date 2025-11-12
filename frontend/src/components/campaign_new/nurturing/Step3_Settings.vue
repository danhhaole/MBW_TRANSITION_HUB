<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center mb-2">
        <div class="w-10 h-10 rounded-lg bg-green-500 text-white flex items-center justify-center mr-3">
          <FeatherIcon name="settings" class="h-5 w-5" />
        </div>
        <div>
          <h3 class="text-lg font-semibold text-gray-900">
            {{ __('Nurturing Settings') }}
          </h3>
          <p class="text-sm text-gray-500">
            {{ __('Configure triggers and automated actions for talent nurturing') }}
          </p>
        </div>
      </div>
    </div>


    <!-- Triggers Section -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h4 class="text-sm font-semibold text-gray-900">
            {{ __('Triggers') }}
          </h4>
          <p class="text-xs text-gray-500">
            {{ __('Events that will activate automated actions') }}
          </p>
        </div>
        <!-- Add Trigger Button with Popover -->
        <Popover placement="bottom">
          <template #target="{ togglePopover }">
            <Button
              variant="solid"
              @click="togglePopover()"
            >
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
              {{ __('Add Trigger') }}
            </Button>
          </template>
          <template #body-main>
            <div class="w-80 bg-white rounded-lg border border-gray-200">
              <div class="p-3 border-b border-gray-200">
                <h4 class="text-sm font-semibold text-gray-900">{{ __('Select Trigger Type') }}</h4>
                <p class="text-xs text-gray-500 mt-1">{{ __('Choose when this automation should activate') }}</p>
              </div>
              <div class="p-2 max-h-96 overflow-y-auto">
                <button
                  v-for="option in availableTriggerTypes"
                  :key="option.value"
                  @click="createTrigger(option.value)"
                  class="w-full text-left px-3 py-2 rounded hover:bg-gray-50 transition-colors group"
                >
                  <div class="flex items-start space-x-3">
                    <div class="w-8 h-8 rounded-lg bg-green-100 flex items-center justify-center flex-shrink-0 group-hover:bg-green-200 transition-colors">
                      <FeatherIcon name="zap" class="h-4 w-4 text-green-600" />
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900">{{ option.label }}</p>
                      <p class="text-xs text-gray-500 mt-0.5">{{ getTriggerDescription(option.value) }}</p>
                    </div>
                  </div>
                </button>
                
                <!-- No available triggers -->
                <div v-if="availableTriggerTypes.length === 0" class="text-center py-6">
                  <p class="text-xs text-gray-500">{{ __('All trigger types have been added') }}</p>
                </div>
              </div>
            </div>
          </template>
        </Popover>
      </div>

      <!-- Triggers List -->
      <div v-if="localTriggers.length > 0" class="space-y-3">
        <div
          v-for="(trigger, index) in localTriggers"
          :key="index"
          class="border border-gray-200 rounded-lg p-4 hover:border-green-300 transition-colors"
        >
          <!-- Trigger Header -->
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-start space-x-3 flex-1">
              <div class="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center flex-shrink-0">
                <FeatherIcon name="zap" class="h-5 w-5 text-green-600" />
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between mb-1">
                  <h5 class="text-sm font-medium text-gray-900">
                    {{ getTriggerLabel(trigger.trigger_type) }}
                  </h5>
                  
                  <!-- Status Toggle Switch -->
                  <button
                    @click.stop="toggleTriggerStatus(index)"
                    class="inline-flex items-center space-x-2 px-3 py-1.5 rounded text-xs font-medium transition-all"
                    :class="getStatusClass(trigger.status || 'active')"
                  >
                    <FeatherIcon :name="getStatusIcon(trigger.status || 'active')" class="h-3.5 w-3.5" />
                    <span>{{ getStatusLabel(trigger.status || 'active') }}</span>
                  </button>
                </div>
                <p class="text-xs text-gray-500">
                  {{ getTriggerDescription(trigger.trigger_type) }}
                </p>
              </div>
            </div>

            <!-- Delete Trigger -->
            <div>
              <Button
                variant="ghost"
                size="sm"
                @click="removeTrigger(index)"
              >
                <FeatherIcon name="trash-2" class="h-4 w-4 text-red-500" />
              </Button>
            </div>
          </div>

          <!-- Trigger Actions -->
          <div class="ml-10 mt-3">
            <div class="flex items-center justify-between mb-3">
              <p class="text-xs font-medium text-gray-700">
                {{ __('Actions') }} ({{ trigger.actions?.length || 0 }})
              </p>
            
              <!-- Add Action Button with Popover -->
              <Popover placement="bottom-end">
                <template #target="{ togglePopover }">
                  <Button
                    variant="outline"
                    size="sm"
                    @click="togglePopover()"
                  >
                    <template #prefix>
                      <FeatherIcon name="plus" class="h-3 w-3" />
                    </template>
                    {{ __('Add Action') }}
                  </Button>
                </template>
                <template #body-main="{ close }">
                  <div class="w-72 bg-white rounded-lg border border-gray-200">
                    <div class="p-3 border-b border-gray-200">
                      <h4 class="text-xs font-semibold text-gray-900">{{ __('Select Action Type') }}</h4>
                    </div>
                    <div class="p-2 max-h-64 overflow-y-auto">
                      <button
                        v-for="option in actionTypeOptions"
                        :key="option.value"
                        @click="close(); addActionToTrigger(index, option.value)"
                        class="w-full text-left px-3 py-2 rounded hover:bg-gray-50 transition-colors group"
                      >
                        <div class="flex items-center space-x-2">
                          <div class="w-6 h-6 rounded bg-green-100 flex items-center justify-center flex-shrink-0 group-hover:bg-green-200">
                            <FeatherIcon :name="getActionIcon(option.value)" class="h-3 w-3 text-green-600" />
                          </div>
                          <div class="flex-1 min-w-0">
                            <p class="text-xs font-medium text-gray-900">{{ option.label }}</p>
                          </div>
                        </div>
                      </button>
                    </div>
                  </div>
                </template>
              </Popover>
            </div>
            
            <div v-if="trigger.actions && trigger.actions.length > 0">
              <div class="space-y-0">
                <template
                  v-for="(action, actionIndex) in trigger.actions"
                  :key="actionIndex"
                >
                  <!-- Delay Arrow (before action) -->
                  <div v-if="action.delay_minutes > 0" class="flex items-center py-2">
                    <div class="flex-1 flex items-center">
                      <div class="h-px bg-gray-300 flex-1"></div>
                      <div class="mx-2 flex items-center space-x-1 text-xs text-gray-500 bg-green-50 border border-green-200 px-2 py-1 rounded">
                        <FeatherIcon name="clock" class="h-3 w-3 text-green-600" />
                        <span class="font-medium text-green-700">{{ formatDelayLong(action.delay_minutes) }}</span>
                      </div>
                      <div class="h-px bg-gray-300 flex-1"></div>
                    </div>
                  </div>
                  
                  <!-- Immediate indicator (if no delay and not first action) -->
                  <div v-else-if="actionIndex > 0" class="flex items-center py-1">
                    <div class="flex-1 flex items-center">
                      <div class="h-px bg-gray-300 flex-1"></div>
                      <div class="mx-2 text-xs text-gray-400 bg-gray-50 border border-gray-200 px-2 py-0.5 rounded">
                        {{ __('Immediately') }}
                      </div>
                      <div class="h-px bg-gray-300 flex-1"></div>
                    </div>
                  </div>
                  
                  <!-- Action Card -->
                  <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
                    <div class="flex items-start justify-between">
                      <div class="flex items-start space-x-3 flex-1">
                        <div class="w-8 h-8 rounded-lg bg-green-100 flex items-center justify-center flex-shrink-0">
                          <FeatherIcon :name="getActionIcon(action.action_type)" class="h-4 w-4 text-green-600" />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-center justify-between mb-1">
                            <h6 class="text-xs font-medium text-gray-900">
                              {{ getActionLabel(action.action_type) }}
                            </h6>
                          </div>
                          <p class="text-xs text-gray-600 mb-2">
                            {{ getActionSummary(action) }}
                          </p>
                        </div>
                      </div>
                      <div class="flex items-center space-x-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          @click="editAction(action, index, actionIndex)"
                        >
                          <FeatherIcon name="edit-2" class="h-3 w-3" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          theme="red"
                          @click="removeActionFromTrigger(index, actionIndex)"
                        >
                          <FeatherIcon name="trash-2" class="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
            </div>

            <!-- Empty Actions State -->
            <div v-else class="text-center py-6 border-2 border-dashed border-gray-200 rounded-lg">
              <FeatherIcon name="zap" class="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <p class="text-xs text-gray-500">
                {{ __('No actions configured for this trigger') }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12 border-2 border-dashed border-gray-200 rounded-lg">
        <FeatherIcon name="zap" class="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <p class="text-sm font-medium text-gray-900 mb-1">
          {{ __('No triggers configured') }}
        </p>
        <p class="text-xs text-gray-500">
          {{ __('Add triggers to automate actions based on candidate behavior') }}
        </p>
      </div>
    </div>

    <!-- Edit Action Modal -->
    <Dialog
      v-model="showEditAction"
      :options="{
        title: __('Edit Action'),
        size: '4xl'
      }"
    >
      <template #body-content>
        <div v-if="editingAction" class="space-y-6">
          <!-- Action Type Header -->
          <div class="flex items-center space-x-3 pb-4 border-b border-gray-200">
            <div class="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
              <FeatherIcon :name="getActionIcon(editingAction.action_type)" class="h-5 w-5 text-green-600" />
            </div>
            <div>
              <h3 class="text-base font-semibold text-gray-900">{{ getActionLabel(editingAction.action_type) }}</h3>
              <p class="text-xs text-gray-500">{{ getActionDescription(editingAction.action_type) }}</p>
            </div>
          </div>

          <!-- Messenger Content Editor -->
          <div v-if="editingAction.action_type === 'FACEBOOK'">
            <MessengerContentEditor
              :content="editingAction.content || { blocks: [] }"
              @update:content="editingAction.content = $event"
            />
          </div>

          <!-- Zalo Content Editor -->
          <div v-if="editingAction.action_type === 'ZALO'">
            <ZaloContentEditor
              :content="editingAction.content || { blocks: [] }"
              @update:content="editingAction.content = $event"
            />
          </div>

          <!-- SMS Content Editor -->
          <div v-if="editingAction.action_type === 'SMS'">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('SMS Message') }}
                <span class="text-red-500">*</span>
              </label>
              <textarea
                v-model="editingAction.content"
                :placeholder="__('Enter your SMS message...')"
                rows="4"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500 text-sm"
              />
              <div class="flex justify-between items-center mt-2">
                <p class="text-xs text-gray-500">
                  {{ __('Keep it short and clear (max 160 characters)') }}
                </p>
                <span class="text-xs text-gray-500">
                  {{ (editingAction.content?.length || 0) }}/160
                </span>
              </div>
            </div>
          </div>

          <!-- Delay -->
          <div class="pt-4 border-t border-gray-200">
            <DelaySelector
              v-model="editingAction.delay_minutes"
              :label="__('Delay')"
              :optional="true"
            />
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex justify-end space-x-2">
          <Button variant="outline" @click="showEditAction = false">
            {{ __('Cancel') }}
          </Button>
          <Button variant="solid" theme="green" @click="saveAction">
            {{ __('Save') }}
          </Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { FeatherIcon, Button, Dialog, Popover } from 'frappe-ui'
import ZaloContentEditor from '../molecules/ZaloContentEditor.vue'
import MessengerContentEditor from '../molecules/MessengerContentEditor.vue'
import DelaySelector from '../molecules/DelaySelector.vue'

const props = defineProps({
  startDate: String,
  triggers: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits([
  'update:startDate',
  'update:triggers'
])

// Local state
const localTriggers = computed({
  get: () => props.triggers,
  set: (value) => emit('update:triggers', value)
})

const showEditAction = ref(false)
const editingAction = ref(null)
const editingTriggerIndex = ref(-1)
const editingActionIndex = ref(-1)

// Options - Copy from Attraction Campaign
const triggerTypeOptions = [
  { label: 'Message Received', value: 'MESSAGE_RECEIVED' },
  { label: 'Link Clicked', value: 'LINK_CLICKED' },
  { label: 'Comment on Post', value: 'COMMENT_RECEIVED' }
]

// Filter out already added trigger types
const availableTriggerTypes = computed(() => {
  const existingTypes = localTriggers.value.map(t => t.trigger_type)
  return triggerTypeOptions.filter(option => !existingTypes.includes(option.value))
})

const actionTypeOptions = [
  { label: 'Send Facebook Message', value: 'FACEBOOK' },
  { label: 'Send Zalo Message', value: 'ZALO' },
  { label: 'Send SMS', value: 'SMS' }
]

// Status options
const statusOptions = [
  { value: 'active', label: __('Active'), icon: 'check-circle' },
  { value: 'draft', label: __('Draft'), icon: 'circle' }
]

// Helper functions
const getTriggerLabel = (type) => {
  const option = triggerTypeOptions.find(o => o.value === type)
  return option ? option.label : type
}

const getTriggerDescription = (type) => {
  const descriptions = {
    'MESSAGE_RECEIVED': 'When candidate sends a message or replies to your post',
    'LINK_CLICKED': 'When candidate clicks a link in the campaign post',
    'COMMENT_RECEIVED': 'When candidate comments on your Facebook/Zalo post'
  }
  return descriptions[type] || ''
}

const getActionLabel = (type) => {
  const option = actionTypeOptions.find(o => o.value === type)
  return option ? option.label : type
}

const getActionDescription = (type) => {
  const descriptions = {
    'FACEBOOK': 'Send a message via Facebook Messenger',
    'ZALO': 'Send a message via Zalo OA',
    'SMS': 'Send an SMS text message'
  }
  return descriptions[type] || ''
}

const getActionIcon = (type) => {
  const icons = {
    'FACEBOOK': 'facebook',
    'ZALO': 'message-square',
    'SMS': 'smartphone'
  }
  return icons[type] || 'message-circle'
}

const getActionSummary = (action) => {
  if (!action.content) return 'No content configured'
  
  // For Facebook and Zalo (content is object with blocks)
  if ((action.action_type === 'FACEBOOK' || action.action_type === 'ZALO') && typeof action.content === 'object') {
    const blocks = action.content.blocks || []
    const textBlocks = blocks.filter(b => b.type === 'text' && b.text_content)
    if (textBlocks.length > 0) {
      return textBlocks[0].text_content.substring(0, 50) + '...'
    }
    return 'No text content'
  }
  
  // For SMS (content is string)
  if (action.action_type === 'SMS') {
    return action.content.substring(0, 50) + (action.content.length > 50 ? '...' : '')
  }
  
  return 'Action configured'
}

// Trigger management
const createTrigger = (triggerType) => {
  const newTrigger = {
    trigger_type: triggerType,
    status: 'active',
    actions: []
  }
  localTriggers.value = [...localTriggers.value, newTrigger]
}

// Add action to trigger
const addActionToTrigger = (triggerIndex, actionType) => {
  const newAction = {
    action_type: actionType,
    content: getDefaultContent(actionType),
    delay_minutes: 0
  }
  
  const triggers = [...localTriggers.value]
  if (!triggers[triggerIndex].actions) {
    triggers[triggerIndex].actions = []
  }
  triggers[triggerIndex].actions.push(newAction)
  localTriggers.value = triggers
  
  // Open edit modal immediately
  editAction(newAction, triggerIndex, triggers[triggerIndex].actions.length - 1)
}

const getDefaultContent = (actionType) => {
  switch (actionType) {
    case 'FACEBOOK':
    case 'ZALO':
      return { blocks: [] }
    case 'SMS':
      return ''
    default:
      return {}
  }
}

// Edit action
const editAction = (action, triggerIndex, actionIndex) => {
  editingTriggerIndex.value = triggerIndex
  editingActionIndex.value = actionIndex
  editingAction.value = { ...action }
  showEditAction.value = true
}

// Save action
const saveAction = () => {
  const triggers = [...localTriggers.value]
  triggers[editingTriggerIndex.value].actions[editingActionIndex.value] = { ...editingAction.value }
  localTriggers.value = triggers
  
  showEditAction.value = false
  editingAction.value = null
}

// Remove action from trigger
const removeActionFromTrigger = (triggerIndex, actionIndex) => {
  const triggers = [...localTriggers.value]
  triggers[triggerIndex].actions.splice(actionIndex, 1)
  localTriggers.value = triggers
}

// Remove trigger
const removeTrigger = (index) => {
  if (confirm(__('Are you sure you want to delete this trigger and all its actions?'))) {
    const triggers = [...localTriggers.value]
    triggers.splice(index, 1)
    localTriggers.value = triggers
  }
}

// Toggle trigger status
const toggleTriggerStatus = (triggerIndex) => {
  const triggers = [...localTriggers.value]
  const currentStatus = triggers[triggerIndex].status || 'active'
  triggers[triggerIndex].status = currentStatus === 'active' ? 'draft' : 'active'
  localTriggers.value = triggers
}

// Status helper methods
const getStatusLabel = (status) => {
  const option = statusOptions.find(s => s.value === status)
  return option ? option.label : status
}

const getStatusIcon = (status) => {
  const option = statusOptions.find(s => s.value === status)
  return option ? option.icon : 'circle'
}

const getStatusClass = (status) => {
  const classes = {
    'active': 'bg-green-50 text-green-700 border border-green-200 hover:bg-green-100',
    'draft': 'bg-gray-50 text-gray-700 border border-gray-200 hover:bg-gray-100'
  }
  return classes[status] || classes.active
}

const formatDelayLong = (minutes) => {
  if (!minutes || minutes === 0) return __('Immediately')
  
  const weeks = Math.floor(minutes / 10080)
  const days = Math.floor((minutes % 10080) / 1440)
  const hours = Math.floor((minutes % 1440) / 60)
  const mins = minutes % 60
  
  const parts = []
  if (weeks > 0) parts.push(`${weeks} ${weeks === 1 ? __('week') : __('weeks')}`)
  if (days > 0) parts.push(`${days} ${days === 1 ? __('day') : __('days')}`)
  if (hours > 0) parts.push(`${hours} ${hours === 1 ? __('hour') : __('hours')}`)
  if (mins > 0) parts.push(`${mins} ${mins === 1 ? __('minute') : __('minutes')}`)
  
  return parts.join(', ')
}


</script>

<style scoped>
/* Add any custom styles here */
</style>
