<template>
  <div class="space-y-6">
    <!-- Header - Sticky -->
    <div class="sticky top-0 z-10 bg-gray-50 pb-4 -mx-6 px-6 pt-2">
      <div class="flex items-center justify-between">
        <div>
          <h4 class="text-lg font-medium text-gray-900 mb-1">
            {{ __("Content Design") }}
          </h4>
          <p class="text-sm text-gray-600">
            {{ __("Create a series of message templates to nurture your candidates over time") }}
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
          {{ __("Click 'Add Message' to create your first nurturing message template") }}
        </p>
      </div>
    </div>

    <!-- Messages List -->
    <div v-else class="space-y-4">
      <div 
        v-for="(trigger, index) in localTriggers" 
        :key="index"
        class="bg-white border border-gray-200 rounded-lg p-6"
      >
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center mr-3">
              <span class="text-white text-sm font-medium">{{ index + 1 }}</span>
            </div>
            <div>
              <h6 class="text-sm font-medium text-gray-900">
                {{ __('Message Template {0}', [index + 1]) }}
              </h6>
              <p class="text-xs text-gray-500">
                {{ getTriggerTypeLabel(trigger.trigger_type) }} • {{ trigger.delay_days || 0 }} {{ __('days') }}
              </p>
            </div>
          </div>
          
          <Button variant="ghost" size="sm" theme="red" @click="removeTrigger(index)">
            <FeatherIcon name="trash-2" class="h-4 w-4" />
          </Button>
        </div>

        <!-- Configuration -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Trigger Type') }}
            </label>
            <Select
              v-model="trigger.trigger_type"
              :options="triggerTypeOptions"
              :placeholder="__('Select trigger type')"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Delay (days)') }}
            </label>
            <FormControl
              type="number"
              v-model="trigger.delay_days"
              :placeholder="__('0')"
              min="0"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Channel') }}
            </label>
            <Select
              v-model="trigger.channel"
              :options="channelOptions"
              :placeholder="__('Select channel')"
            />
          </div>
        </div>

        <!-- Content Editor -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __('Message Content Template') }}
          </label>
          
          <!-- Email Content -->
          <EmailContentEditor
            v-if="trigger.channel === 'email'"
            v-model="trigger.content"
            :show-error="false"
          />
          
          <!-- Zalo Content -->
          <ZaloContentEditor
            v-else-if="trigger.channel === 'zalo'"
            v-model="trigger.content"
            :show-error="false"
          />
          
          <!-- SMS Content -->
          <FormControl
            v-else-if="trigger.channel === 'sms'"
            type="textarea"
            v-model="trigger.content.content"
            :placeholder="__('Enter SMS message template...')"
            rows="3"
          />
          
          <!-- Default Content -->
          <FormControl
            v-else
            type="textarea"
            v-model="trigger.content.content"
            :placeholder="__('Enter message template content...')"
            rows="3"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Button, FormControl, Select, Dropdown, FeatherIcon } from 'frappe-ui'
import EmailContentEditor from '@/components/campaign_new/molecules/EmailContentEditor.vue'
import ZaloContentEditor from '@/components/campaign_new/molecules/ZaloContentEditor.vue'

const props = defineProps({
  triggers: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:triggers'])

// Local reactive data
const localTriggers = ref([...props.triggers])

// Options
const triggerTypeOptions = [
  { label: __('Time Based'), value: 'time_based' },
  { label: __('Email Opened'), value: 'email_opened' },
  { label: __('Link Clicked'), value: 'link_clicked' },
  { label: __('Profile Updated'), value: 'profile_updated' }
]

const channelOptions = [
  { label: __('Email'), value: 'email' },
  { label: __('SMS'), value: 'sms' },
  { label: __('Zalo'), value: 'zalo' }
]

const channelDropdownOptions = computed(() => {
  return channelOptions.map(channel => ({
    label: `${channel.label} Message`,
    onClick: () => addTrigger(channel.value)
  }))
})

// Methods
const addTrigger = (channel = 'email') => {
  const newTrigger = {
    trigger_type: 'time_based',
    delay_days: localTriggers.value.length * 7, // Default to weekly intervals
    channel: channel,
    content: { content: '' }
  }
  
  localTriggers.value.push(newTrigger)
  emitUpdate()
}

const removeTrigger = (index) => {
  localTriggers.value.splice(index, 1)
  emitUpdate()
}

const getTriggerTypeLabel = (triggerType) => {
  const option = triggerTypeOptions.find(opt => opt.value === triggerType)
  return option ? option.label : triggerType
}

const emitUpdate = () => {
  emit('update:triggers', localTriggers.value)
}

// Watch for changes
watch(() => localTriggers.value, () => {
  emitUpdate()
}, { deep: true, immediate: false })

// Watch for prop changes
watch(() => props.triggers, (newValue) => {
  if (JSON.stringify(newValue) !== JSON.stringify(localTriggers.value)) {
    localTriggers.value = [...newValue]
  }
})
</script>

<style scoped>
/* Add any custom styles if needed */
</style>
