<template>
  <div class="share-config-dialog">
    <div class="space-y-6">
      <!-- Platform info -->
      <div class="flex items-center p-4 bg-gray-50 rounded-lg border border-gray-200">
        <FeatherIcon 
          :name="getPlatformIcon(connection.platform_type)" 
          class="w-8 h-8 mr-3"
          :class="getPlatformColor(connection.platform_type)"
        />
        <div class="flex-1">
          <h4 class="font-semibold text-gray-900 text-base">{{ getPlatformName(connection.platform_type) }}</h4>
          <p class="text-sm text-gray-600 mt-1">{{ getConnectionDisplayName() }}</p>
        </div>
      </div>

      <!-- Job info preview -->
      <div class="border border-gray-200 rounded-lg p-4 bg-white shadow-sm">
        <h5 class="font-semibold text-gray-900 mb-3">{{ __('Job Information') }}</h5>
        <div class="space-y-3">
          <div>
            <label class="text-sm font-medium text-gray-700 block mb-1">{{ __('Title:') }}</label>
            <p class="text-sm text-gray-900 font-medium">{{ job.title || job.job_title || __('Untitled Job') }}</p>
          </div>
          <div v-if="job.description">
            <label class="text-sm font-medium text-gray-700 block mb-1">{{ __('Description:') }}</label>
            <p class="text-sm text-gray-600 line-clamp-3 leading-relaxed">{{ truncateText(job.description, 200) }}</p>
          </div>
          <div v-if="job.location">
            <label class="text-sm font-medium text-gray-700 block mb-1">{{ __('Location:') }}</label>
            <p class="text-sm text-gray-600">{{ job.location }}</p>
          </div>
          <div v-if="jobUrl">
            <label class="text-sm font-medium text-gray-700 block mb-1">{{ __('Application URL:') }}</label>
            <p class="text-sm text-blue-600 break-all font-mono">{{ jobUrl }}</p>
          </div>
        </div>
      </div>

      <!-- Media attachments -->
      <div v-if="jobImageUrl || shareConfig.custom_image_url" class="border border-gray-200 rounded-lg p-4 bg-white shadow-sm">
        <h5 class="font-semibold text-gray-900 mb-4">{{ __('Media Attachment') }}</h5>
        
        <div class="space-y-4">
          <!-- Image preview -->
          <div v-if="getEffectiveImageUrl()" class="relative">
            <img 
              :src="getEffectiveImageUrl()" 
              :alt="job.title || __('Job posting image')"
              class="w-full h-48 object-cover rounded-lg border border-gray-200 shadow-sm"
              @error="handleImageError"
            />
            <div class="absolute top-2 right-2">
              <Button
                size="sm"
                variant="ghost"
                class="bg-white/80 hover:bg-white shadow-sm"
                @click="clearCustomImage"
              >
                <FeatherIcon name="x" class="w-4 h-4" />
              </Button>
            </div>
          </div>

          <!-- Custom image URL input with upload -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Custom Image URL') }}
            </label>
            <div class="space-y-3">
              <!-- URL Input -->
              <input
                v-model="shareConfig.custom_image_url"
                type="url"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm font-mono"
                placeholder="https://example.com/image.jpg"
              />
              
              <!-- Image Uploader Component -->
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">{{ __('Or upload an image:') }}</span>
                <ImageUploader
                  :image_url="shareConfig.custom_image_url"
                  :image_type="'image/*'"
                  @upload="handleImageUpload"
                  @remove="handleImageRemove"
                />
              </div>
            </div>
            <p class="text-xs text-gray-500 mt-2 leading-relaxed">
              {{ __('You can paste an image URL or upload a new image. Leave empty to use the default job image.') }}
            </p>
          </div>

          <!-- Image options -->
          <div class="flex flex-wrap items-center gap-4 pt-2">
            <div class="flex items-center gap-2">
              <input
                id="use-default-image"
                v-model="shareConfig.use_default_image"
                type="checkbox"
                class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              >
              <label for="use-default-image" class="text-sm text-gray-700 font-medium">
                {{ __('Use default job image') }}
              </label>
            </div>
            
            <div class="flex items-center gap-2" v-if="connection.platform_type === 'Facebook'">
              <input
                id="include-link-preview"
                v-model="shareConfig.include_link_preview"
                type="checkbox"
                class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              >
              <label for="include-link-preview" class="text-sm text-gray-700 font-medium">
                {{ __('Include link preview') }}
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Share configuration form -->
      <div class="space-y-5">
        <!-- Custom message -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __('Post Message') }} <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="shareConfig.message"
            rows="8"
            class="w-full px-3 py-3 border border-gray-300 rounded-md resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm leading-relaxed"
            :placeholder="getMessagePlaceholder()"
            required
          />
          <div class="flex justify-between items-center mt-2">
            <span 
              :class="[
                'text-xs font-medium',
                shareConfig.message.length > getMaxMessageLength() ? 'text-red-500' : 'text-gray-500'
              ]"
            >
              {{ shareConfig.message.length.toLocaleString() }}/{{ getMaxMessageLength().toLocaleString() }} {{ __('characters') }}
            </span>
            <Button 
              variant="ghost"
              size="sm"
              @click="useTemplate"
              class="text-blue-600 hover:text-blue-700 font-medium"
            >
              {{ __('Use template') }}
            </Button>
          </div>
        </div>

        <!-- Platform-specific options -->
        <div class="space-y-4">
          <!-- Facebook specific -->
          <div v-if="connection.platform_type === 'Facebook'" class="space-y-4">
            <div v-if="getConnectedAccounts('Page').length > 0">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Target Page') }} <span class="text-red-500">*</span>
              </label>
              <select
                v-model="shareConfig.target_page_id"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                required
              >
                <option value="">{{ __('Select a page') }}</option>
                <option 
                  v-for="page in getConnectedAccounts('Page')" 
                  :key="page.external_account_id" 
                  :value="page.external_account_id"
                  class="py-2"
                >
                  {{ page.account_name }}
                </option>
              </select>
            </div>
            
            <div v-else class="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div class="flex items-start gap-3">
                <FeatherIcon name="alert-triangle" class="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                <div class="text-sm text-yellow-800">
                  <p class="font-semibold mb-1">{{ __('No Facebook Pages Found') }}</p>
                  <p class="leading-relaxed">{{ __('Please ensure your Facebook connection has active pages to post to.') }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Zalo OA specific -->
          <div v-if="connection.platform_type === 'Zalo'" class="space-y-4">
            <div v-if="getConnectedAccounts('OA').length > 0">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Target OA') }}
              </label>
              <select
                v-model="shareConfig.target_oa_id"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              >
                <option 
                  v-for="oa in getConnectedAccounts('OA')" 
                  :key="oa.external_account_id" 
                  :value="oa.external_account_id"
                  class="py-2"
                >
                  {{ oa.account_name }}
                </option>
              </select>
            </div>

            <div class="flex items-center gap-2">
              <input
                id="zalo-broadcast"
                v-model="shareConfig.broadcast_to_followers"
                type="checkbox"
                class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              >
              <label for="zalo-broadcast" class="text-sm text-gray-700 font-medium">
                {{ __('Broadcast to all followers') }}
              </label>
            </div>
          </div>

          <!-- Generic platform options -->
          <div v-if="!['Facebook', 'Zalo'].includes(connection.platform_type)" class="space-y-4">
            <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div class="flex items-start gap-3">
                <FeatherIcon name="info" class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <div class="text-sm text-blue-800">
                  <p class="font-semibold mb-1">{{ getPlatformName(connection.platform_type) }} {{ __('Integration') }}</p>
                  <p class="leading-relaxed">{{ __('Job will be posted to your connected') }} {{ getPlatformName(connection.platform_type) }} {{ __('account.') }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Schedule options -->
        <div class="space-y-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <h6 class="font-semibold text-gray-900">{{ __('Schedule Options') }}</h6>
          
          <div class="space-y-3">
            <div class="flex items-center gap-2">
              <input
                id="share-now"
                v-model="shareConfig.schedule_type"
                type="radio"
                value="now"
                class="text-blue-600 focus:ring-blue-500"
              >
              <label for="share-now" class="text-sm text-gray-700 font-medium">
                {{ __('Post now') }}
              </label>
            </div>

            <div class="flex items-center gap-2">
              <input
                id="share-later"
                v-model="shareConfig.schedule_type"
                type="radio"
                value="later"
                class="text-blue-600 focus:ring-blue-500"
              >
              <label for="share-later" class="text-sm text-gray-700 font-medium">
                {{ __('Schedule for later') }}
              </label>
            </div>

            <div v-if="shareConfig.schedule_type === 'later'" class="ml-6">
              <input
                v-model="shareConfig.scheduled_time"
                type="datetime-local"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                :min="getMinDateTime()"
                required
              >
            </div>
          </div>
        </div>

        <!-- Preview -->
        <div v-if="shareConfig.message.trim()" class="space-y-3 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <h6 class="font-semibold text-gray-900">{{ __('Preview') }}</h6>
          <div class="preview-content">
            <div class="text-sm text-gray-700 whitespace-pre-line mb-4 leading-relaxed bg-white p-3 rounded border">{{ shareConfig.message }}</div>
            
            <!-- Link preview simulation for Facebook -->
            <div v-if="connection.platform_type === 'Facebook' && shareConfig.include_link_preview && jobUrl" 
                 class="border border-gray-200 rounded-lg overflow-hidden bg-white shadow-sm">
              <img 
                v-if="getEffectiveImageUrl()"
                :src="getEffectiveImageUrl()" 
                :alt="job.title"
                class="w-full h-40 object-cover"
                @error="handleImageError"
              />
              <div class="p-4">
                <h6 class="font-semibold text-gray-900 text-sm mb-1">{{ job.title }}</h6>
                <p class="text-xs text-gray-600 mb-2 leading-relaxed">{{ truncateText(job.description, 100) }}</p>
                <p class="text-xs text-gray-500 font-mono">{{ jobUrl }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex justify-end gap-3 pt-6 border-t border-gray-200">
      <Button
        variant="ghost"
        @click="$emit('cancel')"
        class="font-medium"
      >
        {{ __('Cancel')}}
      </Button>
      
      <Button
        variant="solid"
        @click="handleSubmit"
        :loading="props.isSubmitting"
        :disabled="!isValid"
        class="font-semibold min-w-[120px]"
      >
        <template v-if="props.isSubmitting" #prefix>
          <FeatherIcon name="loader" class="w-4 h-4 mr-2 animate-spin" />
          {{ shareConfig.schedule_type === 'now' ? __('Posting...') : __('Scheduling...') }}
        </template>
        <template v-else #prefix>
          <FeatherIcon 
            :name="shareConfig.schedule_type === 'now' ? 'send' : 'clock'" 
            class="w-4 h-4 mr-2" 
          />
          {{ shareConfig.schedule_type === 'now' ? __('Post Now') : __('Schedule Post') }}
        </template>
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import ImageUploader from '@/components/Controls/ImageUploader.vue'

// Props
const props = defineProps({
  connection: {
    type: Object,
    required: true
  },
  job: {
    type: Object,
    required: true
  },
  jobUrl: {
    type: String,
    default: ''
  },
  jobImageUrl: {
    type: String,
    default: ''
  },
  isSubmitting: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['submit', 'cancel'])

// Reactive data
const submitting = ref(false)
const imageError = ref(false)
const shareConfig = ref({
  message: '',
  schedule_type: 'now',
  scheduled_time: '',
  include_link_preview: true,
  target_page_id: '',
  target_oa_id: '',
  broadcast_to_followers: false,
  custom_image_url: '',
  use_default_image: true,
  job_url: '',
  image_url: ''
})

// Computed
const isValid = computed(() => {
  if (!shareConfig.value.message.trim()) return false
  if (shareConfig.value.schedule_type === 'later' && !shareConfig.value.scheduled_time) return false
  if (shareConfig.value.message.length > getMaxMessageLength()) return false
  
  // Facebook requires target page
  if (props.connection.platform_type === 'Facebook') {
    const pages = getConnectedAccounts('Page')
    if (pages.length > 0 && !shareConfig.value.target_page_id) return false
    if(!shareConfig.value.custom_image_url) return false
  }
  
  return true
})

// Methods
const getPlatformIcon = (platformType) => {
  const icons = {
    'Facebook': 'facebook',
    'Zalo': 'message-circle',
    'Instagram': 'instagram',
    'LinkedIn': 'linkedin',
    'Twitter': 'twitter'
  }
  return icons[platformType] || 'globe'
}

const getPlatformColor = (platformType) => {
  const colors = {
    'Facebook': 'text-blue-600',
    'Zalo': 'text-blue-500',
    'Instagram': 'text-pink-600',
    'LinkedIn': 'text-blue-700',
    'Twitter': 'text-blue-400'
  }
  return colors[platformType] || 'text-gray-600'
}

const getPlatformName = (platformType) => {
  const names = {
    'Facebook': 'Facebook',
    'Zalo': 'Zalo OA',
    'Instagram': 'Instagram',
    'LinkedIn': 'LinkedIn',
    'Twitter': 'Twitter'
  }
  return names[platformType] || platformType
}

const getConnectionDisplayName = () => {
  const accounts = getConnectedAccounts()
  const primaryAccount = accounts.find(acc => acc.is_primary) || accounts[0]
  
  if (primaryAccount) {
    return primaryAccount.account_name
  }
  
  return props.connection.user_email || props.connection.full_name || __('Connected Account')
}

const getConnectedAccounts = (accountType = null) => {
  const accounts = props.connection.connected_accounts || []
  if (accountType) {
    return accounts.filter(acc => acc.account_type === accountType)
  }
  return accounts.filter(acc => acc.is_active)
}

const getEffectiveImageUrl = () => {
  if (imageError.value) return null
  
  // Priority 1: Custom image URL (if provided)
  if (shareConfig.value.custom_image_url && shareConfig.value.custom_image_url.trim()) {
    return shareConfig.value.custom_image_url.trim()
  }
  
  // Priority 2: Default job image (if enabled and available)
  if (shareConfig.value.use_default_image && props.jobImageUrl) {
    return props.jobImageUrl
  }
  
  // No image available
  return null
}

const handleImageError = () => {
  imageError.value = true
}

const handleImageUpload = (fileUrl) => {
  shareConfig.value.custom_image_url = fileUrl
  imageError.value = false
}

const handleImageRemove = () => {
  shareConfig.value.custom_image_url = ''
  imageError.value = false
}

const clearCustomImage = () => {
  shareConfig.value.custom_image_url = ''
  shareConfig.value.use_default_image = false
  imageError.value = false
}

const getMessagePlaceholder = () => {
  const placeholders = {
    'Facebook': __('Post this exciting job opportunity with your network...'),
    'Zalo': __('Thông báo cơ hội việc làm hấp dẫn...'),
    'Instagram': __('New job opportunity! Check it out...'),
    'LinkedIn': __('We are looking for talented professionals...'),
    'Twitter': __('New job opening! Apply now...')
  }
  return placeholders[props.connection.platform_type] || __('Post this job posting...')
}

const getMaxMessageLength = () => {
  const limits = {
    'Facebook': 8000,
    'Zalo': 2000,
    'Instagram': 2200,
    'LinkedIn': 3000,
    'Twitter': 280
  }
  return limits[props.connection.platform_type] || 2000
}

const getMinDateTime = () => {
  const now = new Date()
  now.setMinutes(now.getMinutes() + 5)
  return now.toISOString().slice(0, 16)
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const useTemplate = () => {
  const jobTitle = props.job.title || props.job.job_title || __('Amazing Position')
  const jobDescription = props.job.job_description || props.job.description || __('Great opportunity to join our team!')
  const jobUrl = props.jobUrl || `${window.location.origin}/mbw_mira/jobs/${props.job.slug || props.job.id}`
  
  const templates = {
    'Facebook': `🚀 ${__("We're hiring for:")} ${jobTitle}

${truncateText(jobDescription, 200)}

${__('Join our amazing team and make a difference!')} 
${__('Apply now:')} ${jobUrl}

#hiring #jobs #career #opportunity`,

    'Zalo': `🔥 ${__('TUYỂN DỤNG:')} ${jobTitle}

📝 ${__('Mô tả:')} ${truncateText(jobDescription, 150)}

💼 ${__('Ứng tuyển ngay:')} ${jobUrl}

#tuyendung #vieclam #career`,

    'Instagram': `✨ ${__('New job alert!')} ✨

${__("We're looking for:")} ${jobTitle}

${truncateText(jobDescription, 100)}

${__('Link in bio to apply!')} 

#hiring #jobs #career`,

    'LinkedIn': `${__('We are excited to announce a new opening for:')} ${jobTitle}

${truncateText(jobDescription, 250)}

${__("If you're passionate about making an impact and growing your career, we'd love to hear from you.")}

${__('Apply here:')} ${jobUrl}

#hiring #jobs #career #professional`,

    'Twitter': `🎯 ${__("We're hiring:")} ${jobTitle}

${truncateText(jobDescription, 100)}

${__('Apply:')} ${jobUrl}

#hiring #jobs`
  }
  
  shareConfig.value.message = templates[props.connection.platform_type] || templates['Facebook']
}

const handleSubmit = async () => {
  if (!isValid.value) return
  
  try {
    submitting.value = true
    
    const effectiveImageUrl = getEffectiveImageUrl()
    
    // Prepare share data
    const shareData = {
      message: shareConfig.value.message.trim(),
      schedule_type: shareConfig.value.schedule_type,
      scheduled_time: shareConfig.value.scheduled_time || null,
      job_url: props.jobUrl,
      image_url: effectiveImageUrl,
      
      // Platform specific data
      ...(props.connection.platform_type === 'Facebook' && {
        include_link_preview: shareConfig.value.include_link_preview,
        target_page_id: shareConfig.value.target_page_id,
        target_page_name: getConnectedAccounts('Page').find(p => p.external_account_id === shareConfig.value.target_page_id)?.account_name
      }),
      
      ...(props.connection.platform_type === 'Zalo' && {
        oa_id: shareConfig.value.target_oa_id,
        broadcast_to_followers: shareConfig.value.broadcast_to_followers
      })
    }
    
    console.log('Final share data:', shareData)
    
    // Always emit submit, let parent handle the response
    emit('submit', shareData)
  } catch (error) {
    console.error('Error preparing post data:', error)
    submitting.value = false
  }
}

// Methods to control loading state from parent
const resetLoading = () => {
  submitting.value = false
}

// Expose methods to parent
defineExpose({
  resetLoading
})
onMounted(() => {
  // Set URLs
  shareConfig.value.job_url = props.jobUrl
  shareConfig.value.image_url = props.jobImageUrl
  
  // Set default target page for Facebook
  if (props.connection.platform_type === 'Facebook') {
    const pages = getConnectedAccounts('Page')
    if (pages.length > 0) {
      shareConfig.value.target_page_id = pages[0].external_account_id
    }
  }
  
  // Set default target OA for Zalo
  if (props.connection.platform_type === 'Zalo') {
    const oas = getConnectedAccounts('OA')
    if (oas.length > 0) {
      shareConfig.value.target_oa_id = oas[0].external_account_id
    }
  }
  
  // Watch for custom image URL changes to reset error state
  watch(() => shareConfig.value.custom_image_url, () => {
    imageError.value = false
  })
  
  // Auto-populate with template
  useTemplate()
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.preview-content {
  @apply space-y-3;
}

.preview-content img {
  @apply max-w-full h-auto;
}

/* Custom scrollbar for textarea */
textarea::-webkit-scrollbar {
  width: 6px;
}

textarea::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

textarea::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

textarea::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

/* Improved focus states */
input:focus,
textarea:focus,
select:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Button loading animation */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>