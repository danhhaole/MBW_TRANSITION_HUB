<template>
  <Dialog
    v-model="isOpen"
    :options="{
      title: __('Choose Landing Page Template'),
      size: '5xl'
    }"
  >
    <template #body-title>
      <div>
        <h3 class="text-lg font-semibold text-gray-900">
          {{ __('Choose Landing Page Template') }}
        </h3>
        <p class="text-sm text-gray-500 mt-1">
          {{ __('Select a template for your recruitment campaign') }}
        </p>
      </div>
    </template>

    <template #body-content>
      <!-- Search Bar -->
      <div class="mb-4 px-1">
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <FeatherIcon name="search" class="h-4 w-4 text-gray-400" />
          </div>
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="__('Search templates...')"
            class="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            @input="handleSearchInput"
          />
          <button
            v-if="searchQuery"
            @click="clearSearch"
            class="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <FeatherIcon name="x" class="h-4 w-4 text-gray-400 hover:text-gray-600" />
          </button>
        </div>
      </div>

      <div class="overflow-y-auto max-h-[60vh] p-1">
        <!-- Loading State -->
        <div v-if="loading" class="flex flex-col items-center justify-center py-12">
          <FeatherIcon name="loader" class="h-12 w-12 text-blue-600 animate-spin mb-4" />
          <p class="text-gray-600">{{ __('Loading templates...') }}</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="flex flex-col items-center justify-center py-12">
          <FeatherIcon name="alert-circle" class="h-12 w-12 text-red-600 mb-4" />
          <p class="text-red-600 mb-4">{{ error }}</p>
          <Button
            @click="handleRetry"
            variant="solid"
          >
            {{ __('Retry') }}
          </Button>
        </div>

        <!-- Templates Grid -->
        <div v-else-if="templates.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="template in templates"
              :key="template.name"
              class="group border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-all cursor-pointer"
              :class="{ 'ring-2 ring-blue-500': selectedTemplate === template.name }"
              @click="selectTemplate(template)"
            >
              <!-- Preview Image -->
              <div class="relative aspect-video bg-gray-100 overflow-hidden">
                <img
                  v-if="template.preview"
                  :src="template.preview"
                  :alt="template.page_title"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  @error="handleImageError"
                />
                <div v-else class="w-full h-full flex items-center justify-center">
                  <FeatherIcon name="image" class="h-12 w-12 text-gray-400" />
                </div>
                
                <!-- Preview Button Overlay -->
                <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all flex items-center justify-center">
                  <Button
                    @click.stop="openPreview(template)"
                    variant="solid"
                    class="opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <template #prefix>
                      <FeatherIcon name="external-link" class="h-4 w-4" />
                    </template>
                    {{ __('Preview') }}
                  </Button>
                </div>
                
                <!-- Selected Badge -->
                <div
                  v-if="selectedTemplate === template.name"
                  class="absolute top-2 right-2 bg-blue-600 text-white px-3 py-1 rounded-full text-xs font-medium flex items-center z-10"
                >
                  <FeatherIcon name="check" class="h-3 w-3 mr-1" />
                  {{ __('Selected') }}
                </div>
              </div>

              <!-- Template Info -->
              <div class="p-4">
                <div class="flex items-start justify-between mb-2">
                  <h4 class="font-semibold text-gray-900 line-clamp-2 flex-1">
                    {{ template.page_title || template.name }}
                  </h4>
                </div>
                <p class="text-xs text-gray-500 line-clamp-1 mb-3">
                  {{ template.route }}
                </p> 
              </div>
            </div>
          </div>

        <!-- Empty State -->
        <div v-else class="flex flex-col items-center justify-center py-12">
          <FeatherIcon name="inbox" class="h-12 w-12 text-gray-400 mb-4" />
          <p class="text-gray-600">
            {{ searchQuery ? __('No templates found matching your search') : __('No templates available') }}
          </p>
          <Button
            v-if="searchQuery"
            @click="clearSearch"
            variant="outline"
            class="mt-4"
          >
            {{ __('Clear Search') }}
          </Button>
        </div>
      </div>

      <!-- Pagination Controls -->
      <div v-if="!loading && !error && totalPages > 1" class="mt-4 px-1 pt-4 border-t border-gray-200">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-600">
            {{ __('Page {0} of {1}', [currentPage, totalPages]) }}
            <span class="ml-2 text-gray-500">
              ({{ __('Showing {0}-{1} of {2}', [startIndex + 1, endIndex, totalTemplates]) }})
            </span>
          </div>
          <div class="flex gap-2">
            <Button
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1"
              variant="outline"
              size="sm"
            >
              <template #prefix>
                <FeatherIcon name="chevron-left" class="h-4 w-4" />
              </template>
              {{ __('Previous') }}
            </Button>
            <Button
              @click="goToPage(currentPage + 1)"
              :disabled="!hasMore && currentPage >= totalPages"
              variant="outline"
              size="sm"
            >
              {{ __('Next') }}
              <template #suffix>
                <FeatherIcon name="chevron-right" class="h-4 w-4" />
              </template>
            </Button>
          </div>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex items-center justify-between w-full">
        <div class="text-sm text-gray-600">
          <span v-if="selectedTemplate">
            {{ __('1 template selected') }}
          </span>
          <span v-else>
            {{ __('Please select a template') }}
          </span>
        </div>
        <div class="flex gap-3">
          <Button
            @click="closeDialog"
            variant="ghost"
          >
            {{ __('Cancel') }}
          </Button>
          <Button
            @click="confirmSelection"
            :disabled="!selectedTemplate"
            variant="solid"
          >
            {{ __('Confirm Selection') }}
          </Button>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { Dialog, Button, FeatherIcon } from 'frappe-ui'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  templates: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  },
  modelValue: {
    type: String,
    default: ''
  },
  // Pagination props
  currentPage: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 12
  },
  totalTemplates: {
    type: Number,
    default: 0
  },
  hasMore: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'select', 'retry', 'update:modelValue', 'search', 'page-change'])

const isOpen = ref(props.show)
const selectedTemplate = ref(props.modelValue)
const dataSelectedTemplate = ref(null)
const searchQuery = ref('')
let searchTimeout = null

// Computed properties for pagination
const totalPages = computed(() => {
  return Math.ceil(props.totalTemplates / props.pageSize) || 1
})

const startIndex = computed(() => {
  return (props.currentPage - 1) * props.pageSize
})

const endIndex = computed(() => {
  return Math.min(startIndex.value + props.templates.length, props.totalTemplates)
})

// Watch show prop to sync with isOpen
watch(() => props.show, (newVal) => {
  isOpen.value = newVal
  if (newVal) {
    // Reset search when modal opens
    searchQuery.value = ''
  }
})

// Watch isOpen to emit close event
watch(isOpen, (newVal) => {
  if (!newVal) {
    emit('close')
    // Reset selection when closing
    selectedTemplate.value = ''
    dataSelectedTemplate.value = null
  }
})

const selectTemplate = (template) => {
  selectedTemplate.value = template.name
  dataSelectedTemplate.value = template
}

const closeDialog = () => {
  isOpen.value = false
}

const confirmSelection = () => {
  if (selectedTemplate.value) {
    emit('update:modelValue', selectedTemplate.value)
    emit('select', selectedTemplate.value, dataSelectedTemplate.value)
    closeDialog()
  }
}

const openPreview = (template) => {
  if (template.route) {
    window.open(template.route, '_blank', 'noopener,noreferrer')
  }
}

const handleImageError = (event) => {
  event.target.style.display = 'none'
}

// Search functionality
const handleSearchInput = () => {
  // Debounce search to avoid too many API calls
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  searchTimeout = setTimeout(() => {
    console.log('🔍 Searching for:', searchQuery.value)
    emit('search', searchQuery.value)
  }, 500) // Wait 500ms after user stops typing
}

const clearSearch = () => {
  searchQuery.value = ''
  emit('search', '')
}

const handleRetry = () => {
  emit('retry')
}

// Pagination functionality
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    console.log('📄 Going to page:', page)
    emit('page-change', page)
  }
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
