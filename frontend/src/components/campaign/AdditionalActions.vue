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
    <!-- {{ sortedActionsList }} -->
    <!-- Actions List -->
    <div v-if="sortedActionsList.length > 0" class="space-y-3">
      <div
        v-for="(action, index) in sortedActionsList"
        :key="`${action.trigger}-${index}`"
        class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border cursor-pointer hover:bg-gray-100 transition-colors"
        :class="{ 'opacity-50': action.is_disabled }"
        @click="handleActionClick(action, index)"
      >
        <div class="flex items-center space-x-3 flex-1">
          <!-- Action Icon -->
          <div class="w-8 h-8 rounded-full flex items-center justify-center" :class="getActionIconClass(action.trigger)">
            <FeatherIcon :name="getActionIcon(action.trigger)" class="h-4 w-4" />
          </div>
          
          <!-- Action Info -->
          <div class="flex-1">
            <div class="text-sm font-medium text-gray-900 flex items-center gap-2">
              {{ getActionTitle(action.trigger) }}
              <span v-if="action.is_disabled" class="text-xs text-red-600 font-normal">(Disabled)</span>
            </div>
            <div class="text-xs text-gray-500">
              {{ getActionDescription(action.trigger) }}
            </div>
            <!-- Show linked action name if configured -->
            <div v-if="action.configured && action.action_id" class="mt-1 text-xs text-blue-600 flex items-center gap-1">
              <FeatherIcon name="link" class="h-3 w-3" />
              {{ getActionTypeName(action.type) }}
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center space-x-2" @click.stop>
          <!-- Only show Configure if not configured yet -->
          <Button
            v-if="!action.configured || !action.action_id"
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
  },
  // If true, clicking configured action will emit select-action event instead of opening modal
  enableActionSelection: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'select-action'])

// Translation helper
const __ = (text) => text

// State
const actionsList = ref([])
const showConfigModal = ref(false)
const currentAction = ref(null)
const currentActionIndex = ref(-1)
const showDropdown = ref(false)

// Sorted actions list - sort by trigger key to maintain consistent order
const sortedActionsList = computed(() => {
  return [...actionsList.value].sort((a, b) => {
    // Define order for triggers
    const triggerOrder = {
      'email_open': 1,
      'link_click': 2,
      'send_success': 3,
      'send_failed': 4,
      'user_response': 5
    }
    return (triggerOrder[a.trigger] || 999) - (triggerOrder[b.trigger] || 999)
  })
})

// All possible actions based on interaction type
const allActionOptions = computed(() => {
  if (props.interactionType === 'EMAIL') {
    return [
      { label: __("When email is opened"), value: "email_open" },
      { label: __("When link is clicked"), value: "link_click" },
      { label: __("When action is successful"), value: "send_success" },
      { label: __("When action fails"), value: "send_failed" }
    ]
  } else if (props.interactionType === 'ZALO_ZNS') {
    // For SMS and Zalo ZNS
    return [
      { label: __("When message is sent successfully"), value: "send_success" },
      { label: __("When message fails to send"), value: "send_failed" }
    ]
  } else if (props.interactionType === 'ZALO_CARE') {
    // For Zalo OA, Messenger, AI Call
    return [
      { label: __("When message is sent successfully"), value: "send_success" },
      { label: __("When message fails to send"), value: "send_failed" },
      { label: __("When user responds"), value: "user_response" }
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
    send_failed: 'x-circle',
    user_response: 'message-circle'
  }
  return icons[trigger] || 'settings'
}

const getActionIconClass = (trigger) => {
  const classes = {
    email_open: 'bg-blue-100 text-blue-600',
    link_click: 'bg-green-100 text-green-600',
    send_success: 'bg-emerald-100 text-emerald-600',
    send_failed: 'bg-red-100 text-red-600',
    user_response: 'bg-purple-100 text-purple-600'
  }
  return classes[trigger] || 'bg-gray-100 text-gray-600'
}

const getActionTitle = (trigger) => {
  const titles = {
    email_open: __("When email is opened"),
    link_click: __("When link is clicked"),
    send_success: __("When action is successful"),
    send_failed: __("When action fails"),
    user_response: __("When user responds")
  }
  return titles[trigger] || trigger
}

const getActionDescription = (trigger) => {
  const descriptions = {
    email_open: __("Triggered when the email is opened."),
    link_click: __("Triggered when the link is clicked."),
    send_success: __("Triggered when the action is successful."),
    send_failed: __("Triggered when the action fails."),
    user_response: __("Triggered when the user responds to the message.")
  }
  return descriptions[trigger] || ''
}

const getActionTypeName = (type) => {
  const names = {
    'add_tag': __('Add Tag'),
    'remove_tag': __('Remove Tag'),
    'subscribe_to_sequence': __('Subscribe to Sequence'),
    'start_flow': __('Start Flow'),
    'send_email': __('Send Email'),
    'add_custom_field': __('Add Custom Field'),
    'smart_delay': __('Smart Delay'),
    'unsubscribe': __('Unsubscribe'),
    'sms': __('Send SMS'),
    'zalo': __('Send Zalo')
  }
  return names[type] || type
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

const handleActionClick = (action, index) => {
  // If action is configured and has action_id, select it in FlowEditor
  console.log('🔍 Action clicked:', action)
  console.log('   - enableActionSelection:', props.enableActionSelection)
  console.log('   - action.configured:', action.configured)
  console.log('   - action.action_id:', action.action_id)
  
  if (props.enableActionSelection && action.configured && action.action_id) {
    console.log('✅ Action configured, selecting in FlowEditor:', action.action_id)
    emit('select-action', action.action_id)
  } else {
    // If not configured or enableActionSelection is false, open configure modal
    console.log('⚙️ Opening modal')
    configureAction(action, index)
  }
}

const removeAction = (index) => {
  console.log('🗑️ Removing action at index:', index)
  console.log('📋 Before remove:', actionsList.value)
  
  actionsList.value.splice(index, 1)
  
  console.log('📋 After remove:', actionsList.value)
  emitUpdate()
}

const configureAction = (action, index) => {
  // Open modal to configure (only for unconfigured actions)
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
    // Emit immediately when saving config (important action)
    emitUpdateImmediate()
  }
  showConfigModal.value = false
  currentAction.value = null
  currentActionIndex.value = -1
}

// Debounce timer for emit
let emitTimer = null

const emitUpdateImmediate = () => {
  // Clear any pending debounced emit
  if (emitTimer) {
    clearTimeout(emitTimer)
    emitTimer = null
  }
  
  // Create a fresh object from current actionsList
  const actionsData = {}
  actionsList.value.forEach(action => {
    actionsData[action.trigger] = {
      type: action.type,
      data: action.data,
      configured: action.configured,
      action_id: action.action_id || null  // ✅ Include action_id
    }
  })
  
  console.log('📤 Emitting additional_actions:', actionsData)
  console.log('📋 Current actionsList:', actionsList.value)
  
  emit('update:modelValue', actionsData)
}

const emitUpdate = () => {
  // Clear previous timer
  if (emitTimer) {
    clearTimeout(emitTimer)
  }
  
  // Debounce emit to avoid too many updates
  emitTimer = setTimeout(() => {
    emitUpdateImmediate()
  }, 300) // Wait 300ms before emitting
}

// Track if we're updating to prevent infinite loop
const isUpdatingFromProps = ref(false)

// Initialize from props
watch(() => props.modelValue, (newValue, oldValue) => {
  // Prevent infinite loop: skip if we just emitted an update
  if (isUpdatingFromProps.value) {
    console.log('⏭️ Skipping props update - just emitted')
    return
  }
  
  // Deep equality check to avoid unnecessary updates
  const newValueStr = JSON.stringify(newValue)
  const oldValueStr = JSON.stringify(oldValue)
  if (newValueStr === oldValueStr) {
    console.log('⏭️ Skipping props update - no changes')
    return
  }
  
  console.log('🔍 AdditionalActions - Syncing from props:', newValue)
  console.log('🔍 Old value:', oldValue)
  isUpdatingFromProps.value = true
  
  // IMPORTANT: Always create a fresh array from props, don't merge with existing
  if (newValue && Object.keys(newValue).length > 0) {
    // Create fresh actionsList from props
    actionsList.value = Object.keys(newValue).map(trigger => ({
      trigger,
      type: newValue[trigger].type || '',
      data: newValue[trigger].data || {},
      configured: newValue[trigger].configured || false,
      action_id: newValue[trigger].action_id || null
    }))
    console.log('✅ Synced actionsList from props:', actionsList.value)
  } else {
    // If props is empty, clear actionsList
    actionsList.value = []
    console.log('🔄 Props empty, cleared actionsList')
  }
  
  // Reset flag after a short delay
  setTimeout(() => {
    isUpdatingFromProps.value = false
  }, 100)
}, { immediate: true, deep: true })
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
