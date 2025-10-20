<template>
  <Dialog
    :model-value="show"
    @update:model-value="$emit('close')"
    :options="{
      title: 'Add Step to Sequence',
      size: 'lg'
    }"
  >
    <template #body-content>
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Step Type Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-3">
            Choose Message Type
          </label>
          <p class="text-sm text-gray-500 mb-4">
            Select the type of message for this step
          </p>
          
          <div class="grid grid-cols-2 gap-3">
            <!-- Email -->
            <div 
              @click="selectMessageType('Email')"
              class="border rounded-lg p-3 cursor-pointer transition-all duration-200"
              :class="formData.channel === 'Email' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="mail" class="w-3 h-3 text-blue-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">Email</h3>
                </div>
                <div class="ml-2">
                  <div class="w-3 h-3 rounded-full border"
                       :class="formData.channel === 'Email' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                  </div>
                </div>
              </div>
            </div>

            <!-- SMS -->
            <div 
              @click="selectMessageType('SMS')"
              class="border rounded-lg p-3 cursor-pointer transition-all duration-200"
              :class="formData.channel === 'SMS' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-6 h-6 bg-yellow-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="message-square" class="w-3 h-3 text-yellow-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">SMS</h3>
                </div>
                <div class="ml-2">
                  <div class="w-3 h-3 rounded-full border"
                       :class="formData.channel === 'SMS' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                  </div>
                </div>
              </div>
            </div>

            <!-- Messenger -->
            <div 
              @click="selectMessageType('Messenger')"
              class="border rounded-lg p-3 cursor-pointer transition-all duration-200"
              :class="formData.channel === 'Messenger' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-6 h-6 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="message-circle" class="w-3 h-3 text-purple-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">Messenger</h3>
                </div>
                <div class="ml-2">
                  <div class="w-3 h-3 rounded-full border"
                       :class="formData.channel === 'Messenger' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                  </div>
                </div>
              </div>
            </div>

            <!-- Zalo OA -->
            <div 
              @click="selectMessageType('Zalo_OA')"
              class="border rounded-lg p-3 cursor-pointer transition-all duration-200"
              :class="formData.channel === 'Zalo_OA' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="phone" class="w-3 h-3 text-green-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">Zalo OA</h3>
                </div>
                <div class="ml-2">
                  <div class="w-3 h-3 rounded-full border"
                       :class="formData.channel === 'Zalo_OA' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                  </div>
                </div>
              </div>
            </div>

            <!-- Zalo ZNS -->
            <div 
              @click="selectMessageType('Zalo_ZNS')"
              class="border rounded-lg p-3 cursor-pointer transition-all duration-200"
              :class="formData.channel === 'Zalo_ZNS' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-6 h-6 bg-indigo-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="smartphone" class="w-3 h-3 text-indigo-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">Zalo ZNS</h3>
                </div>
                <div class="ml-2">
                  <div class="w-3 h-3 rounded-full border"
                       :class="formData.channel === 'Zalo_ZNS' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                  </div>
                </div>
              </div>
            </div>

            <!-- AI Call -->
            <div 
              @click="selectMessageType('AI_Call')"
              class="border rounded-lg p-3 cursor-pointer transition-all duration-200"
              :class="formData.channel === 'AI_Call' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-6 h-6 bg-red-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="phone-call" class="w-3 h-3 text-red-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">AI Call</h3>
                </div>
                <div class="ml-2">
                  <div class="w-3 h-3 rounded-full border"
                       :class="formData.channel === 'AI_Call' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Delay Setting -->
        <FormControl
          label="Delay from Previous Step"
          v-model="formData.delay_from_previous"
          type="text"
          placeholder="e.g., 1 day, 2 hours, 30 minutes"
        >
          <template #description>
            How long to wait before sending this message
          </template>
        </FormControl>

        <!-- Template ID -->
        <FormControl
          label="Template ID (Optional)"
          v-model="formData.template_id"
          type="text"
          placeholder="Enter template ID or leave blank"
        >
          <template #description>
            Specify a template to use for this message
          </template>
        </FormControl>

        <!-- Action if Replied -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Action if Contact Replies
          </label>
          <Select
            v-model="formData.action_if_replied"
            :options="replyActionOptions"
            placeholder="Select action"
          />
        </div>
      </form>
    </template>

    <template #actions>
      <div class="flex items-center justify-end space-x-3">
        <Button variant="outline" theme="gray" @click="$emit('close')">
          Cancel
        </Button>
        <Button
          variant="solid"
          theme="gray"
          @click="handleSubmit"
          :loading="loading"
        >
          Add Step
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, FeatherIcon, FormControl, Select } from 'frappe-ui'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  existingSteps: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'success'])
const toast = useToast()

// Form data
const formData = ref({
  channel: '',
  delay_from_previous: '1 day',
  template_id: '',
  action_if_replied: 'Continue',
  related_action: ''
})

const loading = ref(false)

// Options
const replyActionOptions = [
  { label: 'Continue Sequence', value: 'Continue' },
  { label: 'Stop Sequence', value: 'Stop Sequence' }
]

// Methods
const selectMessageType = (type) => {
  formData.value.channel = type
}

const handleSubmit = async () => {
  if (!formData.value.channel) {
    toast.error('Please select a message type')
    return
  }

  try {
    const newStep = {
      step_order: props.existingSteps.length + 1,
      delay_from_previous: formData.value.delay_from_previous || '1 day',
      channel: formData.value.channel,
      template_id: formData.value.template_id || '',
      action_if_replied: formData.value.action_if_replied || 'Continue',
      related_action: formData.value.related_action || ''
    }

    emit('success', newStep)
    emit('close')
    resetForm()
  } catch (error) {
    console.error('Error creating step:', error)
    toast.error('Failed to add step')
  }
}

const resetForm = () => {
  formData.value = {
    channel: '',
    delay_from_previous: '1 day',
    template_id: '',
    action_if_replied: 'Continue',
    related_action: ''
  }
}

// Watch for modal close to reset form
watch(() => props.show, (newValue) => {
  if (newValue) {
    resetForm()
  }
})
</script>
