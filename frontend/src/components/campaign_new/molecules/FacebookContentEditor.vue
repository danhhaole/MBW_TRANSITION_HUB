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

        <!-- Short Link Input Field (similar to Zalo) -->
        <div v-if="shortLink !== undefined" class="mt-4 space-y-2">
          <label class="block text-xs font-medium text-gray-700">
            {{ __('Short Link') }}
          </label>
          <div class="flex space-x-2">
            <input
              v-model="shortLink"
              :placeholder="__('https://is.gd/...')"
              type="url"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-blue-500 focus:border-blue-500"
              @input="updateShortLink"
            />
            <button
              @click="removeShortLink"
              class="text-red-500 hover:text-red-700 p-2"
            >
              <FeatherIcon name="x" class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Add Short Link Button (similar to Zalo) -->
        <div v-if="shortLink === undefined && sharePageData?.url" class="mt-4">
          <button
            @click="addShortLink"
            class="inline-flex items-center px-3 py-1 border border-gray-300 rounded-md text-xs font-medium text-gray-700 bg-white hover:bg-gray-50"
            :disabled="generatingShortLink"
          >
            <FeatherIcon name="link" class="w-3 h-3 mr-1" />
            {{ generatingShortLink ? __('Generating...') : __('Add Short Link') }}
          </button>
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
import { ref, computed, watch } from 'vue'
import { FeatherIcon, FormControl, FileUploader, TextEditor, Button, call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'

const toast = useToast()

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
  },
  sharePageData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:content', 'update:image', 'update:pageId', 'update:link'])

// Short link state (similar to Zalo)
const shortLink = ref(undefined)

// Short link generation state
const generatingShortLink = ref(false)

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

// Generate short URL using backend API (same as ZaloContentEditor)
const generateShortUrl = async (longUrl) => {
  if (!longUrl) return ''

  try {
    const result = await call('mbw_mira.mbw_mira.doctype.mira_short_url.mira_short_url.create_short_url_with_gdshortener', {
      long_url: longUrl
    })

    if (result && result.success && result.short_url) {
      const cleanShortUrl = String(result.short_url).trim().replace(/,$/, '')
      console.log('✅ Short URL created:', cleanShortUrl)
      return cleanShortUrl
    } else {
      console.error('❌ Short URL API error:', result?.message || 'Unknown error')
      toast.error(__('Error creating short URL: ') + (result?.message || 'Unknown error'))
      return ''
    }
  } catch (e) {
    console.error('❌ Error creating short URL:', e)
    toast.error(__('Failed to create short URL'))
    return ''
  }
}

// Add short link action - create input field and generate short link automatically (similar to Zalo)
const addShortLink = async () => {
  if (!props.sharePageData?.url) {
    toast.error(__('Please select a landing page first'))
    return
  }

  // Create input field first (like Zalo) - set to empty string to show input
  shortLink.value = ''
  generatingShortLink.value = true

  try {
    // Build URL with UTM parameters for Facebook
    const baseUrl = props.sharePageData.url
    const params = new URLSearchParams()
    params.append('utm_source', 'facebook')
    params.append('utm_medium', 'social')
    
    // Ưu tiên dùng campaignId cho utm_campaign nếu có, fallback về campaignName
    const utmCampaign = props.sharePageData.campaignId || props.sharePageData.campaignName
    if (utmCampaign) {
      params.append('utm_campaign', String(utmCampaign).trim())
    }

    const separator = baseUrl.includes('?') ? '&' : '?'
    const urlWithUtm = `${baseUrl}${separator}${params.toString()}`

    // Generate short link automatically (run in background)
    const generatedShortLink = await generateShortUrl(urlWithUtm)
    
    if (generatedShortLink) {
      console.log('✅ Generated short link:', generatedShortLink)
      shortLink.value = generatedShortLink
      // Also insert into content
      insertShortLinkIntoContent(generatedShortLink)
      toast.success(__('Short link generated and added'))
    } else {
      // If generation failed, keep input field visible but empty
      console.warn('⚠️ Short link generation failed, keeping input field')
    }
  } catch (error) {
    console.error('❌ Error adding short link:', error)
    toast.error(__('Failed to add short link'))
    // Keep input field visible even on error
  } finally {
    generatingShortLink.value = false
  }
}

// Insert short link into content
const insertShortLinkIntoContent = (link) => {
  const currentContent = props.content || ''
  
  // Check if content already contains this short link
  if (currentContent.includes(link)) {
    console.log('⚠️ Short link already in content, skipping insert')
    return
  }
  
  // Check if content is HTML
  const isHtml = /<[a-z][\s\S]*>/i.test(currentContent)
  
  let newContent = ''
  if (isHtml) {
    // Insert as HTML link
    const linkHtml = `<a href="${link}" target="_blank" rel="noopener noreferrer">${link}</a>`
    newContent = currentContent ? `${currentContent}<br>${linkHtml}` : linkHtml
  } else {
    // Insert as plain text with newline
    newContent = currentContent ? `${currentContent}\n${link}` : link
  }
  
  console.log('📝 Inserting short link into content:', link)
  emit('update:content', newContent)
}

// Update short link when user edits it (similar to Zalo - just update state and content)
const updateShortLink = () => {
  // When user edits short link, update content with new short link
  if (shortLink.value) {
    const currentContent = props.content || ''
    if (currentContent) {
      // Since we know the old short link was inserted, we can find and replace it
      // But simpler: just insert/update the short link
      insertShortLinkIntoContent(shortLink.value)
    } else {
      // If content is empty, just insert the short link
      insertShortLinkIntoContent(shortLink.value)
    }
  }
}

// Remove short link (similar to Zalo - just remove from state and content)
const removeShortLink = () => {
  // Remove short link from content if it exists
  if (shortLink.value) {
    const currentContent = props.content || ''
    if (currentContent && currentContent.includes(shortLink.value)) {
      // Simple string replace - remove the short link we know (from create_short_url_with_gdshortener)
      const updatedContent = currentContent.replace(shortLink.value, '').trim()
      emit('update:content', updatedContent)
    }
  }
  // Clear short link state (like Zalo)
  shortLink.value = undefined
}

// Watch for sharePageData changes to auto-update short links (similar to Zalo)
watch(() => props.sharePageData?.url, async (newUrl, oldUrl) => {
  // Only regenerate if URL actually changed and we have a short link
  if (newUrl && newUrl !== oldUrl && shortLink.value) {
    console.log('🔄 URL changed, regenerating short link:', newUrl)
    
    generatingShortLink.value = true
    
    try {
      // Build URL with UTM parameters for Facebook
      const baseUrl = newUrl
      const params = new URLSearchParams()
      params.append('utm_source', 'facebook')
      params.append('utm_medium', 'social')
      const utmCampaign = props.sharePageData?.campaignId || props.sharePageData?.campaignName
      if (utmCampaign) {
        params.append('utm_campaign', String(utmCampaign).trim())
      }

      const separator = baseUrl.includes('?') ? '&' : '?'
      const urlWithUtm = `${baseUrl}${separator}${params.toString()}`

      // Generate new short link using create_short_url_with_gdshortener
      const newShortLink = await generateShortUrl(urlWithUtm)
      
      if (newShortLink) {
        // Update short link in state (like Zalo)
        const oldShortLink = shortLink.value
        shortLink.value = newShortLink
        
        // Replace old short link in content with new one (simple string replace)
        const currentContent = props.content || ''
        if (currentContent && oldShortLink) {
          // Simple string replace - replace old short link (from create_short_url_with_gdshortener) with new one
          const updatedContent = currentContent.replace(oldShortLink, newShortLink)
          emit('update:content', updatedContent)
        }
        
        console.log('✅ Updated short link:', newShortLink)
        toast.success(__('Short link updated for new template'))
      }
    } catch (error) {
      console.error('❌ Error updating short link:', error)
      toast.error(__('Failed to update short link'))
    } finally {
      generatingShortLink.value = false
    }
  }
}, { immediate: false })

// No need to detect short link from content (like Zalo)
// Short link is managed in state only, generated via create_short_url_with_gdshortener
</script>

<style scoped>
/* Add any custom styles here */
</style>
