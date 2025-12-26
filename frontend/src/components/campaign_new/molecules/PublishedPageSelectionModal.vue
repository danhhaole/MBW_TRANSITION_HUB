<template>
  <Dialog v-model="dialogVisible" :options="{ size: '5xl' }">
    <template #body-title>
      <div>
        <h3 class="text-lg font-semibold text-gray-900">
          {{ __('Select Published Landing Page') }}
        </h3>
        <p class="text-sm text-gray-500 mt-1">
          {{ __('Choose from published landing pages') }}
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
            :placeholder="__('Search pages...')"
            class="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-sm"
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

      <div class="space-y-4">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <div class="text-center">
            <FeatherIcon name="loader" class="h-8 w-8 text-gray-400 animate-spin mx-auto mb-3" />
            <p class="text-sm text-gray-500">{{ __('Loading published pages...') }}</p>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-12">
          <FeatherIcon name="alert-circle" class="h-12 w-12 text-red-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            {{ __('Failed to Load Pages') }}
          </h3>
          <p class="text-sm text-gray-500 mb-4">
            {{ error }}
          </p>
          <Button @click="handleRetry" variant="solid">
            {{ __('Try Again') }}
          </Button>
        </div>

        <!-- Empty State -->
        <div v-else-if="!pages || pages.length === 0" class="text-center py-12">
          <FeatherIcon name="file-text" class="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            {{ searchQuery ? __('No Pages Found') : __('No Published Pages') }}
          </h3>
          <p class="text-sm text-gray-500">
            {{ searchQuery 
              ? __('No pages found matching your search.') 
              : __('There are no published landing pages available to select from.') 
            }}
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

        <!-- Pages Grid -->
        <div v-else>
          <div class="mb-4">
            <p class="text-sm text-gray-600">
              {{ __('Showing {0} of {1} pages', [pages.length, totalPages * pageSize > totalCount ? totalCount : totalPages * pageSize]) }}
              <span v-if="totalCount > 0" class="text-gray-400 ml-1">
                ({{ __('Total: {0}', [totalCount]) }})
              </span>
            </p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-[50vh] overflow-y-auto">
            <div
              v-for="page in pages"
              :key="page.name"
              @click="selectPage(page)"
              class="border border-gray-200 rounded-lg p-3 hover:border-purple-400 hover:shadow-md cursor-pointer transition-all group"
            >
              <!-- Preview Image -->
              <div class="aspect-video bg-gray-100 rounded-md mb-3 overflow-hidden">
                <img
                  v-if="page.url_preview && page.url_preview !== 'https://builder.mbwcloud.com/assets/builder/images/fallback.png'"
                  :src="page.url_preview"
                  :alt="page.title"
                  class="w-full h-full object-cover"
                  @error="handleImageError"
                />
                <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-purple-100 to-blue-100">
                  <FeatherIcon name="layout" class="h-8 w-8 text-purple-400" />
                </div>
              </div>
              
              <!-- Page Info -->
              <div class="space-y-2">
                <h4 class="text-sm font-medium text-gray-900 truncate group-hover:text-purple-600 transition-colors">
                  {{ page.title || page.page_title }}
                </h4>
                <p class="text-xs text-gray-500 truncate">
                  {{ page.router }}
                </p>
                <div class="flex items-center justify-between">
                  <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    <FeatherIcon name="globe" class="h-3 w-3 mr-1" />
                    {{ __('Published') }}
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="opacity-0 group-hover:opacity-100 transition-opacity"
                    @click.stop="previewPage(page)"
                  >
                    <template #prefix>
                      <FeatherIcon name="external-link" class="h-3 w-3" />
                    </template>
                    {{ __('Preview') }}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination Controls -->
      <div v-if="!loading && !error && totalPages > 1" class="mt-4 px-1 pt-4 border-t border-gray-200">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-600">
            {{ __('Page {0} of {1}', [currentPage, totalPages]) }}
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
      <div class="flex justify-end gap-2">
        <Button variant="ghost" @click="handleClose">
          {{ __('Cancel') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FeatherIcon, Button, Dialog } from 'frappe-ui'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  pages: {
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
  // Pagination props
  currentPage: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 12
  },
  totalCount: {
    type: Number,
    default: 0
  },
  hasMore: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'select', 'retry', 'search', 'page-change'])

const searchQuery = ref('')
let searchTimeout = null

// Computed for v-model dialog visibility
const dialogVisible = computed({
  get: () => props.show,
  set: (value) => {
    if (!value) {
      handleClose()
    }
  }
})

// Computed for total pages
const totalPages = computed(() => {
  return Math.ceil(props.totalCount / props.pageSize) || 1
})

// Reset search when modal opens
watch(() => props.show, (newVal) => {
  if (newVal) {
    searchQuery.value = ''
  }
})

const selectPage = (page) => {
  emit('select', page)
  emit('close')
}

const previewPage = (page) => {
  if (page.router) {
    window.open(page.router, '_blank', 'noopener,noreferrer')
  }
}

const handleImageError = (event) => {
  event.target.style.display = 'none'
}

const handleClose = () => {
  searchQuery.value = ''
  emit('close')
}

// Search functionality
const handleSearchInput = () => {
  // Debounce search to avoid too many API calls
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  searchTimeout = setTimeout(() => {
    console.log('🔍 Searching pages for:', searchQuery.value)
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
/* Custom scrollbar for the grid */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
