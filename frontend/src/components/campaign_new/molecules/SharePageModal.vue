<template>
  <Dialog v-model="isOpen" :options="{ title: __('Share Software Implementation Specialist Recruitment'), size: '3xl' }">
    <template #body-content>
      <div v-if="pageData" class="space-y-6">
        <!-- Share Links Section -->
        <div class="bg-white rounded-lg p-6">
          <!-- Landing Page URL with UTM -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Copy Link') }}</label>
            <div class="flex items-center space-x-2">
              <div class="flex-1">
                <input
                  type="text"
                  :value="generatedUrl"
                  readonly
                  class="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-sm font-mono"
                />
              </div>
              <Button
                @click="copyToClipboard(generatedUrl)"
                variant="outline"
                size="sm"
              >
                <template #prefix>
                  <FeatherIcon name="copy" class="h-4 w-4" />
                </template>
                {{ __('Copy') }}
              </Button>
            </div>
          </div>

          <!-- Short URL -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Short Link') }}</label>
            <div class="flex items-center space-x-2">
              <div class="flex-1">
                <input
                  type="text"
                  :value="shortUrl"
                  readonly
                  class="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-sm font-mono"
                />
              </div>
              <Button
                @click="copyToClipboard(shortUrl)"
                variant="outline"
                size="sm"
              >
                <template #prefix>
                  <FeatherIcon name="copy" class="h-4 w-4" />
                </template>
                {{ __('Copy') }}
              </Button>
            </div>
          </div>
        </div>

        <!-- Social Media Configuration -->
        <div class="bg-gray-50 rounded-lg p-6">
          <div class="flex items-center mb-4">
            <FeatherIcon name="target" class="h-5 w-5 mr-2 text-red-500" />
            <h4 class="text-base font-semibold text-gray-900">{{ __('Setup Source & Tracking Code') }}</h4>
          </div>

          <!-- Platform Selector -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              <FeatherIcon name="link" class="h-4 w-4 inline mr-1 text-blue-500" />
              {{ selectedPlatform }}
            </label>
            <select
              v-model="selectedPlatform"
              class="w-full px-3 py-2 border border-gray-300 rounded-md bg-white text-sm"
              @change="updateUrl"
            >
              <option value="Facebook">Facebook</option>
              <option value="Zalo">Zalo</option>
            </select>
          </div>

          <!-- Campaign Name -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Campaign Name') }}</label>
            <input
              v-model="campaignName"
              type="text"
              readonly
              class="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-sm"
            />
          </div>

          <!-- Content -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">{{ __('Content - Optional') }}</label>
            <TextEditor
              variant="outline"
              :content="contentValue"
              @change="(content) => { contentValue = content; updateUrl(); }"
              :placeholder="__('Example: creative_a, banner_1, job_title...')"
              :bubbleMenu="true"
              :fixedMenu="true"
              :editorClass="'prose-sm !w-full !max-w-full overflow-auto min-h-[150px] max-h-80 py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 focus:border-gray-500 focus:ring-0 transition-colors'"
            />
          </div>
        </div>

      </div>
    </template>

    <template #actions>
      <div class="flex justify-end">
        <Button
          variant="solid"
          @click="saveShortUrl"
          :loading="isSaving"
        >
          <template #prefix>
            <FeatherIcon name="save" class="h-4 w-4" />
          </template>
          {{ __('Save Short URL') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, computed } from 'vue'
import { Dialog, Button, FeatherIcon, TextEditor, call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'


const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  pageData: {
    type: Object,
    default: null
  },
  platform: {
    type: String,
    default: 'Facebook' // 'Facebook' or 'Zalo'
  }
})

const emit = defineEmits(['close', 'update:show', 'short-link-generated'])

const toast = useToast()

// UTM Parameters
const selectedPlatform = ref('Facebook')
const campaignName = ref('')
const contentValue = ref('')
const generatedUrl = ref('')
const shortUrl = ref('')
const isShortening = ref(false)
const isSaving = ref(false)
const savedShortUrlData = ref(null)

// Computed property for v-model
const isOpen = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

// Platform to UTM source mapping
const platformToUtmSource = {
  'Facebook': 'facebook',
  'Zalo': 'zalo'
}


// Tạo URL ngắn sử dụng gdshortener qua backend API
const generateShortUrl = async (longUrl) => {
  if (!longUrl) return '';

  try {
    // Gọi API backend sử dụng gdshortener
    const result = await call('mbw_mira.mbw_mira.doctype.mira_short_url.mira_short_url.create_short_url_with_gdshortener', {
      long_url: longUrl
    });

    if (result && result.success && result.short_url) {
      // Loại bỏ dấu phẩy và khoảng trắng ở đầu/cuối
      const cleanShortUrl = String(result.short_url).trim().replace(/,$/, '');
      console.log('✅ Short URL created with gdshortener:', cleanShortUrl);
      return cleanShortUrl;
    } else {
      console.error('❌ gdshortener API error:', result?.message || 'Unknown error');
      toast.error(__('Error creating short URL: ') + (result?.message || 'Unknown error'));
      return longUrl;
    }
  } catch (e) {
    console.error('❌ Error creating short URL:', e);
    toast.error(__('Failed to create short URL'));
    return longUrl;
  }
}

// Update URL with UTM parameters and generate short URL
const updateUrl = async () => {
  if (!props.pageData?.url) return;

  const baseUrl = props.pageData.url;
  const utmSource = platformToUtmSource[selectedPlatform.value] || selectedPlatform.value.toLowerCase();
  const utmMedium = 'social';

  // Build UTM parameters
  const params = new URLSearchParams();
  params.append('utm_source', utmSource);

  // utm_campaign LUÔN dùng campaignId (ví dụ: CPG-251230-00767)
  // Input hiển thị campaignName (tên chiến dịch) nhưng URL dùng campaignId
  if (props.pageData && props.pageData.campaignId) {
    const campaignId = String(props.pageData.campaignId).trim();
    if (campaignId) {
      params.append('utm_campaign', campaignId);
    }
  }

  // Clean content value - remove HTML tags and check if there's actual text
  const cleanContent = contentValue.value.replace(/<[^>]*>/g, '').trim();
  if (cleanContent) {
    params.append('utm_content', cleanContent);
  }

  // Generate final URL
  const separator = baseUrl.includes('?') ? '&' : '?';
  const newUrl = `${baseUrl}${separator}${params.toString()}`;
  generatedUrl.value = newUrl;

  // Generate short URL (await the async function)
  shortUrl.value = await generateShortUrl(newUrl);
  
  // Emit short link when generated
  if (shortUrl.value) {
    emit('short-link-generated', {
      platform: selectedPlatform.value,
      shortUrl: shortUrl.value
    })
  }
}

// Helper to get human-readable campaign name for display
const resolveCampaignName = (pageData) => {
  if (!pageData) return 'campaign'
  // Prefer explicit name fields; avoid falling back to id unless nothing else
  return (
    pageData.campaign_name ||
    pageData.campaignName ||
    pageData.title ||
    pageData.display_name ||
    pageData.name || // last resort
    'campaign'
  )
}

// Watch for modal open to initialize
watch(() => props.show, (newShow) => {
  if (newShow && props.pageData) {
    // Initialize with platform from props or default to Facebook
    selectedPlatform.value = props.platform || 'Facebook'
    campaignName.value = resolveCampaignName(props.pageData)
    contentValue.value = ''
    updateUrl()
  }
})

// Initialize on mount if modal is already open
onMounted(() => {
  if (props.show && props.pageData) {
    selectedPlatform.value = props.platform || 'Facebook';
    campaignName.value = resolveCampaignName(props.pageData);
    contentValue.value = '';
    updateUrl();
  }
});

// Copy to clipboard với fallback method
const copyToClipboard = async (text) => {
  try {
    // Thử dùng Clipboard API hiện đại (yêu cầu HTTPS hoặc localhost)
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text)
      toast.success(__('Link copied to clipboard'))
      return
    }
    
    // Fallback: Sử dụng method cũ (hoạt động trên mọi trình duyệt)
    const textArea = document.createElement('textarea')
    textArea.value = text
    textArea.style.position = 'fixed'
    textArea.style.left = '-999999px'
    textArea.style.top = '-999999px'
    document.body.appendChild(textArea)
    textArea.focus()
    textArea.select()
    
    try {
      const successful = document.execCommand('copy')
      if (successful) {
        toast.success(__('Link copied to clipboard'))
      } else {
        throw new Error('execCommand failed')
      }
    } catch (err) {
      throw new Error('Copy command failed')
    } finally {
      document.body.removeChild(textArea)
    }
  } catch (error) {
    console.error('Error copying to clipboard:', error)
    toast.error(__('Failed to copy link. Please copy manually.'))
  }
}

// Save short URL to database (optional - for tracking purposes)
const saveShortUrl = async () => {
  if (!generatedUrl.value || !shortUrl.value) {
    toast.error(__('No URL to save'))
    return
  }

  isSaving.value = true

  try {
    console.log('=== SAVING SHORT URL ===')
    console.log('Long URL:', generatedUrl.value)
    console.log('Short URL:', shortUrl.value)

    const result = await call('mbw_mira.mbw_mira.doctype.mira_short_url.mira_short_url.shorten_url', {
      long_url: generatedUrl.value,
      short_url: shortUrl.value
    })

    if (result) {
      if (result.existing) {
        toast.warning(__('Short URL already exists: ') + result.message)
      } else {
        savedShortUrlData.value = result
        toast.success(__('Short URL saved for tracking!'))
      }
    }
  } catch (error) {
    console.error('Error saving short URL:', error)
    toast.error(__('Error saving Short URL: ') + (error.message || 'Unknown error'))
  } finally {
    isSaving.value = false
  }
}
</script>
