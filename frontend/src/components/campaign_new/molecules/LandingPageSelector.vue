<template>
  <div class="bg-white rounded-lg border border-gray-200 p-6">
    <div class="flex items-center mb-4">
      <div class="w-8 h-8 rounded-lg bg-purple-500 text-white flex items-center justify-center mr-3">
        <FeatherIcon name="link" class="h-4 w-4" />
      </div>
      <div>
        <h4 class="text-sm font-semibold text-gray-900">
          {{ __('2.1. Landing Page & CTA Link') }}
        </h4>
        <p class="text-xs text-gray-500">
          {{ __('Choose landing page and configure call-to-action') }}
        </p>
      </div>
    </div>

    <div class="space-y-4">
      <!-- Landing Page Selection -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __('Choose Landing Page') }}
          <span class="text-red-500">*</span>
        </label>
        
        <!-- Creating Page Loading -->
        <div v-if="creatingPage" class="mb-3">
          <div class="border border-blue-200 rounded-lg p-4 bg-blue-50">
            <div class="flex items-center">
              <FeatherIcon name="loader" class="h-5 w-5 text-blue-600 animate-spin mr-3" />
              <div>
                <p class="text-sm font-medium text-blue-900">
                  {{ __('Creating landing page...') }}
                </p>
                <p class="text-xs text-blue-700">
                  {{ __('Please wait while we set up your page') }}
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Create Error -->
        <div v-else-if="createError" class="mb-3">
          <div class="border border-red-200 rounded-lg p-4 bg-red-50">
            <div class="flex items-start justify-between">
              <div class="flex items-start flex-1">
                <FeatherIcon name="alert-circle" class="h-5 w-5 text-red-600 mr-3 mt-0.5" />
                <div>
                  <p class="text-sm font-medium text-red-900">
                    {{ __('Failed to create page') }}
                  </p>
                  <p class="text-xs text-red-700">
                    {{ createError }}
                  </p>
                </div>
              </div>
              <Button
                @click="showModal = true"
                variant="ghost"
                size="sm"
              >
                {{ __('Retry') }}
              </Button>
            </div>
          </div>
        </div>
        
        <!-- Page Created Successfully or Edit Mode -->
        <div v-else-if="(landingPage && pageData) || ladipageUrl" class="mb-3">
          <!-- Debug info -->
        
          <div class="border border-green-200 rounded-lg p-4 bg-green-50">
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1">
                <div class="flex items-center mb-2">
                  <FeatherIcon name="check-circle" class="h-5 w-5 text-green-600 mr-2" />
                  <span class="text-sm font-medium text-green-900">
                    {{ pageData ? __('Landing Page Created Successfully') : __('Landing Page Configured') }}
                  </span>
                  <span v-if="pageData?.published" class="ml-2 px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
                    {{ __('Published') }}
                  </span>
                  <span v-else-if="pageData" class="ml-2 px-2 py-0.5 bg-yellow-100 text-yellow-700 text-xs rounded-full">
                    {{ __('Draft') }}
                  </span>
                  <span v-else class="ml-2 px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full">
                    {{ __('Configured') }}
                  </span>
                </div>
                <p v-if="pageData?.page_title" class="text-sm font-medium text-green-900 mb-1">
                  {{ pageData.page_title }}
                </p>
                <p class="text-xs text-green-700 mb-2 font-mono break-all">
                  {{ pageData?.builder_page || ladipageUrl }}
                </p>
                <p v-if="pageData?.page_id" class="text-xs text-green-600">
                  Page ID: {{ pageData.page_id }}
                </p>
              </div>
            </div>
            
            <!-- Page Actions -->
            <div class="flex gap-2 pt-3 border-t border-green-200">
              <Button
                @click="openBuilder"
                variant="solid"
                size="sm"
                class="bg-green-600 hover:bg-green-700"
              >
                <template #prefix>
                  <FeatherIcon name="edit-2" class="h-3 w-3" />
                </template>
                {{ __('Edit in Builder') }}
              </Button>
              <Button
                @click="copyToClipboard(pageData?.builder_page || ladipageUrl)"
                variant="ghost"
                size="sm"
              >
                <template #prefix>
                  <FeatherIcon name="copy" class="h-3 w-3" />
                </template>
                {{ __('Copy URL') }}
              </Button>
              <Button
                v-if="pageData && !pageData.published"
                @click="publishPage"
                variant="ghost"
                size="sm"
              >
                <template #prefix>
                  <FeatherIcon name="upload-cloud" class="h-3 w-3" />
                </template>
                {{ __('Publish') }}
              </Button>
              <Button
                v-else-if="pageData && pageData.published"
                @click="unpublishPage"
                variant="ghost"
                size="sm"
              >
                <template #prefix>
                  <FeatherIcon name="download-cloud" class="h-3 w-3" />
                </template>
                {{ __('Unpublish') }}
              </Button>
            </div>
          </div>
        </div>
        
        <!-- Select Button -->
        <button
          v-else
          @click="showModal = true"
          class="w-full border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-blue-500 hover:bg-blue-50 transition-all group"
        >
          <!-- Debug info -->
          
          <div class="flex flex-col items-center">
            <div class="w-12 h-12 rounded-full bg-gray-100 group-hover:bg-blue-100 flex items-center justify-center mb-3 transition-colors">
              <FeatherIcon name="layout" class="h-6 w-6 text-gray-400 group-hover:text-blue-600 transition-colors" />
            </div>
            <p class="text-sm font-medium text-gray-900 mb-1">
              {{ __('Select Landing Page Template') }}
            </p>
            <p class="text-xs text-gray-500">
              {{ __('Click to browse available templates') }}
            </p>
          </div>
        </button>
        
        <p class="text-xs text-gray-500 mt-2">
          {{ __('Ensure the form on the landing page is connected to sync Lead data to CRM') }}
        </p>
      </div>
      
      <!-- Template Selection Modal -->
      <TemplateSelectionModal
        :show="showModal"
        :templates="templates"
        :loading="loading"
        :error="error"
        :model-value="landingPage"
        @update:model-value="handleTemplateSelect"
        @close="showModal = false"
        @select="handleTemplateSelect"
        @retry="fetchTemplates"
      />

      <!-- CTA Link Configuration - Only show when page is created -->
      <div v-if="landingPage && pageData" class="border border-gray-200 rounded-lg p-4 bg-gray-50">
        <div class="flex items-start mb-3">
          <FeatherIcon name="info" class="h-4 w-4 text-blue-600 mt-0.5 mr-2 flex-shrink-0" />
          <div class="text-xs text-gray-600">
            {{ __('The form on the landing page must be connected to automatically sync Lead data to the system') }}
          </div>
        </div>

        <!-- Preview Landing Page URL -->
        <div class="bg-white border border-gray-200 rounded p-3">
          <div class="flex items-center justify-between">
            <div class="flex-1 mr-3">
              <div class="text-xs text-gray-500 mb-1">{{ __('Landing Page Builder URL') }}</div>
              <div class="text-sm text-gray-900 font-mono break-all">
                {{ pageData?.builder_page || getLandingPageUrl(landingPage) }}
              </div>
            </div>
            <button
              @click="copyToClipboard(pageData?.builder_page || getLandingPageUrl(landingPage))"
              class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded transition-colors"
              :title="__('Copy URL')"
            >
              <FeatherIcon name="copy" class="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- Form Structure Info - Only show when page is created -->
      <div v-if="landingPage && pageData" class="border-l-4 border-yellow-400 bg-yellow-50 p-4 rounded">
        <div class="flex items-start">
          <FeatherIcon name="alert-triangle" class="h-5 w-5 text-yellow-600 mt-0.5 mr-3 flex-shrink-0" />
          <div>
            <h5 class="text-sm font-semibold text-yellow-900 mb-1">
              {{ __('Form Structure Requirements') }}
            </h5>
            <p class="text-xs text-yellow-800">
              {{ __('Ensure the form on the landing page is properly connected to sync data to CRM. Contact your administrator if you need help setting this up.') }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { FeatherIcon, FormControl, Button, call } from 'frappe-ui'
import TemplateSelectionModal from './TemplateSelectionModal.vue'

const props = defineProps({
  landingPage: {
    type: String,
    default: ''
  },
  ladipageUrl: {
    type: String,
    default: ''
  },
  pageData: {
    type: Object,
    default: null
  },
  campaignName: {
    type: String,
    default: ''
  },
  campaignId: {
    type: String,
    default: ''
  },
  companyInfo: {
    type: Object,
    default: () => ({})
  },
  jobInfo: {
    type: Object,
    default: () => ({})
  },
})

console.log('🚀 props:', props)

const emit = defineEmits(['update:landingPage', 'update:pageData', 'update:ladipageUrl'])

// Debug: Watch props changes
watch(() => props.landingPage, (newVal) => {
  console.log('🔍 landingPage changed:', newVal)
}, { immediate: true })

watch(() => props.pageData, (newVal) => {
  console.log('🔍 pageData changed:', newVal)
}, { immediate: true })

// State
const templates = ref([])
const loading = ref(false)
const error = ref(null)
const showModal = ref(false)
const creatingPage = ref(false)
const createError = ref(null)

// Debug computed
const shouldShowSuccess = computed(() => {
  const result = !!((props.landingPage && props.pageData) || props.ladipageUrl)
  console.log('🔍 shouldShowSuccess:', result, {
    landingPage: props.landingPage,
    pageData: props.pageData,
    ladipageUrl: props.ladipageUrl,
    creatingPage: creatingPage.value,
    createError: createError.value
  })
  return result
})

// Fetch templates from CMS API
const fetchTemplates = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await call('mbw_mira.integrations.cms_page.get_templates')
    
    if (response?.status === 'success' && response?.data) {
      templates.value = response.data
    } else if (response?.message?.status === 'success' && response?.message?.data) {
      // Handle nested response structure
      templates.value = response.message.data
    } else {
      error.value = 'Failed to load templates'
      console.error('❌ Invalid response format:', response)
    }
  } catch (err) {
    error.value = err.message || 'Failed to fetch templates'
    console.error('❌ Error fetching templates:', err)
  } finally {
    loading.value = false
  }
}

// Map templates to dropdown options
const landingPageOptions = computed(() => {
  if (!templates.value || templates.value.length === 0) {
    return []
  }
  
  return templates.value.map(template => ({
    label: template.page_title || template.name,
    value: template.name,
    description: template.route
  }))
})

// Get landing page URL by ID
const getLandingPageUrl = (pageId) => {
  if (!pageId) return ''
  
  const template = templates.value.find(t => t.name === pageId)
  return template?.route || ''
}

// Copy to clipboard
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    console.log('✅ Copied to clipboard:', text)
  })
}

// Get selected template name
const getSelectedTemplateName = () => {
  if (!landingPage.value) return ''
  const template = templates.value.find(t => t.name === landingPage.value)
  return template?.page_title || landingPage.value
}

// Handle template selection from modal
const handleTemplateSelect = async (templateId) => {
  // Prevent duplicate calls
  if (creatingPage.value) {
    console.log('⚠️ Already creating page, skipping...')
    return
  }
  
  const template = templates.value.find(t => t.name === templateId)
  if (!template) return
  
  // Create page from template
  await createPageFromTemplate(template)
}

// Create page from template
const createPageFromTemplate = async (template) => {
  creatingPage.value = true
  createError.value = null
  
  try {
    // Prepare data for page creation
    const pageData = {
      template_id: template.name,
      page_title: props.campaignName || template.page_title || 'Campaign Landing Page',
      // Company info (optional)
      ...props.companyInfo,
      // Job info (optional)
      ...props.jobInfo
    }
    
    const response = await call('mbw_mira.integrations.cms_page.create_page_by_template', pageData)

    console.log('✅ Page created:', response)
    
    // Extract page data from nested response
    let pageInfo = null
    if (response?.message?.message?.data) {
      // Triple nested: {message: {message: {data: {...}}}}
      pageInfo = response.message.message.data
    } else if (response?.message?.data) {
      // Double nested: {message: {data: {...}}}
      pageInfo = response.message.data
    } else if (response?.data) {
      // Single nested: {data: {...}}
      pageInfo = response.data
    }
    
    if (pageInfo && pageInfo.page_id) {
      // Build full builder URL
      const builderUrl = `https://builder.mbwcloud.com${pageInfo.builder_page}`
      
      // Update page info with full URL
      const fullPageData = {
        ...pageInfo,
        builder_page: builderUrl,
        published: 0  // Newly created page is unpublished
      }
      
      // Emit both template ID and page data
      emit('update:landingPage', template.name)
      emit('update:pageData', fullPageData)
      
      // Emit builder URL to save in campaign
      emit('update:ladipageUrl', builderUrl)
      
      // Save to database if campaignId is provided
      if (props.campaignId) {
        await saveLadipageUrlToDatabase(builderUrl)
      }
      
      showModal.value = false
      console.log('✅ Page created:', fullPageData)
    } else {
      createError.value = 'Failed to create page from template'
      console.error('❌ Invalid response:', response)
    }
  } catch (err) {
    createError.value = err.message || 'Failed to create page'
    console.error('❌ Error creating page:', err)
  } finally {
    creatingPage.value = false
  }
}

// Open page builder
const openBuilder = () => {
  const builderUrl = props.pageData?.builder_page || props.ladipageUrl
  if (builderUrl) {
    window.open(builderUrl, '_blank', 'noopener,noreferrer')
  }
}

// Publish page
const publishPage = async () => {
  if (!props.pageData?.page_id) return
  
  try {
    const response = await call('mbw_mira.integrations.cms_page.publish_page', {
      page_id: props.pageData.page_id
    })
    
    if (response?.status === 'success' || response?.message?.status === 'success') {
      // Update page data with published status
      emit('update:pageData', {
        ...props.pageData,
        published: 1
      })
      console.log('✅ Page published successfully')
    }
  } catch (err) {
    console.error('❌ Error publishing page:', err)
  }
}

// Unpublish page
const unpublishPage = async () => {
  if (!props.pageData?.page_id) return
  
  try {
    const response = await call('mbw_mira.integrations.cms_page.unpublish_page', {
      page_id: props.pageData.page_id
    })
    
    if (response?.status === 'success' || response?.message?.status === 'success') {
      // Update page data with unpublished status
      emit('update:pageData', {
        ...props.pageData,
        published: 0
      })
      console.log('✅ Page unpublished successfully')
    }
  } catch (err) {
    console.error('❌ Error unpublishing page:', err)
  }
}

// Save ladipage URL to database
const saveLadipageUrlToDatabase = async (builderUrl) => {
  try {
    console.log(`💾 Saving ladipage_url to campaign ${props.campaignId}:`, builderUrl)
    
    await call('frappe.client.set_value', {
      doctype: 'Mira Campaign',
      name: props.campaignId,
      fieldname: 'ladipage_url',
      value: builderUrl
    })
    
    console.log('✅ Successfully saved ladipage_url to database')
  } catch (err) {
    console.error('❌ Error saving ladipage_url to database:', err)
    // Don't throw error - this is not critical for the flow
  }
}

// Fetch templates on mount
onMounted(() => {
  fetchTemplates()
})
</script>

<style scoped>
/* Add any custom styles here */
</style>
