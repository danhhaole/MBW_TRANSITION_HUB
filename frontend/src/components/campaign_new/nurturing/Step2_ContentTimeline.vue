<template>
  <div class="space-y-6">
    <!-- Landing Page Selector (Section 2.1) -->
    <LandingPageSelector
      v-model:ladipage-url="localLadipageUrl"
      v-model:ladipage-id="localLadipageId"
      :campaign-id="props.name"
      :campaign-name="campaignName"
      :doctype="doctype"
    />

    <!-- Header - Sticky -->
    <div class="sticky top-0 z-10 bg-gray-50 pb-4 -mx-6 px-6 pt-2">
      <div class="flex items-center justify-between">
        <div>
          <h4 class="text-lg font-medium text-gray-900 mb-1">
            {{ __("Content Design") }}
          </h4>
          <p class="text-sm text-gray-600">
            {{ __("Create a series of messages to nurture your candidates over time") }}
          </p>
        </div>

        <!-- Add Message Dropdown -->
        <Dropdown :options="channelDropdownOptions">
          <template v-slot="{ open }">
            <Button variant="solid" theme="gray">
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
              {{ __('Add') }}
              <template #suffix>
                <FeatherIcon :name="open ? 'chevron-up' : 'chevron-down'" class="h-4 w-4" />
              </template>
            </Button>
          </template>
        </Dropdown>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="localTriggers.length === 0" class="text-center py-16 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
      <div class="flex flex-col items-center">
        <div class="bg-gray-200 p-4 rounded-full mb-4">
          <FeatherIcon name="message-circle" class="h-8 w-8 text-gray-500" />
        </div>
        <h5 class="text-lg font-medium text-gray-900 mb-2">
          {{ __("No messages yet") }}
        </h5>
        <p class="text-sm text-gray-600 mb-4">
          {{ __("Click 'Add Message' to create your first nurturing message") }}
        </p>
      </div>
    </div>

    <!-- Timeline Container -->
    <div v-else class="relative">
      <!-- Timeline Line -->
      <div class="absolute left-32 top-0 bottom-0 w-0.5 bg-gray-300"
           v-if="localTriggers.length > 0"></div>

      <!-- Timeline Items -->
      <div class="space-y-8">
        <div
          v-for="(trigger, index) in localTriggers"
          :key="trigger.id"
          class="relative"
        >
          <!-- Timeline Left Side - Delay Info -->
          <div class="absolute left-0 top-6 w-32 text-right pr-4">
            <button
              v-if="index === 0"
              @click="openScheduleEditor(index)"
              class="inline-flex flex-col items-end cursor-pointer group"
              :title="__('Click to set start time')"
            >
              <div class="inline-block px-2 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded group-hover:bg-gray-200 transition-colors whitespace-nowrap">
                {{ __('Start') }}
              </div>
              <div v-if="trigger.schedule_time" class="text-xs text-gray-500 mt-1 whitespace-nowrap">
                {{ formatScheduleTime(trigger.schedule_time) }}
              </div>
            </button>
            <button
              v-else
              @click="openDelayEditor(index)"
              class="inline-flex flex-col items-end cursor-pointer group"
              :title="__('Click to edit delay')"
            >
              <div class="inline-flex items-center px-2 py-1 text-xs font-medium text-blue-700 bg-blue-50 border border-blue-200 rounded group-hover:bg-blue-100 group-hover:border-blue-300 transition-all whitespace-nowrap">
                <FeatherIcon name="clock" class="h-3 w-3 mr-1 group-hover:scale-110 transition-transform" />
                +{{ formatDelayShort(trigger.delay_minutes) }}
              </div>
              <div v-if="getCalculatedScheduleTime(index)" class="text-xs text-gray-500 mt-1 whitespace-nowrap">
                {{ formatScheduleTime(getCalculatedScheduleTime(index)) }}
              </div>
            </button>
          </div>

          <!-- Timeline Node -->
          <div class="absolute left-32 top-6 w-4 h-4 -ml-2 rounded-full border-4 border-white"
               :class="trigger.channel === 'email' ? 'bg-blue-500' : trigger.channel === 'zalo' ? 'bg-green-500' : 'bg-blue-400'">
          </div>

          <!-- Content Card -->
          <div class="ml-40">
            <div class="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
              <!-- Card Header -->
              <div class="p-4 border-b border-gray-200 bg-white">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <!-- Channel Icon -->
                    <div class="flex items-center justify-center w-10 h-10 rounded-full"
                         :class="trigger.channel === 'email' ? 'bg-blue-100' : 'bg-green-100'">
                      <FeatherIcon
                        :name="trigger.channel === 'email' ? 'mail' : 'message-circle'"
                        class="h-5 w-5"
                        :class="trigger.channel === 'email' ? 'text-blue-600' : 'text-green-600'"
                      />
                    </div>

                    <div>
                      <h5 class="text-sm font-semibold text-gray-900">
                        {{ __("Message") }} #{{ index + 1 }} - {{ getChannelLabel(trigger.channel) }}
                      </h5>
                      <p class="text-xs text-gray-500 mt-0.5">
                        {{ getTimingLabel(trigger, index) }}
                      </p>
                    </div>
                  </div>

                  <!-- Actions -->
                  <div class="flex items-center space-x-2">
                    <Button
                      v-if="localTriggers.length > 1"
                      icon="trash-2"
                      variant="ghost"
                      theme="red"
                      size="sm"
                      @click="removeTrigger(index)"
                    />
                    <Button
                      :icon="trigger.expanded ? 'chevron-up' : 'chevron-down'"
                      variant="ghost"
                      size="sm"
                      @click="toggleExpand(index)"
                    />
                  </div>
                </div>
              </div>


              <!-- Card Body (Expandable) -->
              <div v-if="trigger.expanded" class="p-4 space-y-4">
                <!-- Timing Configuration - Only for first message -->
                <div v-if="index === 0" class="space-y-2">
                  <label class="block text-sm font-medium text-gray-700">
                    {{ __("Schedule Time") }} <span class="text-red-500">*</span>
                  </label>
                  <FormControl
                    type="datetime-local"
                    v-model="trigger.schedule_time"
                    :placeholder="__('Select date and time')"
                  />
                  <p class="text-xs text-gray-500">
                    {{ __("When should this first message be sent?") }}
                  </p>
                </div>

                <!-- Delay info for subsequent messages (read-only, edit via modal) -->
                <div v-else class="space-y-2">
                  <label class="block text-sm font-medium text-gray-700">
                    {{ __("Delay After Previous Message") }}
                  </label>
                  <div class="flex items-center justify-between p-3 border rounded-lg bg-gray-50">
                    <div class="flex items-center space-x-2">
                      <FeatherIcon name="clock" class="h-4 w-4 text-gray-600" />
                      <span class="text-sm font-medium text-gray-900">
                        {{ formatDelay(trigger.delay_minutes) }}
                      </span>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      @click="openDelayEditor(index)"
                    >
                      <template #prefix>
                        <FeatherIcon name="edit-2" class="h-3 w-3" />
                      </template>
                      {{ __("Edit") }}
                    </Button>
                  </div>
                  <p class="text-xs text-gray-500">
                    {{ __("Click 'Edit' or the delay badge on the left to change timing") }}
                  </p>
                </div>

                <!-- Channel Display (Read-only) -->
                <!-- <div class="space-y-2">
                  <label class="block text-sm font-medium text-gray-700">
                    {{ __("Channel") }}
                  </label>
                  <div class="flex items-center space-x-3 p-3 border rounded-lg bg-gray-50">
                    <FeatherIcon :name="getChannelIcon(trigger.channel)" class="h-5 w-5 text-gray-600" />
                    <span class="text-sm font-medium text-gray-900">
                      {{ getChannelLabel(trigger.channel) }}
                    </span>
                  </div>
                  <p class="text-xs text-gray-500">
                    {{ __("Channel is set when creating the message") }}
                  </p>
                </div> -->

                <!-- Sender Account Selection -->
                <div class="space-y-2">
                  <label class="block text-sm font-medium text-gray-700">
                    {{ __("Sender Account") }}
                  </label>
                  <Autocomplete
                    v-model="trigger.sender_account"
                    :options="getSenderAccountOptions(trigger.channel)"
                    :placeholder="__('Select sender account (optional)')"
                  />
                  <p class="text-xs text-gray-500">
                    {{ __("Choose which account will send this message") }}
                  </p>
                </div>

                <!-- Content Editor -->
                <div class="space-y-2">

                  <!-- Email Editor -->
                                                      <EmailContentEditor
                    v-if="trigger.channel === 'email'"
                    :content="trigger.content"
                    @update:content="updateTriggerContent(index, $event)"
                  >
                    <template #actions>
                      <Button @click="openTestEmailModal(trigger)" variant="solid" theme="blue" size="sm">
                        <template #prefix>
                          <FeatherIcon name="send" class="h-4 w-4" />
                        </template>
                        {{ __('Send Email To Check') }}
                      </Button>
                    </template>
                  </EmailContentEditor>

                  <!-- Zalo Editor -->
                  <ZaloContentEditor
                    v-else-if="trigger.channel === 'zalo'"
                    :content="trigger.content"
                    @update:content="updateTriggerContent(index, $event)"
                  />

                  <!-- Messenger Editor -->
                  <div v-else-if="trigger.channel === 'messenger'" class="space-y-4">
                    <FormControl
                      type="textarea"
                      v-model="trigger.content.message"
                      :placeholder="__('Enter your message...')"
                      :rows="6"
                    />
                  </div>
                </div>


              </div>

            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Summary -->
    <div v-if="localTriggers.length > 0" class="bg-blue-50 rounded-lg p-4">
      <div class="flex items-start space-x-3">
        <FeatherIcon name="info" class="h-5 w-5 text-blue-600 mt-0.5" />
        <div>
          <h5 class="text-sm font-semibold text-blue-900 mb-1">
            {{ __("Campaign Summary") }}
          </h5>
          <p class="text-sm text-blue-700">
            {{ __("Total messages:") }} <strong>{{ localTriggers.length }}</strong>
          </p>
          <p class="text-sm text-blue-700">
            {{ __("Duration:") }} <strong>{{ getTotalDuration() }}</strong>
          </p>
        </div>
      </div>
    </div>

    <!-- Delay Editor Dialog -->
    <Dialog
      v-model="showDelayEditor"
      :options="{
        title: __('Edit Delay Time'),
        size: 'sm'
      }"
    >
      <template #body-content>
        <div v-if="editingTriggerIndex !== null" class="space-y-4">
          <p class="text-sm text-gray-600">
            {{ __('Set the delay after the previous message') }}
          </p>

          <DelaySelector
            v-model="editingDelay"
            :label="__('Delay Time')"
            :optional="false"
          />
        </div>
      </template>

      <template #actions>
        <div class="flex items-center justify-end gap-2">
          <Button variant="outline" theme="gray" @click="showDelayEditor = false">
            {{ __("Cancel") }}
          </Button>
          <Button variant="solid" theme="blue" @click="saveDelay">
            {{ __("Save") }}
          </Button>
        </div>
      </template>
    </Dialog>

    <!-- Schedule Time Editor Dialog -->
    <Dialog
      v-model="showScheduleEditor"
      :options="{
        title: __('Set Start Time'),
        size: 'sm'
      }"
    >
      <template #body-content>
        <div class="space-y-4">
          <p class="text-sm text-gray-600">
            {{ __('When should the first message be sent?') }}
          </p>

          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">
              {{ __("Schedule Time") }} <span class="text-red-500">*</span>
            </label>
            <FormControl
              type="datetime-local"
              v-model="editingScheduleTime"
              :placeholder="__('Select date and time')"
            />
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex items-center justify-end gap-2">
          <Button variant="outline" theme="gray" @click="showScheduleEditor = false">
            {{ __("Cancel") }}
          </Button>
          <Button variant="solid" theme="blue" @click="saveScheduleTime">
            {{ __("Save") }}
          </Button>
        </div>
      </template>
    </Dialog>

    <!-- Test Email Dialog -->
    <Dialog
      v-model="showTestEmailModal"
      :options="{
        title: __('Test Email Configuration'),
        size: '3xl'
      }"
    >
      <template #body-content>
        <div class="space-y-4">
          <div class="space-y-1">
            <label class="block text-sm font-medium text-gray-700">
              {{ __('Email') }} <span class="text-red-500">*</span>
            </label>
            <FormControl
              type="email"
              v-model="testEmailAddress"
              :placeholder="__('Enter email address')"
            />
          </div>
		   <label class="block text-sm font-medium text-gray-700">
              {{ __('Content') }}
            </label>
          <div class="border rounded overflow-hidden">
            <iframe
              class="w-full p-2 h-80 bg-white"
              :srcdoc="getPreviewIframeDoc(testEmailTrigger?.content)"
              scrolling="auto"
            ></iframe>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex items-center justify-end gap-2">
          <Button variant="outline" theme="gray" @click="showTestEmailModal = false">
            {{ __('Cancel') }}
          </Button>
          <Button
            variant="solid"
            theme="blue"
            @click="confirmSendTestEmail"
            :disabled="!isTestEmailValid || isSendingEmail"
            :loading="isSendingEmail"
          >
            {{ isSendingEmail ? __('Sending...') : __('Send Email') }}
          </Button>
        </div>
      </template>
    </Dialog>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useToast } from '@/composables/useToast'
import { FeatherIcon, Button, FormControl, Autocomplete, Dropdown, Dialog, call } from 'frappe-ui'
import DelaySelector from '../molecules/DelaySelector.vue'
import EmailContentEditor from '../molecules/EmailContentEditor.vue'
import ZaloContentEditor from '../molecules/ZaloContentEditor.vue'
import LandingPageSelector from '../molecules/LandingPageSelector.vue'

const props = defineProps({
  triggers: {
    type: Array,
    default: () => []
  },
  campaignName: {
    type: String,
    default: ''
  },
  ladipageUrl: {
    type: String,
    default: ''
  },
  ladipageId: {
    type: String,
    default: ''
  },
  name: {
    type: String,
    default: ''
  },
  doctype: {
    type: String,
    default: 'Mira Campaign' // 'Mira Campaign' or 'Mira Campaign Template'
  },
  targetPool: {
    type: String,
    default: null
  }
})
const emit = defineEmits(['update:triggers', 'update:ladipageUrl', 'update:ladipageId'])
const toast = useToast()

// Available channels for nurturing (no Facebook posts)
const availableChannels = [
  { value: 'email', label: __('Email'), icon: 'mail' },
  { value: 'zalo', label: __('Zalo Message'), icon: 'message-circle' }
  // Messenger not available for nurturing campaigns
]

// Dropdown options for adding messages
const channelDropdownOptions = computed(() => {
  return availableChannels.map(channel => ({
    label: channel.label,
    icon: channel.icon,
    onClick: () => addTrigger(channel.value)
  }))
})

// Local triggers state
const localTriggers = ref([])

// Landing page computed properties
const localLadipageUrl = computed({
  get: () => props.ladipageUrl,
  set: (value) => emit('update:ladipageUrl', value)
})

const localLadipageId = computed({
  get: () => props.ladipageId,
  set: (value) => emit('update:ladipageId', value)
})

// Delay editor state
const showDelayEditor = ref(false)
const editingTriggerIndex = ref(null)
const editingDelay = ref(0)

// Schedule editor state
const showScheduleEditor = ref(false)
const editingScheduleTime = ref('')

// Email accounts
const emailAccounts = ref([])
const loadingEmailAccounts = ref(false)

// Zalo accounts
const zaloAccounts = ref([])
const loadingZaloAccounts = ref(false)

// Initialize triggers
const initializeTriggers = () => {
  if (props.triggers && props.triggers.length > 0) {
    localTriggers.value = props.triggers.map(t => ({
      ...t,
      expanded: t.expanded !== undefined ? t.expanded : false
    }))
  }
  // Don't create default trigger - start empty
}

// Add new trigger
const addTrigger = (channel = 'email') => {
  let content = {};
  let sender_account = null;

  // Always create a new empty template for the trigger
  if (channel === 'email') {
    content = {
      email_subject: '',
      email_content: '',
      block_content: '',
      template_content: '',
      mjml_content: '',
      attachments: []
    };
  } else if (channel === 'zalo') {
    content = {
      message: '',
      image: null
    };
  } else if (channel === 'messenger') {
    content = {
      message: ''
    };
  }

  const newTrigger = {
    id: Date.now(),
    channel: channel,
    schedule_time: null,
    delay_minutes: localTriggers.value.length === 0 ? 0 : 1440, // First message: immediate, others: 1 day default
    sender_account: sender_account,
    content: content,
    expanded: true
  };

  localTriggers.value.push(newTrigger)

  // Collapse other triggers
  localTriggers.value.forEach((t, i) => {
    if (i !== localTriggers.value.length - 1) {
      t.expanded = false
    }
  })
}

// Remove trigger
const removeTrigger = (index) => {
  if (localTriggers.value.length === 1) {
    return // Keep at least one
  }
  localTriggers.value.splice(index, 1)
}

// Toggle expand
const toggleExpand = (index) => {
  localTriggers.value[index].expanded = !localTriggers.value[index].expanded
}

// Update trigger content
const updateTriggerContent = (index, content) => {
  console.log('🔄 [Step2] Updating trigger content:', { index, content })
  localTriggers.value[index].content = content

  // Debug: Log the updated trigger
  console.log('✅ [Step2] Updated trigger:', localTriggers.value[index])

  // Emit updated triggers to parent
  emit('update:triggers', localTriggers.value)
}

// Get content preview for email
const getContentPreview = (content) => {
  if (!content) return ''

  // Try block_content first (EmailBuilder format)
  if (content.block_content) {
    try {
      const design = JSON.parse(content.block_content)
      if (design.blocks && Array.isArray(design.blocks)) {
        let previewText = ''
        design.blocks.forEach(block => {
          if (block.type === 'text' && block.props?.content) {
            // Strip HTML tags for preview
            const div = document.createElement('div')
            div.innerHTML = block.props.content
            previewText += div.textContent + ' '
          }
        })
        return previewText.trim().substring(0, 100) + (previewText.length > 100 ? '...' : '')
      }
    } catch (e) {
      console.warn('Failed to parse block_content:', e)
    }
  }

  // Fallback to template_content (HTML)
  if (content.template_content) {
    const div = document.createElement('div')
    div.innerHTML = content.template_content
    const text = div.textContent || div.innerText || ''
    return text.trim().substring(0, 100) + (text.length > 100 ? '...' : '')
  }

  // Fallback to email_content (legacy)
  if (content.email_content) {
    if (typeof content.email_content === 'string' && content.email_content.startsWith('{')) {
      // Try to parse as JSON
      try {
        const design = JSON.parse(content.email_content)
        if (design.blocks) {
          return getContentPreview({ block_content: content.email_content })
        }
      } catch (e) {
        // Treat as HTML
        const div = document.createElement('div')
        div.innerHTML = content.email_content
        const text = div.textContent || div.innerText || ''
        return text.trim().substring(0, 100) + (text.length > 100 ? '...' : '')
      }
    } else {
      // Treat as HTML
      const div = document.createElement('div')
      div.innerHTML = content.email_content
      const text = div.textContent || div.innerText || ''
      return text.trim().substring(0, 100) + (text.length > 100 ? '...' : '')
    }
  }

  return ''
}

// Get content preview for Zalo
const getZaloPreview = (content) => {
  if (!content) return ''

  if (content.blocks && Array.isArray(content.blocks)) {
    let previewText = ''
    content.blocks.forEach(block => {
      if (block.type === 'text' && block.text_content) {
        previewText += block.text_content + ' '
      }
    })
    return previewText.trim().substring(0, 100) + (previewText.length > 100 ? '...' : '')
  }

  // Fallback to simple message
  if (content.message) {
    return content.message.substring(0, 100) + (content.message.length > 100 ? '...' : '')
  }

  return ''
}

// Open delay editor
const openDelayEditor = (index) => {
  editingTriggerIndex.value = index
  editingDelay.value = localTriggers.value[index].delay_minutes || 0
  showDelayEditor.value = true
}

// Save delay
const saveDelay = () => {
  if (editingTriggerIndex.value !== null) {
    localTriggers.value[editingTriggerIndex.value].delay_minutes = editingDelay.value
  }
  showDelayEditor.value = false
  editingTriggerIndex.value = null
  editingDelay.value = 0
}

// Open schedule editor for first message
const openScheduleEditor = (index) => {
  if (index === 0) {
    editingScheduleTime.value = localTriggers.value[0].schedule_time || ''
    showScheduleEditor.value = true
  }
}

// Save schedule time
const saveScheduleTime = () => {
  if (editingScheduleTime.value) {
    localTriggers.value[0].schedule_time = editingScheduleTime.value
  }
  showScheduleEditor.value = false
  editingScheduleTime.value = ''
}

// Format schedule time for display (DD/MM/YYYY HH:MM)
const formatScheduleTime = (scheduleTime) => {
  if (!scheduleTime) return ''
  const date = new Date(scheduleTime)
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear() // Full 4 digits year
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${day}/${month}/${year} ${hours}:${minutes}`
}

// Calculate schedule time for subsequent messages
const getCalculatedScheduleTime = (index) => {
  if (index === 0) return null

  const firstTrigger = localTriggers.value[0]
  if (!firstTrigger.schedule_time) return null

  let baseTime = new Date(firstTrigger.schedule_time)

  // Add up all delays from first message to current
  for (let i = 1; i <= index; i++) {
    const delayMinutes = localTriggers.value[i].delay_minutes || 0
    baseTime = new Date(baseTime.getTime() + delayMinutes * 60000)
  }

  return baseTime.toISOString()
}

// Get channel label
const getChannelLabel = (channel) => {
  const ch = availableChannels.find(c => c.value === channel)
  return ch ? ch.label : channel
}

// Get channel icon
const getChannelIcon = (channel) => {
  const ch = availableChannels.find(c => c.value === channel)
  return ch ? ch.icon : 'message-circle'
}

// Get timing label
const getTimingLabel = (trigger, index) => {
  if (index === 0) {
    if (trigger.schedule_time) {
      const date = new Date(trigger.schedule_time)
      return __('Scheduled for') + ': ' + date.toLocaleString()
    }
    return __('Not scheduled yet')
  } else {
    const minutes = trigger.delay_minutes || 0
    return formatDelay(minutes) + ' ' + __('after previous message')
  }
}

// Format delay
const formatDelay = (minutes) => {
  if (minutes === 0) return __('Immediately')

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

// Format delay short (for timeline left side)
const formatDelayShort = (minutes) => {
  if (minutes === 0) return '0m'

  const weeks = Math.floor(minutes / 10080)
  const days = Math.floor((minutes % 10080) / 1440)
  const hours = Math.floor((minutes % 1440) / 60)
  const mins = minutes % 60

  if (weeks > 0) return `${weeks}w`
  if (days > 0) return `${days}d`
  if (hours > 0) return `${hours}h`
  return `${mins}m`
}

// Get total duration
const getTotalDuration = () => {
  if (localTriggers.value.length === 0) return __('No messages')
  if (localTriggers.value.length === 1) return __('Single message')

  let totalMinutes = 0
  for (let i = 1; i < localTriggers.value.length; i++) {
    totalMinutes += localTriggers.value[i].delay_minutes || 0
  }

  return formatDelay(totalMinutes)
}

// Messenger accounts
const messengerAccounts = ref([])
const loadingMessengerAccounts = ref(false)

// Get sender account options
const getSenderAccountOptions = (channel) => {
  if (channel === 'email') {
    return emailAccounts.value.map(acc => ({
      label: `${acc.email_id} (${acc.email_account_name})`,
      value: acc.name,
      description: acc.email_id
    }))
  } else if (channel === 'zalo') {
    return zaloAccounts.value.map(acc => ({
      label: `${acc.oa_name} (${acc.oa_id})`,
      value: acc.name,
      description: acc.oa_id
    }))
  } else if (channel === 'messenger') {
    return messengerAccounts.value.map(acc => ({
      label: `${acc.page_name} (${acc.page_id})`,
      value: acc.name,
      description: acc.page_id
    }))
  }
  return []
}

// Load email accounts
const loadEmailAccounts = async () => {
  loadingEmailAccounts.value = true
  try {
    const result = await call('frappe.client.get_list', {
      doctype: 'Email Account',
      filters: {
        enable_outgoing: 1
      },
      fields: ['name', 'email_id', 'email_account_name'],
      limit_page_length: 100
    })
    emailAccounts.value = result || []
  } catch (error) {
    console.error('Error loading email accounts:', error)
  } finally {
    loadingEmailAccounts.value = false
  }
}

// Load Zalo accounts
const loadZaloAccounts = async () => {
  loadingZaloAccounts.value = true
  try {
    // First get Mira External Connection with platform_type = Zalo
    const connections = await call('frappe.client.get_list', {
      doctype: 'Mira External Connection',
      filters: {
        platform_type: 'Zalo',
        connection_status: 'Connected',
        active_status: 1
      },
      fields: ['name', 'platform_type'],
      limit_page_length: 100
    })

    // Then get accounts from child table for each connection
    const accounts = []
    for (const conn of connections || []) {
      try {
        const childAccounts = await call('frappe.client.get_list', {
          doctype: 'Mira External Connection Account',
          filters: {
            parent: conn.name,
            account_type: 'OA',
            is_active: 1
          },
          fields: ['name', 'external_account_id', 'account_name', 'is_primary'],
          limit_page_length: 100
        })

        for (const account of childAccounts || []) {
          accounts.push({
            name: conn.name, // External connection name
            oa_id: account.external_account_id,
            oa_name: account.account_name,
            account_id: account.name, // Child table row name
            is_primary: account.is_primary
          })
        }
      } catch (childError) {
        console.error('Error loading child accounts for', conn.name, childError)
      }
    }

    zaloAccounts.value = accounts
  } catch (error) {
    console.error('Error loading Zalo accounts:', error)
  } finally {
    loadingZaloAccounts.value = false
  }
}

// Load Messenger accounts
const loadMessengerAccounts = async () => {
  loadingMessengerAccounts.value = true
  try {
    // First get Mira External Connection with platform_type = Facebook
    const connections = await call('frappe.client.get_list', {
      doctype: 'Mira External Connection',
      filters: {
        platform_type: 'Facebook',
        connection_status: 'Connected',
        active_status: 1
      },
      fields: ['name', 'platform_type'],
      limit_page_length: 100
    })

    // Then get accounts from child table for each connection
    const accounts = []
    for (const conn of connections || []) {
      try {
        const childAccounts = await call('frappe.client.get_list', {
          doctype: 'Mira External Connection Account',
          filters: {
            parent: conn.name,
            account_type: 'Page',
            is_active: 1
          },
          fields: ['name', 'external_account_id', 'account_name', 'is_primary'],
          limit_page_length: 100
        })

        for (const account of childAccounts || []) {
          accounts.push({
            name: conn.name, // External connection name
            page_id: account.external_account_id,
            page_name: account.account_name,
            account_id: account.name, // Child table row name
            is_primary: account.is_primary
          })
        }
      } catch (childError) {
        console.error('Error loading child accounts for', conn.name, childError)
      }
    }

    messengerAccounts.value = accounts
  } catch (error) {
    console.error('Error loading Messenger accounts:', error)
  } finally {
    loadingMessengerAccounts.value = false
  }
}

// Flag to prevent recursive updates
const isUpdatingFromProps = ref(false)

// Watch for triggers changes
watch(localTriggers, (newTriggers) => {
  if (isUpdatingFromProps.value) {
    return
  }
  emit('update:triggers', newTriggers)
}, { deep: true })

// Watch for props changes
watch(() => props.triggers, (newTriggers) => {
  isUpdatingFromProps.value = true

  if (newTriggers && newTriggers.length > 0) {
    localTriggers.value = newTriggers.map(t => ({
      ...t,
      expanded: t.expanded !== undefined ? t.expanded : false
    }))
  } else {
    localTriggers.value = []
  }

  setTimeout(() => {
    isUpdatingFromProps.value = false
  }, 0)
}, { deep: true })

// Initialize
initializeTriggers()
loadEmailAccounts()
loadZaloAccounts()
loadMessengerAccounts()

const sendTestEmail = async (trigger) => {
  if (!props.targetPool) {
    toast.error(__('Target pool is not set. Cannot send emails.'));
    return;
  }

  if (trigger.channel !== 'email') {
    toast.error(__('This function is only for email channels.'));
    return;
  }

  try {
    console.log('Trigger content:', JSON.stringify(trigger.content, null, 2));

    const subject = trigger.content?.email_subject || 'Welcome to the Campaign';

    // Try to get content in order of preference
    let content = '';
    if (trigger.content?.block_content) {
      content = trigger.content.block_content;
      console.log('Using block_content');
    } else if (trigger.content?.template_content) {
      content = trigger.content.template_content;
      console.log('Using template_content');
    } else if (trigger.content?.email_content) {
      content = trigger.content.email_content;
      console.log('Using email_content');
    } else if (trigger.content?.mjml_content) {
      content = trigger.content.mjml_content;
      console.log('Using mjml_content');
    } else if (trigger.content?.content) {
      content = trigger.content.content;
      console.log('Using content');
    } else if (trigger.content) {
      // If we can't find a specific content field, try to stringify the whole content object
      content = typeof trigger.content === 'string' ? trigger.content : JSON.stringify(trigger.content);
      console.log('Using full content object');
    }

    if (!content) {
      toast.error(__('Email content is empty.'));
      return;
    }

    const result = await call('mbw_mira.api.campaign.run_mass_email_for_pool', {
      pool_name: props.targetPool,
      subject: `${subject}`,
      content: content
    });

    console.log('Email send result:', result);

    if (result && result.status === 'success') {
      toast.success(__('The email has been successfully sent.'));
    } else {
      const errorMsg = result?.message || 'Unknown error occurred';
      console.error('Email send failed:', errorMsg);
      toast.error(__('Failed to send test email: ') + errorMsg);
    }
  } catch (error) {
    console.error('Error sending test email:', error);
    toast.error(__('Failed to send test email.'));
  }
};

const showTestEmailModal = ref(false)
const testEmailTrigger = ref(null)
const testEmailAddress = ref('')
const isSendingEmail = ref(false)

const openTestEmailModal = (trigger) => {
  testEmailTrigger.value = trigger
  testEmailAddress.value = ''
  showTestEmailModal.value = true
}

const stripHtml = (html) => {
  const div = document.createElement('div')
  div.innerHTML = html
  return div.textContent || div.innerText || ''
}

const getPreviewIframeDoc = (content) => {
  const html = getPreviewHtml(content)
  // Basic doc with Tailwind CDN stripped to avoid conflicts
  return `<!DOCTYPE html><html><head><meta charset='utf-8'><style>body, p, div, span{font-family: Arial, sans-serif;font-size:14px;margin:0;padding:12px;color:#3c414b;font-weight:400;}</style></head><body>${html}</body></html>`
}

const getPreviewPlainText = (content) => {
  if (!content) return ''
  if (content.template_content) return stripHtml(content.template_content)
  if (content.email_content) return stripHtml(content.email_content)
  if (content.block_content) {
    try {
      const design = JSON.parse(content.block_content)
      let text = ''
      design.blocks?.forEach(block => {
        if (block.type === 'text' && block.props?.content) {
          text += stripHtml(block.props.content) + '\n'
        }
      })
      return text.trim()
    } catch (e) {
      return stripHtml(content.block_content)
    }
  }
  return typeof content === 'string' ? content : JSON.stringify(content)
}

// old function kept for other uses
const getPreviewHtml = (content) => {
  if (!content) return ''
  if (content.template_content) return content.template_content
  if (content.email_content) return content.email_content
  if (content.block_content) {
    try {
      const design = JSON.parse(content.block_content)
      let html = ''
      design.blocks?.forEach(block => {
        if (block.type === 'text' && block.props?.content) {
          html += block.props.content
        }
      })
      return html
    } catch (e) {
      return content.block_content
    }
  }
  return typeof content === 'string' ? content : JSON.stringify(content)
}

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const isTestEmailValid = computed(() => emailPattern.test(testEmailAddress.value))

const wrapEmailContent = (html) => {
  // center aligned single column table 600px with white background
  return `<!DOCTYPE html><html><head><meta charset='utf-8'></head>
  <body style="margin:0;padding:0;background:#f5f5f5;font-family:Arial,sans-serif;">
    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate !important;background:#f5f5f5;padding:40px 0;">
      <tr>
        <td align="center">
          <table role="presentation" cellpadding="0" cellspacing="0" width="600" align="center" style="border-collapse:separate !important;margin:0 auto;background:#ffffff;border-radius:8px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,0.05);font-size:14px;line-height:1.6;color:#000000;">
            <tr><td>${html}</td></tr>
          </table>
        </td>
      </tr>
    </table>
  </body></html>`
}

const sendEmail = async (trigger, recipient) => {
  isSendingEmail.value = true;
  try {
    const subject = trigger.content?.email_subject || 'Test Email';
    let rawContent = getPreviewHtml(trigger.content);
    // Replace placeholders with actual values (handle both with and without spaces)
    rawContent = rawContent.replace(/\{\{\s*full_name\s*\}\}/g, recipient);

    // Replace localhost URLs and relative paths with production domain
    console.log('🔍 Before replace:', rawContent);

    // Replace absolute localhost URLs
    rawContent = rawContent.replaceAll('http://localhost:8080', 'https://hireos.fastwork.vn');
    rawContent = rawContent.replaceAll('http://localhost:8000', 'https://hireos.fastwork.vn');
    rawContent = rawContent.replaceAll('http://127.0.0.1:8080', 'https://hireos.fastwork.vn');
    rawContent = rawContent.replaceAll('http://127.0.0.1:8000', 'https://hireos.fastwork.vn');

    // Replace relative paths like /files/... with full domain
    rawContent = rawContent.replace(/src="\/files\//g, 'src="https://hireos.fastwork.vn/files/');
    rawContent = rawContent.replace(/href="\/files\//g, 'href="https://hireos.fastwork.vn/files/');

    console.log('✅ After replace:', rawContent);

    // Check if replacement worked
    if (rawContent.includes('localhost')) {
      console.warn('⚠️ WARNING: localhost still found in content after replacement!');
    }

    const content = wrapEmailContent(rawContent);

    const result = await call('mbw_mira.api.campaign.send_test_email', {
      recipient: recipient,
      subject,
      content
    });

    if (result && result.status === 'success') {
      toast.success(__('The email has been successfully sent.'));
      showTestEmailModal.value = false;
    } else {
      toast.error(__('Failed to send email'));
    }
  } catch (error) {
    console.error('Error sending email:', error);
    let errorMessage = __('Failed to send email');
    if (error.message) {
      errorMessage += `: ${error.message}`;
    } else if (error.exc_type) {
      errorMessage += `: ${error.exc_type}`;
      if (error.exception) {
        errorMessage += ` - ${error.exception}`;
      }
    }
    toast.error(errorMessage);
  } finally {
    isSendingEmail.value = false;
  }
};

const confirmSendTestEmail = async () => {
  if (!isTestEmailValid.value) {
    toast.error(__('Please enter a valid email address'));
    return;
  }

  const trigger = testEmailTrigger.value;
  if (!trigger) return;

  const scheduleTime = trigger.schedule_time ? new Date(trigger.schedule_time) : null;
  const now = new Date();

  if (scheduleTime && scheduleTime > now) {
    const delay = scheduleTime.getTime() - now.getTime();
    toast.info(`Email scheduled to be sent at ${formatScheduleTime(trigger.schedule_time)}`);
    showTestEmailModal.value = false;

    setTimeout(() => {
      sendEmail(trigger, testEmailAddress.value);
    }, delay);

  } else {
    toast.info(__('Sending email...'));
    await sendEmail(trigger, testEmailAddress.value);
  }
};

</script>

<style scoped>
/* Timeline styles */
.timeline-node {
  position: absolute;
  left: 2rem;
  top: 1.5rem;
  width: 1rem;
  height: 1rem;
  margin-left: -0.5rem;
  border-radius: 9999px;
  border-width: 4px;
  border-color: white;
}
</style>
