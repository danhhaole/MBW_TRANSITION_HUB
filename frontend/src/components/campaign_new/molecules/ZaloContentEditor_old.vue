<template>
  <div>
    <!-- Header (optional, shown only if title prop is provided and showHeader is true) -->
    <div v-if="showHeader && title" class="flex items-center mb-4">
      <div class="w-8 h-8 rounded-lg bg-green-500 text-white flex items-center justify-center mr-3">
        <FeatherIcon name="message-circle" class="h-4 w-4" />
      </div>
      <h4 class="text-sm font-semibold text-gray-900">
        {{ title }}
      </h4>
    </div>

    <!-- Two Column Layout: Editor + Preview -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Left: Editor -->
      <div class="space-y-4">
      <!-- Post Content -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Post Content') }}
          <span v-if="required" class="text-red-500">*</span>
        </label>
        <FormControl
          type="textarea"
          :model-value="content"
          :placeholder="placeholder || __('Write your Zalo post content here...')"
          :rows="rows"
          @update:model-value="$emit('update:content', $event)"
        />
        <p class="text-xs text-gray-500 mt-1">
          {{ content?.length || 0 }} {{ __('characters') }}
        </p>
      </div>

      <!-- Image Upload -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Post Image') }}
          <span v-if="!required" class="text-gray-500 text-xs">({{ __('Optional') }})</span>
        </label>
        <FileUploader
          :file-types="['image/*']"
          @success="handleImageUpload"
        >
          <template #default="{ openFileSelector, uploading, progress }">
            <div
              v-if="!image"
              @click="openFileSelector"
              class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-green-400 transition-colors"
            >
              <FeatherIcon name="image" class="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <p class="text-sm text-gray-600">
                {{ uploading ? `${__('Uploading')}... ${progress}%` : __('Click to upload image') }}
              </p>
              <p class="text-xs text-gray-500 mt-1">
                {{ __('PNG, JPG, GIF up to 10MB') }}
              </p>
            </div>
            <div v-else class="relative">
              <img :src="image" class="w-full h-48 object-cover rounded-lg" alt="Preview" />
              <button
                @click.stop="$emit('update:image', null)"
                class="absolute top-2 right-2 p-1.5 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors shadow-lg"
                :title="__('Remove image')"
              >
                <FeatherIcon name="x" class="h-4 w-4" />
              </button>
            </div>
          </template>
        </FileUploader>
      </div>

      <!-- Zalo OA Selection (Optional) -->
      <div v-if="showOASelector">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Select Zalo OA') }}
          <span v-if="required" class="text-red-500">*</span>
        </label>
        <FormControl
          type="select"
          :model-value="oaId"
          :options="oaOptions"
          :placeholder="__('Choose a Zalo Official Account...')"
          @update:model-value="$emit('update:oaId', $event)"
        />
        <p v-if="!oaId && showError" class="text-xs text-red-600 mt-1">
          {{ __('Please select a Zalo OA') }}
        </p>
      </div>

      <!-- Link/CTA (Optional) -->
      <div v-if="showLinkInput">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Link URL') }}
          <span class="text-gray-500 text-xs">({{ __('Optional') }})</span>
        </label>
        <FormControl
          type="text"
          :model-value="link"
          :placeholder="__('https://example.com/job-opening')"
          @update:model-value="$emit('update:link', $event)"
        />
      </div>

      <!-- Message Type (for ZNS) -->
      <div v-if="showMessageType">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Message Type') }}
        </label>
        <FormControl
          type="select"
          :model-value="messageType"
          :options="messageTypeOptions"
          @update:model-value="$emit('update:messageType', $event)"
        />
      </div>
    </div>

    <!-- Right: Preview -->
    <div class="space-y-4">
      <div class="sticky top-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Preview') }}
        </label>
        
        <!-- Zalo Message Preview Card -->
        <div class="border border-gray-300 rounded-lg bg-white shadow-sm overflow-hidden">
          <!-- Chat Header -->
          <div class="bg-gradient-to-r from-blue-500 to-blue-600 p-4 text-white">
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center mr-3">
                <FeatherIcon name="message-circle" class="h-5 w-5" />
              </div>
              <div class="flex-1">
                <div class="text-sm font-semibold">
                  {{ oaId ? getOAName(oaId) : __('Your Zalo OA') }}
                </div>
                <div class="text-xs opacity-90">
                  {{ __('Online') }}
                </div>
              </div>
            </div>
          </div>

          <!-- Chat Content -->
          <div class="p-4 bg-gray-50 min-h-[200px]">
            <!-- Message Bubble -->
            <div class="flex justify-start">
              <div class="max-w-[80%]">
                <!-- Text Content -->
                <div 
                  v-if="content"
                  class="bg-white rounded-2xl rounded-tl-sm p-3 shadow-sm"
                >
                  <div class="text-sm text-gray-900 whitespace-pre-wrap break-words">
                    {{ content }}
                  </div>
                </div>
                <div v-else class="bg-white rounded-2xl rounded-tl-sm p-3 shadow-sm">
                  <div class="text-sm text-gray-400 italic">
                    {{ __('Your message will appear here...') }}
                  </div>
                </div>

                <!-- Image -->
                <div v-if="image" class="mt-2">
                  <img 
                    :src="image" 
                    alt="Message image" 
                    class="rounded-lg max-w-full max-h-64 object-cover shadow-sm"
                  />
                </div>

                <!-- Timestamp -->
                <div class="text-xs text-gray-500 mt-1 ml-2">
                  {{ __('Just now') }}
                </div>
              </div>
            </div>
          </div>

          <!-- Chat Actions -->
          <div class="border-t border-gray-200 p-3 bg-white">
            <div class="flex items-center space-x-2">
              <button class="p-2 rounded-full hover:bg-gray-100 transition-colors">
                <FeatherIcon name="smile" class="h-5 w-5 text-gray-600" />
              </button>
              <div class="flex-1 bg-gray-100 rounded-full px-4 py-2 text-sm text-gray-500">
                {{ __('Type a message...') }}
              </div>
              <button class="p-2 rounded-full hover:bg-gray-100 transition-colors">
                <FeatherIcon name="send" class="h-5 w-5 text-blue-600" />
              </button>
            </div>
          </div>
        </div>

        <!-- Preview Note -->
        <p class="text-xs text-gray-500 mt-2 text-center">
          {{ __('This is a preview. Actual message may vary.') }}
        </p>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { FeatherIcon, FormControl, FileUploader } from 'frappe-ui'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  showHeader: {
    type: Boolean,
    default: false
  },
  content: {
    type: String,
    default: ''
  },
  image: {
    type: String,
    default: null
  },
  oaId: {
    type: String,
    default: null
  },
  link: {
    type: String,
    default: ''
  },
  messageType: {
    type: String,
    default: 'text'
  },
  placeholder: {
    type: String,
    default: ''
  },
  rows: {
    type: Number,
    default: 6
  },
  required: {
    type: Boolean,
    default: false
  },
  showOASelector: {
    type: Boolean,
    default: false
  },
  showLinkInput: {
    type: Boolean,
    default: false
  },
  showMessageType: {
    type: Boolean,
    default: false
  },
  oaOptions: {
    type: Array,
    default: () => [
      { label: 'Company Zalo OA - Main', value: 'oa_1' },
      { label: 'Company Zalo OA - HR', value: 'oa_2' }
    ]
  },
  messageTypeOptions: {
    type: Array,
    default: () => [
      { label: 'Text Message', value: 'text' },
      { label: 'ZNS Template', value: 'zns' },
      { label: 'Care Message', value: 'care' }
    ]
  },
  showError: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:content', 'update:image', 'update:oaId', 'update:link', 'update:messageType'])

const handleImageUpload = (file) => {
  emit('update:image', file.file_url)
}

// Get OA name from oaId
const getOAName = (id) => {
  const oa = props.oaOptions.find(o => o.value === id)
  return oa ? oa.label : __('Your Zalo OA')
}

// Translation helper
const __ = (text) => text
</script>

<style scoped>
/* Add any custom styles here */
</style>
