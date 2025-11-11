<template>
  <div class="bg-gray-50 rounded-lg p-6">
    <div class="text-center mb-6">
      <h4 class="text-lg font-semibold mb-2 text-gray-900">
        {{ title }}
      </h4>
      <p class="text-sm text-gray-600">
        {{ description }}
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div
        v-for="channel in channels"
        :key="channel.value"
        class="border rounded-lg p-4 transition-all duration-200"
        :class="[
          modelValue === channel.value
            ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
            : 'border-gray-200',
          disabled
            ? 'cursor-not-allowed opacity-60'
            : 'cursor-pointer hover:border-gray-300 hover:shadow-md'
        ]"
        @click="selectChannel(channel.value)"
      >
        <div class="text-center">
          <div
            class="flex items-center justify-center w-12 h-12 rounded-full mx-auto mb-3"
            :class="
              modelValue === channel.value
                ? 'bg-blue-100 text-blue-600'
                : 'bg-gray-100 text-gray-400'
            "
          >
            <FeatherIcon :name="channel.icon" class="h-6 w-6" />
          </div>
          <h5
            class="text-sm font-semibold mb-1"
            :class="
              modelValue === channel.value
                ? 'text-blue-900'
                : 'text-gray-900'
            "
          >
            {{ channel.title }}
          </h5>
          <p class="text-xs text-gray-600">
            {{ channel.description }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: 'Select Channel'
  },
  description: {
    type: String,
    default: 'Choose the channel you want to use'
  },
  channels: {
    type: Array,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const selectChannel = (value) => {
  if (!props.disabled) {
    emit('update:modelValue', value)
  }
}
</script>
