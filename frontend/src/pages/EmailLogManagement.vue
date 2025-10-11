<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <Button
          variant="solid"
          @click="openFormModal()"
        >
          <template #prefix>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
          </template>
          {{ __('Add New Log') }}
        </Button>
      </template>
    </LayoutHeader>

    <div class="min-h-screen container mx-auto bg-slate-50 p-4 md:p-6">
      <!-- Header -->


      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 012 2z" />
              </svg>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ stats.total }}</div>
              <div class="text-sm text-slate-500">{{ __('Total Emails') }}</div>
            </div>
          </div>
        </div>
        <div class="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ stats.success }}</div>
              <div class="text-sm text-slate-500">{{ __('Success') }}</div>
            </div>
          </div>
        </div>
        <div class="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ stats.failed }}</div>
              <div class="text-sm text-slate-500">{{ __('Failed') }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters & Search -->
      <div class="bg-white border border-slate-200 rounded-lg mb-6">
        <div class="p-4">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            <FormControl
              type="text"
              v-model="search"
              :placeholder="__('Search emails...')"
              class="md:col-span-2"
              @update:model-value="debouncedSearch"
            >
              <template #prefix>
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </template>
            </FormControl>
            <FormControl
              type="select"
              v-model="filters.status"
              :options="statusOptions"
              :placeholder="__('Status')"
              @change="applyFilters"
            />
            <FormControl
              type="text"
              v-model="filters.sender"
              :placeholder="__('Sender')"
              @update:model-value="applyFilters"
            />
          </div>
          <div class="mt-4 flex justify-end space-x-3">
            <Button
              variant="outline"
              @click="handleRefresh"
              :loading="loading"
            >
              <template #prefix>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-4 h-4"
                  :class="{ 'animate-spin': loading }"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
              </template>
              {{ __('Refresh') }}
            </Button>
            <Button
              variant="outline"
              @click="clearFilters"
            >
              {{ __('Clear Filters') }}
            </Button>
          </div>
        </div>
      </div>

      <!-- Data Table -->
      <div class="bg-white border border-slate-200 rounded-lg">
        <div class="p-4 border-b border-slate-200">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-medium text-slate-800">{{ __('Email Logs') }} ({{ pagination.total }})</h3>
            <div class="flex gap-2">
              <Button
                v-if="selected.length > 0"
                variant="outline"
                class="text-red-600 border-red-200 hover:bg-red-50"
                @click="bulkDelete"
              >
                <template #prefix>
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </template>
                {{ __('Delete Selected') }} ({{ selected.length }})
              </Button>
              <Button
                variant="outline"
                @click="exportData"
              >
                <template #prefix>
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </template>
                {{ __('Export') }}
              </Button>
            </div>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-slate-200 bg-slate-50">
                <th class="text-left p-3 w-12">
                  <input
                    type="checkbox"
                    :checked="isAllSelected"
                    @change="toggleSelectAll"
                    class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                  />
                </th>
                <th class="text-left p-3 font-medium text-slate-700">{{ __('Subject') }}</th>
                <th class="text-left p-3 font-medium text-slate-700">{{ __('Recipients') }}</th>
                <th class="text-left p-3 font-medium text-slate-700">{{ __('Sender') }}</th>
                <th class="text-left p-3 font-medium text-slate-700">{{ __('Status') }}</th>
                <th class="text-left p-3 font-medium text-slate-700">{{ __('Modified') }}</th>
                <th class="text-left p-3 font-medium text-slate-700 w-32">{{ __('Actions') }}</th>
              </tr>
            </thead>
            <tbody v-if="!loading">
              <tr
                v-for="item in items"
                :key="item.name"
                class="border-b border-slate-100 hover:bg-slate-50 transition-colors"
              >
                <td class="p-3">
                  <input
                    type="checkbox"
                    :value="item.name"
                    v-model="selected"
                    class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                  />
                </td>
                <td class="p-3">
                  <div class="text-sm text-slate-900 max-w-[300px] truncate">
                    {{ item.subject }}
                  </div>
                </td>
                <td class="p-3">
                  <div class="text-sm text-slate-600 max-w-[200px] truncate">
                    {{ item.recipients }}
                  </div>
                </td>
                <td class="p-3">
                  <div class="text-sm text-slate-600">{{ item.sender }}</div>
                </td>
                <td class="p-3">
                  <Badge :variant="getStatusVariant(item.status)">
                    {{ item.status }}
                  </Badge>
                </td>
                <td class="p-3">
                  <div class="text-sm text-slate-600">
                    {{ formatDate(item.modified) }}
                  </div>
                </td>
                <td class="p-3">
                  <div class="flex items-center gap-1">
                    <button
                      @click="viewDetails(item)"
                      class="p-1 text-slate-400 hover:text-blue-600 transition-colors"
                      :title="__('View Details')"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </button>
                    <button
                      @click="openFormModal(item)"
                      class="p-1 text-slate-400 hover:text-blue-600 transition-colors"
                      :title="__('Edit')"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button
                      @click="confirmDelete(item)"
                      class="p-1 text-slate-400 hover:text-red-600 transition-colors"
                      :title="__('Delete')"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Loading State -->
          <Loading v-if="loading" text="Loading email logs..." />

          <!-- Empty State -->
          <div v-if="!loading && items.length === 0" class="p-8 text-center text-slate-500">
            <svg class="w-12 h-12 mx-auto mb-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 012 2z" />
            </svg>
            <p class="text-lg font-medium mb-2">{{ __('No email logs found') }}</p>
            <p class="text-sm">{{ __('Create your first email log to get started.') }}</p>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="!loading && items.length > 0" class="p-4 border-t border-slate-200">
          <div class="flex items-center justify-between">
            <div class="text-sm text-slate-500">
              {{ __('Showing') }} {{ pagination.showing_from }} {{ __('to') }} {{ pagination.showing_to }} {{ __('of') }} {{ pagination.total }} {{ __('items') }}
            </div>
            <div class="flex items-center gap-2">
              <button
                @click="pagination.page > 1 && (pagination.page--, loadData())"
                :disabled="pagination.page <= 1"
                class="px-3 py-1 text-sm border border-slate-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
              >
                {{ __('Previous') }}
              </button>
              <div class="flex gap-1">
                <button
                  v-for="page in getVisiblePages()"
                  :key="page"
                  @click="page !== '...' && (pagination.page = page, loadData())"
                  :class="[
                    'px-3 py-1 text-sm border rounded-md',
                    page === pagination.page
                      ? 'bg-black text-white border-black'
                      : page === '...'
                      ? 'cursor-default border-slate-300'
                      : 'border-slate-300 hover:bg-slate-50'
                  ]"
                  :disabled="page === '...'"
                >
                  {{ page }}
                </button>
              </div>
              <button
                @click="pagination.page < pagination.pages && (pagination.page++, loadData())"
                :disabled="pagination.page >= pagination.pages"
                class="px-3 py-1 text-sm border border-slate-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50"
              >
                {{ __('Next') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Form Modal -->
      <Dialog v-model="showFormModal" :options="{ title: `${formData.name ? __('Edit') : __('Add')} ${__('Email Log')}`, size: '2xl' }">
        <template #body-content>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="md:col-span-2">
              <FormControl
                type="text"
                :label="__('Subject')"
                v-model="formData.subject"
                :required="true"
                :placeholder="__('Enter email subject')"
              />
            </div>
            <div>
              <FormControl
                type="textarea"
                :label="__('Recipients')"
                v-model="formData.recipients"
                :required="true"
                :placeholder="__('Enter recipients (comma-separated)')"
                :rows="2"
              />
              <p class="text-xs text-slate-500 mt-1">{{ __('Separate multiple emails with commas') }}</p>
            </div>
            <div>
              <FormControl
                type="email"
                :label="__('Sender')"
                v-model="formData.sender"
                :required="true"
                :placeholder="__('Enter sender email')"
              />
            </div>
            <div>
              <FormControl
                type="textarea"
                label="CC"
                v-model="formData.cc"
                :placeholder="__('Enter CC recipients')"
                :rows="2"
              />
              <p class="text-xs text-slate-500 mt-1">{{ __('Separate multiple emails with commas') }}</p>
            </div>
            <div>
              <FormControl
                type="textarea"
                label="BCC"
                v-model="formData.bcc"
                :placeholder="__('Enter BCC recipients')"
                :rows="2"
              />
              <p class="text-xs text-slate-500 mt-1">{{ __('Separate multiple emails with commas') }}</p>
            </div>
            <div>
              <FormControl
                type="select"
                :label="__('Status')"
                v-model="formData.status"
                :options="statusOptions"
                :required="true"
              />
            </div>
            <div>
              <FormControl
                type="textarea"
                :label="__('Attachments')"
                v-model="formData.attachments"
                :placeholder="__('List of attachment paths')"
                :rows="2"
              />
            </div>
            <div class="md:col-span-2">
              <FormControl
                type="textarea"
                :label="__('Content')"
                v-model="formData.content"
                :required="true"
                :placeholder="__('Enter email content')"
                :rows="8"
              />
            </div>
            <div v-if="formData.status === 'Failed'" class="md:col-span-2">
              <FormControl
                type="textarea"
                :label="__('Error Details')"
                v-model="formData.error"
                :placeholder="__('Enter error details')"
                :rows="3"
              />
            </div>
          </div>
        </template>
        <template #actions>
          <Button variant="ghost" @click="closeFormModal">{{ __('Cancel') }}</Button>
          <Button
            variant="solid"
            :loading="saving"
            @click="saveForm"
          >
            {{ formData.name ? __('Update') : __('Save') }}
          </Button>
        </template>
      </Dialog>

      <!-- Delete Confirmation -->
      <Dialog v-model="showDeleteDialog" :options="{ title: __('Confirm Delete'), size: 'xs' }">
        <template #body-content>
          <p class="text-slate-600">{{ __('Are you sure you want to delete this email log? This action cannot be undone.') }}</p>
        </template>
        <template #actions>
          <Button variant="ghost" @click="showDeleteDialog = false">{{ __('Cancel') }}</Button>
          <Button
            variant="solid"
            theme="red"
            :loading="deleting"
            @click="deleteItem"
          >
            {{ __('Delete') }}
          </Button>
        </template>
      </Dialog>

      <!-- Detail Modal -->
      <Dialog v-model="showDetailModal" :options="{ title: __('Email Log Details'), size: '3xl' }">
        <template #body-content>
          <div v-if="selectedItem" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div class="space-y-4">
                <div>
                  <dt class="text-sm font-medium text-slate-500">{{ __('Subject') }}</dt>
                  <dd class="mt-1 text-sm text-slate-900">{{ selectedItem.subject }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-slate-500">{{ __('Recipients') }}</dt>
                  <dd class="mt-1 text-sm text-slate-900">{{ selectedItem.recipients }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-slate-500">{{ __('Sender') }}</dt>
                  <dd class="mt-1 text-sm text-slate-900">{{ selectedItem.sender }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-slate-500">{{ __('Status') }}</dt>
                  <dd class="mt-1">
                    <Badge :variant="getStatusVariant(selectedItem.status)">
                      {{ selectedItem.status }}
                    </Badge>
                  </dd>
                </div>
              </div>
            </div>
            <div>
              <div class="space-y-4">
                <div v-if="selectedItem.cc">
                  <dt class="text-sm font-medium text-slate-500">CC</dt>
                  <dd class="mt-1 text-sm text-slate-900">{{ selectedItem.cc }}</dd>
                </div>
                <div v-if="selectedItem.bcc">
                  <dt class="text-sm font-medium text-slate-500">BCC</dt>
                  <dd class="mt-1 text-sm text-slate-900">{{ selectedItem.bcc }}</dd>
                </div>
                <div v-if="selectedItem.attachments">
                  <dt class="text-sm font-medium text-slate-500">{{ __('Attachments') }}</dt>
                  <dd class="mt-1 text-sm text-slate-900">{{ selectedItem.attachments }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-slate-500">{{ __('Modified') }}</dt>
                  <dd class="mt-1 text-sm text-slate-900">{{ formatDate(selectedItem.modified) }}</dd>
                </div>
              </div>
            </div>
            <div class="md:col-span-2">
              <div class="border-t border-slate-200 pt-6">
                <h4 class="text-sm font-medium text-slate-900 mb-3">{{ __('Content') }}</h4>
                <div class="bg-slate-50 border border-slate-200 rounded-lg p-4 text-sm text-slate-900 whitespace-pre-wrap">{{ selectedItem.content }}</div>
              </div>
            </div>
            <div v-if="selectedItem.error && selectedItem.status === 'Failed'" class="md:col-span-2">
              <div class="border-t border-slate-200 pt-6">
                <h4 class="text-sm font-medium text-red-600 mb-3">{{ __('Error Details') }}</h4>
                <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-sm text-red-900 whitespace-pre-wrap">{{ selectedItem.error }}</div>
              </div>
            </div>
          </div>
        </template>
        <template #actions>
          <Button variant="solid" @click="showDetailModal = false">{{ __('Close') }}</Button>
        </template>
      </Dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Button, FormControl, Dialog, Badge, Breadcrumbs } from 'frappe-ui'
import { emailLogService } from 'frappe-ui'
import { debounce } from 'lodash'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'



// Breadcrumbs
const breadcrumbs = [
  { label: __('Email Logs'), route: { name: 'EmailLogManagement' } }
]

const router = useRouter()

// State
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const items = ref([])
const selected = ref([])
const search = ref('')
const showFormModal = ref(false)
const showDeleteDialog = ref(false)
const showDetailModal = ref(false)
const formValid = ref(false)
const itemToDelete = ref(null)
const selectedItem = ref(null)

// Status options - using label/value format for Frappe UI
const statusOptions = [
  { label: __('Success'), value: 'Success' },
  { label: __('Failed'), value: 'Failed' },
  { label: __('Fallback'), value: 'Fallback' }
]

// Form data - matching EmailLog doctype fields
const formData = reactive({
  name: '',
  subject: '',
  recipients: '',
  cc: '',
  bcc: '',
  sender: '',
  content: '',
  attachments: '',
  status: 'Success',
  error: ''
})

// Filters
const filters = reactive({
  status: '',
  sender: ''
})

// Pagination
const pagination = reactive({
  page: 1,
  limit: 20,
  total: 0,
  pages: 0,
  showing_from: 0,
  showing_to: 0
})

// Stats
const stats = reactive({
  total: 0,
  success: 0,
  failed: 0
})

// Computed
const debouncedSearch = debounce(() => {
  loadData()
}, 300)

const isAllSelected = computed(() => {
  return items.value.length > 0 && selected.value.length === items.value.length
})

// Utility methods
const toggleSelectAll = () => {
  if (isAllSelected.value) {
    selected.value = []
  } else {
    selected.value = items.value.map(item => item.name)
  }
}

const getVisiblePages = () => {
  const current = pagination.page
  const total = pagination.pages
  
  // Handle case when there's only 1 page or no pages
  if (total <= 1) {
    return [1]
  }
  
  const delta = 2
  const range = []
  const rangeWithDots = []

  for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
    range.push(i)
  }

  if (current - delta > 2) {
    rangeWithDots.push(1, '...')
  } else {
    rangeWithDots.push(1)
  }

  rangeWithDots.push(...range)

  if (current + delta < total - 1) {
    rangeWithDots.push('...', total)
  } else if (total > 1) {
    rangeWithDots.push(total)
  }

  // Remove duplicates and return
  return [...new Set(rangeWithDots)]
}

const getStatusVariant = (status) => {
  const variants = {
    'Success': 'green',
    'Failed': 'red',
    'Fallback': 'orange'
  }
  return variants[status] || 'gray'
}

// Methods
const loadData = async () => {
  loading.value = true
  try {
    // Prepare filters
    const apiFilters = {}
    
    // Add non-empty filters
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== '') {
        apiFilters[key] = filters[key]
      }
    })
    
    // Prepare search conditions
    let or_filters = undefined
    if (search.value && search.value.trim() !== '') {
      or_filters = [
        ['subject', 'like', `%${search.value}%`],
        ['recipients', 'like', `%${search.value}%`],
        ['sender', 'like', `%${search.value}%`]
      ]
    }
    const params = {
      filters: apiFilters,
      or_filters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'modified desc',
      fields: ['name', 'subject', 'recipients', 'cc', 'bcc', 'sender', 'content', 'attachments', 'status', 'error', 'modified']
    }

    const result = await emailLogService.getList(params)
    
    if (result.success) {
      items.value = result.data || []
      Object.assign(pagination, result.pagination)
      
      // Update stats
      stats.total = result.pagination.total || 0
      stats.success = result.data?.filter(item => item.status === 'Success').length || 0
      stats.failed = result.data?.filter(item => item.status === 'Failed').length || 0
    } else {
      console.error('Error loading data:', result.error)
      items.value = []
    }
  } catch (error) {
    console.error('Error loading data:', error)
    items.value = []
  } finally {
    loading.value = false
  }
}

const applyFilters = debounce(() => {
  pagination.page = 1
  loadData()
}, 300)

const clearFilters = () => {
  Object.keys(filters).forEach(key => {
    filters[key] = ''
  })
  search.value = ''
  pagination.page = 1
  loadData()
}

const handleRefresh = async () => {
  try {
    await loadData()
    // Show success message
    console.log('Data refreshed successfully')
  } catch (error) {
    console.error('Error refreshing data:', error)
  }
}

const openFormModal = (item = null) => {
  if (item) {
    Object.assign(formData, item)
  } else {
    Object.keys(formData).forEach(key => {
      formData[key] = ''
    })
    formData.status = 'Success'
  }
  showFormModal.value = true
}

const closeFormModal = () => {
  showFormModal.value = false
  Object.keys(formData).forEach(key => {
    formData[key] = ''
  })
}

const saveForm = async () => {
  // Basic validation
  if (!formData.subject || !formData.recipients || !formData.sender || !formData.content) {
    return
  }

  saving.value = true
  try {
    const result = await emailLogService.save(formData, formData.name)
    
    if (result.success) {
      closeFormModal()
      loadData()
    }
  } catch (error) {
    console.error('Error saving:', error)
  } finally {
    saving.value = false
  }
}

const viewDetails = (item) => {
  selectedItem.value = item
  showDetailModal.value = true
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  showDeleteDialog.value = true
}

const deleteItem = async () => {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    const result = await emailLogService.delete(itemToDelete.value.name)
    
    if (result.success) {
      showDeleteDialog.value = false
      itemToDelete.value = null
      loadData()
    }
  } catch (error) {
    console.error('Error deleting:', error)
  } finally {
    deleting.value = false
  }
}

const bulkDelete = async () => {
  if (selected.value.length === 0) return

  const confirmed = confirm(`Are you sure you want to delete ${selected.value.length} email logs?`)
  if (!confirmed) return

  try {
    await Promise.all(
      selected.value.map(name => emailLogService.delete(name))
    )
    selected.value = []
    loadData()
  } catch (error) {
    console.error('Error bulk deleting:', error)
  }
}

const exportData = () => {
  const data = items.value.map(item => ({
    Subject: item.subject,
    Recipients: item.recipients,
    Sender: item.sender,
    Status: item.status,
    Modified: formatDate(item.modified)
  }))

  const csv = [
    Object.keys(data[0]).join(','),
    ...data.map(row => Object.values(row).join(','))
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'email-logs.csv'
  a.click()
  URL.revokeObjectURL(url)
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(async () => {
  await loadData()
})
</script>

<style scoped>
/* Custom scrollbar for table */
.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Loading animation */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Table hover effects */
tbody tr:hover {
  background-color: #f8fafc;
}

/* Button hover effects */
button:hover svg {
  transform: scale(1.05);
}

/* Badge animations */
.badge {
  transition: all 0.15s ease-in-out;
}

/* Form field focus effects */
input:focus, textarea:focus, select:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
</style>
