<template>
  <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
    <!-- Left: Editor -->
    <div class="space-y-4">
      <!-- Facebook Page Selector -->
      <div v-if="showPageSelector">
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Facebook Page') }}
          <span class="text-red-500">*</span>
        </label>
        <FormControl
          type="select"
          :model-value="pageId"
          :options="pageOptions"
          @update:model-value="$emit('update:pageId', $event)"
        />
      </div>

      <!-- Post Content with Rich Text Editor -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Post Content') }}
          <span v-if="required" class="text-red-500">*</span>
        </label>
        <TextEditor
          ref="contentEditor"
          :content="content"
          :placeholder="placeholder || __('Write your Facebook post content here...')"
          :editable="!readonly"
          :bubble-menu="true"
          :fixed-menu="true"
          editor-class="min-h-[200px] max-h-[400px] overflow-auto prose prose-sm max-w-none p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          @change="$emit('update:content', $event)"
        />
        <div class="flex justify-between items-center mt-2">
          <p class="text-xs text-gray-500">
            {{ __('Use rich formatting, links, and mentions') }}
          </p>
          <span class="text-xs text-gray-500">
            {{ contentLength }} {{ __('characters') }}
          </span>
        </div>
      </div>

      <!-- Image Upload -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Post Image/Video') }}
          <span v-if="!required" class="text-gray-500 text-xs">({{ __('Optional') }})</span>
        </label>
        
        <!-- Image Preview -->
        <div v-if="image" class="relative mb-3">
          <img
            :src="image"
            alt="Post image"
            class="w-full h-64 object-cover rounded-lg border border-gray-200"
          />
          <button
            v-if="!readonly"
            @click="$emit('update:image', null)"
            class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-2 hover:bg-red-600 shadow-lg"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </button>
        </div>

        <!-- Upload Button -->
        <FileUploader
          v-if="!image && !readonly"
          :file-types="['image/*', 'video/*']"
          @success="handleImageUpload"
        >
          <template #default="{ openFileSelector, uploading, progress }">
            <div
              @click="openFileSelector"
              class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-400 transition-colors"
            >
              <FeatherIcon name="image" class="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <p class="text-sm text-gray-600 mb-1">
                {{ uploading ? __('Uploading...') : __('Click to upload image or video') }}
              </p>
              <p class="text-xs text-gray-500">
                {{ __('JPG, PNG, GIF, MP4 up to 10MB') }}
              </p>
              <div v-if="uploading" class="mt-3">
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="bg-blue-600 h-2 rounded-full transition-all"
                    :style="{ width: `${progress}%` }"
                  ></div>
                </div>
              </div>
            </div>
          </template>
        </FileUploader>
      </div>

      <!-- Link URL (Optional) -->
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
              class="text-sm text-gray-900 prose prose-sm max-w-none"
              v-html="content"
            ></div>
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

          <!-- Link Preview (if link provided) -->
          <div v-if="link" class="border-t border-gray-200 p-3 bg-gray-50">
            <div class="flex items-center text-xs text-gray-600">
              <FeatherIcon name="link" class="h-3 w-3 mr-1" />
              <span class="truncate">{{ link }}</span>
            </div>
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
</template>

<script setup>
import { computed } from 'vue'
import { FeatherIcon, FormControl, FileUploader, TextEditor } from 'frappe-ui'

const props = defineProps({
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
  pageOptions: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  readonly: {
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
  }
})

const emit = defineEmits(['update:content', 'update:image', 'update:pageId', 'update:link'])

// Computed
const contentLength = computed(() => {
  // Strip HTML tags for character count
  const div = document.createElement('div')
  div.innerHTML = props.content || ''
  return div.textContent?.length || 0
})

const handleImageUpload = (file) => {
  emit('update:image', file.file_url)
}

// Get page name from pageId
const getPageName = (id) => {
  const page = props.pageOptions.find(p => p.value === id)
  return page ? page.label : __('Your Page Name')
}
</script>

<style scoped>
/* Add any custom styles here */
</style>
