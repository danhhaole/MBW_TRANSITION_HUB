<template>
  <div>
    <!-- Header (optional, shown only if title prop is provided and showHeader is true) -->
    <div v-if="showHeader && title" class="flex items-center mb-4">
      <div class="w-8 h-8 rounded-lg bg-blue-500 text-white flex items-center justify-center mr-3">
        <FeatherIcon name="facebook" class="h-4 w-4" />
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
          :placeholder="placeholder || __('Write your Facebook post content here...')"
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
              class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-400 transition-colors"
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

      <!-- Facebook Page Selection -->
      <div v-if="showPageSelector">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Select Facebook Page') }}
          <span v-if="required" class="text-red-500">*</span>
        </label>
        <FormControl
          type="select"
          :model-value="pageId"
          :options="pageOptions"
          :placeholder="__('Choose a Facebook page...')"
          @update:model-value="$emit('update:pageId', $event)"
        />
        <p v-if="!pageId && showError" class="text-xs text-red-600 mt-1">
          {{ __('Please select a Facebook page') }}
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
    </div>

    <!-- Right: Preview -->
    <div class="space-y-4">
      <div class="sticky top-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Preview') }}
        </label>
        
        <!-- Facebook Post Preview Card -->
        <div class="border border-gray-300 rounded-lg bg-white shadow-sm overflow-hidden">
          <!-- Post Header -->
          <div class="p-4 border-b border-gray-200">
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                <FeatherIcon name="facebook" class="h-5 w-5 text-blue-600" />
              </div>
              <div class="flex-1">
                <div class="text-sm font-semibold text-gray-900">
                  {{ pageId ? getPageName(pageId) : __('Your Page Name') }}
                </div>
                <div class="text-xs text-gray-500">
                  {{ __('Just now') }} • <FeatherIcon name="globe" class="h-3 w-3 inline" />
                </div>
              </div>
            </div>
          </div>

          <!-- Post Content -->
          <div class="p-4">
            <div 
              v-if="content"
              class="text-sm text-gray-900 whitespace-pre-wrap break-words"
            >
              {{ content }}
            </div>
            <div v-else class="text-sm text-gray-400 italic">
              {{ __('Your post content will appear here...') }}
            </div>
          </div>

          <!-- Post Image -->
          <div v-if="image" class="border-t border-gray-200">
            <img 
              :src="image" 
              alt="Post image" 
              class="w-full object-cover max-h-96"
            />
          </div>

          <!-- Post Actions -->
          <div class="border-t border-gray-200 p-3">
            <div class="flex items-center justify-around text-gray-600">
              <button class="flex items-center space-x-2 px-3 py-2 rounded hover:bg-gray-100 transition-colors">
                <FeatherIcon name="thumbs-up" class="h-4 w-4" />
                <span class="text-sm">{{ __('Like') }}</span>
              </button>
              <button class="flex items-center space-x-2 px-3 py-2 rounded hover:bg-gray-100 transition-colors">
                <FeatherIcon name="message-circle" class="h-4 w-4" />
                <span class="text-sm">{{ __('Comment') }}</span>
              </button>
              <button class="flex items-center space-x-2 px-3 py-2 rounded hover:bg-gray-100 transition-colors">
                <FeatherIcon name="share-2" class="h-4 w-4" />
                <span class="text-sm">{{ __('Share') }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Preview Note -->
        <p class="text-xs text-gray-500 mt-2 text-center">
          {{ __('This is a preview. Actual post may vary.') }}
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
  pageId: {
    type: String,
    default: null
  },
  link: {
    type: String,
    default: ''
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
  showPageSelector: {
    type: Boolean,
    default: true
  },
  showLinkInput: {
    type: Boolean,
    default: false
  },
  pageOptions: {
    type: Array,
    default: () => [
      { label: 'Company Page - Main', value: 'page_1' },
      { label: 'Company Page - Careers', value: 'page_2' },
      { label: 'Company Page - HR', value: 'page_3' }
    ]
  },
  showError: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:content', 'update:image', 'update:pageId', 'update:link'])

const handleImageUpload = (file) => {
  emit('update:image', file.file_url)
}

// Get page name from pageId
const getPageName = (id) => {
  const page = props.pageOptions.find(p => p.value === id)
  return page ? page.label : __('Your Page Name')
}

// Translation helper
const __ = (text) => text
</script>

<style scoped>
/* Add any custom styles here */
</style>
