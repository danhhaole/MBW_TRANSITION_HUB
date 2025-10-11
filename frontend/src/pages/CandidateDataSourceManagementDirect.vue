<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <!-- Create button -->

        <Button variant="solid" theme="gray" @click="handleCreate" :loading="loading" class="">
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6">
              </path>
            </svg>
          </template>
          {{ __('Create New') }}
        </Button>
      </template>
    </LayoutHeader>

    <!-- Filters & Controls -->
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <!-- Search & Filters -->
          <div class="flex items-center space-x-4 flex-1">
            <!-- Search -->
            <TextInput
              v-model="searchText"
              type="text"
              :placeholder="__('Search data sources...')"
              @input="handleSearchChange"
              class="flex-1 max-w-md"
            >
              <template #prefix>
                <FeatherIcon name="search" class="w-4 h-4" />
              </template>
            </TextInput>

            <!-- Type Filter -->
            <FormControl
              type="select"
              v-model="typeFilter"
              @change="handleFilterChange"
              :options="[
                { label: __('All Types'), value: '' },
                { label: __('ATS'), value: 'ATS' },
                { label: __('Job Board'), value: 'JobBoard' },
                { label: __('Social Network'), value: 'SocialNetwork' },
                { label: __('Manual'), value: 'Manual' },
                { label: __('Other'), value: 'Other' }
              ]"
              class="w-40"
            />

            <!-- Status Filter -->
            <FormControl
              type="select"
              v-model="statusFilter"
              @change="handleFilterChange"
              :options="[
                { label: __('All'), value: '' },
                { label: __('Active'), value: 'active' },
                { label: __('Inactive'), value: 'inactive' },
                { label: __('Error'), value: 'error' }
              ]"
             
              class="w-32"
            />
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center space-x-3">
            <!-- Refresh Button -->
            <Button
              @click="handleRefresh"
              :loading="loading"
              variant="outline"
              theme="gray"
              size="sm"
            >
              <template #prefix>
                <FeatherIcon name="refresh-cw" class="w-4 h-4" />
              </template>
              {{ __('Refresh') }}
            </Button>

            <!-- Create Button -->
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <div class="bg-white shadow-sm border border-gray-200 rounded-lg overflow-hidden">
        <!-- Loading State -->
        <Loading v-if="loading" text="Loading data sources..." />

        <!-- Error State -->
        <div v-else-if="error" class="p-8">
          <div class="text-center">
            <svg class="mx-auto h-12 w-12 text-red-400" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">{{ __('Error loading data') }}</h3>
            <p class="mt-1 text-sm text-gray-500">{{ error }}</p>
            <div class="mt-6">
              <Button @click="handleRefresh" variant="solid" theme="blue">
                {{ __('Try Again') }}
              </Button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="!dataSources || dataSources.length === 0" class="p-8">
          <div class="text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m0 0V9a2 2 0 012-2h8a2 2 0 012 2v4M6 13h12">
              </path>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">{{ __('No data sources') }}</h3>
            <p class="mt-1 text-sm text-gray-500">{{ __('Start by creating your first data source.') }}</p>
            <div class="mt-6">
              <Button variant="solid" theme="gray" @click="handleCreate" :loading="loading" class="px-6 py-3.5">
                <template #prefix>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </template>
                {{ __('Create New') }}
              </Button>
            </div>
          </div>
        </div>

        <!-- Data Table Content -->
        <div v-else>
          <!-- Table Header -->
          <div class="bg-gray-50 px-6 py-3 border-b border-gray-200">
            <div class="grid grid-cols-12 gap-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
              <div class="col-span-3">{{ __('Data Source') }}</div>
              <div class="col-span-2">{{ __('Type') }}</div>
              <div class="col-span-2">{{ __('Status') }}</div>
              <div class="col-span-2">{{ __('Last Sync') }}</div>
              <div class="col-span-2">{{ __('Created') }}</div>
              <div class="col-span-1">{{ __('Actions') }}</div>
            </div>
          </div>

          <!-- Table Body -->
          <div class="divide-y divide-gray-200">
            <div v-for="source in dataSources" :key="source.name"
              class="px-6 py-4 hover:bg-gray-50 transition-colors duration-150">
              <div class="grid grid-cols-12 gap-4 items-center">
                <!-- Source Info -->
                <div class="col-span-3">
                  <div class="flex items-center space-x-3">
                    <div
                      class="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m0 0V9a2 2 0 012-2h8a2 2 0 012 2v4M6 13h12">
                        </path>
                      </svg>
                    </div>
                    <div class="min-w-0 flex-1">
                      <p class="text-sm font-medium text-gray-900 truncate">{{ source.source_name }}</p>
                      <p class="text-xs text-gray-500 truncate">{{ source.name }}</p>
                    </div>
                  </div>
                </div>

                <!-- Type -->
                <div class="col-span-2">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getTypeColor(source.source_type)">
                    {{ source.type_display || source.source_type }}
                  </span>
                </div>

                <!-- Status -->
                <div class="col-span-2">
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 rounded-full" :class="getStatusColor(source.connection_status)"></div>
                    <span class="text-sm text-gray-900">{{ source.display_status }}</span>
                  </div>
                  <div v-if="source.last_error" class="text-xs text-red-600 mt-1 truncate" :title="source.last_error">
                    {{ source.last_error }}
                  </div>
                </div>

                <!-- Last Sync -->
                <div class="col-span-2">
                  <p class="text-sm text-gray-900">{{ source.last_sync_formatted }}</p>
                  <p v-if="source.sync_frequency_minutes" class="text-xs text-gray-500">
                    {{ __('Every {0} minutes', [source.sync_frequency_minutes]) }}
                  </p>
                </div>

                <!-- Created -->
                <div class="col-span-2">
                  <p class="text-sm text-gray-900">{{ formatDate(source.creation) }}</p>
                  <p class="text-xs text-gray-500">{{ source.created_by || source.owner }}</p>
                </div>

                <!-- Actions -->
                <div class="col-span-1">
                  <div class="flex items-center gap-1">
                    <button
                      @click="handleView(source)"
                      class="p-1 text-slate-400 hover:text-blue-600 transition-colors"
                      :title="__('View Details')"
                    >
                      <FeatherIcon name="eye" class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleEdit(source)"
                      class="p-1 text-slate-400 hover:text-blue-600 transition-colors"
                      :title="__('Edit')"
                    >
                      <FeatherIcon name="edit" class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleDelete(source)"
                      class="p-1 text-slate-400 hover:text-red-600 transition-colors"
                      :title="__('Delete')"
                    >
                      <FeatherIcon name="trash-2" class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="pagination && pagination.pages > 1" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex-1 flex justify-between sm:hidden">
                <Button
                  @click="handlePageChange(pagination.page - 1)"
                  :disabled="!pagination.has_prev"
                  variant="outline"
                  size="sm"
                >
                  {{ __('Previous') }}
                </Button>
                <Button
                  @click="handlePageChange(pagination.page + 1)"
                  :disabled="!pagination.has_next"
                  variant="outline"
                  size="sm"
                >
                  {{ __('Next') }}
                </Button>
              </div>

              <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                <div>
                  <p class="text-sm text-gray-700">
                    {{ __('Showing') }}
                    <span class="font-medium">{{ pagination.showing_from }}</span>
                    {{ __('to') }}
                    <span class="font-medium">{{ pagination.showing_to }}</span>
                    {{ __('of') }}
                    <span class="font-medium">{{ pagination.total }}</span>
                    {{ __('results') }}
                  </p>
                </div>
                <div>
                  <nav class="relative z-0 inline-flex items-center space-x-2" aria-label="Pagination">
                    <Button
                      @click="handlePageChange(pagination.page - 1)"
                      :disabled="!pagination.has_prev"
                      variant="outline"
                      size="sm"
                    >
                      <template #prefix>
                        <FeatherIcon name="chevron-left" class="w-4 h-4" />
                      </template>
                      <span class="sr-only">{{ __('Previous page') }}</span>
                    </Button>

                    <span class="px-4 py-2 text-sm font-medium text-gray-700">
                      {{ pagination.page }} / {{ pagination.pages }}
                    </span>

                    <Button
                      @click="handlePageChange(pagination.page + 1)"
                      :disabled="!pagination.has_next"
                      variant="outline"
                      size="sm"
                    >
                      <template #prefix>
                        <FeatherIcon name="chevron-right" class="w-4 h-4" />
                      </template>
                      <span class="sr-only">{{ __('Next page') }}</span>
                    </Button>
                  </nav>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <CandidateDataSourceFormDirect v-model="showForm" :data-source="selectedDataSource" @success="handleFormSuccess"
      @cancel="handleFormCancel" />

    <!-- View Modal -->
    <Dialog v-model="showViewModal" :options="{
      title: __('Data Source Details'),
      size: 'lg'
    }">
      <template #body>
        <div v-if="selectedDataSource" class="p-6">
          <div class="space-y-6">
            <!-- Basic Info -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-4">{{ __('Basic Information') }}</h3>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('Source Name') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedDataSource.source_name }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('Type') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedDataSource.type_display }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('API Base URL') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedDataSource.api_base_url || 'N/A' }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('Authentication Method') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedDataSource.auth_method_display }}</p>
                </div>
              </div>
            </div>

            <!-- Status Info -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-4">{{ __('Status') }}</h3>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('Current Status') }}</label>
                  <div class="mt-1 flex items-center space-x-2">
                    <div class="w-2 h-2 rounded-full" :class="getStatusColor(selectedDataSource.connection_status)">
                    </div>
                    <span class="text-sm text-gray-900">{{ selectedDataSource.display_status }}</span>
                  </div>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('Last Sync') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedDataSource.last_sync_formatted }}</p>
                </div>
              </div>
            </div>

            <!-- Notes -->
            <div v-if="selectedDataSource.notes">
              <h3 class="text-lg font-medium text-gray-900 mb-4">{{ __('Notes') }}</h3>
              <p class="text-sm text-gray-700">{{ selectedDataSource.notes }}</p>
            </div>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Loading Overlay -->
    <div v-if="processing" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-sm w-full mx-4">
        <div class="flex items-center space-x-3">
          <svg class="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
          </svg>
          <span class="text-sm text-gray-700">{{ processingMessage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { Dialog, Button, Breadcrumbs, TextInput, FormControl, FeatherIcon } from 'frappe-ui'
import CandidateDataSourceFormDirect from '@/components/candidateDataSource/CandidateDataSourceFormDirect.vue'
import { useCandidateDataSourceStore } from '@/stores/candidateDataSource.js'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'

// Store
const candidateDataSourceStore = useCandidateDataSourceStore()

// Reactive state
const loading = ref(false)
const processing = ref(false)
const processingMessage = ref('')
const error = ref(null)
const dataSources = ref([])
const pagination = ref({})
const statistics = ref(null)

// Filters and search
const searchText = ref('')
const typeFilter = ref('')
const statusFilter = ref('')

// Modals
const showForm = ref(false)
const showViewModal = ref(false)
const selectedDataSource = ref(null)

// UI state

// Current page
const currentPage = ref(1)

// Breadcrumbs
const breadcrumbs = [
  { label: __('Candidate Data Source Management'), route: { name: 'CandidateDataSourceManagementDirect' } }
]

// Methods
const loadDataSources = async () => {
  loading.value = true
  error.value = null

  try {
    const options = {
      page_length: 20,
      start: (currentPage.value - 1) * 20,
      search_text: searchText.value,
      filters: buildFilters()
    }

    const result = await candidateDataSourceStore.fetchDataSources(options)

    if (result.success) {
      dataSources.value = result.data.data || []
      pagination.value = {
        total: result.data.total || 0,
        page: currentPage.value,
        limit: 20,
        pages: Math.ceil((result.data.total || 0) / 20),
        has_next: result.data.has_next || false,
        has_prev: result.data.has_prev || false,
        showing_from: result.data.showing_from || 0,
        showing_to: result.data.showing_to || 0
      }
    } else {
      error.value = result.error || __('Unable to load data')
      dataSources.value = []
      pagination.value = {}
    }
  } catch (err) {
    console.error('Error loading data sources:', err)
    error.value = __('An error occurred while loading data')
    dataSources.value = []
    pagination.value = {}
  } finally {
    loading.value = false
  }
}

const loadStatistics = async () => {
  try {
    const result = await candidateDataSourceStore.fetchStatistics()
    if (result.success) {
      statistics.value = result.data
    }
  } catch (err) {
    console.error('Error loading statistics:', err)
  }
}

const buildFilters = () => {
  const filters = {}

  if (typeFilter.value) {
    filters.source_type = typeFilter.value
  }

  if (statusFilter.value) {
    switch (statusFilter.value) {
      case 'active':
        filters.is_active = 1
        break
      case 'inactive':
        filters.is_active = 0
        break
      case 'error':
        filters.last_error = ['!=', '']
        break
    }
  }

  return filters
}

// Event handlers
const handleRefresh = () => {
  currentPage.value = 1
  loadDataSources()
  loadStatistics()
}

const handleSearchChange = () => {
  currentPage.value = 1
  loadDataSources()
}

const handleFilterChange = () => {
  currentPage.value = 1
  loadDataSources()
}

const handlePageChange = (page) => {
  if (page >= 1 && page <= pagination.value.pages) {
    currentPage.value = page
    loadDataSources()
  }
}

const handleCreate = () => {
  selectedDataSource.value = null
  showForm.value = true
}

const handleEdit = (dataSource) => {
  selectedDataSource.value = dataSource
  showForm.value = true
}

const handleView = (dataSource) => {
  selectedDataSource.value = dataSource
  showViewModal.value = true
}

const handleDelete = async (dataSource) => {

  if (!confirm(__('Are you sure you want to delete data source "{0}"?', [dataSource.source_name]))) {
    return
  }

  processing.value = true
  processingMessage.value = __('Deleting data source...')

  try {
    const result = await candidateDataSourceStore.deleteDataSource(dataSource.name)

    if (result.success) {
      await loadDataSources()
      await loadStatistics()
    } else {
      alert(__('Error: {0}', [result.error]))
    }
  } catch (err) {
    console.error('Error deleting data source:', err)
    alert(__('An error occurred while deleting the data source'))
  } finally {
    processing.value = false
  }
}



const handleFormSuccess = () => {
  showForm.value = false
  loadDataSources()
  loadStatistics()
}

const handleFormCancel = () => {
  showForm.value = false
}

// Helper functions
const getTypeColor = (type) => {
  const colors = {
    'ATS': 'bg-blue-100 text-blue-800',
    'JobBoard': 'bg-green-100 text-green-800',
    'SocialNetwork': 'bg-purple-100 text-purple-800',
    'Manual': 'bg-gray-100 text-gray-800',
    'Other': 'bg-yellow-100 text-yellow-800'
  }
  return colors[type] || 'bg-gray-100 text-gray-800'
}

const getStatusColor = (status) => {
  const colors = {
    'connected': 'bg-green-500',
    'error': 'bg-red-500',
    'unknown': 'bg-yellow-500',
    'disconnected': 'bg-gray-500'
  }
  return colors[status] || 'bg-gray-500'
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('vi-VN')
}

// Lifecycle hooks
onMounted(() => {
  loadDataSources()
  loadStatistics()
})



// Watch for search text changes with debounce
let searchTimeout
watch(searchText, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    handleSearchChange()
  }, 500)
})
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>