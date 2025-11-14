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
      <!-- Mode Selection -->
      <div v-if="!selectedPage && !creatingPage && !createError">
        <label class="block text-sm font-medium text-gray-700 mb-3">
          {{ __('Choose Landing Page') }}
          <span class="text-red-500">*</span>
        </label>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Select Existing Page -->
          <div 
            @click="loadPublishedPages"
            class="border-2 border-dashed border-gray-300 rounded-lg p-4 hover:border-purple-400 hover:bg-purple-50 cursor-pointer transition-colors"
          >
            <div class="text-center">
              <FeatherIcon name="folder" class="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <h3 class="text-sm font-medium text-gray-900 mb-1">
                {{ __('Select Existing Page') }}
              </h3>
              <p class="text-xs text-gray-500">
                {{ __('Choose from published landing pages') }}
              </p>
            </div>
          </div>

          <!-- Create New Page -->
          <div 
            @click="openCreateModal"
            class="border-2 border-dashed border-gray-300 rounded-lg p-4 hover:border-purple-400 hover:bg-purple-50 cursor-pointer transition-colors"
          >
            <div class="text-center">
              <FeatherIcon name="plus-circle" class="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <h3 class="text-sm font-medium text-gray-900 mb-1">
                {{ __('Create New Page') }}
              </h3>
              <p class="text-xs text-gray-500">
                {{ __('Build a new landing page from template') }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Published Pages Selection Modal -->
      <PublishedPageSelectionModal
        :show="showPublishedPagesModal"
        :pages="publishedPages"
        :loading="loadingPages"
        :error="publishedPagesError"
        @close="showPublishedPagesModal = false"
        @select="selectPublishedPage"
        @retry="loadPublishedPages"
      />

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
      <div v-if="createError" class="mb-3">
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
              @click="resetSelection"
              variant="ghost"
              size="sm"
            >
              {{ __('Back') }}
            </Button>
          </div>
        </div>
      </div>
      
      <!-- Selected Page Display -->
      <div v-if="selectedPage">
        <div class="border border-green-200 rounded-lg p-4 bg-green-50">
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <div class="flex items-center mb-2">
                <FeatherIcon name="check-circle" class="h-5 w-5 text-green-600 mr-2" />
                <span class="text-sm font-medium text-green-900">
                  {{ selectedPage.isPublished ? __('Published Page Selected') : __('Draft Page Selected') }}
                </span>
                <span v-if="selectedPage.isPublished" class="ml-2 px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
                  {{ __('Published') }}
                </span>
                <span v-else class="ml-2 px-2 py-0.5 bg-yellow-100 text-yellow-700 text-xs rounded-full">
                  {{ __('Draft') }}
                </span>
              </div>
              <p class="text-sm font-medium text-green-900 mb-1">
                {{ selectedPage.title }}
              </p>
              <p class="text-xs text-green-700 mb-2 font-mono break-all">
                {{ selectedPage.url }}
              </p>
              <p class="text-xs text-green-600">
                Page ID: {{ selectedPage.id }}
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
              @click="copyToClipboard(selectedPage.url)"
              variant="ghost"
              size="sm"
            >
              <template #prefix>
                <FeatherIcon name="copy" class="h-3 w-3" />
              </template>
              {{ __('Copy URL') }}
            </Button>
            <Button
              v-if="!selectedPage.isPublished"
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
              @click="resetSelection"
              variant="ghost"
              size="sm"
            >
              <template #prefix>
                <FeatherIcon name="x" class="h-3 w-3" />
              </template>
              {{ __('Change') }}
            </Button>
          </div>
        </div>
      </div>
      
      <!-- Template Selection Modal -->
      <TemplateSelectionModal
        :show="showModal"
        :templates="templates"
        :loading="loading"
        :error="error"
        @close="showModal = false"
        @select="(template, data) => handleTemplateSelect(template, data)"
        @retry="fetchTemplates"
      />

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { FeatherIcon, Button, call, toast } from 'frappe-ui'
import TemplateSelectionModal from './TemplateSelectionModal.vue'
import PublishedPageSelectionModal from './PublishedPageSelectionModal.vue'

const props = defineProps({
  ladipageUrl: {
    type: String,
    default: ''
  },
  ladipageId: {
    type: String,
    default: ''
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

const emit = defineEmits(['update:ladipageUrl', 'update:ladipageId'])

// Helper function to build builder URL
const buildBuilderUrl = (pageBuilderIdOrPath) => {
  if (!pageBuilderIdOrPath) return ''
  
  // If it's already a full URL, return as is
  if (pageBuilderIdOrPath.startsWith('http')) {
    return pageBuilderIdOrPath
  }
  
  // If it's just the page builder ID, build the URL
  if (pageBuilderIdOrPath.startsWith('page-')) {
    return `https://hireos.fastwork.vn/builder/${pageBuilderIdOrPath}`
  }
  
  // If it's a path starting with /builder, prepend domain
  if (pageBuilderIdOrPath.startsWith('/builder')) {
    return `https://hireos.fastwork.vn${pageBuilderIdOrPath}`
  }
  
  // Default case
  return `https://hireos.fastwork.vn/builder/${pageBuilderIdOrPath}`
}

// State
const mode = ref('') // 'select' or 'create'
const selectedPage = ref(null)
const publishedPages = ref([])
const loadingPages = ref(false)
const publishedPagesError = ref(null)
const showPublishedPagesModal = ref(false)
const showModal = ref(false)
const templates = ref([])
const loading = ref(false)
const error = ref(null)
const creatingPage = ref(false)
const createError = ref(null)

// Load page details for edit mode
const loadPageDetails = async (pageId) => {
  try {
    const response = await call('mbw_mira.integrations.cms_page.get_page_details', {
      page_id: pageId
    })
    
    if (response?.message?.status === 'success' && response?.message?.data) {
      const page = response.message.data
      selectedPage.value = {
        id: pageId,
        title: page.page_title || '',
        url: props.ladipageUrl,
        isPublished: page.published || false,
        builderUrl: buildBuilderUrl(page.builder_page)
      }
    }
  } catch (error) {
    console.error('❌ Error loading page details:', error)
  }
}

// Load published pages
const loadPublishedPages = async () => {
  loadingPages.value = true
  publishedPagesError.value = null
  showPublishedPagesModal.value = true
  
  try {
    const response = await call('mbw_mira.integrations.cms_page.get_page_public')
    
    if (response?.message?.status === 'success' && response?.message?.data) {
      publishedPages.value = response.message.data
    } else {
      publishedPagesError.value = 'Failed to load published pages'
    }
  } catch (error) {
    console.error('❌ Error loading published pages:', error)
    publishedPagesError.value = error.message || 'Failed to load published pages'
  } finally {
    loadingPages.value = false
  }
}

// Select published page
const selectPublishedPage = async (page) => {
  selectedPage.value = {
    id: page.name,
    title: page.title,
    url: page.router,
    isPublished: true,
    builderUrl: buildBuilderUrl(page.page_builder_id)
  }
  
  // Emit updates
  emit('update:ladipageUrl', page.router)
  emit('update:ladipageId', page.name)
  
  // Save to campaign database if campaignId is provided
  if (props.campaignId) {
    try {
      await call('frappe.client.set_value', {
        doctype: 'Mira Campaign',
        name: props.campaignId,
        fieldname: {
          ladipage_url: page.router,
          ladipage_id: page.name
        }
      })
      console.log('✅ Saved published page to campaign:', props.campaignId)
    } catch (error) {
      console.error('❌ Error saving to campaign:', error)
      // Don't show error toast as this is not critical for UX
    }
  }
  
  toast.success(__('Published page selected'))
}

// Reset selection
const resetSelection = () => {
  mode.value = ''
  selectedPage.value = null
  publishedPages.value = []
  publishedPagesError.value = null
  showPublishedPagesModal.value = false
  createError.value = null
  showModal.value = false
}

// Open create modal and load templates
const openCreateModal = async () => {
  showModal.value = true
  await fetchTemplates()
}

// Load templates for create mode
const fetchTemplates = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await call('mbw_mira.integrations.cms_page.get_templates')
    
    if (response?.message?.status === 'success' && response?.message?.data) {
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

// Handle template selection and create page
const handleTemplateSelect = async (template, data) => {
  if (!template) return

  console.log('Selected template:', template)
  console.log('Selected template data:', data)
  
  creatingPage.value = true
  createError.value = null
  showModal.value = false
  
  try {
    const response = await call('mbw_mira.integrations.cms_page.create_page_by_template', {
      template_id: template,
      page_title: data.page_title ,
      campaign_name: props.campaignName,
      campaign_id: props.campaignId,
      company_info: props.companyInfo,
      job_info: props.jobInfo,
      published: 1
    })
    
    if (response?.message?.status === 'success' && response?.message?.data) {
      const page = response?.message?.data
      
      // Check if page is published (has url_public_page)
      const publicUrl = page.url_public_page || ''
      
      selectedPage.value = {
        id: page.page_id,
        title: page.page_title,
        url: publicUrl,
        isPublished: true,
        builderUrl: buildBuilderUrl(page.builder_page)
      }
      
      // Emit updates based on publish status
      emit('update:ladipageUrl', publicUrl) // URL if published, empty if draft
      emit('update:ladipageId', page.page_id)
      
      // Save to campaign database
      if (props.campaignId) {
        try {
          await call('frappe.client.set_value', {
            doctype: 'Mira Campaign',
            name: props.campaignId,
            fieldname: {
              ladipage_url: publicUrl, // URL if published, empty if draft
              ladipage_id: page.page_id
            }
          })
          console.log('✅ Saved page to campaign:', props.campaignId, { 
            published: isPublished, 
            url: publicUrl 
          })
        } catch (error) {
          console.error('❌ Error saving page to campaign:', error)
          // Don't show error toast as this is not critical for UX
        }
      }
      
      toast.success(__('Page created successfully'))
    } else {
      throw new Error(response?.message || 'Failed to create page')
    }
  } catch (error) {
    console.error('❌ Error creating page:', error)
    createError.value = error.message || 'Failed to create page'
  } finally {
    creatingPage.value = false
  }
}

// Open builder
const openBuilder = () => {
  if (selectedPage.value?.builderUrl) {
    window.open(selectedPage.value.builderUrl, '_blank')
  }
}

// Copy to clipboard
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    toast.success(__('URL copied to clipboard'))
  } catch (error) {
    console.error('❌ Error copying to clipboard:', error)
    toast.error(__('Failed to copy URL'))
  }
}

// Publish page
const publishPage = async () => {
  if (!selectedPage.value?.id) return
  
  try {
    const response = await call('mbw_mira.integrations.cms_page.publish_page', {
      page_id: selectedPage.value.id
    })
    
    if (response?.message?.status === 'success') {
      selectedPage.value.isPublished = true
      
      // Get public URL from response (prioritize url_public_page over router)
      const publicUrl = response?.message?.data?.url_public_page || response?.message?.data?.router || ''
      
      if (publicUrl) {
        selectedPage.value.url = publicUrl
        emit('update:ladipageUrl', publicUrl)
        
        // Save to campaign database
        if (props.campaignId) {
          try {
            await call('frappe.client.set_value', {
              doctype: 'Mira Campaign',
              name: props.campaignId,
              fieldname: {
                ladipage_url: publicUrl,
                ladipage_id: selectedPage.value.id
              }
            })
            console.log('✅ Updated campaign with published URL:', publicUrl)
          } catch (error) {
            console.error('❌ Error updating campaign URL:', error)
          }
        }
      }
      
      toast.success(__('Page published successfully'))
    } else {
      throw new Error(response?.message || 'Failed to publish page')
    }
  } catch (error) {
    console.error('❌ Error publishing page:', error)
    toast.error(__('Failed to publish page'))
  }
}

// Initialize from props - watch after function definitions
watch(() => [props.ladipageUrl, props.ladipageId], ([url, id]) => {
  if (id) {
    // Load page details if we have both URL and ID
    loadPageDetails(id)
  }
}, { immediate: true })
</script>
