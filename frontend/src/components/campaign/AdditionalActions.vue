<template>
  <div class="bg-white border border-gray-200 rounded-lg p-6">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center">
        <FeatherIcon name="plus-circle" class="h-5 w-5 text-blue-600 mr-2" />
        <h3 class="text-lg font-medium text-gray-900">
          {{ __("Additional Actions") }}
        </h3>
      </div>
      
      <!-- Add Action Dropdown - Only show if there are available actions -->
      <div v-if="availableActionOptions.length > 0" class="relative">
        <Button 
          variant="outline" 
          size="sm"
          @click="showDropdown = !showDropdown"
        >
          <div class="flex items-center space-x-2">
            <FeatherIcon name="plus" class="h-4 w-4 mr-1" />
            {{ __("Add Additional Action") }}
            <FeatherIcon :name="showDropdown ? 'chevron-up' : 'chevron-down'" class="h-4 w-4 ml-1" />
          </div>
        </Button>
        
        <!-- Dropdown Menu -->
        <div 
          v-if="showDropdown"
          class="absolute right-0 mt-2 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-10"
        >
          <div class="py-1">
            <button
              v-for="option in availableActionOptions"
              :key="option.value"
              @click="handleAddAction(option)"
              class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
            >
              {{ option.label }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Actions List -->
    <div v-if="actionsList.length > 0" class="space-y-3">
      <div
        v-for="(action, index) in actionsList"
        :key="`${action.trigger}-${index}`"
        class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border"
      >
        <div class="flex items-center space-x-3">
          <!-- Action Icon -->
          <div class="w-8 h-8 rounded-full flex items-center justify-center" :class="getActionIconClass(action.trigger)">
            <FeatherIcon :name="getActionIcon(action.trigger)" class="h-4 w-4" />
          </div>
          
          <!-- Action Info -->
          <div>
            <div class="text-sm font-medium text-gray-900">
              {{ getActionTitle(action.trigger) }}
            </div>
            <div class="text-xs text-gray-500">
              {{ getActionDescription(action.trigger) }}
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center space-x-2">
          <Button
            variant="ghost"
            size="sm"
            @click="configureAction(action, index)"
            class="text-blue-600 hover:text-blue-700"
          >
          <div class="flex items-center space-x-2">
            <FeatherIcon name="settings" class="h-4 w-4 mr-1" />
            {{ __("Configure") }}
          </div>
          </Button>
          <Button
            variant="ghost"
            size="sm"
            @click="removeAction(index)"
            class="text-red-600 hover:text-red-700"
          >
            <FeatherIcon name="trash-2" class="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-8 text-gray-500">
      <FeatherIcon name="zap" class="h-8 w-8 mx-auto mb-2" />
      <p class="text-sm">{{ __("No additional actions added") }}</p>
      <p class="text-xs">{{ __("Click 'Add Additional Action' to get started") }}</p>
    </div>

    <!-- Configuration Modal -->
    <Dialog v-model="showConfigModal" :options="{ title: modalTitle, size: 'lg' }">
      <template #body>
        <ActionConfigModal
          v-if="currentAction"
          :action="currentAction"
          :interaction-type="interactionType"
          @save="saveActionConfig"
          @cancel="showConfigModal = false"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Button, FeatherIcon, Dropdown, Dialog } from 'frappe-ui'
import ActionConfigModal from './ActionConfigModal.vue'

// Props
const props = defineProps({
  interactionType: {
    type: String,
    required: true,
    validator: (value) => ['EMAIL', 'ZALO_ZNS', 'ZALO_CARE'].includes(value)
  },
  modelValue: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['update:modelValue'])

// Translation helper
const __ = (text) => text

// State
const actionsList = ref([])
const showConfigModal = ref(false)
const currentAction = ref(null)
const currentActionIndex = ref(-1)
const showDropdown = ref(false)

// All possible actions based on interaction type
const allActionOptions = computed(() => {
  if (props.interactionType === 'EMAIL') {
    return [
      { label: __("When email is opened"), value: "email_open" },
      { label: __("When link is clicked"), value: "link_click" },
      { label: __("When action is successful"), value: "send_success" },
      { label: __("When action fails"), value: "send_failed" }
    ]
  }
  return []
})

// Available actions (exclude already added ones)
const availableActionOptions = computed(() => {
  const addedTriggers = actionsList.value.map(action => action.trigger)
  console.log('🔍 Debug filtering:', {
    allActions: allActionOptions.value,
    addedTriggers,
    actionsList: actionsList.value
  })
  return allActionOptions.value.filter(option => !addedTriggers.includes(option.value))
})

// Modal title
const modalTitle = computed(() => {
  if (!currentAction.value) return ''
  return `${__("Cấu hình")} - ${getActionTitle(currentAction.value.trigger)}`
})

// Helper functions
const getActionIcon = (trigger) => {
  const icons = {
    email_open: 'mail-open',
    link_click: 'link',
    send_success: 'check-circle',
    send_failed: 'x-circle'
  }
  return icons[trigger] || 'settings'
}

const getActionIconClass = (trigger) => {
  const classes = {
    email_open: 'bg-blue-100 text-blue-600',
    link_click: 'bg-green-100 text-green-600',
    send_success: 'bg-emerald-100 text-emerald-600',
    send_failed: 'bg-red-100 text-red-600'
  }
  return classes[trigger] || 'bg-gray-100 text-gray-600'
}

const getActionTitle = (trigger) => {
  const titles = {
    email_open: __("When email is opened"),
    link_click: __("When link is clicked"),
    send_success: __("When action is successful"),
    send_failed: __("When action fails")
  }
  return titles[trigger] || trigger
}

const getActionDescription = (trigger) => {
  const descriptions = {
    email_open: __("Triggered when the email is opened."),
    link_click: __("Triggered when the link is clicked."),
    send_success: __("Triggered when the action is successful."),
    send_failed: __("Triggered when the action fails.")
  }
  return descriptions[trigger] || ''
}

// Methods
const addAction = (option) => {
  console.log('🔍 Adding action:', option)
  
  // Check if action already exists
  const exists = actionsList.value.some(action => action.trigger === option.value)
  if (exists) {
    console.log('❌ Action already exists')
    return
  }

  const newAction = {
    trigger: option.value,
    type: '',
    data: {},
    configured: false
  }
  
  console.log('✅ Adding new action:', newAction)
  actionsList.value.push(newAction)
  emitUpdate()
}

const handleAddAction = (option) => {
  addAction(option)
  showDropdown.value = false // Close dropdown after adding
}

const removeAction = (index) => {
  actionsList.value.splice(index, 1)
  emitUpdate()
}

const configureAction = (action, index) => {
  currentAction.value = { ...action }
  currentActionIndex.value = index
  showConfigModal.value = true
}

const saveActionConfig = (configData) => {
  if (currentActionIndex.value >= 0) {
    actionsList.value[currentActionIndex.value] = {
      ...actionsList.value[currentActionIndex.value],
      ...configData,
      configured: true
    }
    emitUpdate()
  }
  showConfigModal.value = false
  currentAction.value = null
  currentActionIndex.value = -1
}

const emitUpdate = () => {
  const actionsData = {}
  actionsList.value.forEach(action => {
    actionsData[action.trigger] = {
      type: action.type,
      data: action.data,
      configured: action.configured
    }
  })
  emit('update:modelValue', actionsData)
}

// Initialize from props
watch(() => props.modelValue, (newValue) => {
  console.log('🔍 Initializing from props:', newValue)
  if (newValue && Object.keys(newValue).length > 0) {
    actionsList.value = Object.keys(newValue).map(trigger => ({
      trigger,
      type: newValue[trigger].type || '',
      data: newValue[trigger].data || {},
      configured: newValue[trigger].configured || false
    }))
    console.log('✅ Initialized actionsList:', actionsList.value)
  } else {
    console.log('🔄 No props data, keeping actionsList empty')
  }
}, { immediate: true })
</script>

<style scoped>
/* Custom styles for better visual hierarchy */
.border-l-4 {
  transition: all 0.2s ease-in-out;
}

.border-l-4:hover {
  background-color: rgba(0, 0, 0, 0.02);
}
</style>
