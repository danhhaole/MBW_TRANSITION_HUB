<template>
  <Dialog v-model="show" :options="{ title: 'Edit Step', size: 'lg' }">
    <template #body>
      <div class="p-6 space-y-6">
        <!-- Step Basic Info -->
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Step Name
            </label>
            <input
              v-model="formData.name"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              v-model="formData.description"
              rows="2"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        <!-- Step Type Specific Configuration -->
        <div v-if="formData.type === 'personalized_email' || formData.type === 'templated_email' || formData.type === 'custom_email'">
          <h4 class="text-sm font-medium text-gray-900 mb-3">Email Configuration</h4>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Email Subject
              </label>
              <input
                v-model="formData.config.subject"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter email subject"
              />
            </div>

            <div v-if="formData.type === 'templated_email'">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Email Template
              </label>
              <select
                v-model="formData.config.template"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Select a template</option>
                <option value="welcome">Welcome Email</option>
                <option value="follow-up">Follow-up Email</option>
                <option value="value-content">Value Content Email</option>
                <option value="meeting-request">Meeting Request</option>
              </select>
            </div>

            <div v-else>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Email Content
              </label>
              <textarea
                v-model="formData.config.content"
                rows="4"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter email content..."
              />
            </div>
          </div>
        </div>

        <!-- LinkedIn Configuration -->
        <div v-else-if="formData.type.startsWith('linkedin_')">
          <h4 class="text-sm font-medium text-gray-900 mb-3">LinkedIn Configuration</h4>
          
          <div class="space-y-4">
            <div v-if="formData.type === 'linkedin_connection'">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Connection Message
              </label>
              <textarea
                v-model="formData.config.message"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Hi [Name], I'd like to connect with you..."
              />
            </div>

            <div v-else-if="formData.type === 'linkedin_message'">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Message Content
              </label>
              <textarea
                v-model="formData.config.message"
                rows="4"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Hi [Name], I noticed..."
              />
            </div>
          </div>
        </div>

        <!-- Phone Call Configuration -->
        <div v-else-if="formData.type === 'phone_call'">
          <h4 class="text-sm font-medium text-gray-900 mb-3">Phone Call Configuration</h4>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Call Purpose
              </label>
              <input
                v-model="formData.config.purpose"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="e.g., Initial discovery call"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Call Notes/Script
              </label>
              <textarea
                v-model="formData.config.notes"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Key points to discuss..."
              />
            </div>
          </div>
        </div>

        <!-- SMS Configuration -->
        <div v-else-if="formData.type === 'sms'">
          <h4 class="text-sm font-medium text-gray-900 mb-3">SMS Configuration</h4>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              SMS Message
            </label>
            <textarea
              v-model="formData.config.message"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Hi [Name], this is..."
              maxlength="160"
            />
            <div class="text-xs text-gray-500 mt-1">
              {{ (formData.config.message || '').length }}/160 characters
            </div>
          </div>
        </div>

        <!-- Task Configuration -->
        <div v-else-if="formData.type === 'task'">
          <h4 class="text-sm font-medium text-gray-900 mb-3">Task Configuration</h4>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Task Title
              </label>
              <input
                v-model="formData.config.title"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="e.g., Research company background"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Task Instructions
              </label>
              <textarea
                v-model="formData.config.instructions"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Detailed instructions for this task..."
              />
            </div>
          </div>
        </div>

        <!-- Conditions Section -->
        <div>
          <h4 class="text-sm font-medium text-gray-900 mb-3">Conditions (Optional)</h4>
          <p class="text-xs text-gray-600 mb-3">
            Add conditions to control when this step should execute
          </p>
          
          <div class="space-y-2">
            <div
              v-for="(condition, index) in formData.conditions"
              :key="index"
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <span class="text-sm">{{ condition.name }}</span>
              <Button
                variant="ghost"
                theme="red"
                size="sm"
                @click="removeCondition(index)"
              >
                <FeatherIcon name="x" class="h-4 w-4" />
              </Button>
            </div>
            
            <Button
              variant="outline"
              theme="gray"
              size="sm"
              @click="addCondition"
            >
              <FeatherIcon name="plus" class="h-4 w-4 mr-1" />
              Add Condition
            </Button>
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <Button variant="outline" theme="gray" @click="cancel">
        Cancel
      </Button>
      <Button variant="solid" theme="blue" @click="saveStep">
        Save Changes
      </Button>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { Dialog, Button, FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  step: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'save-step'])

// State
const show = ref(props.modelValue)
const formData = ref({
  name: '',
  description: '',
  type: '',
  config: {},
  conditions: []
})

// Watch modelValue
watch(() => props.modelValue, (newVal) => {
  show.value = newVal
  if (newVal && props.step) {
    formData.value = {
      name: props.step.name || '',
      description: props.step.description || '',
      type: props.step.type || '',
      config: props.step.config || {},
      conditions: props.step.conditions || []
    }
  }
})

watch(show, (newVal) => {
  emit('update:modelValue', newVal)
})

// Methods
const addCondition = () => {
  // For now, add a simple condition
  formData.value.conditions.push({
    id: Date.now(),
    name: 'Is Connected',
    type: 'connection_status',
    value: 'connected'
  })
}

const removeCondition = (index) => {
  formData.value.conditions.splice(index, 1)
}

const cancel = () => {
  show.value = false
}

const saveStep = () => {
  emit('save-step', formData.value)
  show.value = false
}
</script>
