<template>
  <div class="zalo-care-editor space-y-6">
    <!-- Header -->
    <div class="text-center py-4">
      <div class="bg-pink-100 p-3 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
        <FeatherIcon name="heart" class="h-8 w-8 text-pink-600" />
      </div>
      <h3 class="text-xl font-bold text-gray-900 mb-2">{{ __("Zalo Care Editor") }}</h3>
      <p class="text-gray-600">{{ __("Create Zalo Care message with image and action buttons") }}</p>
    </div>

    <!-- Message Preview -->
    <div class="bg-gradient-to-r from-pink-50 to-rose-50 rounded-lg p-6 border border-pink-200">
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-lg font-semibold text-gray-900">{{ __("Message Preview") }}</h4>
        <button 
          @click="showPreview = !showPreview"
          class="text-pink-600 hover:text-pink-800 text-sm font-medium"
        >
          {{ showPreview ? __("Hide Preview") : __("Show Preview") }}
        </button>
      </div>
      
      <div v-if="showPreview" class="bg-white rounded-lg shadow-sm border p-4 max-w-sm">
        <!-- Image preview -->
        <div v-if="localContent.image_url" class="mb-3">
          <img 
            :src="localContent.image_url" 
            :alt="__('Message image')"
            class="w-full h-32 object-cover rounded-lg"
            @error="handleImageError"
          />
        </div>
        <div v-else class="bg-gray-100 h-32 rounded-lg mb-3 flex items-center justify-center">
          <FeatherIcon name="image" class="h-8 w-8 text-gray-400" />
        </div>
        
        <!-- Message bubble -->
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

    <!-- Image Upload -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ __("Message Image") }}
      </label>
      
      <div class="border-2 border-dashed border-gray-300 rounded-lg p-6">
        <div v-if="localContent.image_url" class="text-center">
          <img 
            :src="localContent.image_url" 
            :alt="__('Uploaded image')"
            class="mx-auto h-32 w-auto rounded-lg mb-4"
            @error="handleImageError"
          />
          <div class="flex justify-center space-x-2">
            <button
              v-if="!readonly"
              @click="changeImage"
              class="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
            >
              {{ __("Change Image") }}
            </button>
            <button
              v-if="!readonly"
              @click="removeImage"
              class="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
            >
              {{ __("Remove") }}
            </button>
          </div>
        </div>
        
        <div v-else class="text-center">
          <FeatherIcon name="image" class="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <div class="space-y-2">
            <input
              v-if="!readonly"
              ref="fileInput"
              type="file"
              accept="image/*"
              @change="handleFileUpload"
              class="hidden"
            />
            <button
              v-if="!readonly"
              @click="$refs.fileInput?.click()"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              {{ __("Upload Image") }}
            </button>
            <p class="text-xs text-gray-500">{{ __("Or enter image URL below") }}</p>
            <input
              v-model="localContent.image_url"
              type="url"
              :placeholder="__('https://example.com/image.jpg')"
              :disabled="readonly"
              class="block w-full px-3 py-2 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-pink-500"
            />
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
        :placeholder="carePlaceholder"
        :disabled="readonly"
        :maxlength="640"
        class="block w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500"
        :class="{ 'bg-gray-100 cursor-not-allowed': readonly }"
      />
      <div class="flex justify-between items-center mt-2">
        <p class="text-xs text-gray-500">
          {{ __("Keep message concise and caring") }}
        </p>
        <span class="text-xs" :class="characterCountClass">
          {{ (localContent.message_content?.length || 0) }}/640 {{ __("characters") }}
        </span>
      </div>
    </div>

    <!-- Action Buttons (same as ZNS) -->
    <div>
      <div class="flex items-center justify-between mb-4">
        <label class="block text-sm font-medium text-gray-700">
          {{ __("Action Buttons") }}
        </label>
        <button
          v-if="!readonly && localContent.action_buttons.length < 3"
          @click="addActionButton"
          class="px-3 py-1 text-sm bg-pink-100 text-pink-700 rounded hover:bg-pink-200"
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
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __("Button Title") }}
              </label>
              <input
                v-model="button.title"
                type="text"
                :placeholder="__('Button text')"
                :disabled="readonly"
                class="block w-full px-3 py-2 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-pink-500"
              />
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ __("Action Type") }}
              </label>
              <select
                v-model="button.type"
                :disabled="readonly"
                class="block w-full px-3 py-2 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-pink-500"
              >
                <option value="url">{{ __("Open Link") }}</option>
                <option value="phone">{{ __("Call Phone") }}</option>
                <option value="flow">{{ __("Start Flow") }}</option>
              </select>
            </div>

            <div class="md:col-span-2">
              <label class="block text-xs font-medium text-gray-700 mb-1">
                {{ getActionLabel(button.type) }}
              </label>
              <input
                v-model="button.value"
                type="text"
                :placeholder="getActionPlaceholder(button.type)"
                :disabled="readonly"
                class="block w-full px-3 py-2 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-pink-500"
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
        class="px-6 py-2 bg-pink-600 text-white rounded-lg hover:bg-pink-700"
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
  image_url: '',
  action_buttons: [],
  ...props.content
})

const showPreview = ref(false)
const fileInput = ref(null)

const __ = (text) => text

const carePlaceholder = `Hi there! 👋

We hope you're doing well. We have some exciting career opportunities that might interest you.

Would you like to explore new possibilities with us?`

const characterCountClass = computed(() => {
  const length = localContent.value.message_content?.length || 0
  if (length > 600) return 'text-red-500'
  if (length > 500) return 'text-yellow-500'
  return 'text-gray-500'
})

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // In a real app, you would upload to a server
  // For now, create a local URL for preview
  const reader = new FileReader()
  reader.onload = (e) => {
    localContent.value.image_url = e.target.result
  }
  reader.readAsDataURL(file)
}

const handleImageError = () => {
  console.warn('Failed to load image:', localContent.value.image_url)
}

const changeImage = () => {
  fileInput.value?.click()
}

const removeImage = () => {
  localContent.value.image_url = ''
}

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
