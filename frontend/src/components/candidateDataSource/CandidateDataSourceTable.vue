<template>
  <div class="container mx-auto px-4 py-8 max-w-7xl">
    <!-- Header Section -->
    <div class="bg-white rounded-xl shadow-lg p-6 mb-8">
      <!-- Header with filters -->
      <div class="flex flex-wrap items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-gray-800">{{ __('Candidate Data Source Management') }}</h2>
        
        <div class="flex items-center space-x-4 mt-4 sm:mt-0">
          <!-- Search -->
          <div class="relative">
            <input 
              type="text" 
              :value="searchText"
              @input="handleSearch($event.target.value)"
              :placeholder="__('Search...')" 
              class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 absolute left-3 top-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          
          <!-- Filter -->
          <div class="relative">
            <select 
              :value="statusFilter" 
              @change="handleStatusFilterChange($event.target.value)"
              class="appearance-none bg-white border border-gray-300 rounded-lg px-4 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">{{ __('All Status') }}</option>
              <option value="Active">{{ __('Active') }}</option>
              <option value="Inactive">{{ __('Inactive') }}</option>
            </select>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 absolute right-2 top-3 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>

          <!-- Source Type Filter -->
          <div class="relative">
            <select 
              :value="typeFilter" 
              @change="handleTypeFilterChange($event.target.value)"
              class="appearance-none bg-white border border-gray-300 rounded-lg px-4 py-2 pr-8 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">{{ __('All Types') }}</option>
              <option value="ATS">{{ __('ATS') }}</option>
              <option value="JobBoard">{{ __('Job Board') }}</option>
              <option value="SocialNetwork">{{ __('Social Network') }}</option>
              <option value="Manual">{{ __('Manual') }}</option>
              <option value="Other">{{ __('Other') }}</option>
            </select>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 absolute right-2 top-3 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>

          <!-- Actions -->
          <button
            @click="handleRefresh"
            class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg transition-colors duration-200 flex items-center space-x-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            <span>{{ __('Refresh') }}</span>
          </button>
          
          <button
            @click="$emit('create')"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors duration-200 flex items-center space-x-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            <span>{{ __('Add Data Source') }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="flex items-center space-x-2 text-gray-600">
        <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>{{ __('Loading data...') }}</span>
      </div>
    </div>

    <!-- Table Content -->
    <div v-else class="bg-white rounded-xl shadow-lg overflow-hidden">
      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left py-4 px-6 font-medium text-gray-700">{{ __('Source Name') }}</th>
              <th class="text-left py-4 px-6 font-medium text-gray-700">{{ __('Type') }}</th>
              <th class="text-left py-4 px-6 font-medium text-gray-700">{{ __('Auth Method') }}</th>
              <th class="text-left py-4 px-6 font-medium text-gray-700">{{ __('Status') }}</th>
              <th class="text-left py-4 px-6 font-medium text-gray-700">{{ __('Last Sync') }}</th>
              <th class="text-left py-4 px-6 font-medium text-gray-700">{{ __('Active') }}</th>
              <th class="text-left py-4 px-6 font-medium text-gray-700">{{ __('Actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-if="!dataSources || dataSources.length === 0">
              <td colspan="7" class="py-12 text-center text-gray-500">
                <div class="flex flex-col items-center space-y-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m0 0V9a2 2 0 012-2h8a2 2 0 012 2v4M6 13h12"></path>
                  </svg>
                  <span>{{ __('No data sources yet') }}</span>
                  <button
                    @click="$emit('create')"
                    class="text-blue-600 hover:text-blue-800 font-medium"
                  >
                    {{ __('Create first data source') }}
                  </button>
                </div>
              </td>
            </tr>
            
            <tr 
              v-for="item in dataSources" 
              :key="item.name"
              class="hover:bg-gray-50 transition-colors duration-150"
            >
              <!-- Source Name -->
              <td class="py-4 px-6">
                <div class="flex items-center space-x-3">
                  <div class="flex-shrink-0">
                    <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m0 0V9a2 2 0 012-2h8a2 2 0 012 2v4M6 13h12"></path>
                      </svg>
                    </div>
                  </div>
                  <div>
                    <div class="font-medium text-gray-900">{{ item.source_name }}</div>
                    <div v-if="item.api_base_url" class="text-sm text-gray-500 truncate max-w-xs">
                      {{ item.api_base_url }}
                    </div>
                  </div>
                </div>
              </td>

              <!-- Source Type -->
              <td class="py-4 px-6">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getTypeClass(item.source_type)">
                  {{ getTypeText(item.source_type) }}
                </span>
              </td>

              <!-- Auth Method -->
              <td class="py-4 px-6">
                <span class="text-sm text-gray-900">{{ item.auth_method || '-' }}</span>
              </td>

              <!-- Status -->
              <td class="py-4 px-6">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getStatusClass(item.status)">
                  {{ getStatusText(item.status) }}
                </span>
              </td>

              <!-- Last Sync -->
              <td class="py-4 px-6">
                <div v-if="item.last_sync_at" class="text-sm text-gray-900">
                  {{ formatDate(item.last_sync_at) }}
                </div>
                <div v-else class="text-sm text-gray-500">{{ __('Not synced') }}</div>
                <div v-if="item.last_error" class="text-xs text-red-600 mt-1 truncate max-w-xs" :title="item.last_error">
                  {{ __('Error') }}: {{ item.last_error }}
                </div>
              </td>

              <!-- Active Status -->
              <td class="py-4 px-6">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="item.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                  {{ item.is_active ? __('Active') : __('Paused') }}
                </span>
              </td>

              <!-- Actions -->
              <td class="py-4 px-6">
                <div class="flex items-center gap-1">
                  <button
                    @click="handleView(item)"
                    class="p-1 text-slate-400 hover:text-blue-600 transition-colors"
                    :title="__('View Details')"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                  <button
                    @click="handleEdit(item)"
                    class="p-1 text-slate-400 hover:text-blue-600 transition-colors"
                    :title="__('Edit')"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    @click="handleDelete(item)"
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
      </div>

      <!-- Pagination -->
      <div v-if="pagination && pagination.total > 0" class="border-t border-gray-200 bg-gray-50 px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-700">
            {{ __('Showing') }} {{ pagination.showing_from }} - {{ pagination.showing_to }} {{ __('of') }} {{ pagination.total }} {{ __('results') }}
          </div>
          
          <div class="flex items-center space-x-2">
            <button
              @click="handlePageChange(pagination.page - 1)"
              :disabled="!pagination.has_prev"
              class="px-3 py-1 text-sm border rounded-md transition-colors duration-200"
              :class="pagination.has_prev 
                ? 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50' 
                : 'border-gray-200 text-gray-400 bg-gray-100 cursor-not-allowed'"
            >
              {{ __('Previous') }}
            </button>
            
            <span class="text-sm text-gray-700">
              {{ __('Page') }} {{ pagination.page }} / {{ pagination.pages }}
            </span>
            
            <button
              @click="handlePageChange(pagination.page + 1)"
              :disabled="!pagination.has_next"
              class="px-3 py-1 text-sm border rounded-md transition-colors duration-200"
              :class="pagination.has_next 
                ? 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50' 
                : 'border-gray-200 text-gray-400 bg-gray-100 cursor-not-allowed'"
            >
              {{ __('Next') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog } from 'frappe-ui'

// Props
const props = defineProps({
  dataSources: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  pagination: {
    type: Object,
    default: () => ({
      page: 1,
      limit: 10,
      total: 0,
      pages: 1,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    })
  },
  searchText: {
    type: String,
    default: ''
  },
  statusFilter: {
    type: String,
    default: 'all'
  },
  typeFilter: {
    type: String,
    default: 'all'
  }
})



// Emits
const emit = defineEmits([
  'create', 'edit', 'view', 'delete', 'refresh',
  'update:search-text', 'update:status-filter', 'update:type-filter',
  'page-change'
])

// Methods for UI
const getStatusClass = (status) => {
  const classes = {
    'Active': 'bg-green-100 text-green-800',
    'Inactive': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getStatusText = (status) => {
  const texts = {
    'Active': __('Active'),
    'Inactive': __('Inactive')
  }
  return texts[status] || status
}

const getTypeClass = (type) => {
  const classes = {
    'ATS': 'bg-blue-100 text-blue-800',
    'JobBoard': 'bg-purple-100 text-purple-800',
    'SocialNetwork': 'bg-green-100 text-green-800',
    'Manual': 'bg-gray-100 text-gray-800',
    'Other': 'bg-orange-100 text-orange-800'
  }
  return classes[type] || 'bg-gray-100 text-gray-800'
}

const getTypeText = (type) => {
  const texts = {
    'ATS': __('ATS'),
    'JobBoard': __('Job Board'),
    'SocialNetwork': __('Social Network'),
    'Manual': __('Manual'),
    'Other': __('Other')
  }
  return texts[type] || type
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Event handlers
const handleSearch = (value) => {
  emit('update:search-text', value)
}

const handleStatusFilterChange = (value) => {
  emit('update:status-filter', value)
}

const handleTypeFilterChange = (value) => {
  emit('update:type-filter', value)
}

const handleRefresh = () => {
  emit('refresh')
}

const handleEdit = (item) => {
  emit('edit', item)
}

const handleView = (item) => {
  emit('view', item)
}

const handleDelete = (item) => {
  
  // Using Frappe UI Dialog
  const dialog = new Dialog({
    title: __('Confirm Delete'),
    message: __('Are you sure you want to delete data source "{0}"? This action cannot be undone!', [item.source_name]),
    actions: [
      {
        label: __('Cancel'),
        variant: 'ghost'
      },
      {
        label: __('Delete'),
        variant: 'solid',
        theme: 'red',
        onClick: () => {
          emit('delete', item)
          dialog.hide()
        }
      }
    ]
  })
  dialog.show()
}

const handlePageChange = (page) => {
  emit('page-change', page)
}


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