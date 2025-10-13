<template>
  <Dialog v-model="show" :options="{ title: 'Add New Step', size: 'lg' }">
    <template #body-content>
      <div class="p-6">
        <!-- Step Type Selection -->
        <div class="mb-6">
          <h4 class="text-sm font-medium text-gray-900 mb-3">Choose Action Type</h4>
          <div class="grid grid-cols-2 gap-3">
            <!-- Email Actions -->
            <div class="space-y-2">
              <h5 class="text-xs font-medium text-gray-700 uppercase tracking-wide">Email</h5>
              <div
                v-for="action in emailActions"
                :key="action.type"
                class="action-card p-3 border rounded-lg cursor-pointer transition-all"
                :class="selectedAction?.type === action.type ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
                @click="selectAction(action)"
              >
                <div class="flex items-center">
                  <FeatherIcon :name="action.icon" class="h-4 w-4 mr-2 text-gray-600" />
                  <span class="text-sm font-medium">{{ action.name }}</span>
                </div>
                <p class="text-xs text-gray-500 mt-1">{{ action.description }}</p>
              </div>
            </div>

            <!-- LinkedIn Actions -->
            <div class="space-y-2">
              <h5 class="text-xs font-medium text-gray-700 uppercase tracking-wide">LinkedIn</h5>
              <div
                v-for="action in linkedinActions"
                :key="action.type"
                class="action-card p-3 border rounded-lg cursor-pointer transition-all"
                :class="selectedAction?.type === action.type ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
                @click="selectAction(action)"
              >
                <div class="flex items-center">
                  <FeatherIcon :name="action.icon" class="h-4 w-4 mr-2 text-gray-600" />
                  <span class="text-sm font-medium">{{ action.name }}</span>
                </div>
                <p class="text-xs text-gray-500 mt-1">{{ action.description }}</p>
              </div>
            </div>

            <!-- Other Actions -->
            <div class="space-y-2 col-span-2">
              <h5 class="text-xs font-medium text-gray-700 uppercase tracking-wide">Other</h5>
              <div class="grid grid-cols-2 gap-3">
                <div
                  v-for="action in otherActions"
                  :key="action.type"
                  class="action-card p-3 border rounded-lg cursor-pointer transition-all"
                  :class="selectedAction?.type === action.type ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
                  @click="selectAction(action)"
                >
                  <div class="flex items-center">
                    <FeatherIcon :name="action.icon" class="h-4 w-4 mr-2 text-gray-600" />
                    <span class="text-sm font-medium">{{ action.name }}</span>
                  </div>
                  <p class="text-xs text-gray-500 mt-1">{{ action.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Step Configuration -->
        <div v-if="selectedAction" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Step Name
            </label>
            <input
              v-model="stepName"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :placeholder="selectedAction.name"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              v-model="stepDescription"
              rows="2"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :placeholder="selectedAction.description"
            />
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <Button variant="outline" theme="gray" @click="cancel">
        Cancel
      </Button>
      <Button 
        variant="solid" 
        theme="blue" 
        @click="addStep"
        :disabled="!selectedAction"
      >
        Add Step
      </Button>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'add-step'])

// State
const show = ref(props.modelValue)
const selectedAction = ref(null)
const stepName = ref('')
const stepDescription = ref('')

// Watch modelValue
watch(() => props.modelValue, (newVal) => {
  show.value = newVal
  if (newVal) {
    resetForm()
  }
})

watch(show, (newVal) => {
  emit('update:modelValue', newVal)
})

// Action types
const emailActions = [
  {
    type: 'personalized_email',
    name: 'Personalized Email',
    description: 'Send personalized email with dynamic content',
    icon: 'mail'
  },
  {
    type: 'templated_email',
    name: 'Templated Email',
    description: 'Send email using predefined template',
    icon: 'file-text'
  },
  {
    type: 'custom_email',
    name: 'Custom Email',
    description: 'Send custom email with specific content',
    icon: 'edit'
  }
]

const linkedinActions = [
  {
    type: 'linkedin_connection',
    name: 'LinkedIn Connection',
    description: 'Send connection request on LinkedIn',
    icon: 'user-plus'
  },
  {
    type: 'linkedin_message',
    name: 'LinkedIn Message',
    description: 'Send direct message on LinkedIn',
    icon: 'message-circle'
  },
  {
    type: 'linkedin_post_like',
    name: 'Like LinkedIn Post',
    description: 'Like their recent LinkedIn post',
    icon: 'heart'
  },
  {
    type: 'linkedin_profile_view',
    name: 'View LinkedIn Profile',
    description: 'View their LinkedIn profile',
    icon: 'eye'
  }
]

const otherActions = [
  {
    type: 'phone_call',
    name: 'Phone Call',
    description: 'Schedule or make a phone call',
    icon: 'phone'
  },
  {
    type: 'sms',
    name: 'SMS',
    description: 'Send text message',
    icon: 'smartphone'
  },
  {
    type: 'task',
    name: 'Task',
    description: 'Create a manual task',
    icon: 'check-square'
  },
  {
    type: 'wait',
    name: 'Wait',
    description: 'Wait for a specific period',
    icon: 'clock'
  }
]

// Methods
const selectAction = (action) => {
  selectedAction.value = action
  stepName.value = action.name
  stepDescription.value = action.description
}

const resetForm = () => {
  selectedAction.value = null
  stepName.value = ''
  stepDescription.value = ''
}

const cancel = () => {
  show.value = false
  resetForm()
}

const addStep = () => {
  if (selectedAction.value) {
    emit('add-step', {
      name: stepName.value || selectedAction.value.name,
      description: stepDescription.value || selectedAction.value.description,
      type: selectedAction.value.type,
      icon: selectedAction.value.icon
    })
    show.value = false
    resetForm()
  }
}
</script>

<style scoped>
.action-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
