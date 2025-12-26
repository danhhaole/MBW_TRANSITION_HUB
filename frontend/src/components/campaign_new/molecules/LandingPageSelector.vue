<template>
  <div class="bg-white rounded-lg border border-gray-200 p-6">
    <div class="flex items-center mb-4">
      <div class="w-8 h-8 rounded-lg bg-purple-500 text-white flex items-center justify-center mr-3">
        <FeatherIcon name="link" class="h-4 w-4" />
      </div>
      <div>
        <h4 class="text-sm font-semibold text-gray-900">
          {{ __('Landing Page & CTA Link') }}
        </h4>
        <p class="text-xs text-gray-500">
          {{ __('Choose landing page and configure call-to-action') }}
        </p>
      </div>
    </div>

    <div class="space-y-4">
      <!-- Mode Selection -->
      <div v-if="!selectedPage && !creatingPage && !createError">
        <div class="flex items-center justify-between mb-3">
          <label class="block text-sm font-medium text-gray-700">
            {{ __('Choose Landing Page') }}
            <span class="text-red-500">*</span>
          </label>
          <!-- Cancel button when changing from existing selection -->
          <Button
            v-if="previousSelectedPage"
            @click="cancelChange"
            variant="outline"
            size="sm"
          >
            <template #prefix>
              <FeatherIcon name="arrow-left" class="h-3 w-3" />
            </template>
            {{ __('Cancel') }}
          </Button>
        </div>
        
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
        :current-page="publishedPagesCurrentPage"
        :page-size="publishedPagesSize"
        :total-count="totalPublishedPages"
        :has-more="hasMorePublishedPages"
        @close="handlePublishedPagesModalClose"
        @select="selectPublishedPage"
        @retry="loadPublishedPages"
        @search="handlePublishedPagesSearch"
        @page-change="handlePublishedPagesPageChange"
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
            <div class="flex gap-2">
              <Button
                v-if="selectedPage.url"
                @click="openPreview"
                variant="solid"
              >
                <template #prefix>
                  <FeatherIcon name="eye" class="h-4 w-4" />
                </template>
                {{ __('Preview') }}
              </Button>
              <Button
                @click="handleEditPageInfo"
                variant="outline"
              >
                <template #prefix>
                  <FeatherIcon name="settings" class="h-4 w-4" />
                </template>
                {{ __('Edit Page Info') }}
              </Button>
              <Button
                @click="openBuilder"
                variant="outline"
              >
                <template #prefix>
                  <FeatherIcon name="edit" class="h-4 w-4" />
                </template>
                {{ __('Edit in Builder') }}
              </Button>
            </div>
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
        :current-page="templateCurrentPage"
        :page-size="templatePageSize"
        :total-templates="totalTemplates"
        :has-more="hasMoreTemplates"
        @close="handleModalClose"
        @select="(template, data) => handleTemplateSelect(template, data)"
        @retry="fetchTemplates"
        @search="handleTemplateSearch"
        @page-change="handleTemplatePageChange"
      />
      
      <!-- Company Info Modal -->
      <CompanyInfoModal
        :show="showCompanyInfoModal"
        :selected-template="selectedTemplateData"
        :campaign-name="campaignName"
        :loading="creatingPage"
        :error="createError"
        :is-edit-mode="isEditMode"
        :initial-data="editingPageData"
        @close="handleCompanyInfoModalClose"
        @submit="handleCompanyInfoSubmit"
      />

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { FeatherIcon, Button, call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import TemplateSelectionModal from './TemplateSelectionModal.vue'
import PublishedPageSelectionModal from './PublishedPageSelectionModal.vue'
import CompanyInfoModal from './CompanyInfoModal.vue'

const toast = useToast()

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
  doctype: {
    type: String,
    default: 'Mira Campaign' // 'Mira Campaign' or 'Mira Campaign Template'
  },
})

const emit = defineEmits(['update:ladipageUrl', 'update:ladipageId', 'update'])

// Helper function to build builder URL
const buildBuilderUrl = (pageBuilderIdOrPath) => {
  if (!pageBuilderIdOrPath) {
    console.warn('⚠️ No page builder ID provided')
    return ''
  }
  
  console.log('🔗 Building builder URL from:', pageBuilderIdOrPath)
  
  // If it's already a full URL, return as is
  if (pageBuilderIdOrPath.startsWith('http://') || pageBuilderIdOrPath.startsWith('https://')) {
    console.log('✅ Already full URL:', pageBuilderIdOrPath)
    return pageBuilderIdOrPath
  }
  
  // If it's a path starting with /builder, prepend domain
  if (pageBuilderIdOrPath.startsWith('/builder/')) {
    const url = `https://hireos.fastwork.vn${pageBuilderIdOrPath}`
    console.log('✅ Built URL from path:', url)
    return url
  }
  
  // If it's just the page builder ID (e.g., 'page-123' or just '123'), build the URL
  const url = `https://hireos.fastwork.vn/builder/page/${pageBuilderIdOrPath}`
  console.log('✅ Built URL from ID:', url)
  return url
}

// State
const mode = ref('') // 'select' or 'create'
const selectedPage = ref(null)
const previousSelectedPage = ref(null) // Backup for cancel functionality
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
const showCompanyInfoModal = ref(false)
const selectedTemplateData = ref(null)
const isEditMode = ref(false)
const editingPageData = ref(null)

// Template pagination and search state
const templateCurrentPage = ref(1)
const templatePageSize = ref(12)
const totalTemplates = ref(0)
const templateSearchQuery = ref('')
const hasMoreTemplates = ref(false)
const nextStart = ref(0)

// Published pages pagination and search state
const publishedPagesCurrentPage = ref(1)
const publishedPagesSize = ref(12)
const totalPublishedPages = ref(0)
const publishedPagesSearchQuery = ref('')
const hasMorePublishedPages = ref(false)

// Load page details for edit mode
const loadPageDetails = async (pageId) => {
  try {
    console.log('📄 Loading page details for:', pageId)
    const response = await call('mbw_mira.integrations.cms_page.get_page_details', {
      page_id: pageId
    })
    
    console.log('📦 Page details response:', response)
    
    if (response?.message?.status === 'success' && response?.message?.data) {
      const page = response.message.data
      const builderPage = page.page_builder_id || page.builder_page || page.builder_url || ''
      
      console.log('🏗️ Builder page value:', builderPage)
      
      selectedPage.value = {
        id: pageId,
        title: page.page_title || page.title || '',
        url: props.ladipageUrl,
        isPublished: page.published || false,
        builderUrl: buildBuilderUrl(builderPage)
      }
      
      console.log('✅ Selected page:', selectedPage.value)
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
    // Calculate start index from current page
    const start = (publishedPagesCurrentPage.value - 1) * publishedPagesSize.value
    
    const params = {
      published: 1,
      start: start,
      limit_page_length: publishedPagesSize.value,
      search_query: publishedPagesSearchQuery.value || null
    }
    
    console.log('📋 Fetching published pages with params:', params)
    
    const response = await call('mbw_mira.integrations.cms_page.get_page_public', params)
    
    if (response?.message?.status === 'success' && response?.message?.data) {
      publishedPages.value = response.message.data
      
      // Use new API response fields for pagination
      const msg = response.message
      
      if (msg.total_count !== undefined) {
        totalPublishedPages.value = msg.total_count
      } else {
        totalPublishedPages.value = publishedPages.value.length
      }
      
      hasMorePublishedPages.value = msg.has_more || false
      
      console.log('✅ Published pages loaded:', publishedPages.value.length)
      console.log('📊 Total published pages:', totalPublishedPages.value)
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

// Handle published pages modal close
const handlePublishedPagesModalClose = () => {
  showPublishedPagesModal.value = false
  // Reset pagination state on close
  publishedPagesCurrentPage.value = 1
  publishedPagesSearchQuery.value = ''
}

// Handle published pages search
const handlePublishedPagesSearch = async (searchQuery) => {
  console.log('🔍 Published pages search:', searchQuery)
  publishedPagesSearchQuery.value = searchQuery
  publishedPagesCurrentPage.value = 1 // Reset to first page on new search
  await loadPublishedPages()
}

// Handle published pages page change
const handlePublishedPagesPageChange = async (page) => {
  console.log('📄 Published pages page change:', page)
  publishedPagesCurrentPage.value = page
  await loadPublishedPages()
}

// Select published page
const selectPublishedPage = async (page) => {
  console.log('📄 Selecting published page:', page)
  const builderPage = page.page_builder_id || page.builder_page || page.builder_url || ''
  console.log('🏗️ Builder page from published:', builderPage)
  
  selectedPage.value = {
    id: page.name,
    title: page.title || page.page_title,
    url: page.router,
    isPublished: true,
    builderUrl: buildBuilderUrl(builderPage)
  }
  
  // Clear backup since new selection is made
  previousSelectedPage.value = null
  
  console.log('✅ Selected published page:', selectedPage.value)
  
  // Emit updates
  emit('update:ladipageUrl', page.router)
  emit('update:ladipageId', page.name)
  emit('update')
  
  // Save to parent document (campaign or job opening)
  const parentId = props.campaignId
  if (parentId) {
    try {
      await call('frappe.client.set_value', {
        doctype: props.doctype,
        name: parentId,
        fieldname: {
          ladipage_url: page.router,
          ladipage_id: page.name
        }
      })
      console.log('✅ Saved published page to parent document:', parentId)
    } catch (error) {
      console.error('❌ Error saving to parent document:', error)
      // Don't show error toast as this is not critical for UX
    }
  }
  
  // Save to builder page storage (DocType) - minimal info for published page
  try {
    console.log('💾 Saving published page to builder storage...')
    const storageApi = 'mbw_mira.integrations.cms_page_storage.save_builder_page_data'
    
    const storageParams = {
      page_id: page.name,
      created_from: 'Published Page',
      page_title: page.title,
      url_public_page: page.router,
      page_builder_id: builderPage
    }
          // Add campaign ID
          storageParams.campaign_id = props.campaignId
    
    await call(storageApi, storageParams)
    console.log('✅ Saved published page to builder storage')
  } catch (error) {
    console.error('❌ Error saving to builder storage:', error)
    // Don't fail the whole process if storage save fails
  }
  
  toast.success(__('Published page selected'))
}

// Reset selection (for change button - backup previous selection)
const resetSelection = () => {
  // Backup current selection before clearing
  if (selectedPage.value) {
    previousSelectedPage.value = { ...selectedPage.value }
  }
  
  mode.value = ''
  selectedPage.value = null
  publishedPages.value = []
  publishedPagesError.value = null
  showPublishedPagesModal.value = false
  createError.value = null
  showModal.value = false
}

// Cancel change and restore previous selection
const cancelChange = () => {
  if (previousSelectedPage.value) {
    selectedPage.value = { ...previousSelectedPage.value }
    previousSelectedPage.value = null
  }
  mode.value = ''
  publishedPages.value = []
  publishedPagesError.value = null
  showPublishedPagesModal.value = false
  createError.value = null
  showModal.value = false
}

// Open create modal and load templates
const openCreateModal = async () => {
  // Reset pagination state
  templateCurrentPage.value = 1
  templateSearchQuery.value = ''
  hasMoreTemplates.value = false
  nextStart.value = 0
  
  showModal.value = true
  await fetchTemplates()
}

// Handle modal close
const handleModalClose = () => {
  showModal.value = false
  // Reset pagination state on close
  templateCurrentPage.value = 1
  templateSearchQuery.value = ''
}

// Load templates for create mode
const fetchTemplates = async (options = {}) => {
  loading.value = true
  error.value = null
  try {
    // Calculate start index from current page
    const start = (templateCurrentPage.value - 1) * templatePageSize.value
    
    // Prepare API parameters with defaults
    const params = {
      project_folder: options.project_folder || null,
      fields: options.fields || null,
      start: options.start !== undefined ? options.start : start,
      limit_page_length: options.limit_page_length || templatePageSize.value,
      order_by: options.order_by || null,
      search_query: options.search_query !== undefined ? options.search_query : templateSearchQuery.value
    }
    
    console.log('📋 Fetching templates with params:', params)
    
    const response = await call('mbw_mira.integrations.cms_page.get_templates', params)
    
    if (response?.message?.status === 'success' && response?.message?.data) {
      templates.value = response.message.data
      
      // Use new API response fields for pagination
      // API returns: total_count, page_length, start, has_more, next_start, loaded_count, remaining_count
      const msg = response.message
      
      if (msg.total_count !== undefined) {
        totalTemplates.value = msg.total_count
      } else {
        // Fallback: estimate total from current data
        totalTemplates.value = templates.value.length
      }
      
      // Store additional pagination info for potential use
      hasMoreTemplates.value = msg.has_more || false
      nextStart.value = msg.next_start || 0
      
      console.log('✅ Templates loaded:', templates.value.length)
      console.log('📊 Total templates:', totalTemplates.value)
      console.log('📄 Has more:', hasMoreTemplates.value)
      console.log('➡️ Next start:', nextStart.value)
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

// Handle template search
const handleTemplateSearch = async (searchQuery) => {
  console.log('🔍 Template search:', searchQuery)
  templateSearchQuery.value = searchQuery
  templateCurrentPage.value = 1 // Reset to first page on new search
  await fetchTemplates()
}

// Handle template page change
const handleTemplatePageChange = async (page) => {
  console.log('📄 Template page change:', page)
  templateCurrentPage.value = page
  await fetchTemplates()
}

// Handle template selection - show company info modal
const handleTemplateSelect = async (template, data) => {
  if (!template) return

  console.log('Selected template:', template)
  console.log('Selected template data:', data)
  
  // Store template data and show company info modal
  selectedTemplateData.value = {
    template_id: template,
    template_data: data
  }
  showCompanyInfoModal.value = true
}

// Handle company info submission - both create and update
const handleCompanyInfoSubmit = async (companyInfo) => {
  creatingPage.value = true
  createError.value = null
  
  try {
    if (isEditMode.value) {
      // Update existing page
      if (!selectedPage.value?.id) return
      
      console.log('✏️ Updating page:', selectedPage.value.id)
      console.log('📝 Update data:', companyInfo)
      
      const payload = {
        page_id: selectedPage.value.id,
        ...companyInfo
      }
      
      console.log('📤 Sending update payload to API:', payload)
      console.log('🕐 Timestamp:', new Date().toISOString())
      
      const response = await call('mbw_mira.integrations.cms_page.update_recruitment_page', payload)
      
      console.log('📥 Update response:', response)
      console.log('📥 Response type:', typeof response)
      console.log('📥 Response keys:', response ? Object.keys(response) : 'null')
      console.log('🕐 Response received at:', new Date().toISOString())
      
      // Check both direct and nested response structures
      const status = response?.status || response?.message?.status
      const responseMessage = response?.message?.message || response?.message || 'No message'
      
      console.log('✅ Parsed status:', status)
      console.log('📝 Parsed message:', responseMessage)
      
      if (status === 'success') {
        // Update local selected page data
        selectedPage.value.title = companyInfo.page_title || selectedPage.value.title
        
        // Update builder page storage (DocType)
        try {
          console.log('💾 Updating builder page storage...')
          const storageApi = 'mbw_mira.integrations.cms_page_storage.save_builder_page_data'
          
          const storageParams = {
            page_id: selectedPage.value.id,
            ...companyInfo
          }
          // Add campaign ID
          storageParams.campaign_id = props.campaignId
          
          await call(storageApi, storageParams)
          console.log('✅ Updated builder page storage')
        } catch (error) {
          console.error('❌ Error updating builder page storage:', error)
          // Don't fail the whole process if storage update fails
        }
        
        console.log('✅ Page updated successfully')
        toast.success(__('Page updated successfully'))
        
        // Close modal and reset state on success
        showCompanyInfoModal.value = false
        isEditMode.value = false
        editingPageData.value = null
      } else {
        throw new Error(response?.message || 'Failed to update page')
      }
    } else {
      // Create new page
      if (!selectedTemplateData.value) return
      
      console.log('📝 Creating new page')
      console.log('📝 Company info:', companyInfo)
      console.log('📋 Template data:', selectedTemplateData.value)
      
      // Extract receive_data_configs from companyInfo to handle separately
      const { receive_data_configs, ...otherCompanyInfo } = companyInfo
      
      const payload = {
        template_id: selectedTemplateData.value.template_id,
        published: 1,
        ...otherCompanyInfo
      }
      
      // Always include receive_data_configs, even if empty array
      const configs = receive_data_configs || []
      payload.receive_data_configs = configs
      
      console.log('📧 receive_data_configs extracted:', configs)
      console.log('📧 receive_data_configs in payload:', payload.receive_data_configs || 'NOT INCLUDED')
      console.log('📤 Sending create payload to API:', payload)
      
      const response = await call('mbw_mira.integrations.cms_page.create_page_by_template', payload)
      
      console.log('📥 Create response:', response)
      
      if (response?.message?.status === 'success' && response?.message?.data) {
        const page = response.message.data
        
        // Check if page is published (has url_public_page)
        const publicUrl = page.url_public_page || ''
        const builderPage = page.page_builder_id || page.builder_page || page.builder_url || ''
        
        console.log('🏗️ Builder page from response:', builderPage)
        console.log('📧 Receive data configs from response:', page.receive_data_configs)
        
        selectedPage.value = {
          id: page.page_id,
          title: page.page_title || companyInfo.page_title,
          url: publicUrl,
          isPublished: !!publicUrl,
          builderUrl: buildBuilderUrl(builderPage),
          formConfigId: page.form_config_id,
          receiveDataConfigs: page.receive_data_configs || []
        }
        
        // Clear backup since new page is created
        previousSelectedPage.value = null
        
        console.log('✅ Page created:', selectedPage.value)
        
        // Emit updates based on publish status
        emit('update:ladipageUrl', publicUrl)
        emit('update:ladipageId', page.page_id)
        emit('update')
        
        // Save to parent document (campaign or job opening)
        const parentId = props.campaignId
        if (parentId) {
          try {
            await call('frappe.client.set_value', {
              doctype: props.doctype,
              name: parentId,
              fieldname: {
                ladipage_url: publicUrl,
                ladipage_id: page.page_id
              }
            })
            console.log(`✅ Saved page to ${props.doctype}:`, parentId)
          } catch (error) {
            console.error(`❌ Error saving page to ${props.doctype}:`, error)
          }
        }
        
        // Save to builder page storage (DocType)
        try {
          console.log('💾 Saving to builder page storage...')
          const storageApi = 'mbw_mira.integrations.cms_page_storage.save_builder_page_data'
          
          const storageParams = {
            page_id: page.page_id,
            template_id: selectedTemplateData.value.template_id,
            created_from: 'Template',
            url_public_page: publicUrl,
            page_builder_id: builderPage,
            form_config_id: page.form_config_id,
            ...companyInfo
          }
          // Add campaign ID
          storageParams.campaign_id = props.campaignId
          
          await call(storageApi, storageParams)
          console.log('✅ Saved to builder page storage')
        } catch (error) {
          console.error('❌ Error saving to builder page storage:', error)
          // Don't fail the whole process if storage save fails
        }
        
        toast.success(__('Page created successfully'))
        
        // Close modal and reset state on success
        showCompanyInfoModal.value = false
        showModal.value = false
        selectedTemplateData.value = null
      } else {
        throw new Error(response?.message || 'Failed to create page')
      }
    }
  } catch (error) {
    console.error('❌ Error:', error)
    createError.value = error.message || (isEditMode.value ? 'Failed to update page' : 'Failed to create page')
    // Don't close modal on error - keep it open to show error
  } finally {
    creatingPage.value = false
  }
}

// Handle company info modal close
const handleCompanyInfoModalClose = () => {
  showCompanyInfoModal.value = false
  createError.value = null
  selectedTemplateData.value = null
  isEditMode.value = false
  editingPageData.value = null
}

// Handle edit page info
const handleEditPageInfo = async () => {
  if (!selectedPage.value?.id) return
  
  console.log('✏️ Loading page details for editing:', selectedPage.value.id)
  
  try {
    // Load from local DocType storage first
    const storageApi = 'mbw_mira.integrations.cms_page_storage.get_builder_page_data'
    
    const response = await call(storageApi, {
      page_id: selectedPage.value.id
    })
    
    console.log('📥 Builder page data response:', response)
    
    if (response?.status === 'success' && response?.data) {
      const pageData = response.data
      
      // Map API response to form data format
      editingPageData.value = {
        page_title: pageData.page_title || '',
        company_name: pageData.company_name || '',
        company_logo: pageData.company_logo || '',
        company_slogan: pageData.company_slogan || '',
        company_short_description: pageData.company_short_description || '',
        company_vision: pageData.company_vision || '',
        company_mission: pageData.company_mission || '',
        web_favicon: pageData.web_favicon || '',
        job_title: pageData.job_title || '',
        work_address: pageData.work_address || '',
        employment_type: pageData.employment_type || '',
        salary: pageData.salary || '',
        hiring_quantity: pageData.hiring_quantity || '',
        application_deadline: pageData.application_deadline || '',
        published_date: pageData.published_date || '',
        job_description: pageData.job_description || '',
        job_requirements: pageData.job_requirements || '',
        job_benefits: pageData.job_benefits || '',
        company_number_one: pageData.company_number_one || '',
        company_number_two: pageData.company_number_two || '',
        company_email_one: pageData.company_email_one || '',
        company_email_two: pageData.company_email_two || '',
        head_office: pageData.head_office || '',
        company_website: pageData.company_website || '',
        company_fb: pageData.company_fb || '',
        company_linkedin: pageData.company_linkedin || '',
        company_youtube: pageData.company_youtube || '',
        company_zalo_oa: pageData.company_zalo_oa || '',
        company_tiktok: pageData.company_tiktok || '',
        
        // Form configuration
        form_config_id: pageData.form_config_id || null,
        receive_data_configs: pageData.receive_data_configs || [],
        template_id: pageData.template_id || null
      }

      console.log('Loaded page data:', editingPageData.value);
      console.log('Template ID:', editingPageData.value.template_id);
      
      isEditMode.value = true;
      showCompanyInfoModal.value = true;
    } else {
      throw new Error(response?.message || 'Failed to load page details')
    }
  } catch (error) {
    console.error('❌ Error loading page details:', error)
    toast.error(__('Failed to load page details: '))
  }
}

// Open preview
const openPreview = () => {
  console.log('👁️ Opening preview for page:', selectedPage.value)
  if (selectedPage.value?.url) {
    console.log('🔗 Page URL:', selectedPage.value.url)
    window.open(selectedPage.value.url, '_blank', 'noopener,noreferrer')
  } else {
    console.error('❌ No page URL available')
    toast.error(__('Page URL not available'))
  }
}

// Open builder
const openBuilder = () => {
  console.log('🚀 Opening builder for page:', selectedPage.value)
  if (selectedPage.value?.builderUrl) {
    console.log('🔗 Builder URL:', selectedPage.value.builderUrl)
    window.open(selectedPage.value.builderUrl, '_blank', 'noopener,noreferrer')
  } else {
    console.error('❌ No builder URL available')
    toast.error(__('Builder URL not available'))
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
        emit('update')
        
        // Save to parent document (campaign or job opening)
        const parentId = props.campaignId
        if (parentId) {
          try {
            await call('frappe.client.set_value', {
              doctype: props.doctype,
              name: parentId,
              fieldname: {
                ladipage_url: publicUrl,
                ladipage_id: selectedPage.value.id
              }
            })
            console.log(`✅ Updated ${props.doctype} with published URL:`, publicUrl)
          } catch (error) {
            console.error(`❌ Error updating ${props.doctype} URL:`, error)
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

// Get fields by template
const getFieldsByTemplate = async (templateId) => {
  try {
    const response = await call('mbw_mira.integrations.cms_page.get_fields_by_template', {
      template_id: templateId
    })
    
    if (response?.message?.status === 'success' && response?.message?.data) {
      return response.message.data
    } else {
      throw new Error(response?.message || 'Failed to get template fields')
    }
  } catch (error) {
    console.error('❌ Error getting template fields:', error)
    toast.error(__('Failed to get template fields: '))
    return []
  }
}

// Create receive data config
const createReceiveDataConfig = async (formConfigId, receiveDataConfig) => {
  try {
    const response = await call('mbw_mira.integrations.cms_page.create_link_account', {
      form_config_id: formConfigId,
      receive_data_config: receiveDataConfig
    })
    
    if (response?.message?.status === 'success') {
      toast.success(__('Receive data config created successfully'))
      return response.message.data
    } else {
      throw new Error(response?.message || 'Failed to create receive data config')
    }
  } catch (error) {
    console.error('❌ Error creating receive data config:', error)
    toast.error(__('Failed to create receive data config: '))
    throw error
  }
}

// Update receive data config
const updateReceiveDataConfig = async (receiveDataConfig) => {
  try {
    const response = await call('mbw_mira.integrations.cms_page.update_link_account', {
      receive_data_config: receiveDataConfig
    })
    
    if (response?.message?.status === 'success') {
      toast.success(__('Receive data config updated successfully'))
      return response.message.data
    } else {
      throw new Error(response?.message || 'Failed to update receive data config')
    }
  } catch (error) {
    console.error('❌ Error updating receive data config:', error)
    toast.error(__('Failed to update receive data config: '))
    throw error
  }
}

// Delete receive data config
const deleteReceiveDataConfig = async (receiveDataConfigId) => {
  try {
    const response = await call('mbw_mira.integrations.cms_page.delete_link_account', {
      receive_data_config_id: receiveDataConfigId
    })
    
    if (response?.message?.status === 'success') {
      toast.success(__('Receive data config deleted successfully'))
      return true
    } else {
      throw new Error(response?.message || 'Failed to delete receive data config')
    }
  } catch (error) {
    console.error('❌ Error deleting receive data config:', error)
    toast.error(__('Failed to delete receive data config: '))
    throw error
  }
}

// Expose methods for parent components
defineExpose({
  getFieldsByTemplate,
  createReceiveDataConfig,
  updateReceiveDataConfig,
  deleteReceiveDataConfig,
  selectedPage
})

// Initialize from props - watch after function definitions
watch(() => [props.ladipageUrl, props.ladipageId], ([url, id]) => {
  if (id) {
    // Load page details if we have both URL and ID
    loadPageDetails(id)
  }
}, { immediate: true })
</script>
