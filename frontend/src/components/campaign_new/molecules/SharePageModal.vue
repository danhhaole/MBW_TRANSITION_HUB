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
  }
})

const emit = defineEmits(['close', 'update:show'])

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

// Tạo URL ngắn sử dụng Is.gd API (miễn phí, không cần API key)
const generateShortUrl = async (longUrl) => {
  if (!longUrl) return '';

  try {
    // Sử dụng Is.gd API để tạo short URL
    const apiUrl = `https://is.gd/create.php?format=json&url=${encodeURIComponent(longUrl)}`;

    const response = await fetch(apiUrl);
    const data = await response.json();

    if (data.shorturl) {
      console.log('✅ Short URL created:', data.shorturl);
      return data.shorturl;
    } else if (data.errormessage) {
      console.error('❌ Is.gd API error:', data.errormessage);
      toast.error(__('Error creating short URL: ') + data.errormessage);
      return longUrl;
    }

    return longUrl;
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

  if (campaignName.value.trim()) {
    params.append('utm_campaign', campaignName.value.trim());
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
}

// Watch for modal open to initialize
watch(() => props.show, (newShow) => {
  if (newShow && props.pageData) {
    // Initialize with actual campaign data
    selectedPlatform.value = 'Facebook'
    campaignName.value = props.pageData.campaignName || 'campaign'
    contentValue.value = ''
    updateUrl()
  }
})

// Initialize on mount if modal is already open
onMounted(() => {
  if (props.show && props.pageData) {
    selectedPlatform.value = 'Facebook';
    campaignName.value = props.pageData.campaignName || 'campaign';
    contentValue.value = '';
    updateUrl();
  }
});

// Copy to clipboard
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    toast.success(__('Link copied to clipboard'))
  } catch (error) {
    console.error('Error copying to clipboard:', error)
    toast.error(__('Failed to copy link'))
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
