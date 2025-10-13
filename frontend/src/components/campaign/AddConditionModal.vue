<template>
  <Dialog v-model="show" :options="{ title: 'Add Condition', size: 'lg' }">
    <template #body>
      <div class="p-6">
        <!-- Condition Type Selection -->
        <div class="mb-6">
          <h4 class="text-sm font-medium text-gray-900 mb-3">Choose Condition Type</h4>
          <div class="grid grid-cols-1 gap-3">
            <div
              v-for="condition in conditionTypes"
              :key="condition.type"
              class="condition-card p-4 border rounded-lg cursor-pointer transition-all"
              :class="selectedCondition?.type === condition.type ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-gray-300'"
              @click="selectCondition(condition)"
            >
              <div class="flex items-start">
                <FeatherIcon :name="condition.icon" class="h-5 w-5 mr-3 text-gray-600 mt-0.5" />
                <div class="flex-1">
                  <h5 class="font-medium text-gray-900">{{ condition.name }}</h5>
                  <p class="text-sm text-gray-600 mt-1">{{ condition.description }}</p>
                  <div class="mt-2 text-xs text-gray-500">
                    <strong>Example:</strong> {{ condition.example }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Condition Configuration -->
        <div v-if="selectedCondition" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Condition Name
            </label>
            <input
              v-model="conditionName"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              :placeholder="selectedCondition.name"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              v-model="conditionDescription"
              rows="2"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              :placeholder="selectedCondition.description"
            />
          </div>

          <!-- Condition-specific configuration -->
          <div v-if="selectedCondition.type === 'response_received'">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Wait for Response (days)
            </label>
            <input
              v-model.number="conditionConfig.waitDays"
              type="number"
              min="1"
              max="30"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              placeholder="7"
            />
          </div>

          <div v-else-if="selectedCondition.type === 'email_opened'">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Check After (hours)
            </label>
            <input
              v-model.number="conditionConfig.checkAfterHours"
              type="number"
              min="1"
              max="72"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              placeholder="24"
            />
          </div>

          <div v-else-if="selectedCondition.type === 'linkedin_connected'">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Connection Timeout (days)
            </label>
            <input
              v-model.number="conditionConfig.timeoutDays"
              type="number"
              min="1"
              max="14"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              placeholder="3"
            />
          </div>

          <!-- Timing Configuration -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Check Condition After
            </label>
            <div class="flex space-x-2">
              <input
                v-model.number="conditionDelay"
                type="number"
                min="0"
                class="w-20 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                placeholder="1"
              />
              <select
                v-model="conditionDelayUnit"
                class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              >
                <option value="minutes">minutes</option>
                <option value="hours">hours</option>
                <option value="days">days</option>
                <option value="weeks">weeks</option>
              </select>
            </div>
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
        theme="purple" 
        @click="addCondition"
        :disabled="!selectedCondition"
      >
        Add Condition
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
const emit = defineEmits(['update:modelValue', 'add-condition'])

// State
const show = ref(props.modelValue)
const selectedCondition = ref(null)
const conditionName = ref('')
const conditionDescription = ref('')
const conditionDelay = ref(1)
const conditionDelayUnit = ref('days')
const conditionConfig = ref({})

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

// Condition types
const conditionTypes = [
  {
    type: 'response_received',
    name: 'Response Received',
    description: 'Check if prospect replied to email or message',
    icon: 'mail',
    example: 'If prospect replies within 7 days → Yes branch, else → No branch'
  },
  {
    type: 'email_opened',
    name: 'Email Opened',
    description: 'Check if prospect opened the email',
    icon: 'eye',
    example: 'If email is opened within 24 hours → Yes branch, else → No branch'
  },
  {
    type: 'linkedin_connected',
    name: 'LinkedIn Connected',
    description: 'Check if LinkedIn connection was accepted',
    icon: 'user-plus',
    example: 'If connection accepted within 3 days → Yes branch, else → No branch'
  },
  {
    type: 'link_clicked',
    name: 'Link Clicked',
    description: 'Check if prospect clicked a link in email',
    icon: 'external-link',
    example: 'If any link is clicked → Yes branch, else → No branch'
  },
  {
    type: 'profile_viewed',
    name: 'Profile Viewed',
    description: 'Check if prospect viewed your LinkedIn profile',
    icon: 'eye',
    example: 'If profile viewed within 2 days → Yes branch, else → No branch'
  },
  {
    type: 'custom_condition',
    name: 'Custom Condition',
    description: 'Define your own custom condition logic',
    icon: 'settings',
    example: 'Based on custom field values or external data'
  }
]

// Methods
const selectCondition = (condition) => {
  selectedCondition.value = condition
  conditionName.value = condition.name
  conditionDescription.value = condition.description
  
  // Set default config based on condition type
  conditionConfig.value = {}
  switch (condition.type) {
    case 'response_received':
      conditionConfig.value = { waitDays: 7 }
      break
    case 'email_opened':
      conditionConfig.value = { checkAfterHours: 24 }
      break
    case 'linkedin_connected':
      conditionConfig.value = { timeoutDays: 3 }
      break
    default:
      conditionConfig.value = {}
  }
}

const resetForm = () => {
  selectedCondition.value = null
  conditionName.value = ''
  conditionDescription.value = ''
  conditionDelay.value = 1
  conditionDelayUnit.value = 'days'
  conditionConfig.value = {}
}

const cancel = () => {
  show.value = false
  resetForm()
}

const addCondition = () => {
  if (selectedCondition.value) {
    emit('add-condition', {
      name: conditionName.value || selectedCondition.value.name,
      description: conditionDescription.value || selectedCondition.value.description,
      type: selectedCondition.value.type,
      delay: conditionDelay.value,
      delayUnit: conditionDelayUnit.value,
      config: {
        ...conditionConfig.value,
        conditionType: selectedCondition.value.type
      }
    })
    show.value = false
    resetForm()
  }
}
</script>

<style scoped>
.condition-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
