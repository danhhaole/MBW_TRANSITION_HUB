<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="border-b border-gray-200 pb-4">
      <div class="flex items-center space-x-2 mb-2">
        <FeatherIcon name="zap" class="h-5 w-5 text-purple-600" />
        <h3 class="text-lg font-medium text-gray-900">{{ __('Config Trigger') }}</h3>
      </div>
      <p class="text-sm text-gray-500">{{ __('Config trigger to activate flow') }}</p>
    </div>

    <!-- Trigger Name & Description (Read-only) -->
    <div class="space-y-4">

    </div>

    <!-- Connected Account Selection -->
    

    <!-- Sequence Selection (only for sequence triggers) -->
    <div v-if="isSequenceTrigger()" class="space-y-3">
      <label class="block text-sm font-medium text-gray-700">
        <FeatherIcon name="list" class="inline h-4 w-4 mr-1" />
        {{ __('Select Sequence') }}
      </label>
      <select
        v-model="localContent.sequence_id"
        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
        @change="updateContent"
      >
        <option value="">{{ __('Select sequence') }}</option>
        <option value="seq_1">{{ __('Welcome new subscriber') }}</option>
        <option value="seq_2">{{ __('Promotion at the end of the week') }}</option>
        <option value="seq_3">{{ __('VIP care') }}</option>
      </select>
    </div>

    <!-- Channel Selection (only for new subscriber trigger) -->
    <div v-if="isNewSubscriberTrigger()" class="space-y-3">
      <label class="block text-sm font-medium text-gray-700">
        <FeatherIcon name="radio" class="inline h-4 w-4 mr-1" />
        {{ __('Channel Selection') }}
      </label>
      <div class="flex flex-wrap gap-3">
        <label class="inline-flex items-center">
          <input
            v-model="localContent.channels"
            type="checkbox"
            value="zalo"
            class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            @change="updateContent"
          />
          <span class="ml-2 text-sm text-gray-700">{{ __('Zalo') }}</span>
        </label>
        <label class="inline-flex items-center">
          <input
            v-model="localContent.channels"
            type="checkbox"
            value="facebook"
            class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            @change="updateContent"
          />
          <span class="ml-2 text-sm text-gray-700">{{ __('Facebook') }}</span>
        </label>
        <label class="inline-flex items-center">
          <input
            v-model="localContent.channels"
            type="checkbox"
            value="email"
            class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            @change="updateContent"
          />
          <span class="ml-2 text-sm text-gray-700">{{ __('Email') }}</span>
        </label>
        <label class="inline-flex items-center">
          <input
            v-model="localContent.channels"
            type="checkbox"
            value="sms"
            class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            @change="updateContent"
          />
          <span class="ml-2 text-sm text-gray-700">{{ __('SMS') }}</span>
        </label>
      </div>
    </div>

    <!-- Status Selection -->
    <div class="space-y-3">
      <label class="block text-sm font-medium text-gray-700">
        <FeatherIcon name="activity" class="inline h-4 w-4 mr-1" />
        {{ __("Status") }}
      </label>
      <FormControl
        type="select"
        v-model="localContent.status"
        :options="statusOptions"
        @change="updateContent"
      />
      <p class="text-xs text-gray-500">
        {{ __("Set the status of this trigger") }}
      </p>
    </div>

    <!-- Conditional Split -->
    <div class="space-y-3">
      <div class="flex items-center justify-between">
        <label class="block text-sm font-medium text-gray-700">
          <FeatherIcon name="git-branch" class="inline h-4 w-4 mr-1" />
          {{ __('Conditional Split') }}
        </label>
        <button
          @click="addCondition"
          class="inline-flex items-center px-3 py-1 text-xs font-medium text-blue-700 bg-blue-100 rounded-md hover:bg-blue-200"
        >
          <FeatherIcon name="plus" class="h-3 w-3 mr-1" />
          {{ __('Add condition') }}
        </button>
      </div>
      <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <div class="space-y-3">
          <div v-for="(condition, index) in localContent.Conditional_Split" :key="index" 
               class="bg-white border border-gray-200 rounded-lg p-3">
            <div class="flex items-center space-x-2">
              <select
                v-model="condition.field"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
                @change="updateContent"
              >
                <option value="">{{ __('Select field') }}</option>
                <option value="ho_ten">{{ __('Full name') }}</option>
                <option value="email">{{ __('Email') }}</option>
                <option value="phone">{{ __('Phone') }}</option>
                <option value="age">{{ __('Age') }}</option>
                <option value="gender">{{ __('Gender') }}</option>
                <option value="location">{{ __('Location') }}</option>
                <option value="source">{{ __('Source') }}</option>
                <option value="tag">{{ __('Tag') }}</option>
              </select>
                
                <select
                  v-model="condition.operator"
                  class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
                  @change="updateContent"
                >
                  <option value="equals">{{ __('Is') }}</option>
                  <option value="not_equals">{{ __('Is not') }}</option>
                  <option value="contains">{{ __('Contains') }}</option>
                  <option value="not_contains">{{ __('Does not contain') }}</option>
                  <option value="starts_with">{{ __('Starts with') }}</option>
                  <option value="ends_with">{{ __('Ends with') }}</option>
                  <option value="greater_than">{{ __('Greater than') }}</option>
                  <option value="less_than">{{ __('Less than') }}</option>
                  <option value="is_empty">{{ __('Is empty') }}</option>
                  <option value="is_not_empty">{{ __('Is not empty') }}</option>
                </select>
                
                <input
                  v-if="!['is_empty', 'is_not_empty'].includes(condition.operator)"
                  v-model="condition.value"
                  type="text"
                  :placeholder="getFieldPlaceholder(condition.field)"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
                  @input="updateContent"
                />
                
                <button
                  @click="removeCondition(index)"
                  class="text-red-500 hover:text-red-700 p-1 rounded "
                  title="{{ __('Remove condition') }}"
                >
                  <FeatherIcon name="trash-2" class="h-4 w-4" />
                </button>
            </div>
              
              <!-- Condition Preview -->
              <div v-if="condition.field && condition.operator" class="mt-2 text-xs text-gray-600 bg-blue-50 px-2 py-1 rounded">
                {{ getConditionPreview(condition) }}
              </div>
            </div>
            
            <!-- Add Condition Button -->
            <button
              @click="addCondition"
              class="w-full inline-flex items-center justify-center px-3 py-2 border border-dashed border-gray-300 rounded-md text-sm font-medium text-gray-600 bg-white hover:bg-gray-50 hover:border-gray-400"
            >
              <FeatherIcon name="plus" class="h-4 w-4 mr-1" />
              {{ __('Add condition') }}
            </button>
          </div>
      </div>
    </div>

    <!-- Preview Summary -->
    <!-- <div v-if="localContent.trigger_type" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <div class="flex items-start space-x-2">
        <FeatherIcon name="info" class="h-4 w-4 text-blue-600 mt-0.5" />
        <div>
          <h4 class="text-sm font-medium text-blue-900">{{ __('Summary') }}</h4>
          <p class="text-sm text-blue-700 mt-1">
            {{ getTriggerSummary() }}
          </p>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FeatherIcon, FormControl } from 'frappe-ui'

const props = defineProps({
  content: { type: Object, default: () => ({}) },
  readonly: { type: Boolean, default: false }
})

const emit = defineEmits(['update:content'])

// Local content with default structure
const localContent = ref({
  name: '',
  description: '',
  connected_account: '',
  trigger_type: '',
  sequence_id: '',
  channels: [],
  status: 'DRAFT',
  Conditional_Split: [],
  ...props.content
})

// Watch for external content changes
watch(() => props.content, (newContent) => {
  localContent.value = {
    name: '',
    description: '',
    connected_account: '',
    trigger_type: '',
    sequence_id: '',
    channels: [],
    status: 'DRAFT',
    Conditional_Split: [],
    ...newContent
  }
}, { deep: true, immediate: true })

// Status options for FormControl
const statusOptions = [
  { label: 'Draft', value: 'DRAFT' },
  { label: 'Active', value: 'ACTIVE' },
  { label: 'Paused', value: 'PAUSED' },
  { label: 'Archived', value: 'ARCHIVED' },
]

// Update content
const updateContent = () => {
  emit('update:content', { ...localContent.value })
}

// Helper methods to check trigger type
const isSequenceTrigger = () => {
  return localContent.value.trigger_type === 'subscribe_sequence' || 
         localContent.value.trigger_type === 'unsubscribe_sequence'
}

const isNewSubscriberTrigger = () => {
  return localContent.value.trigger_type === 'new_subscriber_all'
}

// Add condition
const addCondition = () => {
  localContent.value.Conditional_Split.push({
    field: '',
    operator: 'equals',
    value: ''
  })
  updateContent()
}

// Remove condition
const removeCondition = (index) => {
  localContent.value.Conditional_Split.splice(index, 1)
  updateContent()
}

// Get field placeholder
const getFieldPlaceholder = (field) => {
  const placeholders = {
    ho_ten: __('E.g: Minh, Nguyen Van A'),
    email: __('E.g: minh@example.com'),
    phone: __('E.g: 0123456789'),
    age: __('E.g: 25'),
    gender: __('E.g: Male, Female'),
    location: __('E.g: Hanoi, HCMC'),
    source: __('E.g: Facebook, Website'),
    tag: __('E.g: VIP, New customer')
  }
  return placeholders[field] || __('Enter value...')
}

// Get condition preview
const getConditionPreview = (condition) => {
  if (!condition.field || !condition.operator) return ''
  
  const fieldNames = {
    ho_ten: __('Full name'),
    email: __('Email'),
    phone: __('Phone number'),
    age: __('Age'),
    gender: __('Gender'),
    location: __('Location'),
    source: __('Registration source'),
    tag: __('Tag')
  }
  
  const operatorNames = {
    equals: __('is'),
    not_equals: __('is not'),
    contains: __('contains'),
    not_contains: __('does not contain'),
    starts_with: __('starts with'),
    ends_with: __('ends with'),
    greater_than: __('greater than'),
    less_than: __('less than'),
    is_empty: __('is empty'),
    is_not_empty: __('is not empty')
  }
  
  const fieldName = fieldNames[condition.field] || condition.field
  const operatorName = operatorNames[condition.operator] || condition.operator
  
  if (['is_empty', 'is_not_empty'].includes(condition.operator)) {
    return `${fieldName} ${operatorName}`
  }
  
  return `${fieldName} ${operatorName} "${condition.value || '...'}"`
}

// Get trigger summary
const getTriggerSummary = () => {
  const triggerTypes = {
    subscribe_sequence: __('Trigger when customer subscribes to sequence'),
    unsubscribe_sequence: __('Trigger when customer unsubscribes from sequence'),
    new_subscriber_all: __('Trigger when there is a new subscriber')
  }
  
  let summary = triggerTypes[localContent.value.trigger_type] || ''
  
  if (localContent.value.sequence_id && (localContent.value.trigger_type === 'subscribe_sequence' || localContent.value.trigger_type === 'unsubscribe_sequence')) {
    summary += ` "${localContent.value.sequence_id}"`
  }
  
  if (localContent.value.channels && localContent.value.channels.length > 0) {
    summary += ` ${__('from channels')}: ${localContent.value.channels.join(', ')}`
  }
  
  if (localContent.value.Conditional_Split && localContent.value.Conditional_Split.length > 0) {
    summary += ` ${__('when')} ${localContent.value.Conditional_Split.map(c => getConditionPreview(c)).join(` ${__('and')} `)}`
  }
  
  return summary
}
</script>
