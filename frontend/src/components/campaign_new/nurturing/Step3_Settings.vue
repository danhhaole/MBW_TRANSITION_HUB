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
                    <div class="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0 group-hover:bg-blue-200 transition-colors">
                      <FeatherIcon :name="getTriggerIcon(option.value)" class="h-4 w-4 text-blue-600" />
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
          :key="trigger.trigger_type"
          class="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
        >
          <!-- Trigger Header -->
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-start space-x-3 flex-1">
              <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
                <FeatherIcon :name="getTriggerIcon(trigger.trigger_type)" class="h-5 w-5 text-blue-600" />
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

          <!-- Tag Selection for ON_TAG_ADDED/ON_TAG_REMOVED triggers -->
          <div
            v-if="['ON_TAG_ADDED', 'ON_TAG_REMOVED'].includes(trigger.trigger_type)"
            class="ml-10 mt-3 mb-4"
          >
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <div class="flex items-start space-x-2">
                <FeatherIcon name="info" class="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                <div class="flex-1">
                  <p class="text-xs font-medium text-blue-900 mb-2">
                    {{ trigger.trigger_type === 'ON_TAG_ADDED' ? __('When which tag is added?') : __('When which tag is removed?') }}
                  </p>

                  <!-- Tag selector -->
                  <div class="mb-2">
                    <Autocomplete
                      :modelValue="getTriggerTagId(trigger)"
                      @update:modelValue="(value) => handleTriggerTagSelect(index, value)"
                      :options="tagOptions"
                      :placeholder="__('Select tag...')"
                    />
                  </div>

                  <!-- Show selected tag -->
                  <div v-if="getTriggerTag(trigger)" class="flex items-center space-x-2 bg-white border border-blue-200 rounded px-2 py-1.5">
                    <div
                      class="w-3 h-3 rounded"
                      :style="{ backgroundColor: getTriggerTag(trigger).color || '#6B7280' }"
                    ></div>
                    <span class="text-xs font-medium text-gray-900">{{ getTriggerTag(trigger).title }}</span>
                    <span class="text-xs text-gray-500">({{ getTriggerTag(trigger).name }})</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Days Configuration for ON_NO_EMAIL_CLICK trigger -->
          <div
            v-if="trigger.trigger_type === 'ON_NO_EMAIL_CLICK'"
            class="ml-10 mt-3 mb-4"
          >
            <div class="bg-orange-50 border border-orange-200 rounded-lg p-3">
              <div class="flex items-start space-x-2">
                <FeatherIcon name="clock" class="h-4 w-4 text-orange-600 mt-0.5 flex-shrink-0" />
                <div class="flex-1">
                  <p class="text-xs font-medium text-orange-900 mb-2">
                    {{ __('After how many minutes without email click? (For testing: 5 minutes = 5 days in production)') }}
                  </p>

                  <!-- Days input -->
                  <div class="mb-2">
                    <FormControl
                      type="number"
                      :modelValue="getTriggerDays(trigger)"
                      @update:modelValue="(value) => handleTriggerDaysChange(index, value)"
                      :placeholder="__('Enter number of minutes for testing...')"
                      :min="1"
                      :max="1440"
                    />
                  </div>

                  <!-- Show configured days -->
                  <div v-if="getTriggerDays(trigger)" class="flex items-center space-x-2 bg-white border border-orange-200 rounded px-2 py-1.5 mb-2">
                    <FeatherIcon name="alert-circle" class="h-3 w-3 text-orange-600" />
                    <span class="text-xs font-medium text-gray-900">
                      {{ __('Trigger after {0} minute without email click', [getTriggerDays(trigger)]) }}
                    </span>
                  </div>

                  <!-- Test buttons -->
                  <div class="flex gap-2 mt-4">
                    <Button
                      variant="outline"
                      size="sm"
                      :loading="testingEmail"
                      @click="testSendTrackedEmail"
                    >
                      <Mail class="w-4 h-4 mr-2" />
                      Send Test Email
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      :loading="testingTrigger"
                      @click="testTriggerNow"
                    >
                      <Zap class="w-4 h-4 mr-2" />
                      Test Trigger Now
                    </Button>
                  </div>

                  <p class="text-xs text-gray-500 mt-2">
                    {{ __('Actions will be triggered if candidate does not click any email within this period (1 minute for testing).') }}
                  </p>
                </div>
              </div>
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
                          <div class="w-6 h-6 rounded bg-gray-100 flex items-center justify-center flex-shrink-0 group-hover:bg-gray-200">
                            <FeatherIcon :name="getActionIcon(option.value)" class="h-3 w-3 text-gray-600" />
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
                      <div class="mx-2 flex items-center space-x-1 text-xs text-gray-500 bg-blue-50 border border-blue-200 px-2 py-1 rounded">
                        <FeatherIcon name="clock" class="h-3 w-3 text-blue-600" />
                        <span class="font-medium text-blue-700">{{ formatDelayLong(action.delay_minutes) }}</span>
                      </div>
                      <div class="h-px bg-gray-300 flex-1"></div>
                    </div>
                  </div>

                  <!-- Immediate indicator (if no delay and not first action) -->
                  <div v-else-if="actionIndex > 0" class="flex items-center py-1">
                    <div class="flex-1 flex items-center">
                      <div class="h-px bg-gray-300 flex-1"></div>
                      <div class="mx-2 flex items-center space-x-1 text-xs text-green-600 bg-green-50 px-2 py-0.5 rounded">
                        <FeatherIcon name="zap" class="h-3 w-3" />
                        <span class="font-medium">{{ __('Immediate') }}</span>
                      </div>
                      <div class="h-px bg-gray-300 flex-1"></div>
                    </div>
                  </div>

                  <!-- Action Card -->
                  <div class="bg-gray-50 rounded-lg px-3 py-2 border border-gray-200 hover:border-blue-300 transition-colors group">
                    <div class="flex items-center justify-between mb-1">
                      <div class="flex items-center space-x-2 text-xs text-gray-600">
                        <FeatherIcon :name="getActionIcon(action.action_type)" class="h-3 w-3" />
                        <span class="font-medium">{{ getActionLabel(action.action_type) }}</span>
                      </div>
                      <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          @click="editAction(index, actionIndex)"
                          class="p-1 hover:bg-white rounded transition-colors"
                          :title="__('Edit action')"
                        >
                          <FeatherIcon name="edit" class="h-3 w-3 text-gray-500" />
                        </button>
                        <button
                          @click="removeActionFromTrigger(index, actionIndex)"
                          class="p-1 hover:bg-white rounded transition-colors"
                          :title="__('Delete action')"
                        >
                          <FeatherIcon name="trash-2" class="h-3 w-3 text-red-500" />
                        </button>
                      </div>
                    </div>
                    <!-- Show content preview -->
                    <div v-if="getActionPreview(action)" class="text-xs text-gray-500 mt-1 line-clamp-2">
                      <span class="italic">"{{ getActionPreview(action) }}"</span>
                    </div>
                    <div v-else class="text-xs text-gray-400 italic mt-1">
                      {{ __('No content yet') }}
                    </div>
                  </div>

                  <!-- Arrow pointing down (between actions) -->
                  <div v-if="actionIndex < trigger.actions.length - 1" class="flex justify-center py-1">
                    <FeatherIcon name="arrow-down" class="h-4 w-4 text-gray-400" />
                  </div>
                </template>
              </div>
            </div>

            <!-- Empty state -->
            <div v-else class="text-center py-6 bg-gray-50 rounded border-2 border-dashed border-gray-300">
              <p class="text-xs text-gray-500">
                {{ __('No actions added yet. Click "Add Action" to get started.') }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
        <FeatherIcon name="zap" class="h-12 w-12 text-gray-400 mx-auto mb-3" />
        <p class="text-sm text-gray-600 mb-2">
          {{ __('No triggers configured') }}
        </p>
        <p class="text-xs text-gray-500">
          {{ __('Add triggers to automate actions based on candidate behavior') }}
        </p>
      </div>
    </div>

    <!-- Action Editor -->
    <ActionEditor
      v-model:show="showEditAction"
      :action="editingAction"
      @save="handleActionSave"
      @cancel="handleActionCancel"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { FeatherIcon, Button, FormControl, Dialog, TextEditor, Popover, Autocomplete, call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import ActionEditor from '../molecules/ActionEditor.vue'
import {
  CAMPAIGN_TYPES,
  getTriggerTypes,
  getActionTypes,
  getTriggerIcon as getCampaignTriggerIcon,
  getTriggerLabel as getCampaignTriggerLabel,
  getTriggerDescription as getCampaignTriggerDescription,
  getActionIcon as getCampaignActionIcon,
  getActionLabel as getCampaignActionLabel,
  getActionDescription as getCampaignActionDescription
} from '../../../config/campaigns'

// Campaign type for this component
const CAMPAIGN_TYPE = CAMPAIGN_TYPES.NURTURING

// Get campaign-specific trigger and action types
const triggerTypeOptions = getTriggerTypes(CAMPAIGN_TYPE)
const actionTypeOptions = getActionTypes(CAMPAIGN_TYPE)

const toast = useToast()

const props = defineProps({
  triggers: {
    type: Array,
    default: () => []
  },
  startDate: {
    type: String,
    default: ''
  },
  showError: {
    type: Boolean,
    default: false
  },
  targetPool: {
    type: String,
    default: null
  },
  campaignId: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['update:triggers', 'update:startDate'])

// Local state with sorting
const triggerOrder = ['MESSAGE_RECEIVED', 'LINK_CLICKED', 'COMMENT_RECEIVED']

const localTriggers = computed({
  get: () => {
    // Sort triggers by predefined order
    return [...props.triggers].sort((a, b) => {
      const indexA = triggerOrder.indexOf(a.trigger_type)
      const indexB = triggerOrder.indexOf(b.trigger_type)
      return indexA - indexB
    })
  },
  set: (value) => emit('update:triggers', value)
})

// Edit action state
const showEditAction = ref(false)
const editingAction = ref(null)
const editingTriggerIndex = ref(null)
const editingActionIndex = ref(null)

// Tags state
const tags = ref([])
const loadingTags = ref(false)
const hasBirthdayInPool = ref(false)

// Testing state
const testingEmail = ref(false)
const testingTrigger = ref(false)

// Check if pool has birthday
const checkPoolEligibility = async () => {
  console.log('🔍 Step3: checkPoolEligibility called. targetPool:', props.targetPool)
  if (!props.targetPool) {
    console.log('⚠️ Step3: No targetPool provided, skipping check.')
    hasBirthdayInPool.value = false
    return
  }

  try {
    console.log('🚀 Step3: Calling check_pool_has_birthday API for:', props.targetPool)
    const result = await call('mbw_mira.api.campaign.check_pool_has_birthday', {
      pool_name: props.targetPool
    })

    console.log('✅ Step3: API Result:', result)

    if (result) {
      // Handle both direct result (common in frappe-ui call) and wrapped message
      const data = result.message || result
      hasBirthdayInPool.value = data.has_birthday

      console.log('🎂 Step3: Has birthday in pool?', hasBirthdayInPool.value)

      if (data.logs && data.logs.length > 0) {
        console.group('📜 Backend Birthday Check Logs')
        data.logs.forEach(log => console.log(log))
        console.groupEnd()
      }
    }
  } catch (error) {
    console.error('❌ Step3: Error checking birthday eligibility:', error)
  }
}

// Watch targetPool changes
watch(() => props.targetPool, () => {
  checkPoolEligibility()
}, { immediate: true })

// Filter out already added trigger types
const availableTriggerTypes = computed(() => {
  const existingTypes = localTriggers.value.map(t => t.trigger_type)
  const conditionalTypes = ['ON_BIRTHDAY', 'ON_NO_EMAIL_CLICK']

  return triggerTypeOptions.filter(option => {
    // 1. Filter out existing
    if (existingTypes.includes(option.value)) return false

    // 2. Conditional Visibility for Birthday/No-Click
    if (conditionalTypes.includes(option.value)) {
      return hasBirthdayInPool.value
    }

    return true
  })
})

const statusOptions = [
  {
    label: __('Active'),
    value: 'active',
    description: __('Flow is running'),
    icon: 'check-circle',
    iconColor: 'text-green-600'
  },
  {
    label: __('Draft'),
    value: 'draft',
    description: __('Not published yet'),
    icon: 'edit-3',
    iconColor: 'text-gray-600'
  },
  {
    label: __('Paused'),
    value: 'paused',
    description: __('Temporarily stopped'),
    icon: 'pause-circle',
    iconColor: 'text-orange-600'
  },
  {
    label: __('Archived'),
    value: 'archived',
    description: __('No longer in use'),
    icon: 'archive',
    iconColor: 'text-gray-400'
  }
]

const channelTypeOptions = [
  { label: __('Email'), value: 'Email' },
  { label: __('SMS'), value: 'SMS' },
  { label: __('Zalo'), value: 'Zalo' },
  { label: __('Messenger'), value: 'Messenger' }
]

// Computed tag options for Autocomplete
const tagOptions = computed(() => {
  return tags.value.map(tag => ({
    label: tag.title,
    value: tag.name,
    description: tag.name,
    color: tag.color
  }))
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
      console.log('✅ Loaded tags for triggers:', tags.value.length)
    }
  } catch (error) {
    console.error('❌ Error loading tags:', error)
  } finally {
    loadingTags.value = false
  }
}

// Helper methods to get/set tag in trigger conditions
const getTriggerTagId = (trigger) => {
  if (!trigger.conditions) return null

  try {
    const conditions = typeof trigger.conditions === 'string'
      ? JSON.parse(trigger.conditions)
      : trigger.conditions
    return conditions?.tag_id || null
  } catch (e) {
    return null
  }
}

const getTriggerTag = (trigger) => {
  const tagId = getTriggerTagId(trigger)
  if (!tagId) return null
  return tags.value.find(tag => tag.name === tagId)
}

const handleTriggerTagSelect = (triggerIndex, selectedValue) => {
  console.log('🏷️ Trigger tag selected:', selectedValue, 'for trigger index:', triggerIndex)

  // Get the tag ID from selected value
  const tagId = typeof selectedValue === 'object' ? selectedValue.value : selectedValue

  // Find tag details
  const tag = tags.value.find(t => t.name === tagId)
  if (!tag) return

  // Get the trigger from sorted array
  const sortedTrigger = localTriggers.value[triggerIndex]

  // Find it in the original props.triggers array
  const triggers = [...props.triggers]
  const originalIndex = triggers.findIndex(t => t.trigger_type === sortedTrigger.trigger_type)

  if (originalIndex !== -1) {
    // Store tag info in conditions field as formatted JSON (for Code field)
    const conditions = {
      tag_id: tag.name,
      tag_name: tag.title,
      tag_color: tag.color
    }

    // Format with indent for better readability in Code editor
    triggers[originalIndex].conditions = JSON.stringify(conditions, null, 2)
    console.log('✅ Trigger conditions updated:', triggers[originalIndex].conditions)
    emit('update:triggers', triggers)
  }
}

// Helper methods for ON_NO_EMAIL_CLICK days configuration
const getTriggerDays = (trigger) => {
  if (!trigger.conditions) return 1 // Default to 1 minute for testing

  try {
    const conditions = typeof trigger.conditions === 'string'
      ? JSON.parse(trigger.conditions)
      : trigger.conditions
    return conditions?.days_without_click || 1
  } catch (e) {
    return 1
  }
}

const handleTriggerDaysChange = (triggerIndex, days) => {
  console.log('📅 Days changed:', days, 'for trigger index:', triggerIndex)

  // Ensure days is a valid number
  const daysValue = parseInt(days) || 1

  // Get the trigger from sorted array
  const sortedTrigger = localTriggers.value[triggerIndex]

  // Find it in the original props.triggers array
  const triggers = [...props.triggers]
  const originalIndex = triggers.findIndex(t => t.trigger_type === sortedTrigger.trigger_type)

  if (originalIndex !== -1) {
    // Store days in conditions field as formatted JSON
    const conditions = {
      days_without_click: daysValue
    }

    // Format with indent for better readability
    triggers[originalIndex].conditions = JSON.stringify(conditions, null, 2)
    console.log('✅ Trigger days updated:', triggers[originalIndex].conditions)
    emit('update:triggers', triggers)
  }
}

// Load tags on mount
onMounted(() => {
  loadTags()
})

// Helper methods
const needsContent = (actionType) => {
  return ['FACEBOOK', 'ZALO', 'SMS'].includes(actionType)
}

const getContentPlaceholder = (actionType) => {
  const placeholders = {
    'FACEBOOK': __('Hi! Thanks for your interest in our job opening. How can we help you?'),
    'ZALO': __('Xin chào! Cảm ơn bạn đã quan tâm đến vị trí tuyển dụng. Chúng tôi có thể giúp gì cho bạn?'),
    'SMS': __('Thanks for your interest! Reply with your questions.')
  }
  return placeholders[actionType] || __('Write your message...')
}

const getChannelFromActionType = (actionType) => {
  const channelMap = {
    'FACEBOOK': 'Messenger',
    'ZALO': 'Zalo',
    'SMS': 'SMS'
  }
  return channelMap[actionType] || ''
}

const handleActionTypeChange = (action) => {
  // Auto-set channel based on action type
  action.channel_type = getChannelFromActionType(action.action_type)

  // Reset content if not needed
  if (!needsContent(action.action_type)) {
    action.content = ''
  }
}

// Wrapper functions for campaign-specific helpers (keep same names for template compatibility)
const getTriggerIcon = (triggerType) => getCampaignTriggerIcon(triggerType, CAMPAIGN_TYPE)
const getTriggerLabel = (triggerType) => getCampaignTriggerLabel(triggerType, CAMPAIGN_TYPE)
const getTriggerDescription = (triggerType) => getCampaignTriggerDescription(triggerType, CAMPAIGN_TYPE)
const getActionIcon = (actionType) => getCampaignActionIcon(actionType, CAMPAIGN_TYPE)
const getActionLabel = (actionType) => getCampaignActionLabel(actionType, CAMPAIGN_TYPE)
const getActionDescription = (actionType) => getCampaignActionDescription(actionType, CAMPAIGN_TYPE)

const stripHtml = (html) => {
  if (!html) return ''
  const div = document.createElement('div')
  div.innerHTML = html
  return div.textContent || div.innerText || ''
}

const getActionPreview = (action) => {
  // Parse action_parameters if available
  let params = {}
  if (action.action_parameters) {
    try {
      params = typeof action.action_parameters === 'string'
        ? JSON.parse(action.action_parameters)
        : action.action_parameters
    } catch (e) {
      // Ignore parse errors
    }
  }

  // Generate preview based on action type
  switch (action.action_type) {
    case 'EMAIL':
      return params.email_subject || action.email_subject || __('Email message')

    case 'MESSAGE':
      if (params.content || action.content) {
        const content = params.content || action.content
        // For Facebook and Zalo (content is object with blocks)
        if (typeof content === 'object' && content.blocks) {
          const blocks = content.blocks || []
          const textBlocks = blocks.filter(b => b.type === 'text' && b.text_content)
          if (textBlocks.length > 0) {
            return textBlocks[0].text_content
          }
        }
        // For SMS (content is string)
        return stripHtml(content)
      }
      return __('Message content')

    case 'ADD_TAG':
      return `${__('Add tag')}: ${params.tag_name || action.tag_name || '...'}`

    case 'REMOVE_TAG':
      return `${__('Remove tag')}: ${params.tag_name || action.tag_name || '...'}`

    case 'ADD_CUSTOM_FIELD':
      return `${__('Update')} ${params.field_label || params.field_name || action.field_name || '...'} = ${params.field_value || action.field_value || '...'}`

    case 'START_FLOW':
      return `${__('Start flow')}: ${params.flow_title || action.flow_title || params.flow_id || action.flow_id || '...'}`

    case 'STOP_FLOW':
      return `${__('Stop flow')}: ${params.flow_title || action.flow_title || params.flow_id || action.flow_id || '...'}`

    case 'SENT_NOTIFICATION':
      return `${__('Create task')}: ${params.task_subject || action.task_subject || '...'} → ${params.assignee_name || action.assignee_name || params.assignee || action.assignee || '...'}`

    case 'EXTERNAL_REQUEST':
      const recipientCount = params.recipient_count || action.recipient_count
      if (recipientCount) {
        return `${params.notification_title || action.notification_title || __('Notification')} → ${recipientCount} ${__('users')}`
      }
      return `${params.notification_title || action.notification_title || __('Notification')}`

    case 'AI_CALL':
      return `${__('Handoff to')} ${params.ats_system || action.ats_system || 'ATS'}`

    case 'UNSUBSCRIBE':
      return __('Unsubscribe talent')

    case 'UPDATE_FIELD_VALUE':
      return `${__('Update')} ${params.field_label || params.field_name || action.field_name || '...'} = ${params.field_value || action.field_value || '...'}`

    case 'CHANGE_STATUS':
      return `${__('Change to')}: ${params.new_status || action.new_status || '...'}`

    case 'STOP_TRACKING':
      const stop_reason = params.stop_reason || action.stop_reason
      return stop_reason ? `${__('Stop tracking')}: ${stop_reason}` : __('Stop tracking this talent')

    case 'INTERNAL_NOTIFICATION':
      return `${params.notification_title || action.notification_title || __('Notification')}`

    case 'HANDOFF_TO_ATS':
      const notes = params.transfer_notes || action.transfer_notes
      return notes ? `${__('Handoff to')} ${params.ats_system || action.ats_system || 'ATS'}: ${notes}` : `${__('Handoff to')} ${params.ats_system || action.ats_system || 'ATS'}`

    default:
      // Fallback to old content field
      if (action.content) {
        return stripHtml(action.content)
      }
      return ''
  }
}

// Methods
// Create new trigger
const createTrigger = (triggerType) => {
  const newTrigger = {
    trigger_type: triggerType,
    status: 'active',  // Default to active
    actions: []
  }

  // Set default conditions for specific trigger types
  if (triggerType === 'ON_NO_EMAIL_CLICK') {
    newTrigger.conditions = JSON.stringify({
      days_without_click: 1  // 1 phút trong test mode để test nhanh
    }, null, 2)
  }

  localTriggers.value = [...localTriggers.value, newTrigger]
}

// Add action to trigger
const addActionToTrigger = (triggerIndex, actionType) => {
  const newAction = {
    action_type: actionType,
    channel_type: getChannelFromActionType(actionType),
    content: '',
    delay_minutes: 0
  }

  // Get the trigger from sorted array
  const sortedTrigger = localTriggers.value[triggerIndex]

  // Find it in the original props.triggers array
  const triggers = [...props.triggers]
  const originalIndex = triggers.findIndex(t => t.trigger_type === sortedTrigger.trigger_type)

  if (originalIndex !== -1) {
    if (!triggers[originalIndex].actions) {
      triggers[originalIndex].actions = []
    }
    triggers[originalIndex].actions.push(newAction)
    emit('update:triggers', triggers)

    // Open edit modal immediately
    editAction(triggerIndex, triggers[originalIndex].actions.length - 1)
  }
}

// Edit action
const editAction = (triggerIndex, actionIndex) => {
  editingTriggerIndex.value = triggerIndex
  editingActionIndex.value = actionIndex

  const action = { ...localTriggers.value[triggerIndex].actions[actionIndex] }

  console.log('📝 Editing action:', action)
  console.log('📦 action_parameters type:', typeof action.action_parameters)
  console.log('📦 action_parameters value:', action.action_parameters)

  // Parse and spread action_parameters based on action type
  let params = {}

  if (action.action_parameters) {
    // Parse if string, use if object
    if (typeof action.action_parameters === 'string') {
      try {
        params = JSON.parse(action.action_parameters)
        console.log('✅ Parsed params from string:', params)
      } catch (e) {
        console.error('❌ Error parsing action_parameters:', e)
      }
    } else if (typeof action.action_parameters === 'object') {
      params = { ...action.action_parameters }
      console.log('✅ Using params from object:', params)
    }
  }

  // Spread all parameters into action for form binding
  Object.assign(action, params)

  // Special handling for specific action types to ensure correct field mapping
  switch (action.action_type) {
    case 'ADD_TAG':
    case 'REMOVE_TAG':
      // Ensure tag fields are available: tag_id, tag_name, tag_color
      console.log('🏷️ Tag action fields:', {
        tag_id: action.tag_id,
        tag_name: action.tag_name,
        tag_color: action.tag_color
      })
      break

    case 'ADD_CUSTOM_FIELD':
      // Ensure field update fields are available: field_name, field_value, field_type, field_label
      console.log('📝 Field update action:', {
        field_name: action.field_name,
        field_value: action.field_value,
        field_type: action.field_type,
        field_label: action.field_label
      })
      break

    case 'START_FLOW':
    case 'STOP_FLOW':
      // Ensure flow fields are available: flow_id, flow_title, flow_type, flow_status
      console.log('🔄 Flow action:', {
        flow_id: action.flow_id,
        flow_title: action.flow_title,
        flow_type: action.flow_type,
        flow_status: action.flow_status
      })
      break

    case 'SENT_NOTIFICATION':
      // Ensure task fields are available: task_subject, task_description, assignee, priority, due_date
      console.log('📋 Task action:', {
        task_subject: action.task_subject,
        task_description: action.task_description,
        assignee: action.assignee,
        task_priority: action.task_priority,
        task_due_date: action.task_due_date
      })
      break

    case 'EXTERNAL_REQUEST':
      // Ensure notification fields are available: notification_title, notification_message, recipients
      console.log('🔔 Notification action:', {
        notification_title: action.notification_title,
        notification_message: action.notification_message,
        recipients: action.recipients
      })
      break

    case 'EMAIL':
      // Ensure email fields are available: email_subject, block_content, template_content, mjml_content, attachments, sender_account
      console.log('📧 Email action:', {
        email_subject: action.email_subject,
        email_content: action.email_content,        // Legacy field
        block_content: action.block_content,        // EmailBuilder format (primary for editing)
        template_content: action.template_content,  // HTML format
        mjml_content: action.mjml_content,          // MJML format
        attachments: action.attachments,
        sender_account: action.sender_account
      })
      break

    case 'MESSAGE':
      // Ensure message fields are available: channel, content
      console.log('💬 Message action:', {
        channel: action.channel,
        content: action.content
      })
      break
  }

  console.log('🎯 Final action for editing:', action)
  editingAction.value = action
  showEditAction.value = true
}

// Action Editor handlers
const handleActionSave = async (updatedAction) => {
  console.log('💾 Saving action:', updatedAction)

  // Get the trigger from sorted array
  const sortedTrigger = localTriggers.value[editingTriggerIndex.value]

  // Find it in the original props.triggers array
  const triggers = [...props.triggers]
  const originalIndex = triggers.findIndex(t => t.trigger_type === sortedTrigger.trigger_type)

  if (originalIndex !== -1) {
    // Merge action parameters into logic
    let finalAction = { ...updatedAction }

    // Ensure all params are accessible
    if (finalAction.action_parameters) {
       Object.assign(finalAction, finalAction.action_parameters)
    }

    triggers[originalIndex].actions[editingActionIndex.value] = finalAction
    console.log('✅ Updated triggers:', triggers)
    emit('update:triggers', triggers)

    // Auto-send logic for Birthday Emails (User Request)
    // Auto-send logic (User Request)
    if (finalAction.action_type === 'EMAIL') {
        const poolName = props.targetPool
        if (poolName) {
            try {
                // Determine content to send
                // updatedAction coming from ActionEditor save() should have 'email_content' populated
                // either from block_content conversion or direct value.
                const subject = finalAction.email_subject || 'No Subject'
                const content = finalAction.email_content || ''

                if (sortedTrigger.trigger_type === 'ON_BIRTHDAY') {
                     // Birthday Trigger: Check condition
                    toast.info(__('Saving and checking for birthday matches...'))

                    const res = await call('mbw_mira.api.campaign.run_birthday_test_for_pool', {
                        pool_name: poolName,
                        subject: subject,
                        content: content
                    })

                    if (res && res.status === 'success') {
                        if (res.sent_count > 0) {
                            toast.success(__('Email sent successfully'))
                        } else {
                            toast.info(__('Saved. No candidates found with birthday today in this pool.'))
                        }
                    }
                } else {
                     // Other Triggers: Send to ALL in pool (Mass Send)
                    toast.info(__('Saving and sending emails to all pool members...'))

                    const res = await call('mbw_mira.api.campaign.run_mass_email_for_pool', {
                        pool_name: poolName,
                        subject: subject,
                        content: content
                    })

                    if (res && res.status === 'success') {
                        toast.success(__('Email sent successfully to {0} talents', [res.sent_count]))
                    }
                }
            } catch (e) {
                console.error("Auto-send failed", e)
                toast.error(__('Failed to send email: {0}', [e.message]))
            }
        }
    }
  }

  showEditAction.value = false
  editingAction.value = null
}

const handleActionCancel = () => {
  showEditAction.value = false
  editingAction.value = null
}

// Remove action from trigger
const removeActionFromTrigger = (triggerIndex, actionIndex) => {
  // Get the trigger from sorted array
  const sortedTrigger = localTriggers.value[triggerIndex]

  // Find it in the original props.triggers array
  const triggers = [...props.triggers]
  const originalIndex = triggers.findIndex(t => t.trigger_type === sortedTrigger.trigger_type)

  if (originalIndex !== -1) {
    triggers[originalIndex].actions.splice(actionIndex, 1)
    emit('update:triggers', triggers)
  }
}

// Remove trigger
const removeTrigger = (index) => {
  if (confirm(__('Are you sure you want to delete this trigger and all its actions?'))) {
    localTriggers.value = localTriggers.value.filter((_, i) => i !== index)
  }
}

// Toggle trigger status (between active and draft)
const toggleTriggerStatus = (triggerIndex) => {
  // Get the trigger from sorted array
  const sortedTrigger = localTriggers.value[triggerIndex]

  // Find it in the original props.triggers array by trigger_type
  const triggers = [...props.triggers]
  const originalIndex = triggers.findIndex(t => t.trigger_type === sortedTrigger.trigger_type)

  if (originalIndex !== -1) {
    const currentStatus = triggers[originalIndex].status || 'active'
    triggers[originalIndex].status = currentStatus === 'active' ? 'draft' : 'active'
    emit('update:triggers', triggers)
  }
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

const formatDelayShort = (minutes) => {
  if (!minutes || minutes === 0) return __('Immediate')

  const weeks = Math.floor(minutes / 10080)
  const days = Math.floor((minutes % 10080) / 1440)
  const hours = Math.floor((minutes % 1440) / 60)
  const mins = minutes % 60

  // Show the largest unit only for brevity
  if (weeks > 0) return `${weeks}w`
  if (days > 0) return `${days}d`
  if (hours > 0) return `${hours}h`
  return `${mins}m`
}

const formatDelayLong = (minutes) => {
  if (!minutes || minutes === 0) return __('Immediate')

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

// Test functions for email tracking
const testSendTrackedEmail = async () => {
  try {
    testingEmail.value = true

    // Get target pool for testing
    const targetPool = props.targetPool || 'TEST_POOL'

    const result = await call('mbw_mira.api.email_tracking_test.test_send_tracked_email_to_pool', {
      target_pool: targetPool,
      subject: 'Test No-Click Trigger Email',
      content: 'This is a test email to verify the no-click trigger functionality. Please do not click any links to test the follow-up system.'
    })

    if (result && result.success) {
      toast.success(__('Test email sent successfully! Check for follow-up in 5 minutes if not clicked.'))
      console.log('📧 Test email sent:', result)
    } else {
      const errorMsg = result ? result.error : 'Unknown error'
      toast.error(__('Failed to send test email: {0}', [errorMsg]))
    }
  } catch (error) {
    console.error('❌ Error sending test email:', error)
    toast.error(__('Error sending test email: {0}', [error.message || error]))
  } finally {
    testingEmail.value = false
  }
}

const testTriggerNow = async () => {
  try {
    testingTrigger.value = true

    // Get campaign ID from props - now properly passed from parent
    const campaignId = props.campaignId

    console.log('🔍 Campaign ID for trigger test:', campaignId)

    if (!campaignId) {
      toast.error(__('No campaign ID available for testing'))
      return
    }

    const result = await call('mbw_mira.api.email_tracking.manual_trigger_email_tracking', {
      campaign_id: campaignId
    })

    if (result.success) {
      console.log('🚫 Full result:', result)
      console.log('🚫 Stats object:', result.results)

      // Use correct keys from backend response
      const checkedCount = result.results.talents_checked || 0
      const stoppedCount = result.results.nurturing_stopped || 0

      toast.success(__('Nurturing check completed! Checked: {0} emails, Stopped nurturing for: {1} talents', [
        checkedCount,
        stoppedCount
      ]))

      // Show detailed results if available
      if (result.results.details && result.results.details.length > 0) {
        console.log('📋 Talents with stopped nurturing:', result.results.details)
      }
    } else {
      toast.error(__('Nurturing check failed: {0}', [result.error || 'Unknown error']))
    }
  } catch (error) {
    console.error('❌ Error in manual trigger:', error)
    toast.error(__('Error in manual trigger: {0}', [error.message || error]))
  } finally {
    testingTrigger.value = false
  }
}
</script>

<style scoped>
/* Add any custom styles here */
</style>
