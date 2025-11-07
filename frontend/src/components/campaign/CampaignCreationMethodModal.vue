<template>
  <Dialog
    :options="{
      title: __('Create Campaign'),
      size: 'xl',
    }"
    v-model="show"
  >
    <template #body-content>
      <div class="">
        <p class="text-gray-600 mb-6">
          {{ __('Choose how you want to create your campaign') }}
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Manual Creation Option -->
          <div
            @click="selectMethod('manual')"
            class="group relative cursor-pointer rounded-lg border-2 p-6 transition-all hover:border-blue-500 hover:shadow-lg"
            :class="selectedMethod === 'manual' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'"
          >
            <div class="flex flex-col items-center text-center">
              <div
                class="mb-4 flex h-16 w-16 items-center justify-center rounded-full transition-colors"
                :class="selectedMethod === 'manual' ? 'bg-blue-100' : 'bg-gray-100 group-hover:bg-blue-100'"
              >
                <FeatherIcon name="edit-3" class="h-8 w-8" :class="selectedMethod === 'manual' ? 'text-blue-600' : 'text-gray-600 group-hover:text-blue-600'" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">
                {{ __('Manual Creation') }}
              </h3>
              <p class="text-sm text-gray-600">
                {{ __('Create campaign from scratch with full customization') }}
              </p>
            </div>
            
            <!-- Selected Indicator -->
            <div
              v-if="selectedMethod === 'manual'"
              class="absolute top-3 right-3"
            >
              <div class="flex h-6 w-6 items-center justify-center rounded-full bg-blue-500">
                <FeatherIcon name="check" class="h-4 w-4 text-white" />
              </div>
            </div>
          </div>

          <!-- Template Creation Option -->
          <div
            @click="selectMethod('template')"
            class="group relative cursor-pointer rounded-lg border-2 p-6 transition-all hover:border-blue-500 hover:shadow-lg"
            :class="selectedMethod === 'template' ? 'border-blue-500 bg-blue-50' : 'border-gray-200'"
          >
            <div class="flex flex-col items-center text-center">
              <div
                class="mb-4 flex h-16 w-16 items-center justify-center rounded-full transition-colors"
                :class="selectedMethod === 'template' ? 'bg-blue-100' : 'bg-gray-100 group-hover:bg-blue-100'"
              >
                <FeatherIcon name="layout" class="h-8 w-8" :class="selectedMethod === 'template' ? 'text-blue-600' : 'text-gray-600 group-hover:text-blue-600'" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">
                {{ __('From Template') }}
              </h3>
              <p class="text-sm text-gray-600">
                {{ __('Start with a pre-built template and customize as needed') }}
              </p>
            </div>
            
            <!-- Selected Indicator -->
            <div
              v-if="selectedMethod === 'template'"
              class="absolute top-3 right-3"
            >
              <div class="flex h-6 w-6 items-center justify-center rounded-full bg-blue-500">
                <FeatherIcon name="check" class="h-4 w-4 text-white" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end space-x-3">
        <Button variant="outline" @click="handleCancel">
          {{ __('Cancel') }}
        </Button>
        <Button
          variant="solid"
          theme="gray"
          @click="handleContinue"
          :disabled="!selectedMethod"
        >
          {{ __('Continue') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Dialog, Button, FeatherIcon } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'select'])

const show = ref(props.modelValue)
const selectedMethod = ref(null)

// Translation helper
const __ = (text) => text

watch(() => props.modelValue, (newVal) => {
  show.value = newVal
  if (newVal) {
    // Reset selection when modal opens
    selectedMethod.value = null
  }
})

watch(show, (newVal) => {
  emit('update:modelValue', newVal)
})

const selectMethod = (method) => {
  selectedMethod.value = method
}

const handleContinue = () => {
  if (selectedMethod.value) {
    emit('select', selectedMethod.value)
    show.value = false
  }
}

const handleCancel = () => {
  show.value = false
  selectedMethod.value = null
}
</script>
