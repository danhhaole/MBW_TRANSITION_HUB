<template>
  <Dialog
    :options="{
      title: __('Choose Template'),
      size: '5xl',
    }"
    v-model="show"
  >
    <template #body-content>
      <div class="">
        <!-- Search and Filters -->
        <div class="border-b border-gray-200 p-4 bg-gray-50">
          <div class="flex items-center gap-4">
            <!-- Search Box -->
            <div class="flex-1">
              <FormControl
                v-model="searchText"
                type="text"
                placeholder="Search templates..."
              >
                <template #prefix>
                  <FeatherIcon name="search" class="h-4 w-4 text-gray-400" />
                </template>
              </FormControl>
            </div>

            <!-- Template Type Filter -->
            <div class="">
              <select
                v-model="templateTypeFilter"
                class="border border-gray-300 rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">{{ __('All Templates') }}</option>
                <option value="default">{{ __('Default Templates') }}</option>
                <option value="my">{{ __('My Templates') }}</option>
              </select>
            </div>

            <!-- Show Recommended Only -->
            <div class="whitespace-nowrap">
              <Checkbox
                v-model="showRecommendedOnly"
                :label="__('Recommended only')"
              />
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <FeatherIcon name="loader" class="h-8 w-8 animate-spin text-gray-400" />
          <span class="ml-3 text-gray-500">{{ __('Loading templates...') }}</span>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-12">
          <FeatherIcon name="alert-circle" class="h-12 w-12 mx-auto mb-4 text-red-500" />
          <p class="text-red-600">{{ error }}</p>
        </div>

        <!-- Templates Grid -->
        <div v-else-if="filteredTemplates.length > 0" class="p-4 max-h-[calc(85vh-200px)] overflow-y-auto">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            <div
              v-for="template in paginatedTemplates"
              :key="template.name"
              @click="selectTemplate(template)"
              class="group relative cursor-pointer rounded-lg border-2 overflow-hidden transition-all hover:shadow-lg"
              :class="selectedTemplate?.name === template.name ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-200 hover:border-blue-300'"
            >
              <!-- Template Preview Image -->
              <div class="relative h-24 bg-gray-100 overflow-hidden">
                <img
                  v-if="template.thumbnail"
                  :src="template.thumbnail"
                  :alt="template.template_name"
                  class="w-full h-full object-cover"
                />
                <div v-else class="flex items-center justify-center h-full">
                  <FeatherIcon name="layout" class="h-16 w-16 text-gray-300" />
                </div>
                
                <!-- Recommended Badge -->
                <div
                  v-if="template.is_suggestion"
                  class="absolute top-3 right-3 bg-green-500 text-white text-xs font-medium px-2 py-1 rounded"
                >
                  {{ __("Recommended") }}
                </div>

                <!-- Premium Badge -->
                <div
                  v-if="template.is_premium"
                  class="absolute top-3 left-3 bg-yellow-500 text-white text-xs font-medium px-2 py-1 rounded"
                >
                  {{ __("Premium") }}
                </div>
                
                <!-- Default Badge -->
                <div
                  v-if="template.is_default"
                  class="absolute bottom-3 left-3 bg-blue-500 text-white text-xs font-medium px-2 py-1 rounded"
                >
                  {{ __("Default") }}
                </div>
              </div>

              <!-- Template Info -->
              <div class="p-4">
                <h3 class="font-semibold text-gray-900 mb-1 line-clamp-1">
                  {{ template.template_name }}
                </h3>
                <p class="text-sm text-gray-600 mb-3 line-clamp-2">
                  {{ template.description || __("No description") }}
                </p>

                <!-- Template Type Badges -->
                <div class="flex items-center gap-2 flex-wrap">
                  <!-- Campaign Type Badge -->
                  <span
                    v-if="template.campaign_type"
                    class="inline-flex items-center px-2 py-1 rounded text-xs font-medium"
                    :class="getCampaignTypeBadgeClass(template.campaign_type)"
                  >
                    <FeatherIcon :name="getCampaignTypeIcon(template.campaign_type)" class="h-3 w-3 mr-1" />
                    {{ getCampaignTypeLabel(template.campaign_type) }}
                  </span>
                  
                  <!-- My Template Badge (for non-default) -->
                  <span
                    v-if="!template.is_default"
                    class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-purple-100 text-purple-700"
                  >
                    <FeatherIcon name="user" class="h-3 w-3 mr-1" />
                    {{ __('My Template') }}
                  </span>
                </div>
              </div>

              <!-- Selected Indicator -->
              <div 
                v-if="selectedTemplate?.name === template.name"
                class="absolute top-2 right-2 bg-blue-500 text-white rounded-full p-1"
              >
                <FeatherIcon name="check" class="h-4 w-4" />
              </div>

              <!-- Hover Overlay -->
              <div class="absolute inset-0 bg-blue-500 bg-opacity-0 group-hover:bg-opacity-10 transition-all pointer-events-none" />
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="flex items-center justify-between border-t border-gray-200 pt-4">
            <div class="text-sm text-gray-600">
              {{ __('Showing') }} {{ startIndex + 1 }} - {{ Math.min(endIndex, filteredTemplates.length) }} {{ __('of') }} {{ filteredTemplates.length }} {{ __('templates') }}
            </div>
            <div class="flex items-center gap-2">
              <button
                @click="currentPage--"
                :disabled="currentPage === 1"
                class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <FeatherIcon name="chevron-left" class="h-4 w-4" />
              </button>
              <span class="text-sm text-gray-700">
                {{ __('Page') }} {{ currentPage }} {{ __('of') }} {{ totalPages }}
              </span>
              <button
                @click="currentPage++"
                :disabled="currentPage === totalPages"
                class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <FeatherIcon name="chevron-right" class="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <FeatherIcon name="inbox" class="h-12 w-12 mx-auto mb-4 text-gray-300" />
          <p class="text-gray-500">{{ __('No templates available') }}</p>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end gap-2">
        <Button variant="outline" @click="handleClose">
          {{ __('Cancel') }}
        </Button>
        <Button 
          variant="solid" 
          theme="blue"
          :disabled="!selectedTemplate || creating"
          :loading="creating"
          @click="confirmSelection"
        >
          <template v-if="creating">
           
            {{ __('Creating...') }}
          </template>
          <template v-else>
            {{ __('Continue') }}
          </template>
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { Dialog, Button, FeatherIcon, FormControl, Checkbox, call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  campaignType: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'select'])

const show = ref(props.modelValue)
const templates = ref([])
const loading = ref(false)
const error = ref(null)
const selectedTemplate = ref(null)
const creating = ref(false)

// Filter states
const searchText = ref('')
const showRecommendedOnly = ref(false)
const templateTypeFilter = ref('')  // '', 'default', 'my'

// Pagination states
const currentPage = ref(1)
const itemsPerPage = 6 // 3x3 grid

// Toast
const { info } = useToast()

// Filtered templates based on search and filters
const filteredTemplates = computed(() => {
  let filtered = templates.value

  // Filter by search text
  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    filtered = filtered.filter(t => 
      t.template_name?.toLowerCase().includes(search) ||
      t.description?.toLowerCase().includes(search)
    )
  }

  // Filter by template type (default vs my templates)
  if (templateTypeFilter.value === 'default') {
    filtered = filtered.filter(t => t.is_default)
  } else if (templateTypeFilter.value === 'my') {
    filtered = filtered.filter(t => !t.is_default)
  }

  // Filter by recommended
  if (showRecommendedOnly.value) {
    filtered = filtered.filter(t => t.is_suggestion)
  }

  return filtered
})

// Pagination computed properties
const totalPages = computed(() => Math.ceil(filteredTemplates.value.length / itemsPerPage))
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage)
const endIndex = computed(() => startIndex.value + itemsPerPage)
const paginatedTemplates = computed(() => 
  filteredTemplates.value.slice(startIndex.value, endIndex.value)
)

// Reset pagination when filters change
watch([searchText, showRecommendedOnly, templateTypeFilter], () => {
  currentPage.value = 1
})

watch(() => props.modelValue, (newVal) => {
  show.value = newVal
  if (newVal) {
    loadTemplates()
  }
})

watch(show, (newVal) => {
  emit('update:modelValue', newVal)
})

const loadTemplates = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Build filters based on campaign type
    const filters = {
      is_active: 1
    }
    
    // Filter by campaign type if provided
    if (props.campaignType) {
      filters.campaign_type = props.campaignType
    }
    
    console.log('📋 Loading templates with filters:', filters)
    
    const result = await call('frappe.client.get_list', {
      doctype: 'Mira Campaign Template',
      fields: [
        'name',
        'template_name',
        'description',
        'campaign_type',
        'scope_type',
        'is_suggestion',
        'is_premium',
        'is_default',
        'thumbnail',
        'modified'
      ],
      filters: filters,
      or_filters: [
        
      ],
      order_by: 'is_suggestion desc, is_default desc, modified desc',
      limit_page_length: 50
    })
    
    console.log('✅ Loaded templates:', result)
    templates.value = result || []
    loading.value = false
  } catch (err) {
    console.error('❌ Error loading templates:', err)
    error.value = 'Failed to load templates'
    loading.value = false
  }
}

const selectTemplate = (template) => {
  // Just select, don't emit yet
  selectedTemplate.value = template
}

const confirmSelection = async () => {
  if (!selectedTemplate.value) return
  
  creating.value = true
  
  try {
    // Create campaign from template
    const result = await call('mbw_mira.api.campaign_from_template.create_campaign_from_template', {
      template_id: selectedTemplate.value.name
    })
    
    if (result?.success) {
      emit('select', { ...selectedTemplate.value, createdCampaign: result.data })
      show.value = false
      selectedTemplate.value = null
    } else {
      const { error: toastError } = useToast()
      toastError(result?.error || __('Failed to create campaign from template'))
    }
  } catch (err) {
    console.error('Error creating campaign from template:', err)
    const { error: toastError } = useToast()
    toastError(__('Error creating campaign from template'))
  } finally {
    creating.value = false
  }
}

const handleClose = () => {
  show.value = false
  selectedTemplate.value = null
}

// Campaign type helpers
const getCampaignTypeIcon = (type) => {
  const iconMap = {
    'ATTRACTION': 'target',
    'NURTURING': 'heart',
    'RECRUITMENT': 'users',
  }
  return iconMap[type] || 'file-text'
}

const getCampaignTypeBadgeClass = (type) => {
  const classMap = {
    'ATTRACTION': 'bg-blue-100 text-blue-700',
    'NURTURING': 'bg-green-100 text-green-700',
    'RECRUITMENT': 'bg-purple-100 text-purple-700',
  }
  return classMap[type] || 'bg-gray-100 text-gray-700'
}

const getCampaignTypeLabel = (type) => {
  const labelMap = {
    'ATTRACTION': __('Attraction'),
    'NURTURING': __('Nurturing'),
    'RECRUITMENT': __('Recruitment'),
  }
  return labelMap[type] || type
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>