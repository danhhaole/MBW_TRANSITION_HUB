<template>
  <Dialog v-model="showModal" :options="{ title: __('Delay'), size: 'sm' }">
    <template #body-content>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __('Message will be sent') }}
          </label>
          
          <div class="flex items-center space-x-2">
            <!-- Number Input -->
            <div class="flex-1">
              <Select
                v-model="delayNumber"
                :options="numberOptions"
                :placeholder="__('1')"
              />
            </div>
            
            <!-- Unit Select -->
            <div class="flex-1">
              <Select
                v-model="delayUnit"
                :options="unitOptions"
                :placeholder="__('Day')"    
              />
            </div>
          </div>
          
          <p class="text-sm text-gray-500 mt-2">
            {{ __('after user receive message from previous step') }}
          </p>
        </div>
      </div>
    </template>
    
    <template #actions>
      <div class="flex justify-end space-x-3">
        <Button
          variant="outline"
          theme="gray"
          @click="cancel"
        >
            {{ __('Cancel') }}
        </Button>
        <Button
          variant="solid"
          theme="gray"
          @click="save"
        >
          {{ __('Save') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { Dialog, Button, Select } from 'frappe-ui'

// Props
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  currentDelay: {
    type: String,
    default: '1 day'
  },
  isInitial: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['update:show', 'save', 'cancel'])

// State
const delayNumber = ref('1')
const delayUnit = ref('day')

// Computed for v-model
const showModal = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

// Options
const numberOptions = computed(() => {
  const options = []
  for (let i = 1; i <= 30; i++) {
    options.push({ label: i.toString(), value: i.toString() })
  }
  return options
})

const unitOptions = [
  { label: __('Minute'), value: 'minute' },
  { label: __('Hour'), value: 'hour' },
  { label: __('Day'), value: 'day' },
  { label: __('Week'), value: 'week' },
  { label: __('Month'), value: 'month' }
]

// Parse current delay when modal opens or currentDelay changes
watch(() => props.currentDelay, (newDelay) => {
  if (newDelay) {
    parseDelay(newDelay)
  }
}, { immediate: true })

// Also parse when modal opens
watch(() => props.show, (isShown) => {
  if (isShown && props.currentDelay) {
    console.log('🔍 Modal opened with currentDelay:', props.currentDelay)
    parseDelay(props.currentDelay)
    console.log('📝 Parsed to:', delayNumber.value, delayUnit.value)
  }
})

const parseDelay = (delayString) => {
  // Parse strings like "1 day", "2 hours", "30 minutes", etc.
  const match = delayString.match(/(\d+)\s*(\w+)/)
  if (match) {
    delayNumber.value = match[1]
    const unit = match[2].toLowerCase()
    
    // Map various unit formats to our standard units
    if (unit.includes('minute') || unit.includes('phút')) {
      delayUnit.value = 'minute'
    } else if (unit.includes('hour') || unit.includes('giờ') || unit.includes('gio')) {
      delayUnit.value = 'hour'  
    } else if (unit.includes('day') || unit.includes('ngày') || unit.includes('ngay')) {
      delayUnit.value = 'day'
    } else if (unit.includes('week') || unit.includes('tuần') || unit.includes('tuan')) {
      delayUnit.value = 'week'
    } else if (unit.includes('month') || unit.includes('tháng') || unit.includes('thang')) {
      delayUnit.value = 'month'
    }
  }
}

const formatDelay = () => {
  // Return English format for consistency: "1 day", "2 hours", etc.
  const unitMap = {
    'minute': 'minute',
    'hour': 'hour', 
    'day': 'day',
    'week': 'week',
    'month': 'month'
  }
  
  const unit = unitMap[delayUnit.value] || delayUnit.value
  // Add 's' for plural
  const pluralUnit = delayNumber.value > 1 ? `${unit}s` : unit
  
  return `${delayNumber.value} ${pluralUnit}`
}

const save = () => {
  const formattedDelay = formatDelay()
  emit('save', formattedDelay)
  emit('update:show', false)
}

const cancel = () => {
  emit('cancel')
  emit('update:show', false)
}
</script>
