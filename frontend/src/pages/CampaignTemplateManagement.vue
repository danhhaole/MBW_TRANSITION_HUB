<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <!-- Create button -->
        <Button variant="solid" theme="gray" @click="handleCreate" :loading="loading">
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6">
              </path>
            </svg>
          </template>
          {{ __('Create Template') }}
        </Button>
      </template>
    </LayoutHeader>

    <!-- Filters & Controls -->
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="bg-white rounded-lg border border-gray-200 p-4 mb-6">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <!-- Search & Filters -->
          <div class="flex items-center space-x-4 flex-1">
            <!-- Search -->
            <TextInput
              v-model="searchText"
              type="text"
              :placeholder="__('Search templates...')"
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
                { label: __('Email'), value: 'Email' },
                { label: __('SMS'), value: 'SMS' },
                { label: __('Ads'), value: 'Ads' },
                { label: __('Social Media'), value: 'Social Media' },
                { label: __('Direct Mail'), value: 'Direct Mail' }
              ]"
              class="w-44"
            />

            <!-- Status Filter -->
            <FormControl
              type="select"
              v-model="statusFilter"
              @change="handleFilterChange"
              :options="[
                { label: __('All Status'), value: '' },
                { label: __('Active'), value: 'active' },
                { label: __('Inactive'), value: 'inactive' }
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
          </div>
        </div>
      </div>

      <!-- Statistics Cards -->
      <div v-if="statistics && !loading" class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-6">
        <div class="bg-white overflow-hidden rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-100 rounded-md flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">{{ __('Total Templates') }}</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ statistics.total || 0 }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-100 rounded-md flex items-center justify-center">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">{{ __('Active') }}</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ statistics.active || 0 }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-gray-100 rounded-md flex items-center justify-center">
                  <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">{{ __('Inactive') }}</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ statistics.inactive || 0 }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-purple-100 rounded-md flex items-center justify-center">
                  <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">{{ __('Most Used') }}</dt>
                  <dd class="text-sm font-medium text-gray-900">{{ getMostUsedType() }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <div class="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <!-- Loading State -->
        <Loading v-if="loading" text="Loading templates..." />

        <!-- Error State -->
        <div v-else-if="error" class="p-8">
          <div class="text-center">
            <svg class="mx-auto h-12 w-12 text-red-400" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">{{ __('Error loading templates') }}</h3>
            <p class="mt-1 text-sm text-gray-500">{{ error }}</p>
            <div class="mt-6">
              <Button @click="handleRefresh" variant="solid" theme="blue">
                {{ __('Try Again') }}
              </Button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="!templates || templates.length === 0" class="p-8">
          <div class="text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
              </path>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">{{ __('No templates found') }}</h3>
            <p class="mt-1 text-sm text-gray-500">{{ __('Start by creating your first campaign template.') }}</p>
            <div class="mt-6">
              <Button variant="solid" theme="gray" @click="handleCreate" :loading="loading" class="px-6 py-3.5">
                <template #prefix>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </template>
                {{ __('Create Template') }}
              </Button>
            </div>
          </div>
        </div>

        <!-- Data Table Content -->
        <div v-else>
          <!-- Table Header -->
          <div class="bg-gray-50 px-6 py-3 border-b border-gray-200">
            <div class="grid grid-cols-12 gap-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
              <div class="col-span-3">{{ __('Template Name') }}</div>
              <div class="col-span-2">{{ __('Type') }}</div>
              <div class="col-span-2">{{ __('Status') }}</div>
              <div class="col-span-1">{{ __('Steps') }}</div>
              <div class="col-span-2">{{ __('Modified') }}</div>
              <div class="col-span-2">{{ __('Actions') }}</div>
            </div>
          </div>

          <!-- Table Body -->
          <div class="divide-y divide-gray-200">
            <div v-for="template in templates" :key="template.name"
              class="px-6 py-4 hover:bg-gray-50 transition-colors duration-150 cursor-pointer"
              @click="handlePreview(template)">
              <div class="grid grid-cols-12 gap-4 items-center">
                <!-- Template Info -->
                <div class="col-span-3">
                  <div class="flex items-center space-x-3">
                    <div
                      class="w-10 h-10 bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg flex items-center justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z">
                        </path>
                      </svg>
                    </div>
                    <div class="min-w-0 flex-1">
                      <p class="text-sm font-medium text-gray-900 truncate">{{ template.template_name }}</p>
                      <p class="text-xs text-gray-500 truncate">{{ template.name }}</p>
                      <p v-if="template.description" class="text-xs text-gray-500 mt-1 truncate" :title="template.description">
                        {{ template.description }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Type -->
                <div class="col-span-2">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getTypeColor(template.campaign_type)">
                    {{ template.type_display || template.campaign_type }}
                  </span>
                </div>

                <!-- Status -->
                <div class="col-span-2">
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 rounded-full" :class="getStatusColor(template.is_active)"></div>
                    <span class="text-sm text-gray-900">{{ template.display_status }}</span>
                  </div>
                </div>

                <!-- Steps Count -->
                <div class="col-span-1">
                  <div class="flex items-center space-x-1">
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                    </svg>
                    <span class="text-sm font-medium text-gray-900">{{ template.step_count || 0 }}</span>
                  </div>
                </div>

                <!-- Modified -->
                <div class="col-span-2">
                  <p class="text-sm text-gray-900">{{ formatDate(template.modified) }}</p>
                  <p class="text-xs text-gray-500">{{ template.modified_by || template.owner }}</p>
                </div>

                <!-- Actions -->
                <div class="col-span-2" @click.stop>
                  <div class="flex items-center gap-2">
                    <!-- <button
                      @click="handlePreview(template)"
                      class="inline-flex items-center px-2.5 py-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                      :title="__('Preview campaign workflow')"
                    >
                      <FeatherIcon name="eye" class="w-3 h-3" />
                      
                    </button> -->
                    <button
                      @click="handleEdit(template)"
                      class="inline-flex border items-center px-2.5 py-1.5 text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      <FeatherIcon name="edit" class="w-3 h-3" />
                      
                    </button>
                    <button
                      @click="handleDelete(template)"
                      class="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                    >
                      <FeatherIcon name="trash-2" class="w-3 h-3" />
                      
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="pagination && pagination.total > pagination.limit" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex-1 flex justify-between sm:hidden">
                <button
                  @click="handlePreviousPage"
                  :disabled="!pagination.has_prev"
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ __('Previous') }}
                </button>
                <button
                  @click="handleNextPage"
                  :disabled="!pagination.has_next"
                  class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ __('Next') }}
                </button>
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
                  <nav class="relative z-0 inline-flex rounded-md -space-x-px" aria-label="Pagination">
                    <button
                      @click="handlePreviousPage"
                      :disabled="!pagination.has_prev"
                      class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <FeatherIcon name="chevron-left" class="w-5 h-5" />
                    </button>
                    <span
                      class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
                    >
                      {{ __('Page {0} of {1}', [pagination.page, pagination.pages]) }}
                    </span>
                    <button
                      @click="handleNextPage"
                      :disabled="!pagination.has_next"
                      class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <FeatherIcon name="chevron-right" class="w-5 h-5" />
                    </button>
                  </nav>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Form Modal -->
    <CampaignTemplateFormModal
      v-if="showFormModal"
      v-model="showFormModal"
      :template="selectedTemplate"
      @saved="handleTemplateSaved"
      @step-changed="handleStepChanged"
    />

    <!-- Preview Modal -->
    <CampaignTemplatePreviewModal
      v-if="showPreviewModal"
      v-model="showPreviewModal"
      :templateId="templateToPreview?.name"
    />

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed z-50 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                <svg class="h-6 w-6 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-gray-900">{{ __('Delete Template') }}</h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    {{ __('Are you sure you want to delete "{0}"? This action cannot be undone and will also delete all associated template steps.', [templateToDelete?.template_name]) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              @click="confirmDelete"
              :disabled="deleteLoading"
              class="w-full inline-flex justify-center rounded-md border border-transparent px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="deleteLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ deleteLoading ? __('Deleting...') : __('Delete') }}
            </button>
            <button
              @click="showDeleteModal = false"
              :disabled="deleteLoading"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ __('Cancel') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Toast Container -->
  <ToastContainer />
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'
import { FormControl, Breadcrumbs, Button } from 'frappe-ui'
import CampaignTemplateFormModal from '@/components/CampaignTemplateFormModal.vue'
import CampaignTemplatePreviewModal from '@/components/CampaignTemplatePreviewModal.vue'

import { useCampaignTemplateStore } from '@/stores/campaignTemplate.js'
import { useToast } from '@/composables/useToast.js'
import { ToastContainer } from '@/components/shared'

// Debounce function
const debounce = (func, delay) => {
  let timeoutId
  return (...args) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func.apply(null, args), delay)
  }
}

// Router
const router = useRouter()

// Toast
const { showSuccess, showError } = useToast()

// Store
const campaignTemplateStore = useCampaignTemplateStore()

// Page setup
const title = 'Campaign Templates'
const breadcrumbs = [{ label: __('Campaign Templates'), route: { name: 'CampaignTemplateManagement' } }]

// Reactive data - using store
const loading = computed(() => campaignTemplateStore.loading)
const error = computed(() => campaignTemplateStore.error)
const templates = computed(() => campaignTemplateStore.templates)
const statistics = computed(() => campaignTemplateStore.statistics)
const pagination = computed(() => campaignTemplateStore.pagination)

// Search & Filters - using store
const searchText = computed({
  get: () => campaignTemplateStore.searchText,
  set: (value) => campaignTemplateStore.setSearchText(value)
})
const typeFilter = computed({
  get: () => campaignTemplateStore.typeFilter,
  set: (value) => campaignTemplateStore.setTypeFilter(value)
})
const statusFilter = computed({
  get: () => campaignTemplateStore.activeFilter,
  set: (value) => campaignTemplateStore.setActiveFilter(value)
})

// Modals & Forms
const showFormModal = ref(false)
const showPreviewModal = ref(false)
const showDeleteModal = ref(false)
const selectedTemplate = ref(null)
const templateToPreview = ref(null)
const templateToDelete = ref(null)
const deleteLoading = ref(false)

// Computed
const getMostUsedType = () => {
  if (!statistics.value.by_type) return 'N/A'
  
  const types = Object.entries(statistics.value.by_type)
  if (types.length === 0) return 'N/A'
  
  const mostUsed = types.reduce((max, current) => 
    current[1].total > max[1].total ? current : max
  )
  
  return mostUsed[0]
}

// Methods
const loadTemplates = async () => {
  const options = {
    page_length: 20,
    start: (pagination.value.page - 1) * 20
  }

  const result = await campaignTemplateStore.fetchTemplates(options)
  
  if (!result.success && result.error) {
    showError(result.error)
  }
}

const loadStatistics = async () => {
  const result = await campaignTemplateStore.fetchStatistics()
  
  if (!result.success && result.error) {
    console.error('Error loading statistics:', result.error)
  }
}


// Event handlers
const handleRefresh = () => {
  campaignTemplateStore.setPagination(1)
  loadTemplates()
  loadStatistics()
}

const handleSearchChange = debounce(() => {
  campaignTemplateStore.setPagination(1)
  loadTemplates()
}, 300)

const handleFilterChange = () => {
  campaignTemplateStore.setPagination(1)
  loadTemplates()
}

const handleCreate = () => {
  selectedTemplate.value = null
  showFormModal.value = true
}

const handlePreview = (template) => {
  console.log('Management - Preview clicked for template:', template)
  templateToPreview.value = template
  console.log('Management - templateToPreview set to:', templateToPreview.value)
  console.log('Management - Template name for ID:', template?.name)
  showPreviewModal.value = true
}

const handleEdit = async (template) => {
  try {
    // Load complete template data
    const result = await campaignTemplateStore.fetchTemplateById(template.name)
    if (result.success) {
      selectedTemplate.value = result.data
      showFormModal.value = true
    } else {
      showError(result.error || __('Failed to load template data'))
    }
  } catch (err) {
    console.error('Error loading template for edit:', err)
    showError(__('An error occurred while loading template'))
  }
}

const handleDelete = (template) => {
  templateToDelete.value = template
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  if (!templateToDelete.value) return

  deleteLoading.value = true
  try {
    const result = await campaignTemplateStore.deleteTemplate(templateToDelete.value.name)
    
    if (result.success) {
      showSuccess(__('Template deleted successfully'))
      
      showDeleteModal.value = false
      templateToDelete.value = null
      loadStatistics() // Refresh statistics
    } else {
      showError(result.error || __('Failed to delete template'))
    }
  } catch (err) {
    console.error('Error deleting template:', err)
    showError(__('An error occurred while deleting template'))
  } finally {
    deleteLoading.value = false
  }
}

const handleTemplateSaved = (template) => {
  // For new templates created in modal, keep modal open but switch to steps tab
  if (!selectedTemplate.value && template) {
    // This was a new template creation - modal will stay open and show steps tab
    loadStatistics()  // Just refresh stats
    return
  }
  
  // For edits, close modal and refresh
  showFormModal.value = false
  handleRefresh()
}

const handleStepChanged = () => {
  // Reload statistics to update step counts when steps are modified
  loadStatistics()
  loadTemplates() // Also refresh templates to update step_count column
}



const handleNextPage = () => {
  if (pagination.value.has_next) {
    campaignTemplateStore.setPagination(pagination.value.page + 1)
    loadTemplates()
  }
}

const handlePreviousPage = () => {
  if (pagination.value.has_prev && pagination.value.page > 1) {
    campaignTemplateStore.setPagination(pagination.value.page - 1)
    loadTemplates()
  }
}

// Utility functions
const formatDate = (dateString) => {
  if (!dateString) return ''
  
  try {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch (e) {
    return dateString
  }
}

const getTypeColor = (type) => {
  const colors = {
    'Email': 'bg-blue-100 text-blue-800',
    'SMS': 'bg-green-100 text-green-800',
    'Ads': 'bg-purple-100 text-purple-800',
    'Social Media': 'bg-pink-100 text-pink-800',
    'Direct Mail': 'bg-orange-100 text-orange-800'
  }
  return colors[type] || 'bg-gray-100 text-gray-800'
}

const getStatusColor = (isActive) => {
  return isActive ? 'bg-green-400' : 'bg-gray-400'
}

// Lifecycle
onMounted(() => {
  loadTemplates()
  loadStatistics()
})
</script> 