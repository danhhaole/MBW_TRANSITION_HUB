<template>
  <Dialog
    :model-value="show"
    @update:model-value="$emit('close')"
    :options="{
      title: __('Create New Sequence'),
      size: 'xl'
    }"
  >
    <template #body-content>
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Sequence Name -->
        <FormControl
          :label="__('Sequence Name')"
          v-model="formData.title"
          type="text"
          :placeholder="__('Sequence Name [Required]')"
          required
        />

      <!-- Message Type Selection -->
      <div class="space-y-3">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __('First Message Type') }} <span class="text-red-500">*</span>
          </label>
          <p class="text-sm text-gray-500 mb-4">
            {{ __('Choose the first message type for the sequence') }}
          </p>
          
          <div class="grid grid-cols-2 gap-4">
            <!-- Messenger -->
            <div 
              @click="selectMessageType('messenger')"
              class="border rounded-lg p-4 cursor-pointer transition-all duration-200"
              :class="formData.messageType === 'messenger' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="message-circle" class="w-4 h-4 text-blue-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">{{ __('Send Messenger Message') }}</h3>
                  <p class="text-xs text-gray-500">{{ __('Send a message to the customer via Messenger') }}</p>
                </div>
                <div class="ml-2">
                  <div class="w-4 h-4 rounded-full border-2"
                       :class="formData.messageType === 'messenger' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                    <div v-if="formData.messageType === 'messenger'" 
                         class="w-2 h-2 bg-white rounded-full mx-auto mt-0.5"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Email -->
            <div 
              @click="selectMessageType('email')"
              class="border rounded-lg p-4 cursor-pointer transition-all duration-200"
              :class="formData.messageType === 'email' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="mail" class="w-4 h-4 text-green-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">{{ __('Send Email') }}</h3>
                  <p class="text-xs text-gray-500">{{ __('Create and send an email to the customer') }}</p>
                </div>
                <div class="ml-2">
                  <div class="w-4 h-4 rounded-full border-2"
                       :class="formData.messageType === 'email' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                    <div v-if="formData.messageType === 'email'" 
                         class="w-2 h-2 bg-white rounded-full mx-auto mt-0.5"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Zalo Quan Tâm -->
            <div 
              @click="selectMessageType('zalo_oa')"
              class="border rounded-lg p-4 cursor-pointer transition-all duration-200"
              :class="formData.messageType === 'zalo_oa' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="phone" class="w-4 h-4 text-blue-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">{{ __('Send Zalo Quan Tâm Message') }}</h3>
                  <p class="text-xs text-gray-500">{{ __('Send a message to the customer via Zalo Quan Tâm') }}</p>
                </div>
                <div class="ml-2">
                  <div class="w-4 h-4 rounded-full border-2"
                       :class="formData.messageType === 'zalo_oa' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                    <div v-if="formData.messageType === 'zalo_oa'" 
                         class="w-2 h-2 bg-white rounded-full mx-auto mt-0.5"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Zalo ZNS -->
            <div 
              @click="selectMessageType('zalo_zns')"
              class="border rounded-lg p-4 cursor-pointer transition-all duration-200"
              :class="formData.messageType === 'zalo_zns' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="smartphone" class="w-4 h-4 text-blue-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">{{ __('Send Zalo ZNS Message') }}</h3>
                  <p class="text-xs text-gray-500">{{ __('Send a message to the customer via Zalo ZNS') }}</p>
                </div>
                <div class="ml-2">
                  <div class="w-4 h-4 rounded-full border-2"
                       :class="formData.messageType === 'zalo_zns' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                    <div v-if="formData.messageType === 'zalo_zns'" 
                         class="w-2 h-2 bg-white rounded-full mx-auto mt-0.5"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- SMS -->
            <div 
              @click="selectMessageType('sms')"
              class="border rounded-lg p-4 cursor-pointer transition-all duration-200"
              :class="formData.messageType === 'sms' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="message-square" class="w-4 h-4 text-yellow-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">{{ __('Send SMS') }}</h3>
                  <p class="text-xs text-gray-500">{{ __('Send a message to the customer via SMS') }}</p>
                </div>
                <div class="ml-2">
                  <div class="w-4 h-4 rounded-full border-2"
                       :class="formData.messageType === 'sms' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                    <div v-if="formData.messageType === 'sms'" 
                         class="w-2 h-2 bg-white rounded-full mx-auto mt-0.5"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- AI Call -->
            <div 
              @click="selectMessageType('ai_call')"
              class="border rounded-lg p-4 cursor-pointer transition-all duration-200"
              :class="formData.messageType === 'ai_call' 
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                : 'border-gray-200 hover:border-gray-300'"
            >
              <div class="flex items-center">
                <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                  <FeatherIcon name="phone-call" class="w-4 h-4 text-purple-600" />
                </div>
                <div class="flex-1">
                  <h3 class="text-sm font-medium text-gray-900">{{ __('AI Call') }}</h3>
                  <p class="text-xs text-gray-500">{{ __('Call automatically using AI Call technology') }}</p>
                </div>
                <div class="ml-2">
                  <div class="w-4 h-4 rounded-full border-2"
                       :class="formData.messageType === 'ai_call' 
                         ? 'border-blue-500 bg-blue-500' 
                         : 'border-gray-300'">
                    <div v-if="formData.messageType === 'ai_call'" 
                         class="w-2 h-2 bg-white rounded-full mx-auto mt-0.5"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tags -->
      <FormControl
        label="Tag"
        v-model="formData.tags"
        type="text"
        :placeholder="__('Search or enter new Tag')"
      />

      </form>
    </template>
    

    <template #actions>
      <div class="flex justify-between w-full">
        <Button variant="outline" theme="gray" @click="$emit('close')">
          {{ __('Cancel') }}
        </Button>
        <Button
          variant="solid"
          theme="gray"
          @click="handleSubmit"
          :loading="loading"
        >
        <div class="flex items-center">
          {{ __('Continue') }}
          <FeatherIcon name="arrow-right" class="w-4 h-4 ml-2" />
        </div>
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Dialog, Button, FeatherIcon, FormControl } from 'frappe-ui'
import { useSequenceStore } from '@/stores/sequence'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'success'])
const router = useRouter()
const sequenceStore = useSequenceStore()
const toast = useToast()

// Form data
const formData = ref({
  title: '',
  messageType: '',
  tags: ''
})

// Computed
const loading = computed(() => sequenceStore.loading)

// Methods
const selectMessageType = (type) => {
  formData.value.messageType = type
}

const createFirstStep = () => {
  const stepMapping = {
    'messenger': {
      step_order: 1,
      delay_from_previous: '0 minutes',
      channel: 'Messenger',
      template_id: '',
      action_if_replied: 'Continue',
      related_action: ''
    },
    'email': {
      step_order: 1,
      delay_from_previous: '0 minutes',
      channel: 'Email',
      template_id: '',
      action_if_replied: 'Continue',
      related_action: ''
    },
    'zalo_oa': {
      step_order: 1,
      delay_from_previous: '0 minutes',
      channel: 'Zalo_OA',
      template_id: '',
      action_if_replied: 'Continue',
      related_action: ''
    },
    'zalo_zns': {
      step_order: 1,
      delay_from_previous: '0 minutes',
      channel: 'Zalo_ZNS',
      template_id: '',
      action_if_replied: 'Continue',
      related_action: ''
    },
    'sms': {
      step_order: 1,
      delay_from_previous: '0 minutes',
      channel: 'SMS',
      template_id: '',
      action_if_replied: 'Continue',
      related_action: ''
    },
    'ai_call': {
      step_order: 1,
      delay_from_previous: '0 minutes',
      channel: 'AI_Call',
      template_id: '',
      action_if_replied: 'Continue',
      related_action: ''
    }
  }
  
  return stepMapping[formData.value.messageType] || stepMapping['email']
}

const handleSubmit = async () => {
  if (!formData.value.title.trim() || !formData.value.messageType) {
    toast.error(__('Please fill in all required fields'))
    return
  }
  
  try {
    // Create first step
    const firstStep = createFirstStep()
    
    // Prepare sequence data
    const sequenceData = {
      title: formData.value.title.trim(),
      purpose: '', // Will be filled in detail screen
      status: 'Draft',
      enrollment_source: 'Manual',
      steps: JSON.stringify([firstStep]),
      tags: formData.value.tags.trim()
    }
    
    // Create sequence
    const result = await sequenceStore.createSequence(sequenceData)
    
    console.log('Create sequence result:', result)
    
    if (result.success && result.data && result.data.name) {
      emit('success', 'Tạo sequence thành công!')
      emit('close')
      
      console.log('Navigating to sequence editor with ID:', result.data.name)
      
      // Navigate to sequence editor
      router.push({ 
        name: 'SequenceEditor', 
        params: { id: result.data.name } 
      })
    } else {
      throw new Error(result.error || 'Có lỗi xảy ra khi tạo sequence')
    }
  } catch (error) {
    console.error('Error creating sequence:', error)
    // Error will be handled by the store and displayed via toast
  }
}

// Reset form when modal closes
const resetForm = () => {
  formData.value = {
    title: '',
    messageType: '',
    tags: ''
  }
}

// Watch for modal close to reset form
watch(() => props.show, (newValue) => {
  if (newValue) {
    resetForm()
  }
})
</script>
