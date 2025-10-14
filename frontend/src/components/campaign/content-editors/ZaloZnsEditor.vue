<template>
  <div class="zalo-zns-editor space-y-6">
    <!-- Header -->
    <div class="text-center py-4">
      <div class="bg-green-100 p-3 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
        <FeatherIcon name="message-circle" class="h-8 w-8 text-green-600" />
      </div>
      <h3 class="text-xl font-bold text-gray-900 mb-2">{{ __("Zalo ZNS Editor") }}</h3>
      <p class="text-gray-600">{{ __("Create Zalo ZNS message with action buttons") }}</p>
    </div>

    <!-- Message Preview -->
    <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-6 border border-green-200">
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-lg font-semibold text-gray-900">{{ __("Message Preview") }}</h4>
        <button 
          @click="showPreview = !showPreview"
          class="text-green-600 hover:text-green-800 text-sm font-medium"
        >
          {{ showPreview ? __("Hide Preview") : __("Show Preview") }}
        </button>
      </div>
      
      <div v-if="showPreview" class="bg-white rounded-lg shadow-sm border p-4 max-w-sm">
        <!-- Zalo message bubble -->
        <div class="bg-blue-500 text-white rounded-lg p-3 mb-3">
          <div class="text-sm whitespace-pre-wrap">{{ localContent.message_content || __("No message content yet...") }}</div>
        </div>
        
        <!-- Action buttons -->
        <div v-if="localContent.action_buttons?.length" class="space-y-2">
          <div
            v-for="(button, index) in localContent.action_buttons"
            :key="index"
            class="border border-blue-500 text-blue-500 rounded-lg p-2 text-center text-sm"
          >
            {{ button.title }}
          </div>
        </div>
      </div>
    </div>

    <!-- Message Content -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ __("Message Content") }} <span class="text-red-500">*</span>
      </label>
      <textarea
        v-model="localContent.message_content"
        rows="6"
        :placeholder="znsPlaceholder"
        :disabled="readonly"
        :maxlength="640"
        class="block w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
        :class="{ 'bg-gray-100 cursor-not-allowed': readonly }"
      />
      <div class="flex justify-between items-center mt-2">
        <p class="text-xs text-gray-500">
          {{ __("Keep message concise and clear") }}
        </p>
        <span class="text-xs" :class="characterCountClass">
          {{ (localContent.message_content?.length || 0) }}/640 {{ __("characters") }}
        </span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div>
      <div class="flex items-center justify-between mb-4">
        <label class="block text-sm font-medium text-gray-700">
          {{ __("Action Buttons") }}
        </label>
        <button
          v-if="!readonly && localContent.action_buttons.length < 3"
          @click="addActionButton"
          class="px-3 py-1 text-sm bg-green-100 text-green-700 rounded hover:bg-green-200"
        >
          <FeatherIcon name="plus" class="h-4 w-4 inline mr-1" />
          {{ __("Add Button") }}
        </button>
      </div>

      <div class="space-y-3">
        <div
          v-for="(button, index) in localContent.action_buttons"
          :key="index"
          class="border border-gray-200 rounded-lg p-4"
        >
          <div class="flex items-center justify-between mb-3">
            <h5 class="text-sm font-medium text-gray-900">{{ __("Button") }} {{ index + 1 }}</h5>
            <button
              v-if="!readonly"
              @click="removeActionButton(index)"
              class="text-red-500 hover:text-red-700"
            >
              <FeatherIcon name="trash-2" class="h-4 w-4" />
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Button Title -->
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __("Button Title") }}
              </label>
              <input
                v-model="button.title"
                type="text"
                :placeholder="__('Button text')"
                :disabled="readonly"
                class="block w-full px-3 py-2 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-green-500"
              />
            </div>

            <!-- Action Type -->
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __("Action Type") }}
              </label>
              <select
                v-model="button.type"
                :disabled="readonly"
                class="block w-full px-3 py-2 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-green-500"
              >
                <option value="url">{{ __("Open Link") }}</option>
                <option value="phone">{{ __("Call Phone") }}</option>
                <option value="flow">{{ __("Start Flow") }}</option>
              </select>
            </div>

            <!-- Action Value -->
            <div class="md:col-span-2">
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ getActionLabel(button.type) }}
              </label>
              <input
                v-model="button.value"
                type="text"
                :placeholder="getActionPlaceholder(button.type)"
                :disabled="readonly"
                class="block w-full px-3 py-2 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-green-500"
              />
            </div>
          </div>
        </div>

        <div v-if="localContent.action_buttons.length === 0" class="text-center py-8 text-gray-500">
          <FeatherIcon name="mouse-pointer" class="h-8 w-8 mx-auto mb-2" />
          <p>{{ __("No action buttons yet") }}</p>
          <p class="text-xs">{{ __("Add buttons to make your message interactive") }}</p>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div v-if="!readonly" class="flex justify-between items-center pt-6 border-t">
      <button
        @click="$emit('preview')"
        class="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
      >
        <FeatherIcon name="eye" class="h-4 w-4 inline mr-2" />
        {{ __("Preview Message") }}
      </button>
      
      <button
        @click="$emit('save')"
        class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
      >
        <FeatherIcon name="save" class="h-4 w-4 inline mr-2" />
        {{ __("Save Content") }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  content: { type: Object, default: () => ({}) },
  readonly: { type: Boolean, default: false }
})

const emit = defineEmits(['update:content', 'save', 'preview'])

const localContent = ref({
  message_content: '',
  action_buttons: [],
  ...props.content
})

const showPreview = ref(false)

const __ = (text) => text

const znsPlaceholder = `Hello! We have an exciting job opportunity that matches your profile.

Position: Senior Developer
Company: Tech Company
Location: Ho Chi Minh City

Would you like to learn more about this opportunity?`

const characterCountClass = computed(() => {
  const length = localContent.value.message_content?.length || 0
  if (length > 600) return 'text-red-500'
  if (length > 500) return 'text-yellow-500'
  return 'text-gray-500'
})

const addActionButton = () => {
  if (localContent.value.action_buttons.length >= 3) return
  
  localContent.value.action_buttons.push({
    title: '',
    type: 'url',
    value: ''
  })
}

const removeActionButton = (index) => {
  localContent.value.action_buttons.splice(index, 1)
}

const getActionLabel = (type) => {
  switch (type) {
    case 'url': return __('URL Link')
    case 'phone': return __('Phone Number')
    case 'flow': return __('Flow Name')
    default: return __('Action Value')
  }
}

const getActionPlaceholder = (type) => {
  switch (type) {
    case 'url': return 'https://example.com'
    case 'phone': return '+84901234567'
    case 'flow': return 'recruitment_flow'
    default: return ''
  }
}

watch(localContent, (newContent) => {
  emit('update:content', newContent)
}, { deep: true })

watch(() => props.content, (newContent) => {
  localContent.value = { ...localContent.value, ...newContent }
}, { deep: true })
</script>
