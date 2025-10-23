<template>
  <div class="space-y-2">
    <!-- Display selected items as chips -->
    <div v-if="selectedItems.length > 0" class="flex flex-wrap gap-2">
      <span 
        v-for="(item, index) in selectedItems" 
        :key="index"
        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
        :class="chipClass"
      >
        {{ item }}
        <button 
          type="button" 
          @click="removeItem(index)"
          class="ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center hover:bg-opacity-20 focus:outline-none"
        >
          <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
            <path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
          </svg>
        </button>
      </span>
    </div>

    <!-- Preview items to be added -->
    <div v-if="previewItems.length > 0" class="flex flex-wrap gap-2">
      <span class="text-xs text-gray-500 w-full">{{ __('Will be added:') }}</span>
      <span 
        v-for="(item, index) in previewItems" 
        :key="`preview-${index}`"
        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600 border-2 border-dashed border-gray-300"
      >
        {{ item }}
      </span>
    </div>
    
    <!-- Input field -->
    <input 
      v-model="inputValue" 
      @keydown.enter.prevent="addItems"
      @blur="addItems"
      type="text"
      :placeholder="placeholder"
      class="block w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
    />
    <!-- <p class="text-xs text-gray-500">
      {{ __('Tip: Enter multiple items separated by commas, then press Enter') }}
    </p> -->
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Enter items separated by commas...'
  },
  chipColor: {
    type: String,
    default: 'blue' // blue, purple, green
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// Local state
const inputValue = ref('')
const selectedItems = ref([])

// Computed
const chipClass = computed(() => {
  const colors = {
    blue: 'bg-blue-100 text-blue-800',
    purple: 'bg-purple-100 text-purple-800',
    green: 'bg-green-100 text-green-800'
  }
  return colors[props.chipColor] || colors.blue
})

const previewItems = computed(() => {
  if (!inputValue.value.trim()) return []
  
  return inputValue.value
    .split(',')
    .map(item => item.trim())
    .filter(item => item.length > 0)
})

// Methods
const addItems = () => {
  if (!inputValue.value.trim()) return
  
  const itemsToAdd = inputValue.value
    .split(',')
    .map(item => item.trim())
    .filter(item => item.length > 0)
    .filter(item => !selectedItems.value.includes(item))
  
  selectedItems.value.push(...itemsToAdd)
  inputValue.value = ''
  
  // Emit as comma-separated string
  emitValue()
}

const removeItem = (index) => {
  selectedItems.value.splice(index, 1)
  emitValue()
}

const emitValue = () => {
  const value = selectedItems.value.join(', ')
  emit('update:modelValue', value)
  emit('change', value)
}

// Parse initial value
const parseValue = (value) => {
  if (!value) {
    selectedItems.value = []
    return
  }
  
  selectedItems.value = value
    .split(',')
    .map(item => item.trim())
    .filter(item => item.length > 0)
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  const currentValue = selectedItems.value.join(', ')
  if (newValue !== currentValue) {
    parseValue(newValue)
  }
}, { immediate: true })
</script>

<style scoped>
/* Add any custom styles if needed */
</style>
